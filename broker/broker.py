# -*- coding: utf-8 -*-

"""
    Basic access and management for pyhomebroker APIs
"""

__all__ = ['auth', 'homebroker']
__version__ = '0.0.1'
__author__ = 'fgr-17'

from ast import arg
from pyhomebroker import HomeBroker

import datetime
import pandas as pd
import requests


class HbAuth:
    """
        pyhomebroker auth data
    """

    auth_file = "./bin/Authfile"

    def __init__(self, *args):
        if self.read_file() is not None:
            self.input_account_data()

    def input_account_data(self):
        print("___ Ingreso cuenta ___")
        self.dni = input("DNI:")
        self.usr = input("User:")
        self.pwd = input("Pass:")
        self.acc = input("Cuenta comitente:")
        self.save_file()

    def print(self):
        print("DNI:{}".format(self.dni))
        print("usuario:{}".format(self.usr))
        print("password:{}".format(self.pwd))
        print("cuenta:{}".format(self.acc))

    def save_file(self):
        fd = open(self.auth_file, "w")
        if(fd != FileNotFoundError):
            fd.write("{},{},{},{}".format(self.dni, self.usr,
                                          self.pwd, self.acc))
            fd.close()

    def read_file(self):
        try:
            fd = open(self.auth_file, "r")
            if(fd != FileNotFoundError):
                self.dni, self.usr, self.pwd, self.acc = fd.read().split(',')
            else:
                return 1
        except IOError:
            return 2


class HbInterface:
    """
        pyhomebroker interface manager
    """

    def __init__(self):
        self.auth = HbAuth()

    def print_auth_data(self):
        self.auth.print()

    # traer valores de la db
    @staticmethod
    def round_price(price):
        decimals = price % 1
        price_no_decimals = price//1

        if (price > 250) and (decimals != 0.5):
            price = round(price)

        elif (price > 100) and (price <= 250)\
                and (decimals not in [0, .25, .5, .75]):

            if decimals < .25:
                price = price_no_decimals
            elif decimals > .25 and decimals < .5:
                price = price_no_decimals + 0.25
            elif decimals > .5 and decimals < .75:
                price = price_no_decimals + 0.5
            else:
                price = price_no_decimals + 0.75

        return price


class Broker(HbInterface):

    def __init__(self, code):
        super().__init__()
        self.code = code

    def start_session(self):
        self.hb = HomeBroker(self.code)
        self.hb.auth.login(self.auth.dni, self.auth.usr,
                           self.auth.pwd, raise_exception=True)
        self.hb.online.connect()

    def end_session(self):
        self.hb.online.disconnect()

    def get_data_from_ticker(self, ticker, n_days):

        data = self.hb.history.get_daily_history(ticker,
                                                 datetime.date.today()
                                                 - datetime.timedelta
                                                 (days=n_days),
                                                 datetime.date.today()
                                                 )

        data.loc[:, "date"] = pd.to_datetime(data.loc[:, "date"])
        data = data.set_index("date")
        return data

    def get_dataset(self, tickers, n_days):
        df = []
        for t in tickers:
            ticker_data = self.get_data_from_ticker(t, n_days)
            ticker_data = ticker_data.close
            ticker_data.name = t
            df.append(ticker_data)

        return pd.concat(df, 1)

    def get_current_price(self, ticker):
        return self.hb.history.get_intraday_history(
            ticker).tail(1).close.values[0]

    def get_current_portfolio(self):
        payload = {'comitente': str(self.auth.acc),
                   'consolida': '0',
                   'proceso': '22',
                   'fechaDesde': None,
                   'fechaHasta': None,
                   'tipo': None,
                   'especie': None,
                   'comitenteMana': None}

        portfolio = requests.post("https://cocoscap.com/Consultas/GetConsulta",
                                  cookies=self.hb.auth.cookies,
                                  json=payload).json()

        # portfolio = portfolio["Result"]["Activos"][1]["Subtotal"]

        # ## esto devuelve el ticker, el precio y la cantidad que tenes
        # portfolio = [( x["NERE"], float(x["PCIO"]),
        # float(x["CANT"]) ) for x in portfolio]
        return portfolio

    def get_changes(old_portfolio, new_portfolio):
        changes = {}
        old_portfolio = dict([
                    (x[0], [x[1], x[2]]) for x in old_portfolio
        ])

        for row in new_portfolio:
            ticker = row[0]
            price = row[1]
            quantity = row[2]

            if ticker in old_portfolio:
                changes[ticker] = [price, quantity - old_portfolio[ticker][1]]
            else:
                changes[ticker] = [price, quantity]
        return changes

    def changes2orders(changes, plazo):
        orders = []
        for ticker, price_quantity in changes.items():
            price, quantity = price_quantity
            if quantity < 0:
                order = ("V", ticker, plazo, price, quantity)
                orders.append(order)
        return orders

    def get_orders(self, old_portfolio, new_portfolio, plazo):
        changes = self.get_changes(old_portfolio, new_portfolio)
        orders = self.changes2orders(changes, plazo)
        return orders

    def execute_orders(self, orders):
        for order in orders:
            if order[0] == "V":
                order_number = self.hb.orders.\
                               send_sell_order(order[1], order[2],
                                               order[3], int(abs(order[4])))
            elif order[0] == "C":
                order_number = self.hb.orders.\
                               send_buy_order(order[1], order[2],
                                              order[3], int(abs(order[4])))

    def sell_order(self, symbol, settlement, price, size):
        o_no = self.hb.orders.send_sell_order(symbol, settlement, price, size)

    def buy_order(self, symbol, settlement, price, size):
        o_no = self.hb.orders.send_buy_order(symbol, settlement, price, size)
