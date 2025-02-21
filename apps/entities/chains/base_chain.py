import asyncio

from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

from apps.entities.chat_models.chat_models import base_chat

# Base LLM Chain Usage


prompt = PromptTemplate(
    template="{country}는 뭘로 유명해? ", input_variables=["country"]
)

# chain = LLMChain(llm=base_chat, prompt=prompt)
chain = prompt | base_chat

# print(chain.invoke({"country": "한국"}))

# print(chain.predict(country="한국"))


"""
stream Usage
"""

"""
batch Usage
"""


async def chain_ainvoke(input_dict):
    print(f"ainvoke 콜 시작!, {input_dict}")
    return await chain.ainvoke(input_dict)


import time


async def main(*args):
    start_time = time.time()
    responses = await asyncio.gather(
        *[
            chain_ainvoke(input_dict={"country": "한국"}),
            chain_ainvoke(input_dict={"country": "미국"}),
            chain_ainvoke(input_dict={"country": "중국"}),
            chain_ainvoke(input_dict={"country": "일본"}),
            chain_ainvoke(input_dict={"country": "대만"}),
            chain_ainvoke(input_dict={"country": "러시아"}),
        ]
    )
    end_time = time.time()
    print(end_time - start_time)
    for response in responses:
        print(response)
    return response


# asyncio.run(main())

# import time
#
# start_time = time.time()
# chain.invoke({"country": "한국"})
# chain.invoke({"country": "미국"})
# chain.invoke({"country": "중국"})
# chain.invoke({"country": "일본"})
# chain.invoke({"country": "대만"})
# chain.invoke({"country": "러시아"})
# end_time = time.time()
#
# print(end_time - start_time)
