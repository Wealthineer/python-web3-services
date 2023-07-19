from flask import Flask, jsonify, request
import web3_provider as w3p
import mint
import binascii
import verifier


app = Flask(__name__)

#curl -X POST -H "Content-Type: application/json" -d '{"mintingId":1, "mintingTargetAddress":"0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"}' http://127.0.0.1:5000/api/mint-nft
@app.route('/api/mint-nft', methods=['POST'])
def mint_single_nft():
    data = request.get_json()  # Get the JSON data from the request

    minting_id = data['mintingId']
    minting_target_address = data ['mintingTargetAddress']

    mint.mint_erc1155_for_single_address(minting_target_address, minting_id)

    # Process the data...
    result = {'status': 'sent', 'data': data}
    return jsonify(result)


#curl -X POST -H "Content-Type: application/json" -d '{"originalMessage":"test message","signedMessageSignature":"6fddb00fa204fb8bae80048c2ee7de658a61054b377817faf4d369f9b665a42d664238bc369a24dce929daa6a292d6cb887271d800867773e7445f575fece7501b", "publicWalletAddress":"0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"}' http://127.0.0.1:5000/api/verify-wallet-ownership
@app.route('/api/verify-wallet-ownership', methods=['POST'])
def verify_wallet_ownership():
    data = request.get_json()  # Get the JSON data from the request

    original_message = data['originalMessage']
    print(original_message)
    signed_message_signature = binascii.unhexlify(data ['signedMessageSignature'])
    print(signed_message_signature)
    public_wallet_address = data['publicWalletAddress']
    print(public_wallet_address)

    isWalletOwner = verifier.verifyWalletOwnership(original_message, signed_message_signature, public_wallet_address)

    # Process the data...
    result = {'isWalletOwner': isWalletOwner}
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)