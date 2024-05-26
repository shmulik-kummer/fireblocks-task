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
    """
       Retrieve the balance of a specific asset in a Fireblocks vault account.

       Args:
           vault_account_id (int): The ID of the vault account.
           asset_id (str): The ID of the asset.

       Returns:
           float: The balance of the asset in the vault account.
           None: If there is an error retrieving the balance.
       """

    try:
        asset_info = fireblocks.get_vault_account_asset(vault_account_id, asset_id)
        balance = asset_info.get("balance")
        if balance is not None:
            formatted_balance = f"{float(balance):.6f}"
            logger.info(f"Current Balance for account id {vault_account_id} is {formatted_balance} {asset_id}")
            return float(formatted_balance)
        else:
            logger.warning(f"No balance information found for asset ID {asset_id} in vault account {vault_account_id}.")
            return None
    except Exception as e:
        logger.error(f"An error occurred while retrieving the balance: {e}")
        return None


def create_transaction(asset_id, amount, src_id, dest_id):
    """
        Create a transaction to transfer an asset from one vault account to another.

        Args:
            asset_id (str): The ID of the asset to transfer.
            amount (float): The amount of the asset to transfer.
            src_id (int): The source vault account ID.
            dest_id (int): The destination vault account ID.

        Returns:
            dict: The transaction result from Fireblocks.
            None: If there is an error creating the transaction.
        """
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
    """
        Check if a transaction is completed and confirmed.

        Args:
            data (dict): The webhook data from Fireblocks.

        Returns:
            bool: True if the transaction is completed and confirmed, False otherwise.
        """
    return data.get("data", {}).get("status") == "COMPLETED" and data.get("data", {}).get("subStatus") == "CONFIRMED"


# utils.py
def handle_low_balance(wallet_id, balance, threshold):
    """
        Handle low balance in an expense wallet by transferring funds from the treasury account.

        Args:
            wallet_id (int): The ID of the expense wallet.
            balance (float): The current balance of the expense wallet.
            threshold (float): The minimum threshold balance for the expense wallet.

        Returns:
            bool: True if the top-up transaction was created successfully, False otherwise.
        """
    amount_to_transfer = float(threshold - balance)

    # Check treasury balance to verify top-up transaction is possible
    treasury_balance = get_wallet_balance(config.TREASURY_ACCOUNT_ID, config.ASSET_ID)
    if treasury_balance is None or treasury_balance < amount_to_transfer:
        logger.error("Not enough funds in treasury account to perform top-up")
        return False

    # Initiate top-up transaction
    logger.info(
        f"Expense account {wallet_id} reached the minimum threshold. Going to top up account with"
        f" {amount_to_transfer:.6f} MATIC")
    transaction = create_transaction(asset_id=config.ASSET_ID, amount=amount_to_transfer,
                                     src_id=config.TREASURY_ACCOUNT_ID,
                                     dest_id=wallet_id)
    if transaction:
        logger.info("Transaction was created successfully. Waiting for it to be confirmed")

        # Send email notification
        subject = "Top-Up Transaction Created"
        body = (f"A top-up transaction has been created to transfer {amount_to_transfer} MATIC from the treasury "
                f"account to the expense account {wallet_id}.")
        send_email_notification(subject, body, config.EMAIL)

        return True

    else:
        logger.error("Failed to create transaction")
        return False


def send_email_notification(subject, body, to_email):
    """
        Send an email notification to a Gmail account

        Args:
            subject (str): The subject of the email.
            body (str): The body of the email.
            to_email (str): The recipient's email address.

        Returns:
            None
        """
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
