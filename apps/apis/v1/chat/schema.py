from pydantic import BaseModel


class ClientInformation(BaseModel):
    session_id: str
    question: str

    def __str__(self):
        return str(self.model_dump())
