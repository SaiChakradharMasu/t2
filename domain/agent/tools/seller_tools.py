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
    def function_schema(schema):
        """Decorator to attach function schema metadata to a function."""
        def wrapper(func):
            func.schema = schema  # Attach schema metadata to function
            return func
        return wrapper
    def load_system_instructions(self) -> bool:
        try:
            storage_client = storage.Client()
            bucket_name = "masu-bucket"
            source_blob_name = "agents_system_instructions/masu_private_agent_instructions.txt"
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            extra_instructions = """### SYSTEM INSTRUCTIONS FOR ORDER CREATION PROCESS
            1 **User enters Company ID → Call `fc_find_customer_by_id`**
            - If the customer exists  → Proceed.
            - If not  → Ask the user to provide the company name.

            2 **User enters Company Name → Call `fc_find_customer_by_name`**
            - If an exact match is found  → Confirm and proceed.
            - If no exact match  → Return fuzzy-matched names sorted by `match_score` and ask the user to choose.

            3 **User enters Product ID → Call `fc_find_product_by_id`**
            - If the product exists → Proceed.
            - If not  → Ask the user to search by product name.

            4 **User enters Product Name → Call `fc_find_product_by_name`**
            - If a matching product is found  → Confirm product ID and proceed.
            - If no match  → Show an error message.

            5 **User finalizes order → Call `fc_create_order`**
            - If successful  → Order is placed and confirmation is sent.
            - If there are missing or incorrect details  → Ask the user to correct errors.

            ### **Function Call Flow**
            - **Primary Calls:**
            - `fc_find_customer_by_id(company_id)`
            - `fc_find_customer_by_name(company_name)`
            - `fc_find_product_by_id(product_id)`
            - `fc_find_product_by_name(product_name)`
            - `fc_create_order(customer_id, products, expected_delivery_start_date, payment_type, delivery_type)`

            - **Clarification Questions:**
            - If customer ID is invalid → "Could you provide the company name instead?"
            - If company name is not found → "We found similar companies: [Company List]. Which one do you mean?"
            - If product ID is invalid → "Could you provide the product name instead?"
            - If product name is not found → "We found similar products: [Product List]. Which one do you mean?"

            💡 **Language Support**: The chatbot should detect if the user is communicating in **English or Spanish** and provide responses accordingly.

            ⚠️ **Restrictions**
            - The chatbot will **not process orders** without verifying the customer and product details.
            - The chatbot **will not modify** existing orders, only create new ones.
            - The chatbot **should ensure all required fields** are collected before calling `fc_create_order`."""
            blob = bucket.get_blob(source_blob_name)
            self.system_instructions = blob.download_as_string().decode('utf-8') #+ extra_instructions
            return True

        except Exception as e:
            print("Error:", e)
            return False
    @function_schema({
        "name": "fc_get_invoice_by_order_id",
        "description": "Retrieves the invoice URL for a given order ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order ID for which the invoice is requested."
                }
            },
            "required": ["order_id"]
        }
    })
    def fc_get_invoice_by_order_id(self, order_id: str) -> dict:
        """
        Returns a test invoice file (PDF) for a given order ID.
        
        Args:
            order_id (str): The order ID for which the invoice is requested.

        Returns:
            dict: JSON containing a file URL pointing to a blank test PDF.
        """
        print("order_id:------------------", order_id)
        # Returning a Static File URL (For testing)
        invoice_response = {
            "message": f"Here is the invoice for Order ID {order_id}.",
            "invoice": {
                "type": "pdf",
                "filename": f"invoice_{order_id}.pdf",
                "url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
            }
        }
        
        return invoice_response
    @function_schema({
    "name": "fc_find_customer_by_id",
    "description": "Finds customer details using a unique company ID.",
    "parameters": {
        "type": "object",
        "properties": {
            "company_id": {
                "type": "string",
                "description": "Unique identifier for the company."
            }
        },
        "required": ["company_id"]
    }
})
    def fc_find_customer_by_id(self, company_id: str) -> dict:
        """Returns company details if the company ID exists."""
        print(10)
        mock_data = {
            "12345": {"customer_id": "12345", "customer_name": "ABC Corp", "exists": True},
            "67890": {"customer_id": "67890", "customer_name": "XYZ Ltd", "exists": True},
        }
        return mock_data.get(company_id, {"exists": False})
    
    def fc_create_order(self, company_id: str, product_id: str, quantity: str, price: str, expected_delivery_start_date: str, payment_type: str, delivery_type: str) -> str:
        """Returns the order details when asked to create the order"""
        print(company_id, product_id, quantity, price, expected_delivery_start_date, payment_type, payment_type, delivery_type)
        
        t1 = self.fc_find_customer_by_id()
        if t1==True:
            print(20)
        else:
            return "Company id is not found provide proper company id"
        return company_id, product_id, quantity, price, expected_delivery_start_date, payment_type, payment_type, delivery_type
    
    


    def get_system_instructions(self) -> str:
        return self.system_instructions
        
    def fc_get_status_of_price_request(self, product_name: str, customer_name: str) -> str:
        """Returns the status of a price request for a specific product, made by a specific customer.
        """
        print(1)
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