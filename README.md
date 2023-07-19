A collection of ideas for python services to interact with Ethereum/EVM chains:

web3_service.py exposes functionality of
    minter.py: Mint NFTs from a contract where the service holds the private key as a minter (e.g. loyalty program that drops free NFTs to customers)
    verifier.py: check the provided message was signed by the wallet that claims to be the signer - useful for verifying wallet ownership when initially connecting a wallet

watcher.py:
    subcribes to events of a smart contract