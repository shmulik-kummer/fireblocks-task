# routes.py
from flask import Blueprint, jsonify, request
import config
from fireblocks_utils import get_wallet_balance, create_transaction

routes = Blueprint('routes', __name__)


@routes.route('/', methods=['GET'])
def root():
    return "Hello from Fireblocks app"


@routes.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    # Proceed only if the status is COMPLETED and subStatus is CONFIRMED
    if data.get("data", {}).get("status") == "COMPLETED" and data.get("data", {}).get("subStatus") == "CONFIRMED":

        # Print webhook
        print("Confirmed transaction Webhook received:", data)

        print("Going to check the balance of the expense account")

        # Check the balance of the expense account
        expense_balance = get_wallet_balance(config.EXPENSE_ACCOUNT_ID, config.ASSET_ID)

        if expense_balance is None:
            print("Failed to retrieve balance")
            return jsonify({"status": "failure", "message": "Failed to retrieve balance"}), 500

        # If balance is below the threshold, create a transaction
        if expense_balance < config.BALANCE_THRESHOLD:
            amount_to_transfer = round(config.BALANCE_THRESHOLD - expense_balance, 3)
            print(
                f"Expense account reached the minimum threshold. going to top up account with {amount_to_transfer} MATIC")
            transaction = create_transaction(asset_id=config.ASSET_ID, amount=amount_to_transfer,
                                             src_id=config.TREASURY_ACCOUNT_ID,
                                             dest_id=config.EXPENSE_ACCOUNT_ID)
            if transaction:
                print("Transaction was created successfully")
                return jsonify({"status": "success", "transaction": transaction}), 200

            else:
                print("Failed to create transaction")
                return jsonify({"status": "failure", "message": "Failed to create transaction"}), 500

        print("Balance is sufficient")
        return jsonify({"status": "success", "message": "Balance is sufficient"}), 200

    # If the status is not COMPLETED, return a simple success response
    return jsonify({"status": "received", "message": "Waiting for transaction to complete"}), 200
