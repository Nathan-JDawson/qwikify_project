import sqlite3

conn = sqlite3.connect("notes.sqlite")

curson = conn.cursor()
sql = """CREATE TABLE notes (
        id integer PRIMARY KEY,
        content text NOT NULL
    )"""
curson.execute(sql)