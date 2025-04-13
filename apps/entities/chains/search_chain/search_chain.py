from langchain_core.runnables import (
    RunnableParallel,
    RunnableBranch,
    RunnablePassthrough,
    RunnableLambda,
)
from apps.entities.chains.search_chain.prompt import search_prompt
from apps.entities.chat_models.chat_models import base_chat
from apps.entities.tools.search.naver.encyclopedia import naver_search_runnable
import asyncio

flatten = RunnableLambda(
    lambda d: {
        **d["passthrough"],  # 원래 query, lang 등
        "search_results": d["search_results"],  # 추가된 검색 결과
    }
)

search_chain = (
    {
        "search_results": RunnableParallel(
            {
                "naver_serach_result": naver_search_runnable,
            }
        ),
        "passthrough": RunnablePassthrough(),
    }
    | flatten
    | search_prompt
    | base_chat
)


# async def main():
#     result = await search_chain.ainvoke("이순신")  # query 문자열을 입력
#     print(result)
#     return result


async def call_chain():
    """
    An asynchronous function that invokes a predefined chain using a provided input
    dictionary and returns the processed result.

    Attributes:
        None

    Args:
        None

    Returns:
        Any: The result obtained after invoking the predefined chain.

    Raises:
        None
    """
    result = await search_chain.ainvoke({"question": "이순신"})
    print(result)
    return result


if __name__ == "__main__":
    asyncio.run(call_chain())
