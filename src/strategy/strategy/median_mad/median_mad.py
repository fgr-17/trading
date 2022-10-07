""" Basic strategy of dividing capital equally over N assets"""

import broker
import pandas as pd

class MedianMad:
    """ median/mad sort strategy class """

    def __init__(self, proxy: broker.Broker, assets, capital: float, delta: int):
        """ Initialize with proxy (exchange or broker), list of assets and total capital"""
        self.proxy = proxy
        self.assets = assets
        self.cap = capital
        self.delta = delta
        self.__pfolio = pd.DataFrame(columns=["Asset", "Size", "Price"])

    def propose_portfolio(self):
        """ The strategy proposes a portfolio """
        money_per_asset = self.cap/len(self.assets)
        
        # creates empty dataframe
        prices_df = pd.DataFrame()
        
        for asset in self.assets:

            h_data = []
            for i in range(self.delta):
                price_i = self.proxy.get_price(asset, i).get_close()
                h_data.append(price_i)
            prices_df[asset] = h_data

        prices_pct = prices_df.pct_change().dropna()
        prices_med_mad = prices_pct.median() / prices_pct.mad()
        prices_med_mad = prices_med_mad.sort_values(ascending=False)

        # rounded_price = broker.Broker.round_price(current_price.get_low())
        # n_assets = money_per_asset//rounded_price
        # row = pd.Series({"Asset": asset, "Size": n_assets, "Price": rounded_price})
        # self.__pfolio = pd.concat([self.__pfolio, row.to_frame().T], ignore_index=True)

        return 0

    def get_portfolio(self):
        """ returns previously built portfolio """
        return self.__pfolio
