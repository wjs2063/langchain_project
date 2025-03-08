"""
ChatModel
"""

from dotenv import load_dotenv
from langchain.tools import BaseTool, Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import os

load_dotenv()

groq_chat = ChatGroq(
    model="gemma2-9b-it",
    temperature=0.7,
    max_tokens=300,
    api_key=os.getenv("GROQ_API_KEY"),
)

groq_deepseek = ChatGroq(
    model="deepseek-r1-distill-qwen-32b",
    temperature=0.7,
    max_tokens=500,
    api_key=os.getenv("GROQ_API_KEY"),
)

base_chat = ChatOpenAI(model="gpt-4o", temperature=0.5, verbose=True)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI assistant skilled at {ability}. "
            "Your goal is to engage in a natural and meaningful conversation while remembering past interactions. "
            "Always respond in Korean, using a friendly and engaging tone.\n\n"
            "Example interactions:\n"
            "User: '오늘 피곤하네...'\n"
            "AI: '오늘 많이 바빴어요? 무슨 일 있었어요?'\n\n"
            "User: '지난번에 추천해준 책 읽었어!'\n"
            "AI: '오! 어땠어요? 가장 인상 깊었던 부분이 뭐였어요?'\n\n"
            "User: '다음 주 여행 간다고 했었지?'\n"
            "AI: '맞아요! 여행 준비는 잘 되고 있어요? 어디로 가는 거죠?'",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)
