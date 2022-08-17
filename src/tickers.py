


class Tickers:

    @classmethod
    def print(cls):
        for index, ticker in enumerate(cls.tickers):
            print(f'{index}, {ticker}')

    @classmethod
    def get(cls, index):
        return cls.tickers(index)

    tickers = [
    "ALUA", "BBAR", "BMA", "BYMA", "CEPU", "COME", "CRES", "CVH", "EDN",
    "GGAL", "HARG", "LOMA", "MIRG", "PAMP", "SUPV", "TECO2", "TGNO4", "TGSU2",
    "TRAN", "TXAR", "VALO", "YPFD"
    ]