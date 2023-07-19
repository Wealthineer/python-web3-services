import web3_provider
from eth_account.messages import encode_defunct

def verifyWalletOwnership(original_message, signed_message_signature, public_wallet_address):
    w3, account= web3_provider.get_web3_provider_and_signer()
    signer_address = w3.eth.account.recover_message(encode_defunct(text=original_message), signature=signed_message_signature)
    return public_wallet_address == signer_address