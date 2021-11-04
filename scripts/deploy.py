import base64
from terra_sdk.client.localterra import LocalTerra
from terra_sdk.core import Coins
from terra_sdk.core.wasm import MsgStoreCode, MsgInstantiateContract, MsgExecuteContract
from terra_sdk.core.auth.data.tx import StdFee


lt = LocalTerra()
test1 = lt.wallets["test1"]

def store() -> int:
    contract_file = open("../artifacts/cw721_metadata_onchain.wasm", "rb")
    file_bytes = base64.b64encode(contract_file.read()).decode()
    store_code = MsgStoreCode(test1.key.acc_address, file_bytes)
    store_code_tx = test1.create_and_sign_tx(msgs=[store_code], fee=StdFee(10000000, "1000000uluna"))
    return int(lt.tx.broadcast(store_code_tx).logs[0].events_by_type["store_code"]["code_id"][0])


def instantiate(code_id: int):
    instantiate = MsgInstantiateContract(
      test1.key.acc_address,
      test1.key.acc_address,
      code_id,
      {
        "name": "ArtsyApes",
        "symbol": "APE",
        "minter": str(test1.key.acc_address)
      },
      Coins({"uluna": 10000000}),
    )
    instantiate_tx = test1.create_and_sign_tx(msgs=[instantiate])
    instantiate_tx_result = lt.tx.broadcast(instantiate_tx)
    contract_addresss = instantiate_tx_result.logs[0].events_by_type['instantiate_contract']['contract_address'][0]
    print(f"Contract address: {contract_addresss}")


if __name__ == '__main__':
    code_id = store()
    instantiate(code_id)
