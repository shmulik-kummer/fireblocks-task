# fireblocks_utils.py
from fireblocks_sdk import FireblocksSDK, TransferPeerPath, DestinationTransferPeerPath, VAULT_ACCOUNT
import config

# Initialize Fireblocks SDK
fireblocks = FireblocksSDK(config.API_SECRET, config.API_KEY, config.API_URL)


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
            return None
    except Exception as e:
        print(f"An error occurred while retrieving the balance: {e}")
        return None


def create_transaction(asset_id, amount, src_id, dest_id):
    tx_result = fireblocks.create_transaction(
        asset_id=asset_id,
        amount=amount,
        source=TransferPeerPath(VAULT_ACCOUNT, src_id),
        destination=DestinationTransferPeerPath(VAULT_ACCOUNT, dest_id),
        note=f"Moving {amount} from account id: {src_id} to account id {dest_id}"
    )
    return tx_result
