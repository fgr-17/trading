#!/opt/venv/bin/python
"""Main routine"""
import sys
import logging
from datetime import datetime

from menu import Menu
import broker as brk
from tickers import Tickers

COCOSAPP_BROKER_ID = 265
cocos_brk = brk.Broker(COCOSAPP_BROKER_ID)

if __name__ == '__main__':

    logfile = f'../bin/log{datetime.now().strftime("%d%m%Y")}'
    logging.basicConfig(filename=logfile, level=logging.DEBUG, format="%(asctime)s %(message)s")

    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    logging.info('==============================================')
    logging.info('BOT-JR: Program started at %s', datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    menu = Menu(cocos_brk)
    menu.loop()

# # print(cocos_brk.get_data_from_ticker("ALUA", 3))
# print(cocos_brk.get_dataset(tickers, 5))

# print(f'current price ALUA: {cocos_brk.get_current_price(tickers[0])}')

# print(cocos_brk.get_current_portfolio())

# print(f'order {cocos_brk.buy_order("ALUA", "48hs", 98.9, 1)}')

    # if cocos_brk.end_session() is True:
    #     logging.info('Cocos session finished')
