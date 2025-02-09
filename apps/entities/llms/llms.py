from typing import Any, Dict, Iterator, List, Mapping, Optional, Union

from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models import LanguageModelInput
from langchain_core.language_models.llms import LLM
from langchain_core.outputs import GenerationChunk
from langchain_core.runnables import Runnable
from pydantic import BaseModel

#
# class CustomLLM(LLM):
#     def _call(self, prompt: str, stop: Optional[list[str]] = None,
#               run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any) -> str:
#         pass
#
#     def _stream(self, prompt: str, stop: Optional[list[str]] = None,
#                 run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any) -> Iterator[GenerationChunk]:
#         pass
#
#     @property
#     def _llm_type(self) -> str:
#         pass
#
#     def with_structured_output(self, schema: Union[dict, type], **kwargs: Any) -> Runnable[
#         LanguageModelInput, Union[dict, BaseModel]]:
#         pass
