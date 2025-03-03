"""
ChatModel
"""

import logging
import typing
import uuid
from typing import Optional, Any, Sequence, Union, Callable, Iterator

from langchain_core.callbacks import Callbacks, CallbackManagerForLLMRun
from langchain_core.language_models import (
    BaseChatModel,
    SimpleChatModel,
    LanguageModelInput,
)
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult, ChatResult, ChatGenerationChunk
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_core.runnables import ConfigurableField
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv

load_dotenv()
#
#
# class CustomChatModel(BaseChatModel):
#
#     def _generate(self, messages: list[BaseMessage], stop: Optional[list[str]] = None,
#                   run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any) -> ChatResult:
#         pass
#
#     def _stream(self, messages: list[BaseMessage], stop: Optional[list[str]] = None,
#                 run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any) -> Iterator[ChatGenerationChunk]:
#         pass
#
#     @property
#     def _llm_type(self) -> str:
#         pass
#
#     def bind_tools(self, tools: Sequence[
#         Union[typing.Dict[str, Any], type, Callable, BaseTool]  # noqa: UP006
#     ], **kwargs: Any) -> Runnable[LanguageModelInput, BaseMessage]:
#         pass
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

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
