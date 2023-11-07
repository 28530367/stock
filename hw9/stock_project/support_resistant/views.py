from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import time
import json
from datetime import datetime
import pandas as pd

from collections import defaultdict
from .lib.stock_analysis import get_all_technical_analysis
from .lib.stock_analysis import get_stock_data

def web(request):
    # render search page
    return (render(request,"quote/support_resistant.html"))


@csrf_exempt
def singleSearch(request):
    start_date = request.POST.get('start_date')
    symbol = request.POST.get('symbol')
    signal_numbers = request.POST.get('signal_numbers').split(',')
    signal_numbers = [int(item) for item in signal_numbers]
    peak_left = request.POST.get('peak_left')
    peak_right = request.POST.get('peak_right')
    valley_left = request.POST.get('valley_left')
    valley_right = request.POST.get('valley_right')
    closeness_threshold = request.POST.get('closeness_threshold')
    swap_times=request.POST.get('swap_times')
    previous_day = request.POST.get('previous_day')
    survival_time = request.POST.get('time_interval')
    gap_interval = request.POST.get('gap_interval')
    nk_valley_left = request.POST.get('nk_valley_left')
    nk_valley_right = request.POST.get('nk_valley_right')
    nk_peak_left = request.POST.get('nk_peak_left')
    nk_peak_right = request.POST.get('nk_peak_right')
    nk_startdate = request.POST.get('nk_startdate')
    nk_enddate = request.POST.get('nk_enddate')
    nk_interval = request.POST.get('nk_interval')
    nk_value = request.POST.get('nk_value')
    
    AllData = get_all_technical_analysis(
        symbol,
        start_date,
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
        nk_value
    )

    AllData['symbol'] = symbol
    AllData = json.dumps(AllData)

    print(AllData)
    return HttpResponse(AllData)


