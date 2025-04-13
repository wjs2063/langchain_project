from typing import Dict, Any, List

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.conversational_retrieval.base import (
    ConversationalRetrievalChain,
    BaseConversationalRetrievalChain,
)
from langchain_core.callbacks import (
    AsyncCallbackManagerForChainRun,
    CallbackManagerForChainRun,
)
from langchain_core.documents import Document
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.retrievers import BaseRetriever
from apps.entities.retrievals.wikipedia_retriever.wiki_retriever import (
    wikipedia_korea_retriever,
    wikipedia_english_retriever,
)


# 다수의 retriever 를 조합한 chain
class ConversationalMultiRetrieverChain(BaseConversationalRetrievalChain):
    def _get_docs(
        self,
        question: str,
        inputs: Dict[str, Any],
        *,
        run_manager: CallbackManagerForChainRun,
    ) -> List[Document]:
        # inputs 에 retriever key 로 받아서 동시호출 날리는 방식
        pass

    async def _aget_docs(
        self,
        question: str,
        inputs: Dict[str, Any],
        *,
        run_manager: AsyncCallbackManagerForChainRun,
    ) -> List[Document]:
        pass

    @property
    def _chain_type(self) -> str:
        pass


runnable_chain = RunnableParallel(
    wikipedia_korea_result=lambda x: wikipedia_korea_retriever.invoke(x["korea_input"]),
    wikipedia_english_result=lambda x: wikipedia_english_retriever.invoke(
        x["english_input"]
    ),
)

# response = runnable_chain.invoke(
#     {"korea_input": "한국", "english_input": "about korea"}
# )

# print(response["wikipedia_korea_result"])
# print(response["wikipedia_english_result"])
#
# runnable = {"question": lambda x: x["question"] + "convert"} | RunnablePassthrough()
#
# print(runnable.invoke({"question": "hello"}))
