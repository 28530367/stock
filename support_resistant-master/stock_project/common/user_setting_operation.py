import json
import mysql.connector
from mysql.connector import errorcode
import pathlib
import os

class ConnectUserDB(object):
    
    def __init__(self):
        try:
            # Connect to MySQL server
            self.db_conn = mysql.connector.connect(
                host='localhost',
                database='accounts',
                user='shouweihuang',
                password='jj533675',
                port='3306'
            )
            print("Connect successful!")

            self.db_cursor = self.db_conn.cursor()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def close_connection(self):
        self.db_cursor.close()
        self.db_conn.close()

    def _get_user_id(self, username):
        sql = """SELECT id FROM auth_user
            WHERE username = %s"""
        sql_val = (username, )
        self.db_cursor.execute(sql, sql_val)
        user_id = self.db_cursor.fetchone()[0]
        return user_id

class UserTrackingHandler(ConnectUserDB):

    def __init__(self):
        super().__init__()

    def add(self, **kwargs):
        user_id = self._get_user_id(kwargs['username'])

        sql = """
            INSERT INTO user_track_supres(user_id, start_date, 
            symbol, number_of_signals, up_gap_interval, down_gap_interval, 
            diff, peak_left, peak_right, valley_left, valley_right, swap_times,
            previous_day, survival_time, nk_valley_left, nk_valley_right, nk_peak_left, nk_peak_right, nk_startdate,
            nk_enddate, nk_interval, nk_value) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE user_id=VALUES(user_id);
        """
        
        # Convert the list to a JSON string
        signals_selected_values_json = json.dumps(kwargs['signals_selected_values'])

        sql_val = (user_id,
                   kwargs['start_date'],
                   kwargs['symbol'],
                   signals_selected_values_json,  # Use the JSON string here
                   kwargs['up_gap_interval'],
                   kwargs['down_gap_interval'],
                   kwargs['diff'],
                   kwargs['peak_left'],
                   kwargs['peak_right'],
                   kwargs['valley_left'],
                   kwargs['valley_right'],
                   kwargs['swap_times'],
                   kwargs['previous_day'],
                   kwargs['survival_time'],
                   kwargs['nk_valley_left'],
                   kwargs['nk_valley_right'],
                   kwargs['nk_peak_left'],
                   kwargs['nk_peak_right'],
                   kwargs['nk_startdate'],
                   kwargs['nk_enddate'],
                   kwargs['nk_interval'],
                   kwargs['nk_value'])

        try:
            self.db_cursor.execute(sql, sql_val)
            self.db_conn.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # remove track
    def remove(self, user, symbol, start_date):
        user_id = self._get_user_id(user)

        sql = f"""DELETE FROM user_track_supres U
                    WHERE U.user_id = %s
                    AND U.symbol = %s
                    AND U.start_date = %s
                """
        sql_val = (user_id, symbol, start_date)
        self.db_cursor.execute(sql, sql_val)
        self.db_conn.commit()
        return    

    # get user email from name
    def get_user_email(self, user):

        sql = f"""
            SELECT email FROM auth_user 
            where username = %s
        """
        sql_val = (user, )
        self.db_cursor.execute(sql, sql_val)
        res = self.db_cursor.fetchall()[0][0]
        return res

    # get user name & email
    def get_all_user_info(self):
        try:
            sql = f"""
                SELECT DISTINCT (auth_user.username), auth_user.email FROM user_track_supres
                INNER JOIN auth_user ON user_track_supres.user_id = auth_user.id;
            """
            self.db_cursor.execute(sql)
            res = self.db_cursor.fetchall()
        except:
            print("get_all_user_info false")
        return res

    # select user 
    def get_all_user_id(self):
        sql = f"""SELECT user_track_supres.user_id 
                FROM user_track_supres 
                GROUP BY user_track_supres.user_id"""
        self.db_cursor.execute(sql)
        res = self.db_cursor.fetchall()
        return res

    # select track spreads
    def get_track_spreads_from_user(self, user):
        sql = """
            SELECT user_track_supres.created_at,
                DATE_FORMAT(start_date, '%Y-%m-%d') AS formatted_start_date,
                symbol,
                number_of_signals,
                up_gap_interval,
                down_gap_interval,
                diff,
                peak_left,
                peak_right,
                valley_left,
                valley_right,
                swap_times,
                previous_day,
                survival_time,
                nk_valley_left,
                nk_valley_right,
                nk_peak_left,
                nk_peak_right,
                nk_startdate,
                nk_enddate,
                nk_interval,
                nk_value
            FROM user_track_supres
            INNER JOIN auth_user ON auth_user.id = user_track_supres.user_id
            WHERE auth_user.username = %s
        """
        sql_val = (user, )
        self.db_cursor.execute(sql, sql_val)
        res = self.db_cursor.fetchall()
        return res
 
    # select underlying
    def get_track_underlying(self):
        sql = f"""
            SELECT DISTINCT (symbol) FROM user_track_spreads
        """
        self.db_cursor.execute(sql)
        res = self.db_cursor.fetchall()
        return [ ele[0] for ele in res]



if __name__ == "__main__":
    ush = UserTrackingHandler()

    ush.add(
        username="cheryl",
        start_date="2022-01-01",
        symbol="QQQ",
        signals_selected_values=[1, 2, 3, 4],
        up_gap_interval=1,
        down_gap_interval=1,
        diff=1,
        peak_left=5,
        peak_right=5,
        valley_left=5,
        valley_right=5,
        swap_times=1,
        previous_day=20,
        survival_time=180,
        nk_valley_left=5,
        nk_valley_right=5,
        nk_peak_left=5,
        nk_peak_right=5,
        nk_startdate=90,
        nk_enddate=90,
        nk_interval=90,
        nk_value=10,
    )

    ush.close_connection()


# if __name__ == "__main__":
#     ush = UserTrackingHandler()

#     ush.add(
#     username = str(request.user),
#     start_date = start_date,
#     symbol = symbol, 
#     signals_selected_values = signals_selected_values, 
#     up_gap_interval = up_gap_interval, 
#     down_gap_interval = down_gap_interval,
#     diff = diff, 
#     peak_left = peak_left, 
#     peak_right = peak_right, 
#     valley_left = valley_left, 
#     valley_right = valley_right, 
#     swap_times = swap_times, 
#     previous_day = previous_day, 
#     survival_time = survival_time, 
#     nk_valley_left = nk_valley_left, 
#     nk_valley_right = nk_valley_right,
#     nk_peak_left = nk_peak_left, 
#     nk_peak_right = nk_peak_right, 
#     nk_startdate = nk_startdate, 
#     nk_enddate = nk_enddate, 
#     nk_interval = nk_interval, 
#     nk_value = nk_value, 
#     )

#     user_info = ush.get_all_user_info()   
#     track_info = ush.get_track_spreads_from_user('thomas')
#     ush.remove('thomas', "UUP", "2023-02-01")
    

    