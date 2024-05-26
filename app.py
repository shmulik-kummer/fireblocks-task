from fireblocks_sdk import FireblocksSDK
from flask import Flask
import config
from routes import routes
import logging_config

app = Flask(__name__)

# Initialize Fireblocks SDK
fireblocks = FireblocksSDK(config.API_SECRET, config.API_KEY, config.API_URL)

# Register Blueprints
app.register_blueprint(routes)

# Start flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
