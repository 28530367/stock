from common.func_api_client import FuncClient
from common.api_client import APIClient
from common.mail import MailHandler
from common.user_setting_operation import UserTrackingHandler
import pandas as pd
import os
from collections import defaultdict
import ast
import sys

class ReportHandler(object):

    def __init__(self):
        # self.ac = APIClient()
        self.mail = MailHandler()
        self.uth = UserTrackingHandler()
        self.fc = FuncClient()
        self.folder_path = "/home/shouweihuang/Lab_Training/stock/support_resistant-master/stock_project/email_report/"

    def _create_local_file(self, data, user):

        # other_row = pd.DataFrame({'symbol': [symbol], 'start_date': [start_date],})
        # df_short = pd.concat([other_row, df_short], ignore_index=True)
        if 'Short' in data and data['Short']:
            df_short = pd.DataFrame(data['Short'])
        else:
            df_short = pd.DataFrame()
        short_writer = pd.ExcelWriter('/home/shouweihuang/Lab_Training/stock/support_resistant-master/stock_project/email_report/all_short_signals.xlsx', engine='xlsxwriter')
        df_short.to_excel(short_writer, sheet_name='Short', index=False)
        # Close the Pandas Excel writer and output the Excel file
        short_writer.close()


        if 'Long' in data and data['Long']:
            df_long = pd.DataFrame(data['Long'])
        else:
            df_long = pd.DataFrame()
        long_writer = pd.ExcelWriter('/home/shouweihuang/Lab_Training/stock/support_resistant-master/stock_project/email_report/all_long_signals.xlsx', engine='xlsxwriter')
        df_long.to_excel(long_writer, sheet_name='Long', index=False)
        # Close the Pandas Excel writer and output the Excel file
        long_writer.close()


        print("Excel completed")

    def _remove_local_file(self, filename: str):
        print(f"successful remove {filename}!")
        os.remove(filename)

    def _get_signals(self, track):
        
        start_date = track[1]
        symbol = track[2]
        signals_selected_values = ast.literal_eval(track[3])
        up_gap_interval = track[4]
        down_gap_interval = track[5]
        diff = track[6]
        peak_left = track[7]
        peak_right = track[8]
        valley_left = track[9]
        valley_right = track[10]
        swap_times = track[11]
        previous_day = track[12]
        survival_time = track[13]
        nk_valley_left = track[14]
        nk_valley_right = track[15]
        nk_peak_left = track[16]
        nk_peak_right = track[17]
        nk_startdate = track[18]
        nk_enddate = track[19]
        nk_interval = track[20]
        nk_value = track[21]
        
        res = self.fc.get_all_signals(
                        symbol = symbol, 
                        signal_numbers = signals_selected_values,
                        start_date = start_date, 
                        up_gap_interval = up_gap_interval,
                        down_gap_interval = down_gap_interval,
                        previous_day = previous_day,
                        survival_time = survival_time,
                        diff = diff, 
                        peak_left = peak_left, 
                        peak_right = peak_right, 
                        valley_left = valley_left, 
                        valley_right = valley_right, 
                        swap_times = swap_times,
                        nk_valley_left = nk_valley_left, 
                        nk_valley_right = nk_valley_right, 
                        nk_peak_left = nk_peak_left, 
                        nk_peak_right = nk_peak_right, 
                        nk_startdate = nk_startdate, 
                        nk_enddate = nk_enddate,
                        nk_interval = nk_interval,
                        nk_value = nk_value)
        
        all_signals = defaultdict(list)
        for status , value in  res.items():
            for signal_num, value1 in value.items():
                for kind, value2 in value1.items():
                    for signal in value2:
                        date = signal[0]
                        price = signal[1]
                        obj = {"number_of_signals":signal_num, "kind":kind, "status":status, "date":date, "price":price}
                        if status =="Long":
                            all_signals['Long'].append(obj)
                        else:
                            all_signals['Short'].append(obj) 
        
        return dict(all_signals)
    
    def main(self):
        user_info = self.uth.get_all_user_info()

        for ele in user_info:
            user, email = ele
            track_info = self.uth.get_track_spreads_from_user(user)
            for track in track_info:
                res = self._get_signals(track)
                # send email
                if res != {}:
                    self._create_local_file(res, user)
                    res = self.mail.send(email, self.folder_path, track[2])

                    if res == {}:
                        print("Send email succseeful!")
                        self._remove_local_file(self.folder_path + "all_long_signals.xlsx")
                        self._remove_local_file(self.folder_path + "all_short_signals.xlsx")
                    else:
                        print("Send email failed")


if __name__ == "__main__":
    report = ReportHandler()
    end = report.main()
    
    