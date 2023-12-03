from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from monitor import models
import json
from common.user_setting_operation import UserTrackingHandler

def web(request):
    if not request.user.is_authenticated:
        messages.success(request, 'Sorry ! Please Log In.')
        return redirect("http://127.0.0.1:3001/account/login")
    return (render(request,"quote/monitor.html"))

@csrf_exempt
def addTrack(request):
    uth = UserTrackingHandler()

    user = str(request.user)
    signals_selected_values = request.POST.get('signals_selected_values').split(',')
    signals_selected_values = [int(num) for num in signals_selected_values]
    start_date = request.POST.get('start_date')
    symbol = request.POST.get('symbol')
    peak_left = int(request.POST.get('peak_left'))
    peak_right = int(request.POST.get('peak_right'))
    valley_left = int(request.POST.get('valley_left'))
    valley_right = int(request.POST.get('valley_right'))
    closeness_threshold = int(request.POST.get('closeness_threshold'))
    swap_times = int(request.POST.get('swap_times'))
    previous_day = int(request.POST.get('previous_day'))
    survival_time = int(request.POST.get('time_interval'))
    gap_interval = float(request.POST.get('gap_interval'))
    nk_valley_left = int(request.POST.get('nk_valley_left'))
    nk_valley_right = int(request.POST.get('nk_valley_right'))
    nk_peak_left = int(request.POST.get('nk_peak_left'))
    nk_peak_right = int(request.POST.get('nk_peak_right'))
    nk_startdate = int(request.POST.get('nk_startdate'))
    nk_enddate = int(request.POST.get('nk_enddate'))
    nk_interval = int(request.POST.get('nk_interval'))
    nk_value = int(request.POST.get('nk_value'))
    
    uth.add(
        username = user,
        start_date = start_date,
        symbol = symbol,
        signals_selected_values = signals_selected_values,
        up_gap_interval = gap_interval,
        down_gap_interval = gap_interval,
        diff = closeness_threshold,
        peak_left = peak_left,
        peak_right = peak_right,
        valley_left = valley_left,
        valley_right = valley_right,
        swap_times = swap_times,
        previous_day = previous_day,
        survival_time = survival_time,
        nk_valley_left = nk_valley_left,
        nk_valley_right = nk_valley_right,
        nk_peak_left = nk_peak_left,
        nk_peak_right = nk_peak_right,
        nk_startdate = nk_startdate,
        nk_enddate = nk_enddate,
        nk_interval = nk_interval,
        nk_value = nk_value,
    )

    uth.close_connection()

    response = {'message': "Add track successful!!!!!!!!!"}
    response = json.dumps(response)

    return HttpResponse(response)

@csrf_exempt
def getTrackList(request):
    username = request.user
    try:
        auth_user = models.AuthUser.objects.get(username=username)
        user_info = models. UserTrackSupres.objects.filter(user=auth_user)
    except ObjectDoesNotExist:
        # Handle the case where the specified username does not exist
        print(f"User with username {username} does not exist.")
        return HttpResponse()

    user_info = list(user_info.values())
    for data in user_info:
        data['start_date'] = data['start_date'].strftime('%Y-%m-%d')
        data['created_at'] = data['created_at'].strftime('%Y-%m-%d')

    response = json.dumps(user_info)
    return HttpResponse(response)

@csrf_exempt
def removeTrack(request):
    uth = UserTrackingHandler()
    username = str(request.user)
    symbol = request.POST.get('symbol')
    start_date = request.POST.get('start_date')

    uth.remove(
        user=username,
        symbol=symbol,
        start_date=start_date,
    )
    try:
        auth_user = models.AuthUser.objects.get(username=username)
        user_info = models. UserTrackSupres.objects.filter(user=auth_user)
    except ObjectDoesNotExist:
        # Handle the case where the specified username does not exist
        print(f"User with username {username} does not exist.")
        return HttpResponse()

    user_info = list(user_info.values())
    for data in user_info:
        data['start_date'] = data['start_date'].strftime('%Y-%m-%d')
        data['created_at'] = data['created_at'].strftime('%Y-%m-%d')

    response = json.dumps(user_info)
    return HttpResponse(response)