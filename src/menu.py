import broker as brk
from tickers import Tickers
import logging

class Menu:

    def __init__(self, brk):
        self.__brk = brk

    menu_options = {
        1: 'Start session',
        2: 'End Session',
        3: 'Get data from ticker',
        4: 'Exit',
    }

    def print(self):
        for key in self.menu_options.keys():
            print (key, '--', self.menu_options[key] )

    def option1(self):

        if self.__brk.start_session() is True:
            logging.info('Cocos session started')

    def option2(self):
        self.__brk.end_session()
    
    def option3(self):

        Tickers.print()

        ticket_no = input('Select a ticker number:')
        ticket_str = Tickers.get_str(ticket_no)

        days = int(input('Days to search back: '))

        self.__brk.get_data_from_ticker(ticket_str, days)



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
                print('Exiting...')
                exit()
            else:
                print('Invalid option. Please enter a number between 1 and 4.')