from django.shortcuts import render
from django.http import JsonResponse
from finlabBacktest.strategy import *


def finlabBacktest(request):
    
    return render(request, 'finlabBacktest.html', locals())

def ajax_finlabBacktest(request):
    strategy_select = request.POST['strategy_select']
    mounth_select = request.POST['mounth_select']

    if mounth_select == '1':
        start_date = '2023-10-01'
        end_date = '2023-10-31'
        ticker_symbols = ['3617.TW', '3325.TWO', '2417.TW', '5225.TW', '6613.TWO']
    elif mounth_select == '2':
        start_date = '2023-11-01'
        end_date = '2023-11-30'
        ticker_symbols = ['1463.TW', '2006.TW', '3176.TWO', '5508.TWO', '6189.TW']
    elif mounth_select == '3':
        start_date = '2023-12-01'
        end_date = '2023-12-31'
        ticker_symbols = ['4550.TWO', '6186.TWO', '6189.TW', '6426.TW', '6435.TWO']

    initial_capital = 2000000

    all_result_data =[]
    highcharts_data = []

    single_initial_capital = initial_capital / len(ticker_symbols)

    if single_initial_capital > initial_capital * 0.33:
        single_initial_capital = initial_capital * 0.33

    if strategy_select == '1':
        for ticker in ticker_symbols:
            daily_result, date_list = simulate_daily_trade(ticker, start_date, end_date, single_initial_capital)
            all_result_data.append(daily_result)
            daily_result['highcharts_list']['data'] = daily_result['highcharts_list']['data'] + ['100'] * (len(date_list) - len(daily_result['highcharts_list']['data']))
            daily_result['highcharts_list']['data'] = [float(value) for value in daily_result['highcharts_list']['data']]
            highcharts_data.append(daily_result['highcharts_list'])

    elif strategy_select == '2':
        for ticker in ticker_symbols:
            finlab_result, date_list = simulate_finlab_trade(ticker, start_date, end_date, single_initial_capital)
            all_result_data.append(finlab_result)
            finlab_result['highcharts_list']['data'] = finlab_result['highcharts_list']['data'] + ['100'] * (len(date_list) - len(finlab_result['highcharts_list']['data']))
            finlab_result['highcharts_list']['data'] = [float(value) for value in finlab_result['highcharts_list']['data']]
            highcharts_data.append(finlab_result['highcharts_list'])

    response = {
        'all_result_data' : all_result_data,
        'highcharts_data': highcharts_data,
        'date_list': date_list
    }

    return JsonResponse(response, safe=False)