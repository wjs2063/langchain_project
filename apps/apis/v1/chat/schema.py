from pydantic import BaseModel


class ClientInformation(BaseModel):
    session_id: str
    question: str

    def __str__(self):
        return str(self.model_dump())

    model_config = {
        "populate_by_name": True,
        "str_strip_whitespace": True,
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "session_id": "123",
                "question": "내일 일정 알려줘",
            }
        },
    }
