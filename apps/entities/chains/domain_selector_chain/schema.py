from typing import List
from pydantic import BaseModel, Field


class Question(BaseModel):
    domain: str = Field(
        ..., description="The domain of the question. rephrased question"
    )
    question: str = Field(..., description="The question text.")


class QuestionResponse(BaseModel):
    questions: List[Question] = Field(..., description="The list of Questions class")
