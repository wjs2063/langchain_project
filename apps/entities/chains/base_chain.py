from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from apps.entities.chat_models.chat_models import base_chat
import asyncio

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
    return await chain.ainvoke({k: v for k, v in input_dict.items()})


async def main(*args):
    responses = await asyncio.gather(
        *[
            chain_ainvoke(input_dict={"country": "한국"}),
            chain_ainvoke(input_dict={"country": "미국"}),
            chain_ainvoke(input_dict={"country": "중국"}),
        ]
    )
    for response in responses:
        print(response)
    return response


asyncio.run(main())
