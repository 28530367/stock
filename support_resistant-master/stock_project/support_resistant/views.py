from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

import time
import json
from datetime import datetime
import pandas as pd
from collections import defaultdict
from common.user_setting_operation import UserTrackingHandler
from .lib.stock_analysis import get_all_technical_analysis, get_signals



def web(request):
    if not request.user.is_authenticated:
        messages.success(request, 'Sorry ! Please Log In.')
        return redirect("http://127.0.0.1:3001/account/login")
    return (render(request,"quote/support_resistant.html"))

@csrf_exempt
def singleSearch(request):
    # email = request.POST.get('email')
    signals_selected_values = request.POST.get('signals_selected_values')
    start_date = request.POST.get('start_date')
    symbol = request.POST.get('symbol')
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

    if len(signals_selected_values) > 1:
        signals_selected_values = list(eval(signals_selected_values))
    else:
        signals_selected_values = [int(ele) for ele in list(signals_selected_values)]


    all_signals = get_signals(
        # email,
        signals_selected_values,
        symbol, 
        start_date, 
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
    
    AllData = get_all_technical_analysis(
        symbol,
        start_date,
        peak_left, 
        peak_right,
        valley_left, 
        valley_right,
        closeness_threshold,swap_times,
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
    AllData['all_signals'] = all_signals
    AllData = json.dumps(AllData)

    return HttpResponse(AllData)

