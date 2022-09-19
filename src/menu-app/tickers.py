""" Cocos tickers list """


class Tickers:
    """ Tickers list for cocos broker """

    @classmethod
    def print(cls):
        """ Print ticker info """
        for index, asset in enumerate(cls._tickers):
            print(f'{index}: {asset}')

    @classmethod
    def get_str(cls, index):
        """ Convert index to ticker str"""
        return cls._tickers[int(index)]

    _tickers = [
        "ALUA", "BBAR", "BMA", "BYMA", "CEPU", "COME", "CRES", "CVH", "EDN",
        "GGAL", "HARG", "LOMA", "MIRG", "PAMP", "SUPV", "TECO2", "TGNO4", "TGSU2",
        "TRAN", "TXAR", "VALO", "YPFD"
    ]
