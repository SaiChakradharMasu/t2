from domain.agent.agent import Agent
# from domain.agent.function_declarations.function_declarations import AgentTools
from domain.agent.tools.agent_tools import AgentTools
from domain.user import User
from domain.conversation import Conversation


def handle_message(conversation: Conversation, message: str, agent_tools: AgentTools) -> str:
    agent = Agent(agent_tools)
    print(agent)
    history = conversation.messages
    
    if history:
        chat_session = agent.start_chat(history)
    else:
        chat_session = agent.start_chat()
        
    response = chat_session.send_message(message)
    
    return response.text

def handle_file(file, message, agent_tools: AgentTools) -> str:
    agent = Agent(agent_tools)
    file_uploaded = agent.uplaoad_file(file)

    chat_session = agent.start_chat()
    response = chat_session.send_message([file_uploaded, message])
    
    return response.text

    