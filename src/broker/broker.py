# -*- coding: utf-8 -*-

"""
    Basic access and management for pyhomebroker APIs
"""

__all__ = ['HbAuth', 'HbInterface', 'Broker']
__version__ = '0.0.1'
__author__ = 'fgr-17'

import os
import datetime

from pyhomebroker import HomeBroker

import pandas as pd
import requests


class HbAuth:
    """
        pyhomebroker auth data
    """

    BIN_PATH = "../bin"

    try:
        os.mkdir(BIN_PATH)
    except OSError as error:
        # print(error)
        pass

    auth_file = f'{BIN_PATH}/Authfile'

    def __init__(self):
        if self.read_file() is not None:
            self.input_account_data()

    def input_account_data(self):
        """
        user enters data manually
        """
        print("___ Ingreso cuenta ___")
        self.dni = input("DNI:")
        self.usr = input("User:")
        self.pwd = input("Pass:")
        self.acc = input("Cuenta comitente:")
        self.save_file()

    def print(self):
        """
        show auth info
        """
        print(f'DNI:{self.dni}')
        print(f'usuario:{self.usr}')
        print(f'password:{self.pwd}')
        print(f'cuenta:{self.acc}')

    def save_file(self):
        """
        save file with auth info
        """
        with open(self.auth_file, "w", encoding="utf8") as file_desc:
            file_desc.write(f'{self.dni},{self.usr},{self.pwd},{self.acc}')
            file_desc.close()

    def read_file(self):
        """
        Read auth file
        """
        try:
            with open(self.auth_file, "w", encoding="utf8") as file_desc:
                self.dni, self.usr, self.pwd,\
                    self.acc = file_desc.read().split(',')
                return 0

        except IOError:
            return 2


class HbInterface:
    """
        pyhomebroker interface manager
    """

    def __init__(self):
        """
        Create the basic connection
        """
        self.auth = HbAuth()

    def print_auth_data(self):
        """
        print all the auth data
        """
        self.auth.print()

    # traer valores de la db
    @staticmethod
    def round_price(price):
        """
        static method of rounding price
        """
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
        """
        Basic constructor
        """
        super().__init__()
        self.code = code
        self.broker = None

    def start_session(self):
        """
        Init broker session
        """
        self.broker = HomeBroker(self.code)

        try:
            self.broker.auth.login(self.auth.dni, self.auth.usr, self.auth.pwd, raise_exception=True)
        except:
            print('Auth data failed')

        self.broker.online.connect()

    def end_session(self):
        """
        close connection
        """
        self.broker.online.disconnect()

    def get_data_from_ticker(self, ticker, n_days):
        """
        retrieve data from the ticker
        """
        data = self.broker.history.get_daily_history(ticker,
                                                     datetime.date.today() - datetime.timedelta(days=n_days),
                                                     datetime.date.today())

        data.loc[:, "date"] = pd.to_datetime(data.loc[:, "date"])
        data = data.set_index("date")
        return data

    def get_dataset(self, tickers, n_days):
        """
        get the entire dataset
        """
        df_ = []
        for ticker in tickers:
            ticker_data = self.get_data_from_ticker(ticker, n_days)
            ticker_data = ticker_data.close
            ticker_data.name = ticker
            df_.append(ticker_data)

        return pd.concat(df_, 1)

    def get_current_price(self, ticker):
        """
        get current price of specific
        """
        return self.broker.history.get_intraday_history(
            ticker).tail(1).close.values[0]

    def get_current_portfolio(self):
        """
        retrieve the whole portfolio
        """
        payload = {'comitente': str(self.auth.acc),
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

        # portfolio = portfolio["Result"]["Activos"][1]["Subtotal"]

        # ## esto devuelve el ticker, el precio y la cantidad que tenes
        # portfolio = [( x["NERE"], float(x["PCIO"]),
        # float(x["CANT"]) ) for x in portfolio]
        return portfolio

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
    def changes2orders(changes, plazo):
        """
        Create orders from change list
        """
        orders = []
        for ticker, price_quantity in changes.items():
            price, quantity = price_quantity
            if quantity < 0:
                order = ("V", ticker, plazo, price, quantity)
                orders.append(order)
        return orders

    # def get_orders(self, old_portfolio, new_portfolio, plazo):
    #     """
    #     get the orders needed to buy
    #     """
    #     changes = self.get_changes(old_portfolio, new_portfolio)
    #     orders = self.changes2orders(changes, plazo)
    #     return orders

    def execute_orders(self, orders):
        """
        run all the orders
        """
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

    def sell_order(self, symbol, settlement, price, size):
        """
        Sell an specific order
        """
        o_no = self.broker.orders.send_sell_order(symbol, settlement, price, size)
        return o_no

    def buy_order(self, symbol, settlement, price, size):
        """
        Buy an specific order
        """
        o_no = self.broker.orders.send_buy_order(symbol, settlement, price, size)
        return o_no
