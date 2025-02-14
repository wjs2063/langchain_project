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
base_chat = ChatOpenAI(model="gpt-4o", temperature=0)
