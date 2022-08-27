import os
import broker as brk
from tickers import Tickers
import logging

import json

class Menu:

    def __init__(self, brk):
        ''' main menu'''
        self.__brk = brk

    menu_options = {
        1: 'Start session',
        2: 'End Session',
        3: 'Get data from ticker',
        4: 'Get current portfolio',
        5: 'Get account subtotal',
        6: 'Buy order',
        7: 'Sell order',
        8: 'Exit',
    }

    def print(self):
        ''' print menu options '''

        print("\n============================")
        for key in self.menu_options.keys():
            print(key, '--', self.menu_options[key] )

    def option1(self):
        ''' start broker session '''
        if self.__brk.start_session() is True:
            logging.info('Cocos session started')

    def option2(self):
        ''' end broker session '''
        if self.__brk.end_session() is True:
            logging.info('Cocos session ended')
    
    def option3(self):
        ''' select a ticker and print info '''
        Tickers.print()

        ticker_no = input('Select a ticker number:')
        ticker_str = Tickers.get_str(ticker_no)

        days = int(input('Days to search back: '))

        print(f'\n===== Ticker info from {days} days =====')
        print(self.__brk.ticker_get_data(ticker_str, days))

        print('\n===== Ticker current price =====')
        print(self.__brk.ticker_get_current_price(ticker_str))

        print('\n===== Ticker current position =====')
        current_pos = self.__brk.ticker_get_current_position(ticker_str)
        if current_pos is not None:
            print(current_pos)
            logging.info(f'Getting info from {ticker_str}, {days} days ago')
        else:
            logging.info('Ticker position not found')

    def option4(self):
        ''' print all portfolio '''
        pf = self.__brk.portfolio_get()
        data = self.__brk.portfolio_get_current_positions(pf)
        json_data = json.dumps(data, indent=2)
        print(json_data)
        logging.info('Getting complete portfolio')

    def option5(self):
        ''' get current account subtotal '''
        pf = self.__brk.portfolio_get()
        data = self.__brk.portfolio_get_curr_account_subtotal(pf)
        json_data = json.dumps(data, indent=2)
        print(json_data)
        logging.info('Getting account subtotal')

    def option6(self):
        ''' buy order '''
        Tickers.print()

        ticker_no = input('Select a ticker number:')
        ticker_str = Tickers.get_str(ticker_no)

        print('\n===== Ticker current price =====')
        print(self.__brk.ticker_get_current_price(ticker_str))

        price = input("Enter buying price:")
        quant = input("Enter quantity:")
        print(self.__brk.order_buy(ticker_str, "48hs", float(price), int(float(quant))))
        logging.info("attempted to buy {ticket_str} price: {price} size: {quant}")

    def option7(self):
        ''' sell order '''
        Tickers.print()

        ticker_no = input('Select a ticker number:')
        ticker_str = Tickers.get_str(ticker_no)

        print('\n===== Ticker current price =====')
        print(self.__brk.ticker_get_current_price(ticker_str))

        print('\n===== Ticker current position =====')
        current_pos = self.__brk.ticker_get_current_position(ticker_str)

        if current_pos is not None:
            print(current_pos)

            price = input("Enter selling price:")
            quant = input("Enter quantity:")
            print(self.__brk.order_sell(ticker_str, "48hs", float(price), int(float(quant))))
            logging.info("attempted to sell {ticket_str} price: {price} size: {quant}")
        else:
            print('Ticker position not found')


    def loop(self):
        while(True):
            self.print()
            option = ''
            try:
                option = int(input('Enter your choice: '))
            except:
                print('Wrong input. Please enter a number ...')
            #Check what choice was entered and act accordingly
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
                os._exit(1)
            else:
                print('Invalid option. Please enter a number between 1 and 4.')