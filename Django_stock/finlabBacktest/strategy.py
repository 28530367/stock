import pandas as pd
import yfinance as yf
from pandas_market_calendars import get_calendar

def simulate_daily_trade(ticker_symbols, start_date, end_date, initial_capital):
    highcharts_list = {}
    profit_rate_list = []
    tabledata = []
    start_text = ''
    enddate_text = ''
    end_text = ''
    calendar = get_calendar('XTAI')
    trading_days = calendar.valid_days(start_date=start_date, end_date=end_date)
    last_day = trading_days[-1].tz_localize(None)

    end_date1 = pd.to_datetime(end_date) + pd.DateOffset(days=1)
    stock_data = yf.download(ticker_symbols, start=start_date, end=end_date1)
    open_price = stock_data['Open'].iloc[0]
    cost_per_share = int(open_price * 1000 + open_price * 1.425)

    shares_purchased = initial_capital // cost_per_share
    total_cost = int(open_price * shares_purchased * 1000) + int(open_price * shares_purchased * 1.425)
    remining_cash = initial_capital - total_cost

    stop_loss_percentage = 0.08
    stop_loss_price = open_price - (open_price * stop_loss_percentage)

    df = pd.DataFrame(stock_data)
    date_list = df.index.strftime('%Y-%m-%d').tolist()

    # print(initial_capital)
    # print(ticker_symbols)
    # print("月初開盤價： ", open_price)
    # print("買進張數： ", shares_purchased, " , 買進總花費（含手續費）： ", total_cost)
    # print("剩餘現金： ", remining_cash)
    # print("停損價格： ", stop_loss_price)

    sell_price = stock_data['Open'].iloc[0]
    start_text = f"進場價：{open_price}，買進張數：{shares_purchased}，買進總花費(含手續費)：{total_cost}，剩餘現金：{remining_cash}，停損價格：{stop_loss_price}"
    
    # print("每日損益：")
    count = 0
    for index, row in stock_data.iterrows():
        dict_result = {}
        count += 1
        profit = int((row['Open'] - open_price) * 1000 * shares_purchased) -\
            int(open_price * 1.425 * shares_purchased) - int(row['Open'] * 1.425 * shares_purchased) -\
            int(row['Open'] * 3 * shares_purchased)
        profit_rate = round((profit / initial_capital) * 100, 2)
        # print(f"{index.date()} - 最低價： {row['Low']:.2f}, 開盤價： {row['Open']:.2f}, 損益： {profit:.2f}, 報酬率： {profit_rate:.2f}%")
        dict_result['date'] = (index.date().strftime("%Y-%m-%d"))
        dict_result['low_price'] = '{:.2f}'.format(row['Low'])
        dict_result['open_price'] = '{:.2f}'.format(row['Open'])
        dict_result['profit'] = '{:.2f}'.format(profit)
        dict_result['profit_rate'] = '{:.2f}'.format(profit_rate)

        profit_rate_list.append('{:.2f}'.format(profit_rate))
        tabledata.append(dict_result)

        if row['Low'] < stop_loss_price:
            # print(f"在 {index} 停損觸發,賣出 {ticker_symbols}。")
            sell_price = stop_loss_price
            break

        if last_day == stock_data.index[-1] and count == len(stock_data):
            # print(f"在 {end_date} 賣出 {ticker_symbols}。")
            sell_price = stock_data['Open'].iloc[-1]

    entry_fee = open_price * 1.425
    exit_fee = sell_price *1.425
    tax = sell_price *3

    final_profit = int((sell_price - open_price) * 1000 * shares_purchased) - int(entry_fee * shares_purchased) - int(exit_fee * shares_purchased) - int(tax * shares_purchased)
    final_profit_rate = round((final_profit / initial_capital) * 100, 2)
    if (row['Low'] < stop_loss_price) or (last_day == stock_data.index[-1]):
        # print(f"交易結果：初始資金 {initial_capital}, 最終資金 {initial_capital + final_profit}, 損益 {final_profit}, 報酬率 {final_profit_rate}%")
        enddate_text = f"在 {index.date()} 出場"
        end_text = f"交易結果：初始資金 {initial_capital}，最終資金 {initial_capital + final_profit}，損益 {final_profit}，報酬率 {final_profit_rate}%"
    
    highcharts_list['name'] = ticker_symbols
    highcharts_list['data'] = profit_rate_list

    result = {
        'tabledata': tabledata,
        'ticker_symbols': ticker_symbols,
        'start_text': start_text,
        'enddate_text': enddate_text,
        'end_text': end_text,
        'highcharts_list': highcharts_list
    }
    return result, date_list

