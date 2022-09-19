""" Basic strategy of dividing capital equally over N assets"""

import broker


class OneOverN:
    """ 1/N strategy class """

    def __init__(self, proxy, assets, capital):
        """ Initialize with proxy (exchange or broker), list of assets and total capital"""
        self.proxy = proxy
        self.assets = assets
        self.cap = capital
        self.__pfolio = []

    def propose_portfolio(self):
        """ The strategy proposes a portfolio """
        money_per_asset = self.cap/len(self.assets)
        for asset in self.assets:
            # ---> move this decision into the math-helper pkg
            current_price = self.proxy.get_price(asset, 0)
            print(current_price)
            if current_price is None:
                return None

            rounded_price = broker.Broker.round_price(current_price.get_low())
            n_assets = money_per_asset//rounded_price
            self.__pfolio.append((asset, n_assets, rounded_price))

        return 0

    def get_portfolio(self):
        """ returns previously built portfolio """
        return self.__pfolio
