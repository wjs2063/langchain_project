import traceback
from entities.chains.domain_selector_chain.domain_selector_chain import (
    merge_multi_domain_output,
)
from apps.entities.utils.time import get_current_time
import asyncio
from apps.exceptions.exception_handler import CustomException
from services.chainlit_service.multi_chain import AbstractProcessingChain
from apps.entities.memories.history import SlidingWindowBufferRedisChatMessageHistory
from apps.infras.redis._redis import _redis_url
from infras.repository.user_repository.user_repository import (
    AbstractUserRepository,
)
from langchain_core.messages import AIMessage, HumanMessage
from apps.entities.chat_models.chat_models import (
    ChatOpenAI,
)
from apps.entities.chains.merge_output_chain.merge_output_chain import (
    merge_output_chain,
)


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

    # @trace(logger=logger)
    async def ainvoke(self, message: str):
        # 첫 질문을 -> 소규모 질문으로 분할
        history = await self.history.aget_messages()
        request_information = {
            "question": message,
            "ability": "chatting",
            "chat_history": history,
            "user_info": get_current_time(region="kr"),
        }
        result = await self.chat_model.ainvoke(request_information)
        result = {**result, **request_information}
        response = await self.process_sub_chains(result)
        merged_output = merge_multi_domain_output(response)

        response = await merge_output_chain.ainvoke(
            {"question": message, "domain_answers": merged_output.content}
        )
        self.history_buffers.append(
            HumanMessage(content=message, additional_kwargs={**request_information})
        )
        self.history_buffers.append(AIMessage(content=response.content))
        await self.history.aadd_messages(self.history_buffers)
        return response

    async def process_sub_chains(self, result):
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
        return await asyncio.gather(*parallel_tasks)

    def get_sub_chains(self, input_data: dict):
        return [
            sub
            for sub in AbstractProcessingChain.__subclasses__()
            if sub.meets_condition(input_data=input_data)
        ]