def simulate_finlab_trade(ticker_symbols, start_date, end_date, initial_capital):
    highcharts_list = {}
    profit_rate_list = []
    stop_check = ''
    start_text = ''
    enddate_text = ''
    end_text = ''
    tabledata = []
    calendar = get_calendar('XTAI')
    trading_days = calendar.valid_days(start_date=start_date, end_date=end_date)
    last_day = trading_days[-1].tz_localize(None)

    end_date1 = pd.to_datetime(end_date) + pd.DateOffset(days=1)
    stock_data = yf.download(ticker_symbols, start=start_date, end=end_date1)
    open_price = stock_data['Open'].iloc[0]
    cost_per_share = int(open_price * 1000 + open_price * 1.425)

    shares_purchased = initial_capital // cost_per_share
    total_cost = int(open_price * shares_purchased * 1000) + int(open_price * shares_purchased * 1.425)
    remining_cash = initial_capital - total_cost

    stop_loss_percentage = 0.08
    stop_loss_price = open_price - (open_price * stop_loss_percentage)

    df = pd.DataFrame(stock_data)
    date_list = df.index.strftime('%Y-%m-%d').tolist()

    # print(initial_capital)
    # print(ticker_symbols)
    # print("月初開盤價： ", open_price)
    # print("買進張數： ", shares_purchased, " , 買進總花費（含手續費）： ", total_cost)
    # print("剩餘現金： ", remining_cash)
    # print("停損價格： ", stop_loss_price)

    sell_price = stock_data['Open'].iloc[0]
    start_text = f"進場價：{open_price}，買進張數：{shares_purchased}，買進總花費(含手續費)：{total_cost}，剩餘現金：{remining_cash}，停損價格：{stop_loss_price}"

    # print("每日損益：")
    count = 0
    for index, row in stock_data.iterrows():
        dict_result = {}
        if stop_check == 'stop':
            # print(f"在 {index} 停損觸發,賣出 {ticker_symbols}。")
            sell_price = row['Open']
            break

        count += 1
        profit = int((row['Open'] - open_price) * 1000 * shares_purchased) -\
            int(open_price * 1.425 * shares_purchased) - int(row['Open'] * 1.425 * shares_purchased) -\
            int(row['Open'] * 3 * shares_purchased)
        profit_rate = round((profit / initial_capital) * 100, 2)
        # print(f"{index.date()} - 最低價： {row['Low']:.2f}, 開盤價： {row['Open']:.2f}, 損益： {profit:.2f}, 報酬率： {profit_rate:.2f}%")
        dict_result['date'] = (index.date().strftime("%Y-%m-%d"))
        dict_result['low_price'] = '{:.2f}'.format(row['Low'])
        dict_result['open_price'] = '{:.2f}'.format(row['Open'])
        dict_result['profit'] = '{:.2f}'.format(profit)
        dict_result['profit_rate'] = '{:.2f}'.format(profit_rate)

        profit_rate_list.append('{:.2f}'.format(profit_rate))
        tabledata.append(dict_result)

        if row['Open'] < stop_loss_price:
            stop_check = 'stop'

        if last_day == stock_data.index[-1] and count == len(stock_data):
            # print(f"在 {end_date} 賣出 {ticker_symbols}。")
            sell_price = stock_data['Open'].iloc[-1]

        last_open_price = row['Open']

    entry_fee = open_price * 1.425
    exit_fee = sell_price *1.425
    tax = sell_price *3

    final_profit = int((sell_price - open_price) * 1000 * shares_purchased) - int(entry_fee * shares_purchased) - int(exit_fee * shares_purchased) - int(tax * shares_purchased)
    final_profit_rate = round((final_profit / initial_capital) * 100, 2)
    if (last_open_price < stop_loss_price) or (last_day == stock_data.index[-1]):
        # print(f"交易結果：初始資金 {initial_capital}, 最終資金 {initial_capital + final_profit}, 損益 {final_profit}, 報酬率 {final_profit_rate}%")
        enddate_text = f"在 {index.date()} 出場"
        end_text = f"交易結果：初始資金 {initial_capital}，最終資金 {initial_capital + final_profit}，損益 {final_profit}，報酬率 {final_profit_rate}%"

    highcharts_list['name'] = ticker_symbols
    highcharts_list['data'] = profit_rate_list

    result = {
        'tabledata': tabledata,
        'ticker_symbols': ticker_symbols,
        'start_text': start_text,
        'enddate_text': enddate_text,
        'end_text': end_text,
        'highcharts_list': highcharts_list
    }
    return result, date_list