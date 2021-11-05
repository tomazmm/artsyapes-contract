import json
import pprint
import random

from terra_sdk.core import AccAddress, Coins
from terra_sdk.core.auth import StdFee
from terra_sdk.core.broadcast import BlockTxBroadcastResult

from scripts.deploy import owner, lt
from terra_sdk.core.wasm import MsgExecuteContract


def mint(contract_address: str):
    mint_msg = MsgExecuteContract(
        owner.key.acc_address,
        AccAddress(contract_address),
        {
            "mint": {
                "token_id": str(random.randint(1, 1000000)),
                "owner": owner.key.acc_address,
                "token_uri": "www.ipfs_link"
            }
        }
    )
    mint_tx = owner.create_and_sign_tx(msgs=[mint_msg], fee=StdFee(1000000, Coins(uluna=1000000)))
    mint_tx_result = lt.tx.broadcast(mint_tx)
    # print_tx_result(mint_tx_result)


def print_tx_result(tx_result: BlockTxBroadcastResult):
    print(f"Height: {tx_result.height}")
    print(f"TxHash: {tx_result.txhash}")
    for event in tx_result.logs[0].events:
        print(f"{event['type']} : {pprint.pformat(event['attributes'])}")


def main():
    try:
        with open("contract.json", "r") as f:
            data = json.load(f)
        mint(data['contract_address'])
    except FileNotFoundError:
        print("Contract.json file not found.\nDeploy contract before minting NFTs.")


if __name__ == '__main__':
    main()
