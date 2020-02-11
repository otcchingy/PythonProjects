import pandas as pd
import json
import requests
import socketio
from datetime import datetime

def get_current_date_in_secs():
    #'2020-01-04 04:42:49.076010
    dt_obj = datetime.strptime(str(datetime.now()),
                           '%Y-%m-%d %H:%M:%S.%f')
    sec = dt_obj.timestamp() * 1000 * 1000
    return sec


class TradeBot:

    def __init__(self, trading_url, access_token, **kwargs):
        self.__trading_url = trading_url
        self.__access_token = access_token
        self.__sio = socketio.Client()
        self.__kwargs = kwargs
        self.__socket_bearer = None
        self.__currency_pair_managers = {}
        self.__on_connect_listener = None
        self.__on_disconnect_listener = None
        self.__work_started = False
        # future params
        #if not __kwargs.keys().__contains__('key'):
        #    self.__kwargs['key'] = 'https://api-demo.fxcm.com:443'

    
    def start(self):
        self.__initialize_socket()
        self.__start_managers()
        self.__is_working = True
        
    def stop(self):
        # TODO: stop socket
        self.__is_working = False
        #resetting payload
        for currency_pair in self.get_active_subscribed_currency_pairs():
            self.__currency_pair_managers[f'{currency_pair}']['status'] = 'not-active'
 
    def  __initialize_socket(self):
        self.__sio.connect(self.get_trading_api_url() + "?" + 'access_token=' + self.get_access_token())
        self.__socket_bearer = 'Bearer ' + self.__sio.sid + self.get_access_token()

        @self.__sio.on('connect')
        def on_connect():
            self.get_on_connect_listener()

        @self.__sio.on('disconnect')
        def on_disconnect():
             self.get_on_disconnect_listener()
             
    def __subscribe_to_currency_pair(self, currency_pair):
    # print(__socket_bearer)
        sub_response = requests.post(self.get_trading_api_url() + '/subscribe',
                                     # request for humans
                                     # method for request
                                     headers={
                                         'User-Agent': 'request',
                                         'Authorization': self.__socket_bearer,
                                         'Accept': 'application/json',
                                         'Content-Type': 'application/x-www-form-urlencoded'
                                     },
                                     data={
                                         # number of hist responses
                                         'pairs': currency_pair
                                     })

        if sub_response.status_code == 200:
            # print('Data Retrieved Successfully')
            data = sub_response.json()
            return data
        # else:
        #    print('Retrieving failed!!! + Error Code: ', sub_response.status_code)

    def __add_on_currency_pair_update_event(self, currency_pair, callback):
        @self.__sio.on(currency_pair)
        def on_price_update(msg):
            if callback is not None:
                callback(msg)

    def __start_service_for(self, currency_pair):
        sub_response = self.__subscribe_to_currency_pair(currency_pair)
        print(sub_response)
        if sub_response:
            payload = self.__currency_pair_managers[f'{currency_pair}']
            self.__add_on_currency_pair_update_event(currency_pair, payload['callback'])
            self.__currency_pair_managers[f'{currency_pair}']['status'] = 'active'

    def __start_managers(self):
        if not self.is_working():
            for currency_pair in self.get_subscribed_currency_pairs():
                self.__start_service_for(currency_pair)
                
    def is_working(self) -> bool:
        return self.__work_started
    
    def set_on_connect_listener(self, listener_callback):
        self.__on_connect_listener = listener_callback
        
    def set_on_disconnect_listener(self, listener_callback):
        self.__on_disconnect_listener = listener_callback
    
    def get_on_connect_listener(self):
        return self.__on_connect_listener

    def get_on_disconnect_listener(self):
        return self.__on_disconnect_listener

    def get_trading_api_url(self):
        return self.__trading_url

    def get_access_token(self):
        return self.__access_token
    
    def get_socket_bearer(self):
        return self.__socket_bearer
    
    def get_subscribed_currency_pairs(self): 
        return list(self.__currency_pair_managers.keys())

    def get_active_subscribed_currency_pairs(self):
        active_list = []
        for currency_pair in self.get_subscribed_currency_pairs():
            if self.is_active_subscribed_currency_pair(currency_pair):
                active_list.push(currency_pair)
        return active_list

    def is_active_subscribed_currency_pair(self, currency_pair):
        payload = self.__currency_pair_managers[f'{currency_pair}']
        return payload['status'] == 'active'

    def add_manager_for_currency_pair(self, currency_pair, callback):
        payload = {'callback': callback, 'status': 'not-active'}
        self.__currency_pair_managers[f'{currency_pair}'] = payload
        
        if self.is_working():
            self.__start_service_for(currency_pair)            
    
    def subscribe_to_currency_pair(self, currency_pair):
        if not self.get_subscribed_currency_pairs().__contains__(currency_pair):
            payload = {'callback': None, 'status': 'not-active'}
            self.__currency_pair_managers[f'{currency_pair}'] = payload

        if self.is_working():
            self.__start_service_for(currency_pair)


             
    def set_subscribed_currency_pair_event_listener(self, currency_pair, listener):
        if not self.is_working():
            if self.get_subscribed_currency_pairs().__contains__(currency_pair):
                payload = {'callback': listener, 'status': 'not-active'}
                self.__currency_pair_managers[f'{currency_pair}'] = payload
            
    def update_subscribed_currency_pair_event_listener(self, currency_pair, listener):
        if self.is_started() and self.get_subscribed_currency_pairs().__contains__(currency_pair):
            payload = self.__currency_pair_managers[f'{currency_pair}']
            if payload['status'] == 'active': 
                self.__currency_pair_managers[f'{currency_pair}']['callback'] = listener
                self.__add_on_currency_pair_update_event(currency_pair, payload['callback'])

    def get_trade_history_dataframe(self, size=1000, _from=1494086400, _to=1503835200):
        hist_response = requests.get(self.get_trading_api_url() + '/candles/1/H1',
                                     # request for humans
                                     # method for request
                                     headers={
                                         'User-Agent': 'request',
                                         'Authorization': self.__socket_bearer,
                                         'Accept': 'application/json',
                                         'Content-Type': 'application/x-www-form-urlencoded'
                                     },
                                     params={
                                         # number of hist responses
                                         'num': size,
                                         'from': _from,
                                         'to': _to
                                     })
        # print(hist_response)
        if hist_response.status_code == 200:
            # print('Data Retrieved Successfully')
            data = hist_response.json()
            data_frame = pd.DataFrame(data['candles'])
            data_frame.columns = ["time", "bidopen", "bidclose", "bidhigh", "bidlow", "askopen", "askclose", "askhigh",
                                 "asklow", "TickQty"]
            data_frame['time'] = pd.to_datetime(data_frame['time'], unit='s')
            return data_frame
        # else:
        #   print('Retrieving failed!!! + Error Code: ', hist_response.status_code)

            
            







        