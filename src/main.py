#!/opt/venv/bin/python
"""Main routine"""
import broker as brk

cocos_brk = brk.Broker(265)

# todo: pasar a una db
tickers = [
    "ALUA", "BBAR", "BMA", "BYMA", "CEPU", "COME", "CRES", "CVH", "EDN",
    "GGAL", "HARG", "LOMA", "MIRG", "PAMP", "SUPV", "TECO2", "TGNO4", "TGSU2",
    "TRAN", "TXAR", "VALO", "YPFD"
]

cocos_brk.start_session()

# # print(cocos_brk.get_data_from_ticker("ALUA", 3))
# print(cocos_brk.get_dataset(tickers, 5))

# print(f'current price ALUA: {cocos_brk.get_current_price(tickers[0])}')

# print(cocos_brk.get_current_portfolio())

# print(f'order {cocos_brk.buy_order("ALUA", "48hs", 98.9, 1)}')

cocos_brk.end_session()
