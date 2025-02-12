import requests
import json
from .agent_tools import AgentTools
from google.cloud import storage

class OperationsPersonTools(AgentTools):
    def __init__(self, token: str, url: str) -> None:
        self.headers = {
            "X-tenant-id": "masu",
            "Authorization": f"Bearer {token}"
        }
        self.base_url = url
        self.load_system_instructions()
        
    def load_system_instructions(self) -> bool:
        try:
            storage_client = storage.Client()
            bucket_name = "masu-bucket"
            source_blob_name = "agents_system_instructions/masu_private_agent_instructions.txt"
            
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.get_blob(source_blob_name)
            self.system_instructions = blob.download_as_string().decode('utf-8') + "If user ask for the his role then tell him that you are a operations person"
            
            return True

        except Exception as e:
            print("Error:", e)
            return False
    
    def get_system_instructions(self) -> str:
        return self.system_instructions
          
    def fc_get_total_number_of_orders_pending(self) -> int:
        """Returns the total number of orders that are pending processing.
        """
        response = requests.get(self.base_url + "/pending-orders-count", headers=self.headers)

        # Verifica el código de estado de la respuesta
        if response.status_code == 200:
            # La petición se realizó con éxito
            data = response.json()
            
            return data
        else:
            # Hubo un error en la petición
            print(f"Error: {response.status_code}")
            print(response.text)
            return "No data found for that params"

    def fc_get_price_requests_pending_approval(self) -> int:
        """Obtains the number of price requests pending approval
        """
        
        response = requests.get(self.base_url + "/pending-price-requests-count", headers=self.headers)

        # Verifica el código de estado de la respuesta
        if response.status_code == 200:
            # La petición se realizó con éxito
            data = response.json()
            
            return data
        else:
            # Hubo un error en la petición
            print(f"Error: {response.status_code}")
            print(response.text)
            return "Unable to obtain information"
        

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