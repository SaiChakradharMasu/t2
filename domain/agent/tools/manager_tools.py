import requests
import json
from .agent_tools import AgentTools
from google.cloud import storage
class ManagerTools(AgentTools):
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
        
    def fc_get_total_sales_by_quarter(self, quarter: int) -> int:
        """Gets the total sales for a specific quarter (1, 2, 3 or 4).

        Args:
            quarter (int): quarter of the year

        Returns:
            int: returns the revenue for the given quarter
        """
        params = {
            "quarter": quarter,
        }

        response = requests.get(self.base_url + "/sales-revenue", params=params, headers=self.headers)
        # Verifica el código de estado de la respuesta
        if response.status_code == 200:
            # La petición se realizó con éxito
            data = response.json()
            revenue = data["revenue"]
            print("REVENUE", revenue)
            return revenue
        else:
            # Hubo un error en la petición
            print(f"Error: {response.status_code}")
            print(response.text)
            return "No data found for that params"

    def fc_get_highest_seller_with_conversion_rate(self) -> str:
        """Get the seller and the rate with the highest conversion rate.

            Returns:
                str: A JSON string whith the 'salesperson' and 'conversionRate'
        """
        
        response = requests.get(self.base_url + "/top-salesperson-conversion", headers=self.headers)

        # Verifica el código de estado de la respuesta
        if response.status_code == 200:
            # La petición se realizó con éxito
            data = response.json()
            
            return json.dumps(data)
        else:
            # Hubo un error en la petición
            print(f"Error: {response.status_code}")
            print(response.text)
            return "Unable to obtain information"

    def fc_get_repeat_orders_from_customers(self) -> str:
        """Obtain the list of customers who have made repeat orders only for this month
        """
        
        response = requests.get(self.base_url + "/repeat-customers", headers=self.headers)

        # Verifica el código de estado de la respuesta
        if response.status_code == 200:
            # La petición se realizó con éxito
            data = response.json()
            name_list = []
            
            for customer in data:
                name = customer["customerName"]
                name_list.append(name)
                
            print("name_list: ", name_list)
            return ", ".join(name_list)
        else:
            # Hubo un error en la petición
            print(f"Error: {response.status_code}")
            print(response.text)
            return "Unable to obtain information"

    def fc_get_average_value_orders_from_new_customers(self) -> int:
        """Gets the average value of orders placed by new customers
        """
        response = requests.get(self.base_url + "/avg-order-value-new-customers", headers=self.headers)
        # Verifica el código de estado de la respuesta
        if response.status_code == 200:
            # La petición se realizó con éxito
            data = response.json()
            avg_order_value = data["avgOrderValue"]
            
            return avg_order_value
        else:
            # Hubo un error en la petición
            print(f"Error: {response.status_code}")
            print(response.text)
            return "Unable to obtain information"

    def get_name_tools(self) -> list:
        """Returns the list names of function callings.
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