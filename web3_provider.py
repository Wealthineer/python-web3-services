from eth_account import Account
from web3.middleware import construct_sign_and_send_raw_middleware
from web3 import Web3
from dotenv import load_dotenv
import os


def get_web3_provider_and_signer():
    load_dotenv()
    rpc_url = os.getenv('RPC_URL')
    private_key = os.getenv('PRIVATE_KEY')
    w3 = Web3(Web3.HTTPProvider(rpc_url))

    assert rpc_url is not None, "You must set RPC_URL environment variable"
    assert private_key is not None, "You must set PRIVATE_KEY environment variable"
    assert private_key.startswith('0x'), "Private key must start with 0x hex prefix"

    account = Account.from_key(private_key)

    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))
    return w3, account
