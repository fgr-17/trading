# -*- coding: utf-8 -*-

""" Basic access and management for pyhomebroker APIs """

import datetime
import requests

from pyhomebroker.common.exceptions import SessionException
import pyhomebroker as phb

from .auth import Auth


class Candle:
    """ Candle object mgmt """

    def __init__(self, openv: float, close: float, high: float, low: float, vol: float):
        """ Init candle object """
        self.__open = openv
        self.__close = close
        self.__high = high
        self.__low = low
        self.__vol = vol

    def get_low(self) -> float:
        """ Return low value """
        return self.__low

    def get_high(self) -> float:
        """ Return high value """
        return self.__high

    def get_open(self) -> float:
        """ Return open value """
        return self.__open

    def get_close(self) -> float:
        """ Return close value """
        return self.__close

    def get_vol(self) -> float:
        """ Return volume """
        return self.__vol

    def get_ave(self):
        """ Return average """
        return (self.__open + self.__close)/2


class HbInterface:
    """ pyhomebroker interface manager """

    def __init__(self):
        """ Create the basic authentication """
        self.auth = Auth.from_file("../bin/Authfile")
        if self.auth is None:
            self.auth = Auth.from_stdin()

    def print_auth_data(self):
        """ print all the auth data """
        self.auth.print()

    # candidate for db refactor (check if values are broker dependant or general)
    @staticmethod
    def round_price(price):
        """ static method of rounding price """
        decimals = price % 1
        price_no_decimals = price//1

        if (price > 250) and (decimals != 0.5):
            price = round(price)

        elif (100 < price <= 250)\
                and (decimals not in [0, .25, .5, .75]):

            if decimals < .25:
                price = price_no_decimals
            elif .25 < decimals < .5:
                price = price_no_decimals + 0.25
            elif .5 < decimals < .75:
                price = price_no_decimals + 0.5
            else:
                price = price_no_decimals + 0.75

        return price


