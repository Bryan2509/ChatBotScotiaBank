import sqlite3

conn=sqlite3.connect('Scott.db')
mycursor = conn.cursor()
print(mycursor.execute("""SELECT * FROM user_scott;"""))
conn.commit()