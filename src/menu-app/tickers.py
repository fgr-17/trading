


class Tickers:

    @classmethod
    def print(cls):
        for index, asset in enumerate(cls._tickers):
            print(f'{index}: {asset}')

    @classmethod
    def get_str(cls, index):
        return cls._tickers[int(index)]

    _tickers = [
    "ALUA", "BBAR", "BMA", "BYMA", "CEPU", "COME", "CRES", "CVH", "EDN",
    "GGAL", "HARG", "LOMA", "MIRG", "PAMP", "SUPV", "TECO2", "TGNO4", "TGSU2",
    "TRAN", "TXAR", "VALO", "YPFD"
    ]