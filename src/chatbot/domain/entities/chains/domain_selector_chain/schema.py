from typing import List
from pydantic import BaseModel, Field


class DomainSchema(BaseModel):
    general: bool = Field(
        ..., description="General query related to common knowledge or conversation."
    )
    wikipedia: bool = Field(
        ..., description="Query related to Wikipedia information retrieval."
    )
    weather: bool = Field(
        ..., description="Query related to weather forecast or conditions."
    )
    schedule: bool = Field(
        ..., description="Query related to scheduling or calendar events."
    )


class ResponseSchema(BaseModel):
    domain: DomainSchema = Field(
        ..., description="Classification of the query into different domains."
    )


class Question(BaseModel):
    domain: str = Field(
        ..., description="The domain of the question. rephrased question"
    )
    question: str = Field(..., description="The question text.")


class QuestionResponse(BaseModel):
    questions: List[Question] = Field(..., description="The list of Questions class")
