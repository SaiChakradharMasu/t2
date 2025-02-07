import requests
from .agent_tools import AgentTools
from google.cloud import storage

class SellerTools(AgentTools):
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
            self.system_instructions = blob.download_as_string().decode('utf-8')
            
            return True

        except Exception as e:
            print("Error:", e)
            return False
    
    def get_system_instructions(self) -> str:
        return self.system_instructions
        
    def fc_get_status_of_price_request(self, product_name: str, customer_name: str) -> str:
        """Returns the status of a price request for a specific product, made by a specific customer.
        """
        # Envía la petición GET con parámetros y cabeceras
        params = {
            "productName": product_name,
            "customerName": customer_name
        }
        
        response = requests.get(self.base_url  + "/price-request-status", params=params, headers=self.headers)

        # Verifica el código de estado de la respuesta
        if response.status_code == 200:
            # La petición se realizó con éxito
            data = response.json()
            status = data["status"]
            
            print(data)
            
            return f"the status of the request for product {product_name} of customer {customer_name} is {status}"
        else:
            # Hubo un error en la petición
            print(f"Error: {response.status_code}")
            print(response.text)
            return "No data found for that params"

    def fc_get_customer_contact_info_by_name(self, customer_name: str) -> str:
        """Returns contact information for a customer given their name.
        Args:
            customer_name (str): Name of the client for whom you wish to obtain contact information.
        Returns:
            str: JSON string containing the customer's contact details: email, phone number.
        """
        # Envía la petición GET con parámetros y cabeceras
        params = {
            "customerName": customer_name
        }
        
        response = requests.get(self.base_url  + "/client-contact", params=params, headers=self.headers)

        # Verifica el código de estado de la respuesta
        if response.status_code == 200:
            # La petición se realizó con éxito
            data = response.json()
            status = data["status"]
            
            print(data)
            
            return f""
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