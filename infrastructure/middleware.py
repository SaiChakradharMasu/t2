from flask import Blueprint, request, jsonify, g, redirect, url_for
import requests

my_blueprint = Blueprint('my_blueprint', __name__)

AUTH_PROFILE_URL = "https://staging.masu-api.com/api/auth/profile"

def valid_token():
    test_bot = request.args.get('test-bot')
    
    if hasattr(g, "is_public") and g.is_public:
        return
    
    data_json = request.get_json()
    print("***************************************")
    print(data_json)
    print("***************************************")
    print(request.headers)
    print("***************************************")
    token = None
    if test_bot:
        print("Entro a Test")
        token = request.headers.get("Role-Token")
        g.test_bot = True
    else:
        print("Entro Normal")
        token = data_json.get("metadata", {}).get("KM_CHAT_CONTEXT", {}).get("token")
    print("***************************************")
    print(token)
    print("***************************************")
    if token:
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": "masu"
        }
        
        try:
            data = requests.get(url=AUTH_PROFILE_URL, headers=headers)

            if data.status_code == 200:
                user_info = data.json()
                print("USER_INFO: ", user_info)
                if hasattr(g, 'user_info'):
                    print( g.user_info )
                else:
                    g.user_info = user_info
                return
            else:
                print(data)
                print("Invalid token")
                return jsonify({ 'message': "Invalid token", 'success': False })
                
        except Exception as ex:
            print(ex)
            return jsonify({ 'message': "Error to trying token", 'success': False })
    else:
        return jsonify({ 'message': "Token is missing", 'success': False })

def check_route():
    url = request.path
    
    if url == "/chat/public":
        g.is_public = True
        return
    elif url == "/chat" or url == "/chat/":
        request.path = request.path + "/seller"
        return
    else:
        return jsonify([{ 'message': "Invalid route path", 'success': False }])

middleware_list = [
    check_route,
    valid_token
]