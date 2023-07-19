import web3_provider
from dotenv import load_dotenv
import os
import json
import time

# Connect to the Ethereum node

load_dotenv()

abi_path = os.getenv('WATCHER_ABI_PATH')
contract_address = os.getenv('WATCHER_CONTRACT_ADDRESS')
event_name = os.getenv('WATCHER_EVENT_NAME')

with open(abi_path) as f:
    info_json = json.load(f)
abi = info_json["abi"]

w3,account = web3_provider.get_web3_provider_and_signer()

# Create the contract object
contract = w3.eth.contract(address=contract_address, abi=abi)

# Define the event filter
event_filter = contract.events[event_name].create_filter(fromBlock='latest')

# Start listening for events
while True:
    time.sleep(1)
    events = event_filter.get_new_entries()
    for event in events:
        if(event['event'] == 'Erc1155ForMinterService_Mint'):
            print(f"Event received: {event['event']}(to:{event['args']['to']}, id:{event['args']['id']}, amount:{event['args']['amount']})")
        else:
            print(f"Event received: {event['event']}")