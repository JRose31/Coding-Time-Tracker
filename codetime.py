
from datetime import datetime
import sqlite3
import matplotlib.pyplot as plt

#get current time when script starts
now = datetime.now()

#format time
current_time = now.strftime("%Y:%m:%d:%H:%M:%S")

#make datetime object to be able to operate with times
now_time_obj = datetime(year=int(current_time[:4]), month=int(current_time[5:7]), day=int(current_time[8:10]), hour=int(current_time[11:13]), minute=int(current_time[14:16]), second=int(current_time[17:]))
print("Starting @:", now_time_obj)

#initiate end time
stop = input("Press enter to stop script")

#get current time when script stops
later = datetime.now()

#format time
end_time = later.strftime("%Y:%m:%d:%H:%M:%S")

#make datetime object to be able to operate with times
end_time_obj = datetime(year=int(end_time[:4]), month=int(end_time[5:7]), day=int(end_time[8:10]), hour=int(end_time[11:13]), minute=int(end_time[14:16]), second=int(end_time[17:]))
print("Session ending @:", end_time_obj)

#get difference of two times
duration = end_time_obj - now_time_obj
print("Session duration recorded:", duration)

#datetime.datetime objects cannot be added so I created a function to add them by parsing their numbers and adding rules for adding times
def add_datetime(etime, ntime):
    sec = int(etime[6:])+int(ntime[6:])
    extramin = 0
    min = int(etime[3:5])+int(ntime[3:5])
    hr = int(etime[:2])+int(ntime[:2])

    if sec > 59:
        sec = sec-60
        extramin += 1
    if min > 59:
        min = min-60
        hr += 1

    print("New returned duration:", str(hr).zfill(2)+":"+str(min+extramin).zfill(2)+":"+str(sec).zfill(2))
    return(str(hr).zfill(2)+":"+str(min+extramin).zfill(2)+":"+str(sec).zfill(2))

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
        print("Existing data:", existing)
        print("Today:", today)


        #if date exist in table (you coded earlier today)
        if today == existing[(len(existing)-1)][0]:

            #get what duration is in table for today
            current_duration = '''SELECT time FROM codeTracker WHERE date = ?'''
            duration_tup = cursor.execute(current_duration, (today,))

            #access data from tuple generated from query
            duration_var = list(duration_tup)[0][0]
            print("Current saved duration:", duration_var)

            #format and add durations to update table with new duration for current date
            format_existing_duaration = datetime(year=int(today[:4]), month=int(end_time[5:7]), day=int(end_time[8:10]), hour=int(duration_var[:2]), minute=int(duration_var[3:5]), second=int(duration_var[6:]))
            format_new_duration = datetime(year=int(today[:4]), month=int(end_time[5:7]), day=int(end_time[8:10]), hour=int(code_duration[:2]), minute=int(code_duration[3:5]), second=int(code_duration[6:]))

            new_duration = add_datetime(str(format_existing_duaration.strftime("%H:%M:%S")), str(format_new_duration.strftime("%H:%M:%S")))

            update_query = '''UPDATE codeTracker set time = ? WHERE date = ?'''
            update_vars = (new_duration, today)
            cursor.execute(update_query, update_vars)

            #get what duration is in table for today
            current_duration = '''SELECT time FROM codeTracker WHERE date = ?'''
            duration_tup = cursor.execute(current_duration, (today,))

            #access data from tuple generated from query
            duration_var = list(duration_tup)[0][0]
            print("Updated Duration:", duration_var)
            sqliteConnection.commit()

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
            print("New database:\n",cursor.fetchall())

    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("sqlite connection is closed")

def showProgress():
    sqliteConnection = sqlite3.connect("SQLite_codeTracker.db")
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite...generating visual...")

    #view all current data in database
    cursor.execute("SELECT * FROM codeTracker")
    existing = cursor.fetchall()
    dates = []
    durations = []

    for data in existing:
        dates.append(data[0])
        durations.append(data[1])

    plt.bar(dates, durations)
    plt.xlabel("Date")
    plt.ylabel("Duration")
    plt.title("Your Session Breakdown")
    plt.show()




#record session time in database
trackCodeTime(str(datetime.now().strftime("%Y:%m:%d")), "0"+str(duration))#concatenate 0 to duration for correct format when indexing time values

#visualize data
showProgress()
