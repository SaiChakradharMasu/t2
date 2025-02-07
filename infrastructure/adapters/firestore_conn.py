from infrastructure.persistence.persistence_base_repository import PersistenceBaseRepository
from domain.conversation import Conversation
from google.cloud import firestore
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

firestore_db = os.environ.get('FIRESTORE_DB') # Get your table ID from environment
db = firestore.Client(database=firestore_db)

class FirestoreConn(PersistenceBaseRepository):
    def create_conversation(self, user_id: int | str) -> Conversation:
        user = db.collection("users").document(user_id)
        conversation_ref = user.collection("conversations").document()
        start_date = datetime.now()
        conversation_ref.set({
                "start_date": start_date,
            })

        conversation_data = {
                "conversation_id": str(conversation_ref.id),
                "user_id": user_id,
                "start_date": start_date,
                "messages": []
            }
        
        print("conversation added.")
        return Conversation(**conversation_data)

    def get_conversation_messages(self, conversation_ref) -> list:
        messages = conversation_ref.collection("messages")
        docs = messages.order_by('created_at').stream()
        messages = []
        for doc in docs:
            messages.append({ "role": doc.get("role"), "parts": [doc.get("parts")] })
        
        return messages


    def get_conversation(self, user_id: int | str) -> Conversation:
        conversations_ref = db.collection('users').document(user_id).collection('conversations')
        conversation = conversations_ref.order_by(
                'start_date', 
                direction=firestore.Query.DESCENDING
            ).limit(1).get()

        if not conversation:
            new_conversation = self.create_conversation(user_id)
            return new_conversation
        
        latest_conversation = conversation[0]
        latest_conversation_ref = conversations_ref.document(latest_conversation.id)

        messages = self.get_conversation_messages(latest_conversation_ref)
        
        info = {
            "conversation_id": latest_conversation.id,
            "user_id": user_id,
            "start_date": latest_conversation.get("start_date"),
            "messages": messages
        }

        return Conversation(**info)
        

    def log_conversation(
        self,
        user_id: int | str,
        conversation_id: int | str,
        role: str,
        parts: str
    ) -> bool:
        
        try:
            user = db.collection("users").document(user_id)
            conversation = user.collection("conversations").document(conversation_id)
            messages = conversation.collection("messages").document()
            messages.set({
                "role": role,
                "parts": parts,
                "created_at": datetime.now()
            })

            print("message added.")
            return True
        except:
            print("Failed to add message")
            return False