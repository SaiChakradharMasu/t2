import json
from flask import g, jsonify
from domain.agent.tools import (
    seller_tools, 
    buyer_tools, 
    operations_person_tools, 
    manager_tools,
    public_tools
)
from infrastructure.adapters.firestore_conn import FirestoreConn
from application.handle_message import handle_message, handle_file

URL = "https://staging.masu-api.com/api/external-api"

class UserRole:
    def __init__(self, data: any, headers: any):
        self.data = data
        self.headers = headers
        pass

    def seller(self):
        try:
            message = self.data['message']
            user_id = self.data['from']
            token = None

            if hasattr(g, "test_bot"):
                token = self.headers.get("Role-Token") #header or json
            else:
                token = self.data['metadata']['KM_CHAT_CONTEXT']['token']
            print("ENTRANDO AL SELLER...")
            agent_tools = seller_tools.SellerTools(token, URL)

            adapter = FirestoreConn()
            conversation = adapter.get_conversation(user_id)
            
            if conversation.is_conversation_available():
                response = handle_message(conversation=conversation, message=message, agent_tools=agent_tools)
                
                adapter.log_conversation(
                    user_id,
                    conversation.conversation_id, 
                    "user", 
                    message
                )
                adapter.log_conversation(
                    user_id,
                    conversation.conversation_id,
                    "model", 
                    response
                )

                return response
            else:
                conversation = adapter.create_conversation(user_id)
                response = handle_message(conversation=conversation, message=message, agent_tools=agent_tools)

                adapter.log_conversation(
                    user_id,
                    conversation.conversation_id, 
                    "user", message
                    )
                adapter.log_conversation(
                    user_id,
                    conversation.conversation_id,
                    "model", response
                    )
                
                return response
        
        except Exception as ex:
            print("ERROR: ", ex)
            return "Something happen"

    def customer(self):
        try:
            message = self.data['message']
            user_id = self.data['from']
            token = None

            if hasattr(g, "test_bot"):
                token = self.headers.get("Role-Token")
            else:
                token = self.data['metadata']['KM_CHAT_CONTEXT']['token']
            
            
            agent_tools = buyer_tools.BuyerTools(token, URL)
            
            adapter = FirestoreConn()
            conversation = adapter.get_conversation(user_id)
            
            if conversation.is_conversation_available():
                response = handle_message(conversation=conversation, message=message, agent_tools=agent_tools)
                
                adapter.log_conversation(
                    user_id,
                    conversation.conversation_id, 
                    "user", 
                    message
                )
                adapter.log_conversation(
                    user_id,
                    conversation.conversation_id,
                    "model", 
                    response
                )
                
                return response
            else:
                conversation = adapter.create_conversation(user_id)
                response = handle_message(conversation=conversation, message=message, agent_tools=agent_tools)

                adapter.log_conversation(
                    user_id,
                    conversation.conversation_id, 
                    "user", message
                    )
                adapter.log_conversation(
                    user_id,
                    conversation.conversation_id,
                    "model", response
                    )
                
                return response
            
        except Exception as ex:
            print("ERROR: ", ex)
            return "Something happen"

    def operations(self):
        try:
            message = self.data['message']
            user_id = self.data['from']
            token = None

            if hasattr(g, "test_bot"):
                token = self.headers.get("Role-Token")
            else:
                token = self.data['metadata']['KM_CHAT_CONTEXT']['token']
            
            agent_tools = operations_person_tools.OperationsPersonTools(token, URL)

            print("data", json.dumps(self.data))
            
            adapter = FirestoreConn()
            conversation = adapter.get_conversation(user_id)
            
            if conversation.is_conversation_available():
                response = handle_message(conversation=conversation, message=message, agent_tools=agent_tools)
                
                adapter.log_conversation(
                    user_id,
                    conversation.conversation_id, 
                    "user", 
                    message
                )
                adapter.log_conversation(
                    user_id,
                    conversation.conversation_id,
                    "model", 
                    response
                )
                
                return response
            else:
                conversation = adapter.create_conversation(user_id)
                response = handle_message(conversation=conversation, message=message, agent_tools=agent_tools)

                adapter.log_conversation(
                    user_id,
                    conversation.conversation_id, 
                    "user", message
                    )
                adapter.log_conversation(
                    user_id,
                    conversation.conversation_id,
                    "model", response
                    )
                
                return response
            
        except Exception as ex:
            print("ERROR: ", ex)
            return "Something happen"

    def admin(self):
        try:
            message = self.data['message']
            user_id = self.data['from']
            token = None

            if hasattr(g, "test_bot"):
                token = self.headers.get("Role-Token")
            else:
                token = self.data['metadata']['KM_CHAT_CONTEXT']['token']
            
            agent_tools = manager_tools.ManagerTools(token, URL)

            print("data", json.dumps(self.data))
            
            adapter = FirestoreConn()
            conversation = adapter.get_conversation(user_id)
            
            if conversation.is_conversation_available():
                response = handle_message(conversation=conversation, message=message, agent_tools=agent_tools)
                
                adapter.log_conversation(
                    user_id,
                    conversation.conversation_id, 
                    "user", 
                    message
                )
                adapter.log_conversation(
                    user_id,
                    conversation.conversation_id,
                    "model", 
                    response
                )
                
                return response
            else:
                conversation = adapter.create_conversation(user_id)
                response = handle_message(conversation=conversation, message=message, agent_tools=agent_tools)

                adapter.log_conversation(
                    user_id,
                    conversation.conversation_id, 
                    "user", message
                    )
                adapter.log_conversation(
                    user_id,
                    conversation.conversation_id,
                    "model", response
                    )
                
                return response
            
        except Exception as ex:
            print("ERROR: ", ex)
            return "Something happen"