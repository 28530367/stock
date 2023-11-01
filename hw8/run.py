from stock_analysis import get_all_technical_analysis

all_technical_analysis = get_all_technical_analysis(
    symbol = 'SPY', 
    start_date = '2022-01-01', 
    end_date = '2023-01-01',
    signal_numbers = [1, 2, 3, 4],
    peak_left = 3,
    peak_right = 3,
    valley_left = 3, 
    valley_right = 3,
    closeness_threshold = 1,
    swap_times = 1,
    previous_day = 20, 
    survival_time = 180,
    gap_interval = 1,
    nk_valley_left = 5,
    nk_valley_right = 5,
    nk_peak_left = 5,
    nk_peak_right = 5,
    nk_startdate = 90,
    nk_enddate = 90,
    nk_interval = 90,
    nk_value = 10,
    )

print(all_technical_analysis)




