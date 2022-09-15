
import broker

class OneOverN :

    def __init__(self, proxy, assets, capital):
        self.proxy = proxy
        self.assets = assets
        self.cap = capital


    def propose_portfolio(self):
        money_per_asset = self.cap/len(self.assets)
        self.portfolio = []
        for asset in self.assets:
            # ---> move this decision into the math-helper pkg
            current_price = self.proxy.get_price(asset, 0)
            if current_price is None:
                return None
            else:
                rounded_price = broker.Broker.round_price(current_price['low'])
                n_assets = money_per_asset//rounded_price
                self.portfolio.append((asset, n_assets, rounded_price))

        return 0
