from entities.retrievals.wikipedia_retriever.wiki_retriever import (
    wikipedia_english_retriever,
    wikipedia_korea_retriever,
)
from pydantic import BaseModel, Field
from entities.chat_models.chat_models import base_chat
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda,
)
from typing import List


class KoreaWikiInput(BaseModel):
    korea_input: str = Field(
        ..., description="The keyword to search on Wikipedia in Korean."
    )


class EnglishWikiInput(BaseModel):
    english_input: str = Field(
        ..., description="The keyword to search on Wikipedia in English."
    )


# base_chat.with_structured_output()
# response = base_chat.with_structured_output(KoreaWikiInput).invoke("kimkoo")
# print(response, type(response))
# print(base_chat.with_structured_output(EnglishWikiInput).invoke("김구"))

wiki_runnable_chain = RunnableParallel(
    input=RunnablePassthrough(),
    korea=lambda x: base_chat.with_structured_output(KoreaWikiInput).invoke(
        x["korea_input"]
    ),
    english=lambda x: base_chat.with_structured_output(KoreaWikiInput).invoke(
        x["english_input"]
    ),  # 아래에서 최초 input 을 유지하는 방법임 . 다른의미는 없음
) | RunnableLambda(lambda x: {**x["input"]})

# print(
#     wiki_runnable_chain.invoke(
#         {"korea_input": "who is lee-jae-yong", "english_input": "지조암이 누구야"}
#     )
# )


class Question(BaseModel):
    domain: str = Field(..., description="The domain of the question.")
    question: str = Field(..., description="The question text.")


class QuestionResponse(BaseModel):
    questions: List[Question]


# print(base_chat.with_structured_output(QuestionResponse).invoke("안녕?"))
