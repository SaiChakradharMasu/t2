from pydantic import BaseModel 

class Message(BaseModel):
    role: str | int
    parts: list[str, any]