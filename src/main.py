#!/opt/venv/bin/python
"""Main routine"""
import sys
import logging
from datetime import datetime

import broker as brk
# import menu

COCOSAPP_BROKER_ID = 265
cocos_brk = brk.Broker(COCOSAPP_BROKER_ID)

tickers = [
    "ALUA", "BBAR", "BMA", "BYMA", "CEPU", "COME", "CRES", "CVH", "EDN",
    "GGAL", "HARG", "LOMA", "MIRG", "PAMP", "SUPV", "TECO2", "TGNO4", "TGSU2",
    "TRAN", "TXAR", "VALO", "YPFD"
]


if __name__ == '__main__':

    logfile = f'../bin/log{datetime.now().strftime("%d%m%Y")}'
    logging.basicConfig(filename=logfile, level=logging.DEBUG, format="%(asctime)s %(message)s")

    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    logging.info('==============================================')
    logging.info('BOT-JR: Session started at %s', datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    if cocos_brk.start_session() is True:
        logging.info('Cocos session started')

# # print(cocos_brk.get_data_from_ticker("ALUA", 3))
# print(cocos_brk.get_dataset(tickers, 5))

# print(f'current price ALUA: {cocos_brk.get_current_price(tickers[0])}')

# print(cocos_brk.get_current_portfolio())

# print(f'order {cocos_brk.buy_order("ALUA", "48hs", 98.9, 1)}')

    if cocos_brk.end_session() is True:
        logging.info('Cocos session finished')
