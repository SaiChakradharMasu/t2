from pydantic import BaseModel
from datetime import datetime

class Conversation(BaseModel):
    conversation_id: str | int
    user_id: str | int
    start_date: datetime | None
    messages: list

    def is_conversation_available(self):
        start = self.start_date.replace(tzinfo=None)
        end = datetime.now().replace(tzinfo=None)
        diff = end - start
        hours = diff.total_seconds() / (60 * 60)
        print(hours)
        return hours <= 22