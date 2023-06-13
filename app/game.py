import sqlite3

con = sqlite3.connect('database.db')

Cursor = con.Cursor()

Cursor.execute(""" CREAT TABLE IF NOT EXISTS Game(
    id INTEGER,
    name STRING,
    genre STRING,
    publisher STRING,
    );""")

con.commit()
Cursor.close()
con.close()
