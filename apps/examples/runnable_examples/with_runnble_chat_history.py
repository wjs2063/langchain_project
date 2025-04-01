from entities.tools.search.tavily.tavily_search import tavily_search_tool
from langchain.agents import AgentType, initialize_agent
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from apps.entities.memories.history import \
    SlidingWindowBufferRedisChatMessageHistory
from apps.entities.tools.utils.etc import current_date_tool
from apps.entities.tools.weathers.weather_tool import get_weather
from apps.entities.tools.wikipedias.wikipedia_tool import wiki_tool
from apps.infras.redis._redis import _redis_url
from apps.services.chainlit_service.prompt import chainlit_prompt

chat_model = ChatOpenAI(model="gpt-4o", temperature=0.5)


def get_history(session_id: str) -> SlidingWindowBufferRedisChatMessageHistory:
    return SlidingWindowBufferRedisChatMessageHistory(
        session_id=session_id, url=_redis_url, buffer_size=8
    )


tools = [tavily_search_tool, current_date_tool, wiki_tool, get_weather]
prompt = PromptTemplate(
    template="""
    넌 유능한 비서야. 사용자의 질문에 대답해
    규칙 :
    1. 맥락에 맞게 대답할것
    2. tool 을 사용할것

    user question : {question}
    """,
    input_variables=["question"],
)
agent_with_tools = initialize_agent(
    llm=chat_model,
    tools=tools,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=2,
    handle_parsing_errors=True,
)
prompt = PromptTemplate(
    template="""
    You are an AI Virtual Personal Assistant designed to remember user conversations and provide context-aware responses in Korean. Your goal is to create a natural and engaging conversation by maintaining continuity, recognizing user preferences, and responding in a friendly and helpful manner.

    Rules:

    - Maintain Context: Remember past interactions and respond accordingly to keep the conversation coherent.
    - Personalized Responses: Tailor responses based on the user's past messages, interests, and preferences.
    - Natural Flow: Avoid robotic replies; use a conversational tone that feels human-like and engaging.
    - Encourage Interaction: Ask relevant questions to keep the conversation going and make the user feel heard.
    - Concise and Clear Information: Provide useful and direct answers without unnecessary complexity.
    - Adapt to New Topics: If the user's message introduces a completely new topic or does not require continuity, do not force context from past conversations. Respond naturally to the new topic instead.

    Language Setting:

    - Always respond in Korean, even though the prompt is in English.
    - Use natural, friendly, and engaging Korean expressions.

    Example Interactions:

    User: "오늘 피곤하네…"
    AI: "오늘 많이 바빴어요? 무슨 일 있었어요?"

    User: "지난번에 추천해준 책 읽었어!"
    AI: "오! 어땠어요? 어떤 부분이 가장 기억에 남아요?"

    User: "다음 주 여행 간다고 했었지?"
    AI: "맞아요! 여행 준비는 잘 돼가요? 어디로 가는 거였죠?"

    User: "요즘 날씨 너무 좋다!"
    AI: "그러게요! 완전 봄 느낌이에요. 어디 나가서 산책이라도 할 생각이에요?"

    User: "갑자기 드는 생각인데, AI는 감정을 느낄 수 있어?"
    AI: "흥미로운 질문이에요! AI는 감정을 직접 느낄 수는 없지만, 사용자 감정을 이해하려고 노력해요."

    ---
    about user information :
    {user_info}

    Previous chat history:
    {chat_history}

    User question: {question}
        """,
    input_variables=["question", "user_info"],
)

# print(prompt.get_output_jsonschema())
chain_with_history = RunnableWithMessageHistory(
    prompt | chat_model,
    verbose=True,
    get_session_history=get_history,
    history_messages_key="chat_history",
    input_messages_key="question",
)
from langchain.callbacks.tracers import ConsoleCallbackHandler

# print(
#     chain_with_history.invoke(
#         {
#             "question": "내가 한 이야기들 말해봐",
#             "ability": "chatting",
#             "user_info": "123",
#         },
#         config={
#             "configurable": {"session_id": "jaehyeon", "user_id": "jaehyeon"},
#             "callbacks": [ConsoleCallbackHandler()],
#         },
#     )
# )
