import requests
from abc import ABC, abstractmethod

class AgentTools(ABC):

    @abstractmethod
    def load_system_instructions(self) -> bool:
        pass

    @abstractmethod
    def get_system_instructions(self) -> str:
        pass
    
    @abstractmethod
    def get_name_tools(self) -> list:
        pass
    
    @abstractmethod
    def get_tools(self) -> list:
        pass