#!/opt/venv/bin/python
"""Main routine"""
import broker as brk
import menu

COCOSAPP_BROKER_ID = 265
cocos_brk = brk.Broker(COCOSAPP_BROKER_ID)

# todo: pasar a una db
tickers = [
    "ALUA", "BBAR", "BMA", "BYMA", "CEPU", "COME", "CRES", "CVH", "EDN",
    "GGAL", "HARG", "LOMA", "MIRG", "PAMP", "SUPV", "TECO2", "TGNO4", "TGSU2",
    "TRAN", "TXAR", "VALO", "YPFD"
]


if __name__ == '__main__':

    cocos_brk.start_session()


# # print(cocos_brk.get_data_from_ticker("ALUA", 3))
# print(cocos_brk.get_dataset(tickers, 5))

# print(f'current price ALUA: {cocos_brk.get_current_price(tickers[0])}')

# print(cocos_brk.get_current_portfolio())

# print(f'order {cocos_brk.buy_order("ALUA", "48hs", 98.9, 1)}')

    cocos_brk.end_session()
