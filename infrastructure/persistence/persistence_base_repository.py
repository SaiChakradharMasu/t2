from abc import ABC, abstractmethod
from domain.conversation import Conversation

class PersistenceBaseRepository(ABC):

    @abstractmethod
    def create_conversation(self, user_id: int | str) -> Conversation:
        pass

    @abstractmethod
    def get_conversation(self, user_id: int | str) -> Conversation:
        pass
    
    @abstractmethod
    def log_conversation(
        self,
        user_id: int | str,
        conversation_id: int | str,
        role: str,
        parts: str
    ) -> bool:
        pass