
import broker

class OneOverN :

    def __init__(self, brk_interface, tickers):
        self.brk_interface = brk_interface
        self.tck = tickers


    def portfolio_get(self, capital):
        
        ''' Toma una lista de tickers y un monto de dinero. Divide el monto
            en la cantidad de tickers, obtiene el precio actual de la accion,
            la redondea segun las reglas de round_price y calcula cuantas puede
            comprar. 
            Devuelve una lista de tuplas, donde cada tupla tiene ticker, precio 
            y cantidad a comprar.'''
        
        money_per_asset = capital/len(self.tck)
        portfolio = []
        for t in self.tck:
            print(self.brk_interface.ticker_get_data(t, 1))
            # current_price = self.brk_interface.ticker_get_data(t)
            # rounded_price = broker.round_price(current_price)
            # n_assets = money_per_asset//rounded_price
            # portfolio.append((t, current_price, n_assets, rounded_price))

        return portfolio


COCOSAPP_BROKER_ID = 265
cocos_brk = broker.Broker(COCOSAPP_BROKER_ID)

if __name__ == '__main__':
    str = OneOverN(cocos_brk, 'ALUA')
    str.portfolio_get(1000)