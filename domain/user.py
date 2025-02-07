from pydantic import BaseModel 

class User(BaseModel):
    user_id: str | int
    user_phone_number: int
    user_email: str
