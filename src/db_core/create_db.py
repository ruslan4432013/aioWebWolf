import sqlite3

from src.config.settings import PATH_TO_DB

con = sqlite3.connect(PATH_TO_DB)
cur = con.cursor()
with open('create_db.sql', 'r') as f:
    text = f.read()

cur.executescript(text)
cur.close()
con.close()
