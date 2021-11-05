from terra_sdk.client.localterra import LocalTerra


class Config:
    __lt = LocalTerra()

    @staticmethod
    def network():
        return {
            "client": Config.__lt,
            "wallets": Config.__lt.wallets["test1"]
        }



