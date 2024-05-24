from fireblocks_sdk import FireblocksSDK
from flask import Flask
import config
from routes import routes

app = Flask(__name__)

# Use configurations from config file
TREASURY_ACCOUNT_ID = config.TREASURY_ACCOUNT_ID
EXPENSE_ACCOUNT_ID = config.EXPENSE_ACCOUNT_ID
ASSET_ID = config.ASSET_ID
BALANCE_THRESHOLD = config.BALANCE_THRESHOLD

# Initialize Fireblocks SDK
fireblocks = FireblocksSDK(config.API_SECRET, config.API_KEY, config.API_URL)

# Register Blueprints
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(port=5000)
