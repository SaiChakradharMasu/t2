from pydantic import BaseModel 

class Chat(BaseModel):
    chat_id: str | int
    history: list