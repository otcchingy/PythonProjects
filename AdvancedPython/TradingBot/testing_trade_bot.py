# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 09:17:53 2020

@author: AKOS
"""
import json
from trading_bot import TradeBot


class DizoTradeBot(TradeBot):
    
    def __init__(self):
        TRADING_API_URL = 'https://api-demo.fxcm.com:443'
        ACCESS_TOKEN = "1dd15457d19e0bacf4f808cb911e4cb0871acde4"
        super().__init__(TRADING_API_URL, ACCESS_TOKEN)
        
        self.__initialize_managers()

    def temp_callback(msg):
        if msg is not None:
            #converts msg to json obj
            response =  json.loads(msg)
            print(response)
                    
    def __initialize_managers(self):
        self.add_manager_for_currency_pair('EUR/USD', self.temp_callback)
        self.add_manager_for_currency_pair('AUD/USD', self.temp_callback)
        self.add_manager_for_currency_pair('BTC/USD', self.temp_callback)


dizobot = DizoTradeBot()
dizobot.start()

print(dizobot.get_trade_history_dataframe())
        
#TRADING_API_URL = 'https://api-demo.fxcm.com:443'
#ACCESS_TOKEN = "1dd15457d19e0bacf4f808cb911e4cb0871acde4"
#
#bot = TradeBot(TRADING_API_URL, ACCESS_TOKEN)
#
#def temp_callback(msg):
#    if msg is not None:
#        #converts msg to json obj
#        response =  json.loads(msg)
#        print(response)
#                
#
#bot.add_manager_for_currency_pair('EUR/USD', temp_callback)
#bot.add_manager_for_currency_pair('AUD/USD', temp_callback)
#bot.add_manager_for_currency_pair('BTC/USD', temp_callback)
#
#bot.start()
