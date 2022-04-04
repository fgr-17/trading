#!/usr/local/bin/python3

import broker as brk

cocos_brk = brk.Broker(265)
# cocos_brk.print_auth_data()

cocos_brk.start_session()

print(cocos_brk.get_data_from_ticker("ALUA", 3))


cocos_brk.end_session()