import base64
from terra_sdk.client.localterra import LocalTerra
from terra_sdk.core import Coins
from terra_sdk.core.wasm import MsgStoreCode, MsgInstantiateContract
from terra_sdk.core.auth.data.tx import StdFee

lt = LocalTerra()
owner = lt.wallets["test1"]


def store() -> int:
    contract_file = open("../artifacts/cw721_metadata_onchain.wasm", "rb")
    file_bytes = base64.b64encode(contract_file.read()).decode()
    store_code = MsgStoreCode(owner.key.acc_address, file_bytes)
    store_code_tx = owner.create_and_sign_tx(msgs=[store_code], fee=StdFee(10000000, "1000000uluna"))
    return int(lt.tx.broadcast(store_code_tx).logs[0].events_by_type["store_code"]["code_id"][0])


def instantiate(code_id: int) -> str:
    init = MsgInstantiateContract(
      owner.key.acc_address,
      owner.key.acc_address,
      code_id,
      {
        "name": "ArtsyApes",
        "symbol": "APE",
        "minter": str(owner.key.acc_address)
      },
      Coins({"uluna": 10000000}),
    )
    instantiate_tx = owner.create_and_sign_tx(msgs=[init])
    instantiate_tx_result = lt.tx.broadcast(instantiate_tx)
    return instantiate_tx_result.logs[0].events_by_type['instantiate_contract']['contract_address'][0]


def deploy():
    code_id = store()
    contract_address = instantiate(code_id)
    print(f"Code ID : {code_id}\nContract address: {contract_address}")
    return code_id, contract_address


if __name__ == '__main__':
    deploy()
