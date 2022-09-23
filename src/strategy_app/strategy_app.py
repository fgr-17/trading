#!/opt/venv/bin/python

""" Basic strategy test app """
import sys
import broker
from strategy.one_over_n import OneOverN
from strategy.median_mad import MedianMad

COCOSAPP_BROKER_ID = 265
cocos_brk = broker.Broker(COCOSAPP_BROKER_ID, 2)

if __name__ == '__main__':

    if cocos_brk.start_session() is True:
        print('Session started')
    else:
        sys.exit(1)

    tickers = ['ALUA', 'YPFD', 'TXAR', 'PAMP']

    s1 = OneOverN(cocos_brk, tickers, 10000)
    r1 = s1.propose_portfolio()
    print('Proposed portfolio 1/N:')
    print(s1.get_portfolio())

    s2 = MedianMad(cocos_brk, tickers, 10000, 60)
    r2 = s2.propose_portfolio()
    print('Proposed portfolio Median/Mad:')
    print(s2.get_portfolio())

    if cocos_brk.end_session() is True:
        print('Session finished')
    else:
        sys.exit(1)

    sys.exit(0)
