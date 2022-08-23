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
        5: 'Exit',
    }

    def print(self):
        ''' print menu options '''
        for key in self.menu_options.keys():
            print (key, '--', self.menu_options[key] )

    def option1(self):
        ''' start broker session '''
        if self.__brk.start_session() is True:
            logging.info('Cocos session started')

    def option2(self):
        ''' end broker session '''
        self.__brk.end_session()
    
    def option3(self):
        ''' select a ticker and print info '''
        Tickers.print()

        ticker_no = input('Select a ticker number:')
        ticker_str = Tickers.get_str(ticker_no)

        days = int(input('Days to search back: '))

        print(self.__brk.ticker_get_data(ticker_str, days))
        print(self.__brk.ticker_get_current_price(ticker_str))
        print(self.__brk.ticker_get_current_position(ticker_str))

    def option4(self):
        ''' print all portfolio '''
        data = self.__brk.get_current_portfolio()
        json_data = json.dumps(data, indent=2)
        print(json_data)


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
                print('Exiting...')
                os._exit(1)
            else:
                print('Invalid option. Please enter a number between 1 and 4.')