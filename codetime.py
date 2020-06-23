
from datetime import datetime
import sqlite3

#get current time when script starts
now = datetime.now()

#format time
current_time = now.strftime("%Y:%m:%d:%H:%M:%S")

#make datetime object to be able to operate with times
now_time_obj = datetime(year=int(current_time[:4]), month=int(current_time[5:7]), day=int(current_time[8:10]), hour=int(current_time[11:13]), minute=int(current_time[14:16]), second=int(current_time[17:]))
print(now_time_obj)

#initiate end time
stop = input("Press any key to stop script")

#get current time when script stops
later = datetime.now()

#format time
end_time = later.strftime("%Y:%m:%d:%H:%M:%S")

#make datetime object to be able to operate with times
end_time_obj = datetime(year=int(end_time[:4]), month=int(end_time[5:7]), day=int(end_time[8:10]), hour=int(end_time[11:13]), minute=int(end_time[14:16]), second=int(end_time[17:]))
print(end_time_obj)

#get difference of two times
duration = end_time_obj - now_time_obj
print(duration)

def trackCodeTime(id, today, code_duration):
    try:
        sqliteConnection = sqlite3.connect("SQLite_codeTracker.db")
        sqlite_create_table_query = '''CREATE TABLE codeTracker (
                                    id INTEGER PRIMARY KEY,
                                    date DATETIME,
                                    time TIME);'''
        
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        
        print("SQLite table created")
        
#ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        sqlite_insert_with_param = '''INSERT INTO 'codeTracker'
                                    ('id', 'date', 'time')
                                    VALUES (?,?,?);'''
                                    
        data_tuple = (id, today, code_duration)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Session recorded successfully!")
#ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!        
        
    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
        
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("sqlite connection is closed")

trackCodeTime(1, datetime.now().strftime("%Y:%m:%d:%H:%M:%S"), duration)
