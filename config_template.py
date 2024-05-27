# Configuration values
TREASURY_ACCOUNT_ID = "ID"
ASSET_ID = "AMOY_POLYGON_TEST"
EXPENSE_ACCOUNT_IDS = [
    {'id': "ID", 'threshold': 0.3},
    # Add additional wallets if needed
]

# Fireblocks SDK configuration
API_KEY = 'YOUR_API_KEY'
API_SECRET_PATH = 'path/to/your/fireblocks_secret.key'
API_URL = 'FIREBLOCKS ENDPOINT (use https://api.fireblocks.io for testing)'

# Gmail config
EMAIL = "USER_EMAIL"
EMAIL_APP_PASSWORD = 'GMAIL_APP_PASSWORD'

# Load API secret (this line can be uncommented once you create your own config.py)
# with open(API_SECRET_PATH, 'r') as file:
#     API_SECRET = file.read()
