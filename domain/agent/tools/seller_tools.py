import requests
from .agent_tools import AgentTools
from google.cloud import storage
import json
class SellerTools(AgentTools):
    def __init__(self, token: str, url: str) -> None:
        self.headers = {
            "X-tenant-id": "masu",
            "Authorization": f"Bearer {token}"
        }
        self.token = token
        self.base_url = url
        print(self.base_url)
        self.load_system_instructions()
        self.CUSTOMER_DATA = {
            "12345": {"customer_id": "12345", "customer_name": "ABC Corp", "exists": True},
            "67890": {"customer_id": "67890", "customer_name": "XYZ Ltd", "exists": True},
            "1f61262f-629e-4d72-a24e-72818f135361": {
                "customer_id": "1f61262f-629e-4d72-a24e-72818f135361",
                "customer_name": "Deepak Polymer Resins PVC",
                "exists": True
            },
            "882aebd3-d93c-464b-a3ae-c049f16434cf": {
                "customer_id": "882aebd3-d93c-464b-a3ae-c049f16434cf",
                "customer_name": "Alexprueba",
                "exists": True
            }
        }

        self.PRODUCT_DATA = {
            "001": {"product_id": "001", "product_name": "Steel Rod", "exists": True},
            "002": {"product_id": "002", "product_name": "Copper Wire", "exists": True},
            "6ff5e1a0-ac65-4ebe-9ad8-24e73fd8f673": {
                "product_id": "6ff5e1a0-ac65-4ebe-9ad8-24e73fd8f673",
                "product_name": "LLDPE 2517",
                "exists": True
            },
            "09c3d0b2-a9c1-4694-bb32-3a16fae3360e": {
                "product_id": "09c3d0b2-a9c1-4694-bb32-3a16fae3360e",
                "product_name": "mLLDPE MARLEX D163",
                "exists": True
            },
            "07b527d1-fec8-4423-be06-3f68300fbb8f": {
                "product_id": "07b527d1-fec8-4423-be06-3f68300fbb8f",
                "product_name": "LDPE LDF0025",
                "exists": True
            },
            "af2b0763-7982-4d9e-94b7-177fc9c5344d": {
                "product_id": "af2b0763-7982-4d9e-94b7-177fc9c5344d",
                "product_name": "PPC PP7032KN",
                "exists": True
            }
        }
        self.CUSTOMER_NAME_DATA = {
    "ABC Corp": {"customer_id": "12345", "customer_name": "ABC Corp"},
    "ABCD Construction": {"customer_id": "67890", "customer_name": "ABCD Construction"},
    "ABC Solutions": {"customer_id": "54321", "customer_name": "ABC Solutions"}
}
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
            source_blob_name = "agents_system_instructions/SI.txt"
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.get_blob(source_blob_name)
            extra_instruction = """
            If user ask for the his role then tell him that you are a seller
            Answer role 
                        Role-Based Supported Queries (Seller)

            Eric supports the following queries for Sellers and dynamically provides assistance based on these queries:
                1.	Checking Price Requests
                •	Example: “What's the status of my price request for [product name] for [customer name]?”
                2.	Order History
                •	Example: “Show me the order history for [customer name] in the last quarter.”
                3.	Top-Selling Products
                •	Example: “What are the top 5 selling products in [product category] this month?”
                4.	Customer Contact Information
                •	Example: “What's the contact information for [customer name]?”
                5.	Pending Payments
                •	Example: “Is there any pending payment from [customer name]?”

            Query Handling for Sellers
                •	If a query lacks details, Eric will prompt for missing information.
            Example:
            User: “What's the status of my price request?”
            Eric: “Could you specify the product name and customer name for the request?”
                •	If the user provides incomplete or incorrect details, Eric will ask for clarification.
            Example:
            Eric: “I couldn't find any data with the details provided. Could you verify the product name or customer name and try again?”

            Guidance for Out-of-Scope Questions
                •	If a Seller asks an unsupported question, Eric will redirect them to relevant queries:
            Example:
            Eric: “I'm sorry, I can't assist with that request. However, I can help with checking price requests, order history, and pending payments. Let me know how I can assist you!"""
            self.system_instructions = blob.download_as_string().decode('utf-8')+ extra_instruction
            print(self.system_instructions)
            return True

        except Exception as e:
            print("Error:", e)
            return False
    import requests

    def create_direct_order(self, customer_id, product_id, presentation, quantity, target_price):
        """
        Function to send a POST request to create an order with required fields and optional fields as null.
        
        :param bearer_token: str, Authorization token for API authentication
        :param customer_id: str, Unique identifier for the customer
        :param product_id: str, Unique identifier for the product
        :param presentation: str, Product packaging/presentation type
        :param quantity: int, Quantity of the product being ordered
        :param target_price: float, Target price for the product
        :return: dict, API response as JSON
        """

        # API Endpoint
        url = "https://staging.masu-api.com/api/orders/create-direct"

        # Headers
        headers = {
            "accept": "application/json",
            "X-Tenant-ID": "masu",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        # Payload with required fields, and optional fields set to null
        payload = {
            "currency": "USD",
            "environment": "",
            "comments": "",
            "isSeller": "",
            "quantityDelivered": "",
            "hasIva": "",
            "customer": {
                "id": customer_id
            },
            "items": [
                {
                    "productId": product_id,
                    "presentation": presentation,
                    "quantity": quantity,
                    "targetPrice": target_price
                }
            ],
            "idRequestUser": "",
            "deliveryFrequency": "Once a week",
            "deliveryDate": "2025-02-11T19:35:58.434Z",
            "addressId": "",
            "paymentTerm": "Crédito",
            "deliveryModel": "Dropshipping",
            "fileOne": "",
            "fileTwo": "",
            "fileThree": "",
            "requiredInvoice": True
        }

        # Making the POST request
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        # Returning response JSON
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response", "status_code": response.status_code, "response": response.text}
        
    def fc_find_customer_by_id1(self,company_id: str) -> dict:
        """
        Finds customer details using a unique company ID.
        """
        return self.CUSTOMER_DATA.get(company_id, {"exists": False})

    def fc_find_product_by_id(self,product_id: str) -> dict:
        """
        Finds product details using a unique product ID.
        """
        return self.PRODUCT_DATA.get(product_id, {"exists": False})

    """    def create_order(self, customer_id: str, product_id: str, presentation: str, quantity: int, target_price: str, price: str) -> dict:

        order_data = {
            "customer id": customer_id,
            "products": product,
            "expected delivery": expected_delivery_start_date,
            "payment type": payment_type,
            "quantity" : quantity,
            "price" : price,
            "delivery type": delivery_type
        }
        print(order_data)
        return {
            "message": "Order successfully created!",
            "order_details": f'customer id={customer_id}' ,
            "Prompt": "Just say order created successfully and the order detials should be exactly as I send, dont take the one in the memeory"

        }"""
    def fc_create_order(self, customer_id: str, product_id: str, presentation: str, quantity: int, target_price: str) -> str:
        """Returns the order details when asked to create the order"""
        print(customer_id, product_id, quantity, presentation, quantity, target_price)
        print("Step 1: Finding Customer by ID")
        customer_info = self.fc_find_customer_by_id1(customer_id)
        product_info = self.fc_find_product_by_id(product_id)
        print("Customer Found:", customer_info)
        y = 0
        if customer_info['exists'] and product_info:
            print(y)
            y =1
            order = self.create_direct_order(
            customer_id= customer_id,
            product_id = product_id,
            quantity = quantity,
            target_price = target_price,
            presentation=presentation,
        )
        if y == 0:
            return "Entered cutomer and product id are not in the system, kindly reenter"
        else:
            return order
        if company_id != "111":
            self.system_instructions+"As the company id worng get the company name and pass it through in the company id order creation "
            return "Entered company id is wrong, kindly enter the correct company id or the company name"

        else:
            return company_id, product_id, quantity, price, expected_delivery_start_date, payment_type, payment_type, delivery_type
    def get_system_instructions(self) -> str:
        return self.system_instructions

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