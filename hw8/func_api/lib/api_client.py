import pathlib
import json
import requests
import time
import threading
import os

class APIClient(object):
    _instance = None
    _app_info = {}
    app_token = {}
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        print(os.getcwd(),'abc')
        account_info = "/home/shouweihuang/Lab_Training/stock/hw8/func_api/lib/api_info.json"
        
        
        # account_info = "stock_project/api_info.json"
        with open (account_info, 'r')as f:
            
            self._api_info = json.load(f)
        
        self._start()
        
    def _auth_token(self, username, password):
        response = requests.post('http://140.116.214.156:7000/usData/token/', data={
                            "username":username,
                            "password":password
                        })
        api_token = response.json()
        return api_token
    
    
    def _refresh_token(self, app):
        request_header = { "Content-Type" : "application/json" }
        request_body = { "refresh" : self.app_token[app]['refresh']}
        response = requests.post("http://140.116.214.156:7000/usData/token/refresh/", data=json.dumps(request_body), headers=request_header)
        if response.status_code != 200:
            self.app_token[app] = self._auth_token(self._app_info[app]['username'], self._app_info[app]['password'])
        
        self.app_token[app] = response.json()    
            
    def _create_refresh_job(self, *args):
        while(True):
            for app in args:
                self._refresh_token(app)
            time.sleep(880)
    
    def _start(self):
        
        # auth token first (app = app name, info = username, password)
        for app, info in self._api_info.items():
            self.app_token[app] = self._auth_token(info['username'], info['password'])
            
        t1 = threading.Thread(target=self._create_refresh_job, args=self._api_info.keys())
        t1.start()
    def send_request_to_apigw(self,api_url, token=None, request_body=None):
        request_header = {
            "Authorization" : f"Bearer {token['access']}",
            "Content-Type"  : "application/json"
            }
        response = requests.post(api_url, data=json.dumps(request_body), headers=request_header)
        if (response.status_code == 401):
            token = self._refresh_token(token['refresh'])
            request_header["Authorization"] = f"Bearer {token['access']}"
            response = requests.post(api_url, data=json.dumps(request_body), headers=request_header)
        
        return response
    def get_underlying_quotes(self,symbol, start_date=None, end_date=None):
        url = 'http://140.116.214.156:7000/usData/market/quotes/'
        request_body = {
            "symbols": symbol,
            "start_date": start_date,
            "end_date": end_date,
        }
        response = self.send_request_to_apigw(url, self.app_token['technical_analysis'], request_body)
        if response.status_code == 200:
            return response.json()['detail']
        
        else:
            print("Something wrong at getting options chain, status code:", response.status_code)
            print(response.json())
            return None
