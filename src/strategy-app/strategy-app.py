import broker
import strategy

COCOSAPP_BROKER_ID = 265
cocos_brk = broker.Broker(COCOSAPP_BROKER_ID)

if __name__ == '__main__':

    if cocos_brk.start_session() is True:
        print('Session started')
    else:
        exit(1)
    
    str = OneOverN(cocos_brk, ['ALUA'], 1000)
    print('q onda')
    str.propose_portfolio()

    if cocos_brk.end_session() is True:
        print('Session finished')
    else:
        exit(1)

    exit(0)