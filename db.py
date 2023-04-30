import sqlite3
import json
from datetime import datetime

def initialize_db() -> tuple:
    # Following code makes a database with user, task, and time
    # Store time as datetime object if possible?
    # id is datetime.datetime.now
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id TEXT PRIMARY KEY NOT NULL,
                        tasks TEXT DEFAULT '{}',
                        complete BOOL,
                        incomplete BOOL)''')
    return conn, cursor

def user_in_db(cursor, user_id) -> bool:
    """ Check if a user is already in the database."""
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    return result

def add_user_to_db(cursor, conn, user_id):
    cursor.execute("INSERT INTO users (user_id, tasks) VALUES (?, '')", (user_id,))
    conn.commit()

    # close database connection
    # cursor.close()
    # conn.close()

def add_task(cursor, conn, user_id, task, time_formatted):
    """ Loads user data from SQL db, converts it into a dict, adds a dict item,
    converts the updated dict back into SQL, and updates the db."""
    cursor.execute("SELECT tasks FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    if result == ('',):
        current_tasks = {}
    else:
        current_tasks = json.loads(result[0])
    current_tasks[task] = time_formatted
    print(current_tasks)
    cursor.execute("UPDATE users SET tasks=? WHERE user_id=?", (json.dumps(current_tasks), user_id))
    conn.commit()

def db_get_tasks(cursor, time):
    cursor.execute("SELECT user_id, tasks FROM users")
    values = cursor.fetchall()
    matching_tasks = []
    for value in values:
        user_id = value[0]
        tasks = json.loads(value[1])
        print(tasks)
        for task in tasks:
            if tasks[task] == time:
                matching_tasks.append((user_id, task))
    return matching_tasks

def display_values(cursor, user_id):
    cursor.execute("SELECT tasks FROM users WHERE user_id=?", (user_id,))
    values = cursor.fetchone()
    return values


