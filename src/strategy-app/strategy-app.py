import broker
from strategy.one_over_n import OneOverN

COCOSAPP_BROKER_ID = 265
cocos_brk = broker.Broker(COCOSAPP_BROKER_ID, 1)

if __name__ == '__main__':

    if cocos_brk.start_session() is True:
        print('Session started')
    else:
        exit(1)
    
    s1 = OneOverN(cocos_brk, ['ALUA'], 10000)
    r = s1.propose_portfolio()

    print(s1.portfolio)

    if cocos_brk.end_session() is True:
        print('Session finished')
    else:
        exit(1)

    exit(0)