from flask import Blueprint, jsonify, request
import config
from utils import get_wallet_balance, create_transaction, is_transaction_completed, handle_low_balance
import logging
import json

logger = logging.getLogger(__name__)

routes = Blueprint('routes', __name__)


@routes.route('/', methods=['GET'])
def root():
    """
    Root endpoint for the Fireblocks app.

    Returns:
        str: A welcome message.
    """
    return "Hello from Fireblocks app"


@routes.route('/webhook', methods=['POST'])
def webhook():
    """
        Webhook endpoint to handle transactional events from Fireblocks.

        This function processes webhook events, checks the balance of multiple expense accounts,
        and initiates a top-up transaction if any expanse account balance is below the specified threshold.

        Returns:
            Response: JSON response indicating the result of the webhook processing.
        """

    data = request.json

    # Proceed only if the status is COMPLETED and subStatus is CONFIRMED
    if is_transaction_completed(data):
        logger.info("Confirmed transaction Webhook received: %s", data)
        logger.info("Going to check the balance of the expense accounts")

        responses = []
        for wallet in config.EXPENSE_ACCOUNT_IDS:
            wallet_id = wallet['id']
            threshold = wallet['threshold']
            logger.info(f"Checking balance for expense account ID {wallet_id}")

            # Check the balance of the expense account
            expense_balance = get_wallet_balance(wallet_id, config.ASSET_ID)

            # If balance is below the threshold, create a transaction
            if expense_balance < threshold:
                handle_balance = handle_low_balance(wallet_id, expense_balance, threshold)
                if not handle_balance:
                    responses.append(
                        {"status": "failed", "message": f"Failed to top up wallet ID {wallet_id}"}), 200

            else:
                logger.info(f"Balance is sufficient for wallet ID {wallet_id}")
                responses.append({"status": "success", "message": f"Balance is sufficient for wallet ID {wallet_id}"})

        return jsonify(responses)

    return jsonify({"status": "received", "message": "Waiting for completed transaction webhook"}), 200
