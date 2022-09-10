
import broker

class OneOverN :

    def __init__(self, proxy, assets, capital):
        self.proxy = proxy
        self.assets = assets
        self.cap = capital
        print('fin init')


    def propose_portfolio(self):
        money_per_asset = self.cap/len(self.assets)
        self.portfolio = []
        for asset in self.assets:
            print(self.proxy.asset_get_current_price(asset))
            # current_price = self.brk_interface.ticker_get_data(t)
            # rounded_price = broker.round_price(current_price)
            # n_assets = money_per_asset//rounded_price
            # portfolio.append((t, current_price, n_assets, rounded_price))

        return 0
