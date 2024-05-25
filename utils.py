from fireblocks_sdk import FireblocksSDK, TransferPeerPath, DestinationTransferPeerPath, VAULT_ACCOUNT
import config
import logging
from flask import jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize Fireblocks SDK
fireblocks = FireblocksSDK(config.API_SECRET, config.API_KEY, config.API_URL)

# Set up logging
logger = logging.getLogger(__name__)


def get_wallet_balance(vault_account_id, asset_id):
    try:
        asset_info = fireblocks.get_vault_account_asset(vault_account_id, asset_id)
        balance = asset_info.get("balance")
        if balance is not None:
            formatted_balance = f"{float(balance):.3f}"
            logger.info(f"Current Balance for account id {vault_account_id} is {formatted_balance} {asset_id}")
            return float(formatted_balance)
        else:
            logger.warning(f"No balance information found for asset ID {asset_id} in vault account {vault_account_id}.")
            return None
    except Exception as e:
        logger.error(f"An error occurred while retrieving the balance: {e}")
        return None


def create_transaction(asset_id, amount, src_id, dest_id):
    try:
        tx_result = fireblocks.create_transaction(
            asset_id=asset_id,
            amount=amount,
            source=TransferPeerPath(VAULT_ACCOUNT, src_id),
            destination=DestinationTransferPeerPath(VAULT_ACCOUNT, dest_id),
            note=f"Moving {amount} from account id: {src_id} to account id {dest_id}"
        )
        return tx_result
    except Exception as e:
        logger.error(f"An error occurred while creating the transaction: {e}")
        return None


def is_transaction_completed(data):
    return data.get("data", {}).get("status") == "COMPLETED" and data.get("data", {}).get("subStatus") == "CONFIRMED"


def handle_low_balance(balance):
    amount_to_transfer = round(config.BALANCE_THRESHOLD - balance, 3)

    # Check treasury balance to verify top up transaction is possible
    treasury_balance = get_wallet_balance(config.TREASURY_ACCOUNT_ID, config.ASSET_ID)
    if treasury_balance < amount_to_transfer:
        logger.error("Not enough funds in treasury account to perform top-up")
        return jsonify({"status": "failure", "message": "Not enough funds in treasury account to perform top-up"}), 200

    # Initiate top up transaction
    logger.info(
        f"Expense account reached the minimum threshold. Going to top up account with {amount_to_transfer} MATIC")
    transaction = create_transaction(asset_id=config.ASSET_ID, amount=amount_to_transfer,
                                     src_id=config.TREASURY_ACCOUNT_ID,
                                     dest_id=config.EXPENSE_ACCOUNT_ID)
    if transaction:
        logger.info("Transaction was created successfully. Waiting for it to be confirmed")

        # Send email notification
        subject = "Top-Up Transaction Created"
        body = (f"A top-up transaction has been created to transfer {amount_to_transfer} MATIC from the treasury "
                f"account to the expense account.")
        send_email_notification(subject, body, config.EMAIL)

        return jsonify({"status": "success", "transaction": transaction}), 200
    else:
        logger.error("Failed to create transaction")
        return jsonify({"status": "failure", "message": "Failed to create transaction"}), 200


def check_treasury_balance(amount_to_transfer):
    treasury_balance = get_wallet_balance(config.TREASURY_ACCOUNT_ID, config.ASSET_ID)
    if treasury_balance < amount_to_transfer:
        logger.info("no enough funds in treasury account to perform top up")
        return False


def send_email_notification(subject, body, to_email):
    from_email = config.EMAIL
    from_password = config.EMAIL_APP_PASSWORD

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Connect to Gmail's SMTP server and send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        logger.info(f"Email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
