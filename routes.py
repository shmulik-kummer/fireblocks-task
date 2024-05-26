from flask import Blueprint, jsonify, request
import config
from utils import get_wallet_balance, create_transaction, is_transaction_completed, handle_low_balance
import logging
import json

logger = logging.getLogger(__name__)

routes = Blueprint('routes', __name__)


@routes.route('/', methods=['GET'])
def root():
    return "Hello from Fireblocks app"


@routes.route('/webhook', methods=['POST'])
def webhook():
    webhook_data = request.json

    # Proceed only if the status is COMPLETED and subStatus is CONFIRMED
    if is_transaction_completed(webhook_data):

        # Pretty-print the JSON data
        pretty_data = json.dumps(webhook_data, indent=4)

        logger.info("Confirmed transaction Webhook received: %s", pretty_data)
        logger.info("Going to check the balance of the expense a"
                    "ccount")

        # Check the balance of the expense account
        expense_balance = get_wallet_balance(config.EXPENSE_ACCOUNT_ID, config.ASSET_ID)

        # If balance is below the threshold, create a transaction
        if expense_balance < config.BALANCE_THRESHOLD:
            return handle_low_balance(balance=expense_balance)

        logger.info("Balance is sufficient")
        return jsonify({"status": "success", "message": "Balance is sufficient"}), 200

    return jsonify({"status": "received", "message": "Waiting for completed transaction webhook"}), 200
