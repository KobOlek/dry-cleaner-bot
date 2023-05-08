import sqlite3 as sq

def create_table():
   with sq.connect("bot.db") as con:
      con.execute("""CREATE TABLE IF NOT EXISTS users(
                            username TEXT,
                            number INTEGER
                        )""")

def get_phone_number(username):
    with sq.connect("bot.db") as con:
        cur = con.execute(f"SELECT number FROM users WHERE username = '{username}'")
        number = cur.fetchone()[0]
        return number

def set_phone_number(username, phone_number):
    with sq.connect("bot.db") as con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO users (username, number) VALUES ('{username}', {phone_number})")
