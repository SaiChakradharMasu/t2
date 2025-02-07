import os
from flask import Flask
from infrastructure.chat_controller import chat_controller
from infrastructure.middleware import middleware_list

app = Flask(__name__)


# Registrar los blueprints
app.before_request_funcs = {'chat_controller': middleware_list}
app.register_blueprint(chat_controller, url_prefix='/chat')
# app.register_blueprint(my_blueprint)

if __name__ == "__main__":
    app.run(
        debug=True, 
        host="0.0.0.0", 
        port=int(os.environ.get("PORT", 8080))
    )
