from chatbot.domain.entities.memories.history import (
    SlidingWindowBufferRedisChatMessageHistory,
)
from chatbot.infra.repository.user_repository.user_repository import (
    AbstractUserRepository,
)
import traceback
from langchain_core.messages import trim_messages
from chatbot.domain.entities.chains.domain_selector_chain.domain_selector_chain import (
    merge_multi_domain_output,
)
from chatbot.domain.entities.utils.time import get_current_time
import asyncio
from chatbot.exceptions.exception_handler import CustomException
from chatbot.domain.chains.interface import AbstractProcessingChain
from chatbot.infra.redis._redis import _redis_url
from langchain_core.messages import AIMessage, HumanMessage
from chatbot.domain.entities.chat_models.chat_models import (
    ChatOpenAI,
)
from chatbot.domain.entities.chains.merge_output_chain.merge_output_chain import (
    merge_output_chain,
)
from chatbot.infra.utils.loggings.root import logger
from chatbot.infra.utils.loggings.usecase import trace
from chainlit.message import Message


class ChatService:
    """
    ChatService provides functionality for managing user interactions with a chat system
    that incorporates advanced AI-driven conversation handling. It is designed to integrate
    with repositories, models, and chat history services to facilitate seamless conversational
    experiences.

    ChatService allows retrieving and displaying chat history, processing user queries, and
    invoking AI models to generate responses. It also supports managing concurrent tasks for
    sub-chains and handling complex multi-domain outputs efficiently.

    Attributes:
        _user_repository (AbstractUserRepository): The repository for managing user data.
        chat_model (ChatOpenAI): The AI model used for generating chat responses.
        history (SlidingWindowBufferRedisChatMessageHistory): Handles storing and retrieving chat history.
        session_id (str): A unique identifier for the chat session.
        history_buffers (list): Temporarily stores recent chat messages for processing.

    Methods:
        get_history(session_id: str) -> SlidingWindowBufferRedisChatMessageHistory
            Retrieves the history instance associated with the given session ID.

        display_chat_history(cl)
            Displays the chat history on the user interface.

        ainvoke(message: Message)
            Processes the user's input message and invokes the chat model to generate a response.

        process_sub_chains(result)
            Orchestrates the execution of multiple asynchronous tasks for sub-chains.

        get_sub_chains(data)
            Retrieves sub-chains matching specific conditions.

    """

    def __init__(
        self,
        user_repository: AbstractUserRepository,
        chat_model: ChatOpenAI,
        history: SlidingWindowBufferRedisChatMessageHistory,
        session_id: str,
    ):
        self._user_repository = user_repository
        self.chat_model = chat_model
        self.history = history
        self.session_id = session_id
        self.history_buffers: list = list()

    @staticmethod
    def get_history(session_id: str) -> SlidingWindowBufferRedisChatMessageHistory:
        return SlidingWindowBufferRedisChatMessageHistory(
            session_id=session_id, url=_redis_url, buffer_size=8
        )

    async def display_chat_history(self, cl):
        """
        대화 이력을 화면에 출력하는 함수
        """
        messages = trim_messages(
            messages=await self.history.aget_messages(),
            strategy="last",
            start_on="human",
            allow_partial=False,
            max_tokens=100,
            token_counter=len,
        )
        if not messages:
            return
        history_msgs = ["-" * 10 + "이전 대화 이력" + "-" * 10]

        for msg in messages:
            author = "User" if isinstance(msg, HumanMessage) else "AI"
            history_msgs.append(f"{author} : {msg.content}")

        history_msgs.append("-" * 20)

        for msg in history_msgs:
            await cl.Message(msg).send()
        await cl.Message("-" * 10 + "이전 대화 이력" + "-" * 10).send()

    @trace(logger=logger)
    async def ainvoke(self, message: Message):
        # 첫 질문을 -> 소규모 질문으로 분할
        history = await self.history.aget_messages()
        request_information = {
            "question": message.content,
            "ability": "chatting",
            "chat_history": history,
            "user_info": get_current_time(region="kr"),
        }
        result = await self.chat_model.ainvoke(request_information)
        result = {**result, **request_information}
        response = await self.process_sub_chains(result)
        merged_output = merge_multi_domain_output(response)

        response = await merge_output_chain.ainvoke(
            {"question": message.content, "domain_answers": merged_output.content}
        )
        self.history_buffers.append(
            HumanMessage(content=message.content, additional_kwargs={"test": "kwargs"})
        )
        self.history_buffers.append(
            AIMessage(content=response.content, additional_kwargs={"test": "kwargs"})
        )
        await self.history.aadd_messages(self.history_buffers)
        return response.content

    async def process_sub_chains(self, result):
        try:
            parallel_tasks = set()

            for data in result.get("questions", []):
                for sub_chain in self.get_sub_chains(input_data=data):
                    task = asyncio.create_task(
                        sub_chain(
                            client_information={},
                        ).arun(
                            request_information={
                                **data,
                                "chat_history": result["chat_history"],
                                "user_info": result["user_info"],
                            }
                        )
                    )
                    parallel_tasks.add(task)
        except Exception as e:
            error_trace = traceback.format_exc()
            raise CustomException(
                status_code=500, detail=error_trace, trace=error_trace
            )
        else:
            return await asyncio.gather(*parallel_tasks)

    def get_sub_chains(self, input_data: dict):
        return [
            sub
            for sub in AbstractProcessingChain.__subclasses__()
            if sub.meets_condition(input_data=input_data)
        ]
