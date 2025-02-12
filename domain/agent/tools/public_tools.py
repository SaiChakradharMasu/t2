import requests
import json
from .agent_tools import AgentTools
from google.cloud.storage import Client, transfer_manager


class PublicTools(AgentTools):
    def __init__(self) -> None:
        self.load_system_instructions()
        
    def load_system_instructions(self) -> bool:
        try:
            bucket_name = "masu-bucket"
            source_blob_name = "agents_system_instructions/masu_public_agent_instructions.txt"
            
            storage_client = Client()
            bucket = storage_client.bucket(bucket_name)
            print("bucket:", bucket)
            blob = bucket.get_blob(source_blob_name)
            self.system_instructions = blob.download_as_string().decode('utf-8') +"If user ask for the his role then tell him that you are public bot"
            
            return True

        except Exception as e:
            print("AQUI Error:", e)
            return False
    
    def get_system_instructions(self) -> str:
        return self.system_instructions
    
    def get_name_tools(self) -> list:
        """Returns the list of function callings.
        """
        all_methods = dir(self)
        cf_methods = []
        
        for method_name in all_methods:
            if method_name.startswith("fc"):
                cf_methods.append(method_name)

        return cf_methods

    def get_tools(self) -> list:
        """Returns the list of function callings.
        """
        name_tools = self.get_name_tools()
        tools = []
        for name in name_tools:
            tools.append(getattr(self, name))
        return tools