class Broker(HbInterface):
    """ general broker class """

    def __init__(self, code, delta):
        """ Basic constructor """
        super().__init__()
        self.code = code
        self.broker = None
        self.delta = delta   # check if integer

    def start_session(self):
        """ Init broker session """
        self.broker = phb.HomeBroker(self.code)

        try:
            self.broker.auth.login(self.auth.get_id_num(), self.auth.get_usr(), self.auth.get_pwd(), raise_exception=True)
        except SessionException as session_exp:
            print(session_exp)
            return False
        except requests.exceptions.HTTPError as http_exp:
            print(http_exp)
            return False

        try:
            self.broker.online.connect()
        except SessionException as session_exp:
            print(session_exp)
            return False
        return True

    def end_session(self):
        """ close connection """
        try:
            return self.broker.online.disconnect()
        except SessionException as session_exp:
            print(session_exp)
            return False

        return True

    def portfolio_get(self):
        """ retrieve the whole portfolio """
        payload = {'comitente': str(self.auth.get_acc()),
                   'consolida': '0',
                   'proceso': '22',
                   'fechaDesde': None,
                   'fechaHasta': None,
                   'tipo': None,
                   'especie': None,
                   'comitenteMana': None}

        portfolio = requests.post("https://cocoscap.com/Consultas/GetConsulta",
                                  cookies=self.broker.auth.cookies,
                                  json=payload, timeout=10).json()
        return portfolio

    def portfolio_get_current_positions(self, portfolio):
        ''' list all assets '''
        portfolio = portfolio["Result"]["Activos"][1]["Subtotal"]
        keys_to_retrieve = ['NERE', 'PCIO', 'CANT']
        portfolio = [{x: asset[x] for x in keys_to_retrieve} for asset in portfolio]
        return portfolio

    def portfolio_set_new_positions(self, portfolio):
        ''' todo: orders in batch mode - CISC not wanted '''
        print("Current portfolio ...")
        print(portfolio)

    def portfolio_get_curr_account_subtotal(self, portfolio):
        ''' get current cash '''
        portfolio = portfolio["Result"]["Activos"][0]["Subtotal"]
        subtotal = portfolio[0]["IMPO"]
        return subtotal

    def asset_get_data(self, asset, delta):
        """ retrieve data from the asset """
        data = self.broker.history.get_daily_history(asset,
                                                     datetime.date.today() - datetime.timedelta(days=delta),
                                                     datetime.date.today())
        # data.loc[:, "date"] = pd.to_datetime(data.loc[:, "date"])
        # data = data.set_index("date")
        return data

    def asset_get_current_price(self, asset):
        """ get current price of specific asset [ONLINE]"""
        # return self.broker.history.get_intraday_history(
        #     asset).tail(1).close.values[0]
        ret = self.broker.history.get_intraday_history(asset)
        if len(ret) != 0:
            candle = Candle(ret.iloc[-1]('open'), ret.iloc[-1]('close'), ret.iloc[-1]('high'), ret.iloc[-1]('low'), ret.iloc[-1]('volume'))
            return candle

        return None

    def __price_fn_zero(self, asset):
        """ function to return price with no delta """
        if self.delta == 0:
            return self.asset_get_current_price(asset)

        return Broker.dict2candle(self.asset_get_data(asset, self.delta).iloc[0])

    def __price_fn_delta(self, asset, delta):
        """ function to return asset price with time delta """
        real_delta = delta + self.delta
        if real_delta <= 0:
            return None

        return Broker.dict2candle(self.asset_get_data(asset, real_delta).iloc[0])

    def get_price(self, asset, delta):
        """ general price function """
        if delta == 0:
            return self.__price_fn_zero(asset)
        if delta > 0:
            return self.__price_fn_delta(asset, int(delta))

        raise ValueError

    def asset_get_current_position(self, asset):
        ''' get current position of a asset '''
        portfolio = self.portfolio_get()
        positions_array = portfolio["Result"]["Activos"][1]["Subtotal"]

        asset_complete = next((item for item in positions_array if item["NERE"] == asset), None)

        if asset_complete is not None:
            keys_to_retrieve = ['NERE', 'PCIO', 'CANT']
            asset_ret = {x: asset_complete[x] for x in keys_to_retrieve}
            return asset_ret

        return None

    # move one layer up
    # def get_dataset(self, assets, n_days):
    #     """ get the entire dataset """
    #     df_ = []
    #     for asset in assets:
    #         asset_data = self.asset_get_data(asset, n_days)
    #         asset_data = asset_data.close
    #         asset_data.name = asset
    #         df_.append(asset_data)

    #     return pd.concat(df_, 1)

    # @staticmethod
    # def get_changes(old_portfolio, new_portfolio):
    #     """
    #     detect changes between 2 portfolios
    #     """
    #     changes = {}
    #     old_portfolio = dict([
    #                 (x[0], [x[1], x[2]]) for x in old_portfolio
    #     ])

    #     for row in new_portfolio:
    #         asset = row[0]
    #         price = row[1]
    #         quantity = row[2]

    #         if asset in old_portfolio:
    #             changes[asset] = [price, quantity - old_portfolio[asset][1]]
    #         else:
    #             changes[asset] = [price, quantity]
    #     return changes

    @staticmethod
    def changes2orders(changes, settlement):
        """ Create orders from change list """
        orders = []
        for asset, price_quantity in changes.items():
            price, quantity = price_quantity
            if quantity < 0:
                order = ("V", asset, settlement, price, quantity)
                orders.append(order)
        return orders

    @staticmethod
    def dict2candle(dict_info) -> Candle:
        """ Creates a candle obj from a dict """
        return Candle(dict_info['open'], dict_info['close'], dict_info['high'], dict_info['close'], dict_info['volume'])


    # def get_orders(self, old_portfolio, new_portfolio, settlement):
    #     """
    #     get the orders needed to buy
    #     """
    #     changes = self.get_changes(old_portfolio, new_portfolio)
    #     orders = self.changes2orders(changes, settlement)
    #     return orders

    def execute_orders(self, orders):
        """ run all the orders """
        for order in orders:
            if order[0] == "V":
                order_number = self.broker.orders.\
                               send_sell_order(order[1], order[2],
                                               order[3], int(abs(order[4])))
            elif order[0] == "C":
                order_number = self.broker.orders.\
                               send_buy_order(order[1], order[2],
                                              order[3], int(abs(order[4])))
        return order_number

    def order_sell(self, symbol, settlement, price, size):
        """ Sell an specific order wrapper """
        o_no = self.broker.orders.send_sell_order(symbol, settlement, price, size)
        return o_no

    def order_buy(self, symbol, settlement, price, size):
        """ Buy an specific order wrapper """
        o_no = self.broker.orders.send_buy_order(symbol, settlement, price, size)
        return o_no
