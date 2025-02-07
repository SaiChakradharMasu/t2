from dotenv import load_dotenv
import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
from .config import agent_config
import tempfile
from .tools.agent_tools import AgentTools
load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class Agent():
    def __init__(self, anget_tools: AgentTools) -> None:

        tools = anget_tools.get_tools()
        print("Test", tools)
        system_instruction = anget_tools.get_system_instructions()#Responsible to get the order status and stuff
        
        config = { 
            **agent_config,
            "tools": tools if tools else None,
            "system_instruction": system_instruction 
        }
        
        self.model = genai.GenerativeModel(**config) #Directly passes the parameters.
        # self.chat_session = None

    def start_chat(self, chat_history=[]) -> genai.ChatSession:
        return self.model.start_chat(
                history=chat_history,
                enable_automatic_function_calling=True
            )
        
    def uplaoad_file(self, file):
        file_uploaded = None
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            mimetype = file.mimetype
            file_data = file.read()
            temp_file.write(file_data)
            temp_file_path = temp_file.name
            
            file_uploaded = genai.upload_file(
                temp_file_path, 
                mime_type=mimetype
            )

            return file_uploaded

        return None