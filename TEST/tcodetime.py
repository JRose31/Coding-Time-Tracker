
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

def trackCodeTime(today, code_duration):
    try:
        #create new database if one hasn't been created
        sqliteConnection = sqlite3.connect("SQLite_codeTracker.db")
        sqlite_create_table_query = '''CREATE TABLE codeTracker (
                                    date TEXT,
                                    time TEXT);'''

        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()

        print("SQLite table created")

        #create new row for new database
        sqlite_insert_with_param = '''INSERT INTO 'codeTracker'
                                    ('date', 'time')
                                    VALUES (?,?);'''

        data_tuple = (today, code_duration)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        
        print("Session recorded successfully!")

    except:
        print("Table already exists...moving on...")

        #view all current data in database
        cursor.execute("SELECT * FROM codeTracker")
        existing = cursor.fetchall()
        print(existing)

        for i in existing:

            #if date exist in table (you coded earlier today)
            if today == i[0]:

                #get what duration is in table for today
                current_duration = '''SELECT time FROM codeTracker WHERE date = ?'''
                duration_tup = cursor.execute(current_duration, (today,))

                #access data from tuple generated from query
                duration_var = list(duration_tup)[0][0]
                print(duration_var)

                #format and add durations to update table with new duration for current date
                format_existing_duaration = datetime(year=int(today[:4]), month=int(end_time[5:7]), day=int(end_time[8:10]), hour=int(duration_var[:1]), minute=int(duration_var[2:4]), second=int(duration_var[5:]))
                format_new_duration = datetime(year=int(today[:4]), month=int(end_time[5:7]), day=int(end_time[8:10]), hour=int(code_duration[:1]), minute=int(code_duration[2:4]), second=int(code_duration[5:]))

                #CANNOT ADD TWO DATETIMES AS YOU CAN SUBTRACT THEM: ERROR THROWN!!!!!!!!!!!
                total_duration = format_existing_duaration + format_new_duration
                print(total_duration)

            else:#if today is a new day of coding, add new row
                sqlite_insert_with_param = '''INSERT INTO 'codeTracker'
                                            ('date', 'time')
                                            VALUES (?,?);'''

                data_tuple = (today, code_duration)
                cursor.execute(sqlite_insert_with_param, data_tuple)
                sqliteConnection.commit()

                print("Session recorded successfully!")

                #view new table
                cursor.execute("SELECT * FROM codeTracker")
                print(cursor.fetchall())

    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("sqlite connection is closed")

print(datetime.now().strftime("%Y:%m:%d:%H:%M:%S"))
trackCodeTime(str(datetime.now().strftime("%Y:%m:%d")), str(duration))
