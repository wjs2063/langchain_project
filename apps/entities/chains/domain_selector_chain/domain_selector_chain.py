from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_core.output_parsers import JsonOutputParser
from entities.chains.domain_selector_chain.schema import QuestionResponse
from entities.chains.general_chat_chain.general_chain import general_chain
from entities.chains.schedule_chain.chain import schedule_agent
from entities.chains.weather_chain.weather_chain import weather_agent

from apps.examples.structured_output.domain_question_examples.prompt import prompt
from apps.entities.chat_models.chat_models import groq_chat, groq_deepseek
from apps.entities.chains.domain_selector_chain.prompt import selector_prompt
from apps.entities.memories.history import SlidingWindowBufferRedisChatMessageHistory
from apps.infras.redis._redis import _redis_url
from langchain_core.messages import AIMessage

domain_selector_chain = selector_prompt | groq_chat

buffered_memory = SlidingWindowBufferRedisChatMessageHistory(
    session_id="123", url=_redis_url, buffer_size=8
)


runnable_chain_branch = RunnableLambda(
    lambda x: {
        **x,
        "domain": domain_selector_chain.invoke(x).content.strip().lower(),
    }  # 기존 input 유지 + "domain" 추가
) | RunnableBranch(
    (lambda x: x["domain"] == "schedule", schedule_agent),
    (lambda x: x["domain"] == "weather", weather_agent),
    lambda x: general_chain,
)


domain_chains = {
    "weather": weather_agent,
    "schedule": schedule_agent,
    "general": general_chain,
}


parser = JsonOutputParser(pydantic_object=QuestionResponse)

prompt = prompt.partial(format_instructions=parser.get_format_instructions())

multi_domain_chain = prompt | groq_chat | parser


def merge_multi_domain_output(datas: list) -> AIMessage:
    """
    input : {"domain": str , "question" : str }
    """
    try:
        answer = []
        for data in datas:
            # if isinstance(data, AIMessage):
            #     data = data.content
            partial_qa_pair = f"""{data["input"]['domain']} question : {data["input"]["question"]}\n output : {data["output"]}"""
            answer.append(partial_qa_pair)
    except Exception as e:
        print(e)
    else:
        return AIMessage(content="\n".join(answer))


# print(multi_domain_chain.invoke({"question": "3일후 스케쥴과 오늘 날씨 알려줘"}))
