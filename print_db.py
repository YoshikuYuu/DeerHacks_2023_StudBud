import sqlite3

def print_db():
     conn = sqlite3.connect('my_database.db')
     cursor = conn.cursor()

     # prints database
     cursor.execute("SELECT * FROM users")
     rows = cursor.fetchall()

     for row in rows:
          print(row)

print_db()
