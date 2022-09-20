""" Basic strategy of dividing capital equally over N assets"""

import broker
import pandas as pd

class MedianMad:
    """ median/mad sort strategy class """

    def __init__(self, proxy: broker.Broker, assets, capital: float, days: int):
        """ Initialize with proxy (exchange or broker), list of assets and total capital"""
        self.proxy = proxy
        self.assets = assets
        self.cap = capital
        self.days = days
        self.__pfolio = pd.DataFrame(columns=["Asset", "Size", "Price"])

    def propose_portfolio(self):
        """ The strategy proposes a portfolio """
        money_per_asset = self.cap/len(self.assets)
        for asset in self.assets:
            # ---> move this decision into the math-helper pkg
            
            h_data = []
            for delta in range(self.days):
                current_price = self.proxy.get_price(asset, delta)
                if current_price is not None:
                    h_data.append(current_price.get_close())    

            df = pd.concat(h_data, 1)

            rounded_price = broker.Broker.round_price(current_price.get_low())
            n_assets = money_per_asset//rounded_price
            row = pd.Series({"Asset": asset, "Size": n_assets, "Price": rounded_price})
            self.__pfolio = pd.concat([self.__pfolio, row.to_frame().T], ignore_index=True)

        return 0

    def get_portfolio(self):
        """ returns previously built portfolio """
        return self.__pfolio
