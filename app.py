from fireblocks_sdk import FireblocksSDK, TransferPeerPath, DestinationTransferPeerPath, VAULT_ACCOUNT
from flask import Flask, jsonify, request
import config

app = Flask(__name__)


# Use configurations from config file
TREASURY_ACCOUNT_ID = config.TREASURY_ACCOUNT_ID
EXPENSE_ACCOUNT_ID = config.EXPENSE_ACCOUNT_ID
ASSET_ID = config.ASSET_ID
BALANCE_THRESHOLD = config.BALANCE_THRESHOLD


# Initialize Fireblocks SDK
fireblocks = FireblocksSDK(config.API_SECRET, config.API_KEY, config.API_URL)


@app.route('/', methods=['GET'])
def root():
    return "Hello from Fireblocks app"


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    # Proceed only if the status is COMPLETED and subStatus is CONFIRMED
    if data.get("data", {}).get("status") == "COMPLETED" and data.get("data", {}).get("subStatus") == "CONFIRMED":

        # Print webhook
        print("Confirmed transaction Webhook received:", data)

        print("Going to check the balance of the expense account")

        # Check the balance of the expense account
        expense_balance = get_wallet_balance(EXPENSE_ACCOUNT_ID, ASSET_ID)

        if expense_balance is None:
            print("Failed to retrieve balance")
            return jsonify({"status": "failure", "message": "Failed to retrieve balance"}), 500

        # If balance is below the threshold, create a transaction
        if expense_balance < BALANCE_THRESHOLD:
            amount_to_transfer = round(BALANCE_THRESHOLD - expense_balance, 3)
            print(
                f"Expense account reached the minimum threshold. going to top up account with {amount_to_transfer} MATIC")
            transaction = create_transaction(asset_id=ASSET_ID, amount=amount_to_transfer, src_id=TREASURY_ACCOUNT_ID,
                                             dest_id=EXPENSE_ACCOUNT_ID, )
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


def get_wallet_balance(vault_account_id, asset_id):
    try:
        asset_info = fireblocks.get_vault_account_asset(vault_account_id, asset_id)
        balance = asset_info.get("balance")
        if balance is not None:
            formatted_balance = f"{float(balance):.3f}"
            print(f"Current Balance for account id {vault_account_id} is {formatted_balance} {asset_id}")
            return float(formatted_balance)
        else:
            print(f"No balance information found for asset ID {asset_id} in vault account {vault_account_id}.")
    except Exception as e:
        print(f"An error occurred while retrieving the balance: {e}")


def create_transaction(asset_id, amount, src_id, dest_id):
    tx_result = fireblocks.create_transaction(
        asset_id=asset_id,
        amount=amount,
        source=TransferPeerPath(VAULT_ACCOUNT, src_id),
        destination=DestinationTransferPeerPath(VAULT_ACCOUNT, dest_id),
        note=f"Moving {amount} from account id: {src_id} to account id {dest_id}"
    )
    return tx_result



if __name__ == '__main__':
    app.run(port=5000)
