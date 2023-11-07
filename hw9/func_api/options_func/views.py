from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
import datetime
import pandas as pd
import json
from pandas import Timestamp
from lib.api_client import APIClient
from lib.gap.gap import SequentialDetectionGapAnalysis
from lib.support_resistance.support_resistance_analysis import SupportResistance
from lib.volume.volume_analysis import ProtrudingVolumeAnalysis
from lib.neckline.neckline_analysis import NecklineAnalysis
import yfinance as yf

ac = APIClient()

class GapViewSet(viewsets.ModelViewSet):
    """
    A ViewSet to handle gap analysis for stock data.
    Supports creation of gap analysis based on provided parameters.
    """
    queryset = None
    parser_classes = (JSONParser,)
    response = None
    required_params = ["symbol", "start_date", "params"]
    valid_params = ["symbol", "start_date", "end_date", "params"]

    def _default_handler(self, obj):
        """
        Default handler to serialize objects to JSON.
        Handles datetime.Timestamp objects by converting them to ISO formatted strings.
        """

        if isinstance(obj, Timestamp):
            return obj.isoformat(sep='-')[0:10]
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    def create(self, request):
        """
        Handle POST request to create a gap analysis for provided stock data.
        Expects input parameters including 'symbol', 'start_date', 'end_date', and 'params'.
        Returns a JSON response containing the gap analysis results.
        """
        input_params = [ele for ele in request.data]
        if set(input_params) - set(self.required_params) == set():
            end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        elif set(input_params) - set(self.required_params) == set(['end_date']):
            end_date = request.data.get("end_date")

        # # Request body contains invalid parameters
        # quote_res = ac.get_underlying_quotes(request.data.get("symbol"), request.data.get("start_date"), end_date)
        # quote_res = quote_res[request.data.get("symbol")]
        # # get stock data to dataframe
        # keys = ['date', 'open', 'high', 'low', 'close', 'volume']
        # result = [list(item) for item in zip(quote_res['date'], quote_res['open'], quote_res['high'], quote_res['low'], quote_res['close'], quote_res['volume'])]
        # final_result = [keys] + result
        # final_result = final_result[1:]
        # stock_history = pd.DataFrame(final_result, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        # stock_history['date'] = pd.to_datetime(stock_history['date'])
        # stock_history.set_index('date', inplace=True)

        #get data by yfinance API
        stock_history = yf.download(request.data.get("symbol"), start=request.data.get("start_date"), end=end_date)
        stock_history = stock_history[["Open", "High", "Low", "Close", "Volume"]]
        stock_history = stock_history.rename({'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, axis='columns')
        stock_history = stock_history.rename_axis("data", axis=0)
    
        # call the gap analysis function
        gap_case = SequentialDetectionGapAnalysis(
            request.data.get("params")["up_gap_interval"],
            request.data.get("params")["down_gap_interval"]
        )
        gap_res = gap_case.sequential_process(stock_history)
        res = {}
        for key, value in gap_res.items():
            date = self._default_handler(key[0])
            key = list(key)
            key[0] = date
            res.update({str(key)[1:-1]: value})
        # transform to json type
        res = json.dumps(res, default=self._default_handler, indent=2)
        res = json.loads(res)
        if res is None:
            response = Response(data={"msg": "not found"})
            response.status_code = 404
            return response
        response = Response(data={"msg": "Succeed", 'detail': res})
        response.status_code = 200
        return response
 

class VolumeViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for analyzing stock volume data.
    Supports creation of volume analysis based on provided parameters.
    """
    queryset = None
    parser_classes = (JSONParser,)
    response = None
    required_params = ["symbol", "start_date", "params"]
    valid_params = ["symbol", "start_date", "end_date", "params"]

    def _default_handler(self, obj):
        """
        Default handler to serialize objects to JSON.
        Handles datetime.Timestamp objects by converting them to ISO formatted strings..
        """
        if isinstance(obj, Timestamp):
            return obj.isoformat(sep='-')[0:10]
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
    
    def create(self, request):
        """
        Handle POST request to create a volume analysis for provided stock data.
        Expects input parameters including 'symbol', 'start_date', 'end_date', and 'params'.
        Returns a JSON response containing the volume analysis results.
        """
        input_params = [ele for ele in request.data]
        if set(input_params)-set(self.required_params) == set():
            end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        elif set(input_params)-set(self.required_params) == set(['end_date']):
            end_date = request.data.get("end_date")

        # # Request body contains invalid parameters
        # quote_res = ac.get_underlying_quotes(request.data.get("symbol"), request.data.get("start_date"), end_date)
        # quote_res = quote_res[request.data.get("symbol")]
        # # get stock data to dataframe
        # keys = ['date', 'open', 'high', 'low', 'close', 'volume']
        # result = [list(item) for item in zip(quote_res['date'], quote_res['open'], quote_res['high'], quote_res['low'], quote_res['close'], quote_res['volume'])]
        # final_result = [keys] + result
        # final_result = final_result[1:]
        # stock_history = pd.DataFrame(final_result, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        # stock_history['date'] = pd.to_datetime(stock_history['date'])
        # stock_history.set_index('date', inplace=True)

        #get data by yfinance API
        stock_history = yf.download(request.data.get("symbol"), start=request.data.get("start_date"), end=end_date)
        stock_history = stock_history[["Open", "High", "Low", "Close", "Volume"]]
        stock_history = stock_history.rename({'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, axis='columns')
        stock_history = stock_history.rename_axis("data", axis=0)

        # call the volume analysis function
        volume_case = ProtrudingVolumeAnalysis(
            request.data.get("params")["previous_day"],
            request.data.get("params")["survival_time"]
        )
        volume_case.sequential_process(stock_history)
        large_volume_res = volume_case.bar_large_volume
        res = {}
        for key, value in large_volume_res.items():
            date = self._default_handler(key[0])
            key = list(key)
            key[0] = date
            res.update({str(key)[1:-1] : value})
        if res is None:
            response = Response(data={"msg":"not found"})
            response.status_code = 404
            return response
        response = Response(data={"msg":"Succeed", 'detail':res})  
        response.status_code = 200
        return response
    

class SupportResistanceViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for detecting support and resistance levels in stock data.
    Supports creation of support and resistance analysis based on provided parameters.
    """
    queryset = None
    parser_classes = (JSONParser,)
    response = None
    required_params = ["symbol", "start_date", "params"]
    valid_params = ["symbol", "start_date", "end_date", "params"]

    def _default_handler(self, obj):
        """
        Default handler to serialize objects to JSON.
        Handles datetime.Timestamp objects by converting them to ISO formatted strings.
        """
        if isinstance(obj, Timestamp):
            return obj.isoformat(sep='-')[0:10]
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    def create(self, request):
        """
        Handle POST request to create support and resistance analysis for provided stock data.
        Expects input parameters including 'symbol', 'start_date', 'end_date', and 'params'.

        Returns a JSON response containing the support and resistance analysis results.
        """
        input_params = [ele for ele in request.data]
        if set(input_params)-set(self.required_params) == set():
            end_date = datetime.datetime.now().strftime('%Y-%m-%d') 
        elif set(input_params)-set(self.required_params) == set(['end_date']):
            end_date = request.data.get("end_date")

        # # Request body contains invalid parameters
        # quote_res = ac.get_underlying_quotes(request.data.get("symbol"), request.data.get("start_date"), end_date)
        # quote_res = quote_res[request.data.get("symbol")]
        # # get stock data to dataframe
        # keys = ['date', 'open', 'high', 'low', 'close', 'volume']
        # result = [list(item) for item in zip(quote_res['date'], quote_res['open'], quote_res['high'], quote_res['low'], quote_res['close'], quote_res['volume'])]
        # final_result = [keys] + result
        # final_result = final_result[1:]
        # stock_history = pd.DataFrame(final_result, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        # stock_history['date'] = pd.to_datetime(stock_history['date'])
        # stock_history.set_index('date', inplace=True)

        #get data by yfinance API
        stock_history = yf.download(request.data.get("symbol"), start=request.data.get("start_date"), end=end_date)
        stock_history = stock_history[["Open", "High", "Low", "Close", "Volume"]]
        stock_history = stock_history.rename({'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, axis='columns')
        stock_history = stock_history.rename_axis("data", axis=0)

        # call the support and resistance analysis function
        sup_res_case = SupportResistance(
            request.data.get("params")["closeness_threshold"],
            request.data.get("params")["peak_left"],
            request.data.get("params")["peak_right"],
            request.data.get("params")["valley_left"],
            request.data.get("params")["valley_right"],
            request.data.get("params")["swap_times"]
        )
        sup_res_case.sequential_process(stock_history)
        sup_res_res = sup_res_case.supp_resis
        res = {}
        for key, value in sup_res_res.items():
            date = self._default_handler(key[0])
            key = list(key)
            key[0] = date
            res.update({str(key)[1:-1] : value})
        if res is None:
            response = Response(data = {"msg":"not found"})
            response.status_code = 404
            return response                                
        response = Response(data={"msg":"Succeed", 'detail':res})  
        response.status_code = 200
        return response


class SupportSignalViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for generating support signals based on stock data.
    Supports creation of support signal analysis based on provided parameters.
    """
    queryset = None
    parser_classes = (JSONParser,)
    response = None
    required_params = ["symbol", "start_date", "params"]
    valid_params = ["symbol", "start_date", "end_date", "params"]

    def _default_handler(self, obj):
        """
        Default handler to serialize objects to JSON.
        Handles datetime.Timestamp objects by converting them to ISO formatted strings.
        """
        if isinstance(obj, Timestamp):
            return obj.isoformat(sep='-')[0:10]
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    def create(self, request):
        """
        Handle POST request to create support signal analysis for provided stock data.
        Expects input parameters including 'symbol', 'start_date', 'end_date', and 'params'.

        Returns a JSON response containing the support signal analysis results.
        """
        input_params = [ele for ele in request.data]
        if set(input_params)-set(self.required_params) == set():
            end_date = datetime.datetime.now().strftime('%Y-%m-%d') 
        elif set(input_params)-set(self.required_params) == set(['end_date']):
            end_date = request.data.get("end_date")

        # # Request body contains invalid parameters
        # quote_res = ac.get_underlying_quotes(request.data.get("symbol"), request.data.get("start_date"), end_date)
        # quote_res = quote_res[request.data.get("symbol")]
        # # get stock data to dataframe
        # keys = ['date', 'open', 'high', 'low', 'close', 'volume']
        # result = [list(item) for item in zip(quote_res['date'], quote_res['open'], quote_res['high'], quote_res['low'], quote_res['close'], quote_res['volume'])]
        # final_result = [keys] + result
        # final_result = final_result[1:]
        # stock_history = pd.DataFrame(final_result, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        # stock_history['date'] = pd.to_datetime(stock_history['date'])
        # stock_history.set_index('date', inplace=True)

        #get data by yfinance API
        stock_history = yf.download(request.data.get("symbol"), start=request.data.get("start_date"), end=end_date)
        stock_history = stock_history[["Open", "High", "Low", "Close", "Volume"]]
        stock_history = stock_history.rename({'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, axis='columns')
        stock_history = stock_history.rename_axis("data", axis=0)

        # call the support and resistance analysis function
        sup_res_case = SupportResistance(
            request.data.get("params")["closeness_threshold"],
            request.data.get("params")["peak_left"],
            request.data.get("params")["peak_right"],
            request.data.get("params")["valley_left"],
            request.data.get("params")["valley_right"],
            request.data.get("params")["swap_times"]
        )
        sup_res_case.sequential_process(stock_history)
        sup_res_res = sup_res_case.support_firstcrossover
        res = {}
        for key, value in sup_res_res.items():
            date = self._default_handler(key)
            key = [key]
            key = date
            res.update({str(key) : value})
        if res is None:
            response = Response(data = {"msg":"not found"})
            response.status_code = 404
            return response
        response = Response(data={"msg":"Succeed", 'detail':res})  
        response.status_code = 200
        return response


class ResistanceSignalViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for generating resistance signals based on stock data.
    Supports creation of resistance signal analysis based on provided parameters.
    """
    queryset = None
    parser_classes = (JSONParser,)
    response = None
    required_params = ["symbol", "start_date", "params"]
    valid_params = ["symbol", "start_date", "end_date", "params"]

    def _default_handler(self, obj):
        """
        Default handler to serialize objects to JSON.
        Handles datetime.Timestamp objects by converting them to ISO formatted strings.
        """
        if isinstance(obj, Timestamp):
            return obj.isoformat(sep='-')[0:10]
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
    
    def create(self, request):
        """
        Handle POST request to create resistance signal analysis for provided stock data.
        Expects input parameters including 'symbol', 'start_date', 'end_date', and 'params'.

        Returns a JSON response containing the resistance signal analysis results.
        """
        input_params = [ele for ele in request.data]
        if set(input_params)-set(self.required_params) == set():
            end_date = datetime.datetime.now().strftime('%Y-%m-%d') 
        elif set(input_params)-set(self.required_params) == set(['end_date']):
            end_date = request.data.get("end_date")

        # # Request body contains invalid parameters
        # quote_res = ac.get_underlying_quotes(request.data.get("symbol"), request.data.get("start_date"), end_date)
        # quote_res = quote_res[request.data.get("symbol")]
        # # get stock data to dataframe
        # keys = ['date', 'open', 'high', 'low', 'close', 'volume']
        # result = [list(item) for item in zip(quote_res['date'], quote_res['open'], quote_res['high'], quote_res['low'], quote_res['close'], quote_res['volume'])]
        # final_result = [keys] + result
        # final_result = final_result[1:]
        # stock_history = pd.DataFrame(final_result, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        # stock_history['date'] = pd.to_datetime(stock_history['date'])
        # stock_history.set_index('date', inplace=True)

        #get data by yfinance API
        stock_history = yf.download(request.data.get("symbol"), start=request.data.get("start_date"), end=end_date)
        stock_history = stock_history[["Open", "High", "Low", "Close", "Volume"]]
        stock_history = stock_history.rename({'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, axis='columns')
        stock_history = stock_history.rename_axis("data", axis=0)

        # call the support and resistance analysis function
        sup_res_case = SupportResistance(
            request.data.get("params")["closeness_threshold"],
            request.data.get("params")["peak_left"],
            request.data.get("params")["peak_right"],
            request.data.get("params")["valley_left"],
            request.data.get("params")["valley_right"],
            request.data.get("params")["swap_times"]
        )
        sup_res_case.sequential_process(stock_history)
        sup_res_res = sup_res_case.resistance_firstcrossover
        res = {}
        for key, value in sup_res_res.items():
            date = self._default_handler(key)
            key = [key]
            key = date
            res.update({str(key) : value})
        if res is None:
            response = Response(data = {"msg":"not found"})
            response.status_code = 404
            return response
        response = Response(data={"msg":"Succeed", 'detail':res})  
        response.status_code = 200
        return response


class NecklineViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for performing neckline analysis on stock data.
    Supports creation of neckline analysis based on provided parameters.
    """
    queryset = None
    parser_classes = (JSONParser,)
    response = None
    required_params = ["symbol", "start_date", "params"]
    valid_params = ["symbol", "start_date", "end_date", "params"]

    def _default_handler(self, obj):
        """
        Default handler to serialize objects to JSON.
        Handles datetime.Timestamp objects by converting them to ISO formatted strings.
        """
        if isinstance(obj, Timestamp):
            return obj.isoformat(sep='-')[0:10]
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    def create(self, request):
        """
        Handle POST request to create neckline analysis for provided stock data.
        Expects input parameters including 'symbol', 'start_date', 'end_date', and 'params'.

        Returns a JSON response containing the neckline analysis results.
        """
        input_params = [ele for ele in request.data]
        if set(input_params)-set(self.required_params) == set():
            end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        elif set(input_params)-set(self.required_params) == set(['end_date']):
            end_date = request.data.get("end_date")

        # # Request body contains invalid parameters
        # quote_res = ac.get_underlying_quotes(request.data.get("symbol"), request.data.get("start_date"), end_date)
        # quote_res = quote_res[request.data.get("symbol")]
        # # get stock data to dataframe
        # keys = ['date', 'open', 'high', 'low', 'close', 'volume']
        # result = [list(item) for item in zip(quote_res['date'], quote_res['open'], quote_res['high'], quote_res['low'], quote_res['close'], quote_res['volume'])]
        # final_result = [keys] + result
        # final_result = final_result[1:]
        # stock_history = pd.DataFrame(final_result, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        # stock_history['date'] = pd.to_datetime(stock_history['date'])
        # stock_history.set_index('date', inplace=True)

        #get data by yfinance API
        stock_history = yf.download(request.data.get("symbol"), start=request.data.get("start_date"), end=end_date)
        stock_history = stock_history[["Open", "High", "Low", "Close", "Volume"]]
        stock_history = stock_history.rename({'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, axis='columns')
        stock_history = stock_history.rename_axis("data", axis=0)

        # call the neckline analysis function
        neckline_case = NecklineAnalysis(
            request.data.get("params")["nk_valley_left"],
            request.data.get("params")["nk_valley_right"],
            request.data.get("params")["nk_peak_left"],
            request.data.get("params")["nk_peak_right"],
            request.data.get("params")["nk_startdate"],
            request.data.get("params")["nk_enddate"],
            request.data.get("params")["nk_interval"],
            request.data.get("params")["nk_value"],
        )
        x_line = [x for x in range(0,len(stock_history))]
        stock_history['X'] = x_line
        neckline_case.sequential_process(stock_history)
        neckline_res = neckline_case.neckline
        res = {}
        for key, value in neckline_res.items():
            date = self._default_handler(key[0])
            key = list(key)
            key[0] = date
            res.update({str(key)[1:-1] : value})
        if res is None:
            response = Response(data = {"msg":"not found"})
            response.status_code = 404
            return response                                             
        response = Response(data={"msg":"Succeed", 'detail' : res})  
        response.status_code = 200
        return response
    

class NecklineSupSignalViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for performing neckline support signal analysis on stock data.
    Supports creation of support signal analysis based on provided parameters.
    """
    queryset = None
    parser_classes = (JSONParser,)
    response = None
    required_params = ["symbol", "start_date", "params"]
    valid_params = ["symbol", "start_date", "end_date", "params"]

    def _default_handler(self, obj):
        """
        Default handler to serialize objects to JSON.
        Handles datetime.Timestamp objects by converting them to ISO formatted strings.
        """
        if isinstance(obj, Timestamp):
            return obj.isoformat(sep='-')[0:10]
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    def create(self, request):
        """
        Handle POST request to create neckline analysis for provided stock data.
        Expects input parameters including 'symbol', 'start_date', 'end_date', and 'params'.

        Returns a JSON response containing the neckline analysis results.
        """
        input_params = [ele for ele in request.data]
        if set(input_params)-set(self.required_params) == set():
            end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        elif set(input_params)-set(self.required_params) == set(['end_date']):
            end_date = request.data.get("end_date")

        # # Request body contains invalid parameters
        # quote_res = ac.get_underlying_quotes(request.data.get("symbol"), request.data.get("start_date"), end_date)
        # quote_res = quote_res[request.data.get("symbol")]
        # # get stock data to dataframe
        # keys = ['date', 'open', 'high', 'low', 'close', 'volume']
        # result = [list(item) for item in zip(quote_res['date'], quote_res['open'], quote_res['high'], quote_res['low'], quote_res['close'], quote_res['volume'])]
        # final_result = [keys] + result
        # final_result = final_result[1:]
        # stock_history = pd.DataFrame(final_result, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        # stock_history['date'] = pd.to_datetime(stock_history['date'])
        # stock_history.set_index('date', inplace=True)

        #get data by yfinance API
        stock_history = yf.download(request.data.get("symbol"), start=request.data.get("start_date"), end=end_date)
        stock_history = stock_history[["Open", "High", "Low", "Close", "Volume"]]
        stock_history = stock_history.rename({'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, axis='columns')
        stock_history = stock_history.rename_axis("data", axis=0)

        # call the neckline analysis function
        neckline_case = NecklineAnalysis(
            request.data.get("params")["nk_valley_left"],
            request.data.get("params")["nk_valley_right"],
            request.data.get("params")["nk_peak_left"],
            request.data.get("params")["nk_peak_right"],
            request.data.get("params")["nk_startdate"],
            request.data.get("params")["nk_enddate"],
            request.data.get("params")["nk_interval"],
            request.data.get("params")["nk_value"],
        )
        x_line = [x for x in range(0,len(stock_history))]
        stock_history['X'] = x_line
        neckline_case.sequential_process(stock_history)
        neckline_res = neckline_case.support_neckline_singal
        res = {}
        for key, value in neckline_res.items():
            date = self._default_handler(key)
            key = [key]
            key = date
            res.update({str(key) : value})
        if res is None:
            response = Response(data = {"msg":"not found"})
            response.status_code = 404
            return response                                                      
        response = Response(data={"msg":"Succeed", 'detail' : res})  
        response.status_code = 200
        return response


class NecklineResSignalViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for performing neckline resistance signal analysis on stock data.
    Supports creation of resistance signal analysis based on provided parameters.
    """
    queryset = None
    parser_classes = (JSONParser,)
    response = None
    required_params = ["symbol", "start_date", "params"]
    valid_params = ["symbol", "start_date", "end_date", "params"]

    def _default_handler(self, obj):
        """
        Default handler to serialize objects to JSON.
        Handles datetime.Timestamp objects by converting them to ISO formatted strings.
        """
        if isinstance(obj, Timestamp):
            return obj.isoformat(sep='-')[0:10]
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    def create(self, request):
        """
        Handle POST request to create neckline resistance signal analysis for provided stock data.
        Expects input parameters including 'symbol', 'start_date', 'end_date', and 'params'.

        Returns a JSON response containing the neckline resistance signal analysis results.
        """
        input_params = [ele for ele in request.data]
        if set(input_params)-set(self.required_params) == set():
            end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        elif set(input_params)-set(self.required_params) == set(['end_date']):
            end_date = request.data.get("end_date")

        # # Request body contains invalid parameters
        # quote_res = ac.get_underlying_quotes(request.data.get("symbol"), request.data.get("start_date"), end_date)
        # quote_res = quote_res[request.data.get("symbol")]
        # # get stock data to dataframe
        # keys = ['date', 'open', 'high', 'low', 'close', 'volume']
        # result = [list(item) for item in zip(quote_res['date'], quote_res['open'], quote_res['high'], quote_res['low'], quote_res['close'], quote_res['volume'])]
        # final_result = [keys] + result
        # final_result = final_result[1:]
        # stock_history = pd.DataFrame(final_result, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        # stock_history['date'] = pd.to_datetime(stock_history['date'])
        # stock_history.set_index('date', inplace=True)

        #get data by yfinance API
        stock_history = yf.download(request.data.get("symbol"), start=request.data.get("start_date"), end=end_date)
        stock_history = stock_history[["Open", "High", "Low", "Close", "Volume"]]
        stock_history = stock_history.rename({'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, axis='columns')
        stock_history = stock_history.rename_axis("data", axis=0)

        # call the neckline analysis function
        neckline_case = NecklineAnalysis(
            request.data.get("params")["nk_valley_left"],
            request.data.get("params")["nk_valley_right"],
            request.data.get("params")["nk_peak_left"],
            request.data.get("params")["nk_peak_right"],
            request.data.get("params")["nk_startdate"],
            request.data.get("params")["nk_enddate"],
            request.data.get("params")["nk_interval"],
            request.data.get("params")["nk_value"],
        )
        x_line = [x for x in range(0,len(stock_history))]
        stock_history['X'] = x_line
        neckline_case.sequential_process(stock_history)
        neckline_res = neckline_case.resistance_neckline_singal
        res = {}
        for key, value in neckline_res.items():
            date = self._default_handler(key)
            key = [key]
            key = date
            res.update({str(key) : value})
        if res is None:
            response = Response(data = {"msg":"not found"})
            response.status_code = 404
            return response       
        response = Response(data={"msg":"Succeed", 'detail' : res})  
        response.status_code = 200
        return response
    

class Find_Technical_Analysis_Signals(viewsets.ModelViewSet):

    queryset = None
    parser_classes = (JSONParser,)
    response = None
    required_params = ["symbol", "start_date", "signal_numbers", "params"]
    valid_params = ["symbol", "start_date", "end_date", "signal_numbers", "params"]
    long_result = dict
    short_result = dict

    def find_2signals(self, signal1, signal2):
        common_timestamps = set(data[0] for data in signal1) & set(data[0] for data in signal2)
        same_date = [data for data in signal1 if data[0] in common_timestamps]
        return same_date

    def find_3signals(self, signal1, signal2, signal3):
        common_timestamps = set(data[0] for data in signal1) & set(data[0] for data in signal2) & set(data[0] for data in signal3)
        same_date = [data for data in signal1 if data[0] in common_timestamps]
        return same_date

    def find_4signals(self, signal1, signal2, signal3, signal4):
        common_timestamps = set(data[0] for data in signal1) & set(data[0] for data in signal2) & set(data[0] for data in signal3) & set(data[0] for data in signal4)
        same_date = [data for data in signal1 if data[0] in common_timestamps]
        return same_date
    
    def create(self, request):

        input_params = [ele for ele in request.data]
        if set(input_params)-set(self.required_params) == set():
            end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        elif set(input_params)-set(self.required_params) == set(['end_date']):
            end_date = request.data.get("end_date")

        # Get parames
        signal_numbers = request.data.get("signal_numbers")

        # gap
        up_gap_interval = request.data.get("params")["gap_interval"]
        down_gap_interval = request.data.get("params")["gap_interval"]

        # volume
        previous_day = request.data.get("params")["previous_day"]
        survival_time = request.data.get("params")["survival_time"]

        # support resistant
        closeness_threshold = request.data.get("params")["closeness_threshold"]
        peak_left = request.data.get("params")["peak_left"]
        peak_right = request.data.get("params")["peak_right"]
        valley_left = request.data.get("params")["valley_left"]
        valley_right = request.data.get("params")["valley_right"]
        swap_times = request.data.get("params")["swap_times"]

        # neckline
        nk_valley_left = request.data.get("params")["nk_valley_left"]
        nk_valley_right = request.data.get("params")["nk_valley_right"]
        nk_peak_left = request.data.get("params")["nk_peak_left"]
        nk_peak_right = request.data.get("params")["nk_peak_right"]
        nk_startdate = request.data.get("params")["nk_startdate"]
        nk_enddate = request.data.get("params")["nk_enddate"]
        nk_interval = request.data.get("params")["nk_interval"]
        nk_value = request.data.get("params")["nk_value"]

        # Request body contains invalid parameters
        quote_res = ac.get_underlying_quotes(request.data.get("symbol"), request.data.get("start_date"), end_date)[request.data.get("symbol")]
        keys = ['date', 'open', 'high', 'low', 'close', 'volume']
        result = [list(item) for item in zip(quote_res['date'], quote_res['open'], quote_res['high'], quote_res['low'], quote_res['close'], quote_res['volume'])]
        final_result = [keys] + result
        final_result = final_result[1:]
        stock_history = pd.DataFrame(final_result, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        stock_history['date'] = pd.to_datetime(stock_history['date'])
        stock_history.set_index('date', inplace=True)

        # call the gap analysis function
        gap_case = SequentialDetectionGapAnalysis(up_gap_interval, down_gap_interval)
        gap_signal = dict(gap_case.sequential_process(stock_history))

        # call the volume analysis function
        volume_case = ProtrudingVolumeAnalysis(previous_day, survival_time)
        volume_case.sequential_process(stock_history)
        large_volume_signal = dict(volume_case.bar_large_volume)

        # call the support and resistance analysis function
        sup_res_case = SupportResistance(closeness_threshold, peak_left, peak_right, valley_left, valley_right, swap_times)
        sup_res_case.sequential_process(stock_history)
        support_signal = dict(sup_res_case.support_firstcrossover)
        resistance_signal = dict(sup_res_case.resistance_firstcrossover)

        # call the neckline analysis function
        neckline_case = NecklineAnalysis(nk_valley_left, nk_valley_right, nk_peak_left, nk_peak_right, nk_startdate, nk_enddate, nk_interval, nk_value)
        stock_history['X'] = [x for x in range(0, len(stock_history))]
        neckline_case.sequential_process(stock_history)
        support_neckline_signal = dict(neckline_case.support_neckline_singal)
        resistance_neckline_signal = dict(neckline_case.resistance_neckline_singal)

        # Convert format
        all_down_gap_signal = [[datetime.datetime.strptime(str(key[0]), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'), key[1]] for key,value in gap_signal.items() if value["attribute"]=="down_gap"]
        all_up_gap_signal = [[datetime.datetime.strptime(str(key[0]), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'), key[1]] for key,value in gap_signal.items() if value["attribute"]=="up_gap"]
        
        all_bar_signal = [[datetime.datetime.strptime(str(key[0]), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'), key[1]] for key,value in large_volume_signal.items()]

        all_support_signal = [[key.strftime('%Y-%m-%d'), value] for key,value in support_signal.items()]
        all_resistant_signal = [[key.strftime('%Y-%m-%d'), value] for key,value in resistance_signal.items()]

        all_support_neckline_signal = [[key.strftime('%Y-%m-%d'), value] for key,value in support_neckline_signal.items()]
        all_resistant_neckline_signal = [[key.strftime('%Y-%m-%d'), value] for key,value in resistance_neckline_signal.items()]

        # find intersection
        self.short_result = {}
        self.long_result = {}

        if 1 in signal_numbers:
            # Long Signal
            one_signal_long = {}
            one_signal_long["gap"] = all_up_gap_signal
            one_signal_long["bar"] = all_bar_signal
            one_signal_long["resistance"] = all_resistant_signal
            one_signal_long["neckline"] = all_resistant_neckline_signal
            one_signal_long = {key: value for key,value in one_signal_long.items() if value != []}
            self.long_result["one_signal"] = one_signal_long
            # Short Signal
            one_signal_short = {}
            one_signal_short["gap"] = all_down_gap_signal
            one_signal_short["bar"] = all_bar_signal
            one_signal_short["support"] = all_support_signal
            one_signal_short["neckline"] = all_support_neckline_signal
            one_signal_short = {key: value for key,value in one_signal_short.items() if value != []}
            self.short_result["one_signal"] = one_signal_short

        if 2 in signal_numbers:
            # Long Signal
            two_signal_long = {}
            two_signal_long["gap_bar"] = self.find_2signals(all_up_gap_signal, all_bar_signal)
            two_signal_long["gap_resistance"] = self.find_2signals(all_up_gap_signal, all_resistant_signal)
            two_signal_long["gap_neckline"] = self.find_2signals(all_up_gap_signal, all_resistant_neckline_signal)
            two_signal_long["bar_resistance"] = self.find_2signals(all_bar_signal, all_resistant_signal)
            two_signal_long["bar_neckline"] = self.find_2signals(all_bar_signal, all_resistant_neckline_signal)
            two_signal_long["resistance_neckline"] = self.find_2signals(all_resistant_signal, all_resistant_neckline_signal)
            two_signal_long = {key: value for key,value in two_signal_long.items() if value != []}
            self.long_result["two_signal"] = two_signal_long
            # Short Signal
            two_signal_short = {}
            two_signal_short["gap_bar"] = self.find_2signals(all_down_gap_signal, all_bar_signal)
            two_signal_short["gap_support"] = self.find_2signals(all_down_gap_signal, all_support_signal)
            two_signal_short["gap_neckline"] = self.find_2signals(all_down_gap_signal, all_support_neckline_signal)
            two_signal_short["bar_support"] = self.find_2signals(all_bar_signal, all_support_signal)
            two_signal_short["bar_neckline"] = self.find_2signals(all_bar_signal, all_support_neckline_signal)
            two_signal_short["support_neckline"] = self.find_2signals(all_support_signal, all_support_neckline_signal)
            two_signal_short = {key: value for key,value in two_signal_short.items() if value != []}
            self.short_result["two_signal"] = two_signal_short

        if 3 in signal_numbers:
            # Long Signal
            three_signal_long = {}
            three_signal_long["gap_bar_resistance"] = self.find_3signals(all_up_gap_signal, all_bar_signal, all_resistant_signal)
            three_signal_long["gap_bar_neckline"] = self.find_3signals(all_up_gap_signal, all_bar_signal, all_resistant_neckline_signal)
            three_signal_long["gap_resistance_neckline"] = self.find_3signals(all_up_gap_signal, all_resistant_signal, all_resistant_neckline_signal)
            three_signal_long["bar_resistance_neckline"] = self.find_3signals(all_bar_signal, all_resistant_signal, all_resistant_neckline_signal)
            three_signal_long = {key: value for key,value in three_signal_long.items() if value != []}
            self.long_result["three_signal"] = three_signal_long
            # Short Signal
            three_signal_short = {}
            three_signal_short["gap_bar_support"] = self.find_3signals(all_up_gap_signal, all_bar_signal, all_support_signal)
            three_signal_short["gap_bar_neckline"] = self.find_3signals(all_up_gap_signal, all_bar_signal, all_support_neckline_signal)
            three_signal_short["gap_support_neckline"] = self.find_3signals(all_up_gap_signal, all_support_signal, all_support_neckline_signal)
            three_signal_short["bar_support_neckline"] = self.find_3signals(all_bar_signal, all_support_signal, all_support_neckline_signal)
            three_signal_short = {key: value for key,value in three_signal_short.items() if value != []}
            self.short_result["three_signal"] = three_signal_short

        if 4 in signal_numbers:
            # Long Signal
            four_signal_long = {}
            four_signal_long["long"] = self.find_4signals(all_up_gap_signal, all_bar_signal, all_resistant_signal, all_resistant_neckline_signal)
            four_signal_long = {key: value for key,value in four_signal_long.items() if value != []}
            self.long_result["four_signal"] = four_signal_long
            # Short Signal
            four_signal_short = {}
            four_signal_short["short"] = self.find_4signals(all_down_gap_signal, all_bar_signal, all_support_signal, all_support_neckline_signal)
            four_signal_short = {key: value for key,value in four_signal_short.items() if value != []}
            self.short_result["four_signal"] = four_signal_short

        res = {'Short': self.short_result, 'Long': self.long_result}
        if res is None:
            response = Response(data = {"msg": "not found"})
            response.status_code = 404
            return response
        
        response = Response(data = {"msg": "Success", 'detail': res})
        response.status_code = 200
        return response