import time
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import tkinter as tk

start_time = []
end_time = []
durations = []
counter = 0

def recordTime():
    if len(start_time) == len(end_time):
        start_time.append(time.time())
    else:
        print("Stop timer before starting another session!")

def stopTime():
    #track stop time and get duration
    if len(start_time) == (len(end_time) + 1):
        end_time.append(time.time())
        global counter
        durations.append(end_time[counter]-start_time[counter])
        print("Elapsed time:", durations[counter])
        counter += 1


#--------------------------------UPLOAD DATA TO SQL-------------------------------------#

        #assing date and duration to variables
        today = (str(datetime.now().strftime("%Y:%m:%d")))
        duration = round(durations[len(durations)-1])#get last instance of list
        try:
            #create new database if one hasn't been created
            sqliteConnection = sqlite3.connect("SQLite_codeTrackerTest.db")
            sqlite_create_table_query = '''CREATE TABLE codeTracker (
                                        date TEXT,
                                        time INTEGER);'''

            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")

            cursor.execute(sqlite_create_table_query)
            sqliteConnection.commit()

            print("SQLite table created")

            #create new row for new database
            sqlite_insert_with_param = '''INSERT INTO 'codeTracker'
                                        ('date', 'time')
                                        VALUES (?,?);'''

            data_tuple = (today, duration)
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

            dates = []
            for i in existing:
                dates.append(i[0])


            #if date exist in table (you coded earlier today)
            if today in dates:

                #get what duration is in table for today
                current_duration = '''SELECT time FROM codeTracker WHERE date = ?'''
                duration_tup = cursor.execute(current_duration, (today,))

                #access data from tuple generated from query
                duration_var = list(duration_tup)[0][0]
                print("Current saved duration:", duration_var)

                new_duration = duration_var + duration

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

                data_tuple = (today, duration)
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
#------------------------------------------------------------------------------------------#
    else:
        print("No active session! Press start to activate new session.")



def trackCodeTime():
    today = (str(datetime.now().strftime("%Y:%m:%d")))
    duration = round(sum(durations))
    try:
        #create new database if one hasn't been created
        sqliteConnection = sqlite3.connect("SQLite_codeTrackerTest.db")
        sqlite_create_table_query = '''CREATE TABLE codeTracker (
                                    date TEXT,
                                    time INTEGER);'''

        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()

        print("SQLite table created")

        #create new row for new database
        sqlite_insert_with_param = '''INSERT INTO 'codeTracker'
                                    ('date', 'time')
                                    VALUES (?,?);'''

        data_tuple = (today, duration)
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

        dates = []
        for i in existing:
            dates.append(i[0])


        #if date exist in table (you coded earlier today)
        if today in dates:

            #get what duration is in table for today
            current_duration = '''SELECT time FROM codeTracker WHERE date = ?'''
            duration_tup = cursor.execute(current_duration, (today,))

            #access data from tuple generated from query
            duration_var = list(duration_tup)[0][0]
            print("Current saved duration:", duration_var)

            new_duration = duration_var + duration

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

            data_tuple = (today, duration)
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

def plotData():
    sqliteConnection = sqlite3.connect("SQLite_codeTrackerTest.db")
    cursor = sqliteConnection.cursor()

    print("Connected to SQLite...generating visual...")

    cursor.execute("SELECT * FROM codeTracker")
    existing = cursor.fetchall()

    #rounds number as integer despite what decimal is
    def truncate(n, decimals=0):
        multiplier = 10 ** decimals
        return int(n * multiplier) / multiplier

    #collect data for plotting
    dates = list(i[0] for i in existing)
    seconds = list(i[1] for i in existing)
    labels = []

    #converts seconds into hour, minutes, seconds string format and add to list of labels
    for i in seconds:
        if i < 60:
            labels.append(str(i) + " seconds")
        elif i > 59 and i < 3700:
            minute = truncate(i/60)
            sec = i-(minute*60)
            labels.append(str(truncate(minute)) + " minutes " + str(truncate(sec)) + " seconds")
        elif i > 3699:
            hr = truncate(i/3700)
            minutes = i-(hr*3700)
            if minutes > 59:
                mins = minutes/60
                labels.append(str(truncate(hr)) + " hrs " + str(truncate(mins)) + " minutes ")
            elif minutes < 60:
                labels.append(str(truncate(hr)) + " hrs " + str(truncate(minutes)) + " minutes ")

    #create graph
    plt.style.use('ggplot')
    plt.bar(dates, seconds)

    plt.yticks(seconds, labels, rotation=60, fontsize='x-small')
    plt.xticks(dates, rotation=40, fontsize='x-small')

    plt.xlabel('Dates', fontweight='bold')
    plt.ylabel('Duration', fontweight='bold')
    plt.title('Time Tracker Data', fontweight='bold')

    plt.tight_layout()
    plt.show()



window = tk.Tk()

b1 = tk.Button(text = "Start", command=recordTime)
b2 = tk.Button(text = "Stop", command=stopTime)
b3 = tk.Button(text = 'Plot Data', command=plotData)
b1.pack(side='left')
b2.pack(side='left')
b3.pack(side='left')


window.mainloop()
