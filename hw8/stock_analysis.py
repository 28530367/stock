from typing import Any, List
import pandas as pd
import datetime
from datetime import datetime
import time
import pprint
from func_api_client import FuncClient
import yfinance as yf

func_client = FuncClient()

def convert_timestamp_to_highchart(time_str):
    return int(time.mktime(datetime.strptime(time_str, "%Y-%m-%d").timetuple()))*1000

def convert_str_to_datetime(time_str):
    return datetime.strptime(time_str, "%Y-%m-%d")

def get_stock_data(symbol, start_date):
    end_date = datetime.now().strftime('%Y-%m-%d')

    stock_data = yf.download(symbol, start=start_date, end=end_date)
    stock_data = stock_data[["Open", "High", "Low", "Close", "Volume"]]
    stock_data = stock_data.rename({'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, axis='columns')
    stock_data = stock_data.rename_axis("data", axis=0)
    dates = [datetime.strftime(date, '%Y-%m-%d') for date in list(stock_data.index)]
    dates = pd.Series(dates)
    #get ohlcv data
    timestamp_series = list(map(convert_timestamp_to_highchart, dates))
    datetime_series = list(map(convert_str_to_datetime, dates))
    ohlc = list(zip(timestamp_series, list(stock_data['open']), list(stock_data['high']), list(stock_data['low']), list(stock_data['close'])))
    ohlcv1 = list(zip(datetime_series, list(stock_data['open']), list(stock_data['high']), list(stock_data['low']), list(stock_data['close']), list(stock_data['volume'])))
    volume = list(zip(timestamp_series, list(stock_data['volume'])))
    stock_data = pd.DataFrame(ohlcv1, columns=["date", 'open', 'high', 'low', 'close', 'volume'])
    stock_data.sort_values('date', inplace=True)
    dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
    dates = pd.Series(dates)
    ohlc = list(zip((dates.astype(int)/1000000), list(stock_data['open']), list(stock_data['high']), list(stock_data['low']), list(stock_data['close'])))
    volume = list(zip((dates.astype(int)/1000000), list(stock_data['volume'])))
    stock_data = stock_data.set_index('date')
    x_line = [x for x in range(0, len(stock_data))]
    stock_data['X'] = x_line
    return [stock_data, ohlc, volume]

def find_2signals(list1, list2):
    common_timestamps = set(data[0] for data in list1) & set(data[0] for data in list2)
    same_date = [data for data in list1 if data[0] in common_timestamps]
    return same_date

def find_3signals(list1, list2, list3):
    common_timestamps = set(data[0] for data in list1) & set(data[0] for data in list2) & set(data[0] for data in list3)
    same_date = [data for data in list1 if data[0] in common_timestamps]
    return same_date

def find_4signals(list1, list2, list3, list4):
    common_timestamps = set(data[0] for data in list1) & set(data[0] for data in list2) & set(data[0] for data in list3) & set(data[0] for data in list4)
    same_date = [data for data in list1 if data[0] in common_timestamps]
    return same_date

def get_all_technical_analysis(symbol, 
                               start_date, 
                               end_date,
                               signal_numbers,
                               peak_left,
                               peak_right,
                               valley_left, 
                               valley_right,
                               closeness_threshold,
                               swap_times,
                               previous_day, 
                               survival_time,
                               gap_interval,
                               nk_valley_left,
                               nk_valley_right,
                               nk_peak_left,
                               nk_peak_right,
                               nk_startdate,
                               nk_enddate,
                               nk_interval,
                               nk_value):

    res = func_client.get_all_signal(symbol, 
                                     start_date, 
                                     end_date,
                                     signal_numbers,
                                     peak_left,
                                     peak_right,
                                     valley_left, 
                                     valley_right,
                                     closeness_threshold,
                                     swap_times,
                                     previous_day, 
                                     survival_time,
                                     gap_interval,
                                     nk_valley_left,
                                     nk_valley_right,
                                     nk_peak_left,
                                     nk_peak_right,
                                     nk_startdate,
                                     nk_enddate,
                                     nk_interval,
                                     nk_value)

    return res
