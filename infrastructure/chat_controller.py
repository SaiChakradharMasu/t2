from flask import Blueprint, request, jsonify, g, redirect, url_for
from application.handle_message import handle_message, handle_file
from infrastructure.adapters.firestore_conn import FirestoreConn
from domain.agent.tools import (
    seller_tools, 
    buyer_tools, 
    operations_person_tools, 
    manager_tools,
    public_tools
)

from .user_role import UserRole
import json
import sys

chat_controller = Blueprint('chat_controller', __name__)
URL = "https://staging.masu-api.com/api/external-api"

@chat_controller.route('', methods=['POST'])
def chat():
    url = request.path
    role = g.user_info["role"] #Buyer, 
    print(role)
    data = request.get_json()
    headers = request.headers
    user_role = UserRole(data, headers)

    if getattr(user_role, role):
        response = getattr(user_role, role)() #type of agent 
        return jsonify([{'message': response, 'success': True }])
    else:
        return jsonify([{'message': "role and method do not match", 'success': False }])

@chat_controller.route('/public', methods=['POST'])
def chat_public():
    try:
        data = request.get_json()

        message = data['message']
        from_user = data['from']
        
        agent_tools = public_tools.PublicTools()
        print("data", json.dumps(data))
        print(agent_tools)
        sys.stdout.flush()
        
        adapter = FirestoreConn()
        conversation = adapter.get_conversation(from_user)
        
        if conversation.is_conversation_available():
            response = handle_message(conversation=conversation, message=message, agent_tools=agent_tools)
            
            adapter.log_conversation(
                from_user,
                conversation.conversation_id, 
                "user", 
                message
            )
            adapter.log_conversation(
                from_user,
                conversation.conversation_id,
                "model", 
                response
            )

            response = jsonify([{'message': response }])
            return response
        else:
            conversation = adapter.create_conversation(from_user)
            response = handle_message(conversation=conversation, message=message, agent_tools=agent_tools)

            adapter.log_conversation(
                from_user,
                conversation.conversation_id, 
                "user", message
                )
            adapter.log_conversation(
                from_user,
                conversation.conversation_id,
                "model", response
                )

            response = jsonify([{'message': response, 'success': True }])
            return response
        
    except Exception as ex:
        print("ERROR: ", ex)
        sys.stdout.flush()
        return jsonify({ 'message': "ERROR", 'success': False })

    try:
        data = request.get_json()
        message = data['message']
        from_user = data['from']
        token = data['metadata']['KM_CHAT_CONTEXT']['token']
        botId = ""
        if token:
            botId = "eric-priv-uozpt"
        else:
            botId = "eric-by-masu-iybyf"
        
        return jsonify(
            [{
                "message": message,
                "from": from_user,
                "metadata": {
                    "KM_ASSIGN_TO": botId,
                    "token": token
                }
            }]
        )
    except Exception as ex:
        print("ERROR: ", ex)
        sys.stdout.flush()
        return jsonify({ 'message': "ERROR", 'success': False })