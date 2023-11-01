from stock_analysis import get_all_technical_analysis

all_technical_analysis = get_all_technical_analysis(
    symbol = 'SPY', 
    start_date = '2022-01-01', 
    end_date = '2023-01-01',
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

long_keys = [
    'two_signals_upgap_bar', 'two_signals_upgap_resistance', 'two_signals_upgap_resistance_neckline',
    'two_signals_bar_resistance', 'two_signals_bar_resistance_neckline', 'two_signals_resistance_resistance_neckline',
    'three_signals_upgap_bar_resistance', 'three_signals_upgap_bar_resistance_neckline',
    'three_signals_bar_resistance_resistance_neckline', 'three_signals_upgap_resistance_resistance_neckline',
    'four_signals_buy'
]

long_data = {key: all_technical_analysis[key] for key in all_technical_analysis if key in long_keys}

short_keys = [
    'two_signals_downgap_bar', 'two_signals_downgap_support', 'two_signals_downgap_support_neckline',
    'two_signals_bar_support', 'two_signals_bar_support_neckline', 'two_signals_support_support_neckline',
    'three_signals_downgap_bar_support', 'three_signals_downgap_bar_support_neckline', 'three_signals_bar_support_support_neckline',
      'three_signals_downgap_support_support_neckline', 'four_signals_sell'
]

short_data = {key: all_technical_analysis[key] for key in all_technical_analysis if key in short_keys}

signal_data = {key: all_technical_analysis[key] for key in all_technical_analysis if (key not in short_keys) and (key not in long_keys)}

for key, value in signal_data.items():
    print(key)
    print(value)
    print('----------------------------------------------------------------------')

print('long')
print(long_data)
print('----------------------------------------------------------------------')
print('short')
print(short_data)