# -*- coding: utf-8 -*-

""" Basic access and management for pyhomebroker APIs """

import datetime

from pyhomebroker.common.exceptions import SessionException
import pyhomebroker as phb
import requests

from .auth import Auth

class HbInterface:
    """ pyhomebroker interface manager """

    def __init__(self):
        """ Create the basic authentication """
        self.auth = auth.Auth.from_file("../bin/Authfile")
        if self.auth is None:
            self.auth = auth.Auth.from_stdin()

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

    def __init__(self, code):
        """ Basic constructor """
        super().__init__()
        self.code = code
        self.broker = None

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
                                  json=payload).json()
        return portfolio

    def portfolio_get_current_positions(self, portfolio):
        ''' list all tickers '''
        portfolio = portfolio["Result"]["Activos"][1]["Subtotal"]
        keys_to_retrieve = ['NERE', 'PCIO', 'CANT']
        portfolio = [{x: ticker[x] for x in keys_to_retrieve} for ticker in portfolio]
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

    def ticker_get_data(self, ticker, n_days):
        """ retrieve data from the ticker """
        data = self.broker.history.get_daily_history(ticker,
                                                     datetime.date.today() - datetime.timedelta(days=n_days),
                                                     datetime.date.today())
        # data.loc[:, "date"] = pd.to_datetime(data.loc[:, "date"])
        # data = data.set_index("date")
        return data

    def ticker_get_current_price(self, ticker):
        """ get current price of specific ticker [ONLINE]"""
        # return self.broker.history.get_intraday_history(
        #     ticker).tail(1).close.values[0]
        return self.broker.history.get_intraday_history(ticker)

    def ticker_get_current_position(self, ticker):
        ''' get current position of a ticker '''
        portfolio = self.portfolio_get()
        positions_array = portfolio["Result"]["Activos"][1]["Subtotal"]

        ticker_complete = next((item for item in positions_array if item["NERE"] == ticker), None)

        if ticker_complete is not None:
            keys_to_retrieve = ['NERE', 'PCIO', 'CANT']
            ticker_ret = {x: ticker_complete[x] for x in keys_to_retrieve}
            return ticker_ret

        return None

    # move one layer up
    # def get_dataset(self, tickers, n_days):
    #     """ get the entire dataset """
    #     df_ = []
    #     for ticker in tickers:
    #         ticker_data = self.ticker_get_data(ticker, n_days)
    #         ticker_data = ticker_data.close
    #         ticker_data.name = ticker
    #         df_.append(ticker_data)

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
    #         ticker = row[0]
    #         price = row[1]
    #         quantity = row[2]

    #         if ticker in old_portfolio:
    #             changes[ticker] = [price, quantity - old_portfolio[ticker][1]]
    #         else:
    #             changes[ticker] = [price, quantity]
    #     return changes

    @staticmethod
    def changes2orders(changes, settlement):
        """ Create orders from change list """
        orders = []
        for ticker, price_quantity in changes.items():
            price, quantity = price_quantity
            if quantity < 0:
                order = ("V", ticker, settlement, price, quantity)
                orders.append(order)
        return orders

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
