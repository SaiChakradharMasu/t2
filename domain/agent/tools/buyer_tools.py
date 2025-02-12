import requests
import json
from .agent_tools import AgentTools
from google.cloud import storage

class BuyerTools(AgentTools):
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
            self.system_instructions = blob.download_as_string().decode('utf-8')+"If user ask for the his role then tell him that you are a buyer" #"Extract the order id from the message"
            return True

        except Exception as e:
            print("Error:", e)
            return False
    
    def get_system_instructions(self) -> str:
        return self.system_instructions
        
    def fc_get_status_by_order_id(self, order_id: str) -> str:
        """Returns the status of a specific order using its order_id.

        Args:
            order_id (str): ID of the order whose status you want to obtain.

        Returns:
            str: JSON string containing the "status" and the "orderId".
        """

        return "Order 111 is ready to go"
        # Envía la petición GET con parámetros y cabeceras
        params = {
            "orderId": order_id,
        }
        
        response = requests.get(self.base_url  + "/order-status", params=params, headers=self.headers)

        # Verifica el código de estado de la respuesta
        if response.status_code == 200:
            # La petición se realizó con éxito
            data = response.json()
            
            return json.dumps(data)
        else:
            # Hubo un error en la petición
            print(f"Error: {response.status_code}")
            print(response.text)
            return "No data found for that params"

    def fc_available_presentations_by_product_name(self, pruduct_name: str) -> str:
        """Returns the available presentations or grades of a product given its name.
        
        Args:
            pruduct_name (str): Name of the product for which you wish to obtain the presentations.
            
        Returns:
            str: String list of presentations or grades available for that product.
        """
        # Envía la petición GET con parámetros y cabeceras
        params = {
            "pruductName": pruduct_name
        }
        
        response = requests.get(self.base_url  + "/product-grades", params=params, headers=self.headers)

        # Verifica el código de estado de la respuesta
        if response.status_code == 200:
            # La petición se realizó con éxito
            data = response.json()
            grades = data["grades"]
            
            return ", ".join(grades)
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