""" Menu for CLI app """

import logging
import json
from tickers import Tickers


class Menu():
    """ Basic menu mgmt """

    def __init__(self, brok):
        ''' main menu'''
        self.__brk = brok

    menu_options = {
        1: 'Start session',
        2: 'End Session',
        3: 'Get data from asset',
        4: 'Get current portfolio',
        5: 'Get account subtotal',
        6: 'Buy order',
        7: 'Sell order',
        8: 'Exit',
    }

    def print(self):
        ''' print menu options '''

        print("\n============================")
        for key, label in self.menu_options.items():
            print(key, '--', label)

    def option1(self):
        ''' start broker session '''
        if self.__brk.start_session() is True:
            logging.info('Cocos session started')

    def option2(self):
        ''' end broker session '''
        if self.__brk.end_session() is True:
            logging.info('Cocos session ended')

    def option3(self):
        ''' select a asset and print info '''
        Tickers.print()

        asset_no = input('Select a asset number:')
        asset_str = Tickers.get_str(asset_no)

        days = int(input('Days to search back: '))

        print(f'\n===== Ticker info from {days} days =====')
        # print(self.__brk.asset_get_data(asset_str, days))

        # print('\n===== Ticker current price =====')
        # current_price = self.__brk.asset_get_current_price(asset_str)
        # print(type(current_price))
        print(self.__brk.get_price(asset_str, days))

        print('\n===== Ticker current position =====')
        current_pos = self.__brk.asset_get_current_position(asset_str)
        if current_pos is not None:
            print(current_pos)
            logging.info('Getting info from %s, %i days ago', asset_str, days)
        else:
            logging.info('Ticker position not found')

    def option4(self):
        ''' print all portfolio '''
        portf = self.__brk.portfolio_get()
        data = self.__brk.portfolio_get_current_positions(portf)
        json_data = json.dumps(data, indent=2)
        print(json_data)
        logging.info('Getting complete portfolio')

    def option5(self):
        ''' get current account subtotal '''
        portf = self.__brk.portfolio_get()
        data = self.__brk.portfolio_get_curr_account_subtotal(portf)
        json_data = json.dumps(data, indent=2)
        print(json_data)
        logging.info('Getting account subtotal')

    def option6(self):
        ''' buy order '''
        Tickers.print()

        asset_no = input('Select a asset number:')
        asset_str = Tickers.get_str(asset_no)

        print('\n===== Ticker current price =====')
        print(self.__brk.asset_get_current_price(asset_str))

        price = input("Enter buying price:")
        quant = input("Enter quantity:")
        print(self.__brk.order_buy(asset_str, "48hs", float(price), int(float(quant))))
        logging.info("attempted to buy {ticket_str} price: {price} size: {quant}")

    def option7(self):
        ''' sell order '''
        Tickers.print()

        asset_no = input('Select a asset number:')
        asset_str = Tickers.get_str(asset_no)

        print('\n===== Ticker current price =====')
        print(self.__brk.asset_get_current_price(asset_str))

        print('\n===== Ticker current position =====')
        current_pos = self.__brk.asset_get_current_position(asset_str)

        if current_pos is not None:
            print(current_pos)

            price = input("Enter selling price:")
            quant = input("Enter quantity:")
            print(self.__brk.order_sell(asset_str, "48hs", float(price), int(float(quant))))
            logging.info("attempted to sell {ticket_str} price: {price} size: {quant}")
        else:
            print('Ticker position not found')

    def loop(self):
        """ Main app loop """
        while True:
            self.print()
            option = ''
            try:
                option = int(input('Enter your choice: '))
            except ValueError:
                print('Wrong input. Please enter a number ...')

            if option == 1:
                self.option1()
            elif option == 2:
                self.option2()
            elif option == 3:
                self.option3()
            elif option == 4:
                self.option4()
            elif option == 5:
                self.option5()
            elif option == 6:
                self.option6()
            elif option == 7:
                self.option7()
            elif option == 8:
                print('Exiting...')
                return 0
            else:
                print('Invalid option. Please enter a number between 1 and 4.')
