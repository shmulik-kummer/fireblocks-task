from app import fireblocks
import json
from fireblocks_sdk import TransferPeerPath, DestinationTransferPeerPath, VAULT_ACCOUNT, \
    PagedVaultAccountsRequestFilters



# Get supported assets

supportedAssets = fireblocks.get_supported_assets()
print(supportedAssets)

# # # Get vault accounts
vault_accounts = fireblocks.get_vault_accounts_with_page_info(PagedVaultAccountsRequestFilters())
print(json.dumps(vault_accounts, indent=1))






