from web3 import Web3
from eth_account import Account
import json
import web3_provider

from dotenv import load_dotenv
import os

from web3.middleware import construct_sign_and_send_raw_middleware


def mint_erc1155_for_single_address(minting_target_address, minting_id):
    if not isinstance(minting_target_address, str):
        raise TypeError("target_address needs to be a str")

    if not isinstance(minting_id, int):
        raise TypeError("minting_id needs to be int")

    load_dotenv()
    # rpc_url = os.getenv('RPC_URL')
    # private_key = os.getenv('PRIVATE_KEY')
    w3, account = web3_provider.get_web3_provider_and_signer()
    # w3 = Web3(Web3.HTTPProvider(rpc_url))
    # account = Account.from_key(private_key)

    # assert rpc_url is not None, "You must set RPC_URL environment variable"
    # assert private_key is not None, "You must set PRIVATE_KEY environment variable"
    # assert private_key.startswith('0x'), "Private key must start with 0x hex prefix"

    abi_path = os.getenv('ERC1155_ABI_PATH')
    contract_address = os.getenv('ERC1155_CONTRACT_ADDRESS')

    with open(abi_path) as f:
        info_json = json.load(f)
    abi = info_json["abi"]

    base_erc1155_contract = w3.eth.contract(address=contract_address, abi=abi)

    # %%
    minting_target = Web3.to_checksum_address(minting_target_address)

    transaction = base_erc1155_contract.functions.mint(minting_target, minting_id, 1).build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address)
    })
    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=account.key)
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    w3.eth.wait_for_transaction_receipt(transaction_hash)

    print("NFT minted")

def mint_erc20_for_single_address(minting_target_address, amount, w3):


    if not isinstance(minting_target_address, str):
        raise TypeError("target_address needs to be a str")

    if not isinstance(amount, int):
        raise TypeError("amount needs to be int")

    if not isinstance(w3, Web3):
        raise TypeError("w3 must be Web3")

    load_dotenv()

    abi_path = os.getenv('ERC20_ABI_PATH')
    contract_address = os.getenv('ERC20_CONTRACT_ADDRESS')

    with open(abi_path) as f:
        info_json = json.load(f)
    abi = info_json["abi"]

    erc20_contract = w3.eth.contract(address=contract_address, abi=abi)
    minting_target = Web3.toChecksumAddress(minting_target_address)
    erc20_contract.functions.mint(minting_target, amount).transact()
