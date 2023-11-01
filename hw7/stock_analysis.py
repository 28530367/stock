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

def get_all_technical_analysis(
          symbol, 
          start_date, 
          end_date,
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
    analysis_results = {}

    def output_format(data):
    # 初始化空列表用於存儲轉換後的數據
        transformed_data = []

        # 遍歷JSON數據，將每個日期和價格轉換為子列表
        for key in data.keys():
            # 刪除外部引號和空格，然後按逗號拆分字符串
            parts = key.replace("'", "").split(', ')
            
            # 將日期和價格轉換為子列表
            date = parts[0]
            price = float(parts[1])
            transformed_data.append([date, price])
        return transformed_data
    
    analysis_results = {}
    # Gap
    res = func_client.get_gap(symbol, start_date, end_date, gap_interval)
    # 初始化變數用於存儲'state'為'up_gap'和'down_gap'的項目
    up_gap_items = {}
    down_gap_items = {}

    # 遍歷JSON數據，根據'state'的值將項目添加到相應的變數中
    for key, value in res.items():
        state = value['attribute']
        if state == 'up_gap':
            up_gap_items[key] = value
        elif state == 'down_gap':
            down_gap_items[key] = value
    gap_up_signal = output_format(up_gap_items)
    gap_down_signal = output_format(down_gap_items)

    analysis_results["all_up_gap_signal"] = gap_up_signal
    analysis_results["all_down_gap_signal"] = gap_down_signal

    # Volume
    res = func_client.get_volume(symbol, start_date, end_date, previous_day, survival_time)
    large_volume_strategy = output_format(res)
    analysis_results["all_bar_signal"] = large_volume_strategy
    
    # support signal
    res = func_client.get_supsignal(symbol, start_date, end_date, closeness_threshold, peak_left, peak_right, valley_left, valley_right, swap_times)
    sup_signal = []
    for date, price in res.items():
        sup_signal.append([date, price])
    analysis_results["all_support_signal"] = sup_signal

    # resistance signal
    res = func_client.get_ressignal(symbol, start_date, end_date, closeness_threshold, peak_left, peak_right, valley_left, valley_right, swap_times)
    res_signal = []
    for date, price in res.items():
        res_signal.append([date, price])
    analysis_results["all_resistance_signal"] = res_signal

    # Neckline support signal
    res = func_client.get_neckline_sup_signal(symbol, start_date, end_date, nk_valley_left, nk_valley_right, nk_peak_left, nk_peak_right, nk_startdate, nk_enddate,nk_interval,nk_value)
    neckline_sup_signal = []
    for date, price in res.items():
        neckline_sup_signal.append([date, price])
    analysis_results["all_support_neckline_signal"] = neckline_sup_signal

    # Neckline resistance signal
    res = func_client.get_neckline_res_signal(symbol, start_date, end_date, nk_valley_left, nk_valley_right, nk_peak_left, nk_peak_right, nk_startdate, nk_enddate,nk_interval,nk_value)
    neckline_res_signal = []
    for date, price in res.items():
        neckline_res_signal.append([date, price])
    analysis_results["all_resistance_neckline_signal"] = neckline_res_signal
    
    #  Long signals
    two_signals_upgap_bar=find_2signals(gap_up_signal,large_volume_strategy)
    two_signals_upgap_resistance=find_2signals(gap_up_signal,res_signal)
    two_signals_upgap_resistance_neckline=find_2signals(gap_up_signal,neckline_res_signal)
    two_signals_bar_resistance=find_2signals(large_volume_strategy,res_signal)
    two_signals_bar_resistance_neckline=find_2signals(large_volume_strategy,neckline_res_signal)
    two_signals_resistance_resistance_neckline=find_2signals(res_signal,neckline_res_signal)
    three_signals_upgap_bar_resistance=find_3signals(gap_up_signal,large_volume_strategy,res_signal)
    three_signals_upgap_bar_resistance_neckline=find_3signals(gap_up_signal,large_volume_strategy,neckline_res_signal)
    three_signals_upgap_resistance_resistance_neckline=find_3signals(gap_up_signal,res_signal,neckline_res_signal)
    three_signals_bar_resistance_resistance_neckline=find_3signals(large_volume_strategy,res_signal,neckline_res_signal)
    four_signals_buy=find_4signals(gap_up_signal,large_volume_strategy,res_signal,neckline_res_signal)
    # Short Signals
    two_signals_downgap_bar=find_2signals(gap_down_signal,large_volume_strategy)
    two_signals_downgap_support=find_2signals(gap_down_signal,sup_signal)
    two_signals_downgap_support_neckline=find_2signals(gap_down_signal,neckline_sup_signal)
    two_signals_bar_support=find_2signals(large_volume_strategy,sup_signal)
    two_signals_bar_support_neckline=find_2signals(large_volume_strategy,neckline_sup_signal)
    two_signals_support_support_neckline=find_2signals(sup_signal,neckline_sup_signal)
    three_signals_downgap_bar_support=find_3signals(gap_down_signal,large_volume_strategy,sup_signal)
    three_signals_downgap_bar_support_neckline=find_3signals(gap_down_signal,large_volume_strategy,neckline_sup_signal)
    three_signals_bar_support_support_neckline=find_3signals(large_volume_strategy,sup_signal,neckline_sup_signal)
    three_signals_downgap_support_support_neckline=find_3signals(gap_down_signal,sup_signal,neckline_sup_signal)
    four_signals_sell=find_4signals(gap_down_signal,large_volume_strategy,sup_signal,neckline_sup_signal)
    analysis_results["two_signals_upgap_bar"]=two_signals_upgap_bar
    analysis_results["two_signals_upgap_resistance"]=two_signals_upgap_resistance
    analysis_results["two_signals_upgap_resistance_neckline"]=two_signals_upgap_resistance_neckline
    analysis_results["two_signals_bar_resistance"]=two_signals_bar_resistance
    analysis_results["two_signals_bar_resistance_neckline"]=two_signals_bar_resistance_neckline
    analysis_results["two_signals_resistance_resistance_neckline"]=two_signals_resistance_resistance_neckline
    analysis_results["three_signals_upgap_bar_resistance"]=three_signals_upgap_bar_resistance
    analysis_results["three_signals_upgap_bar_resistance_neckline"]=three_signals_upgap_bar_resistance_neckline
    analysis_results["three_signals_bar_resistance_resistance_neckline"]=three_signals_bar_resistance_resistance_neckline
    analysis_results["three_signals_upgap_resistance_resistance_neckline"]=three_signals_upgap_resistance_resistance_neckline
    analysis_results["four_signals_buy"]=four_signals_buy
    analysis_results["two_signals_downgap_bar"]=two_signals_downgap_bar
    analysis_results["two_signals_downgap_support"]=two_signals_downgap_support
    analysis_results["two_signals_downgap_support_neckline"]=two_signals_downgap_support_neckline
    analysis_results["two_signals_bar_support"]=two_signals_bar_support
    analysis_results["two_signals_bar_support_neckline"]=two_signals_bar_support_neckline
    analysis_results["two_signals_support_support_neckline"]=two_signals_support_support_neckline
    analysis_results["three_signals_downgap_bar_support"]=three_signals_downgap_bar_support
    analysis_results["three_signals_downgap_bar_support_neckline"]=three_signals_downgap_bar_support_neckline
    analysis_results["three_signals_bar_support_support_neckline"]=three_signals_bar_support_support_neckline
    analysis_results["three_signals_downgap_support_support_neckline"]=three_signals_downgap_support_support_neckline
    analysis_results["four_signals_sell"]=four_signals_sell

    return analysis_results
