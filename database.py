import sqlite3 as sq
from email_sender import *

def create_table():
   with sq.connect("bot.db") as con:
      con.execute("""CREATE TABLE IF NOT EXISTS users(
                            username TEXT,
                            number INTEGER DEFAULT 0
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

def update_phone_number(username, new_phone_number):
    with sq.connect("bot.db") as con:
        cur = con.cursor()
        cur.execute(f"UPDATE users SET number = {new_phone_number} WHERE username = '{username}'")

def delete_data(username):
    with sq.connect("bot.db") as con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM users WHERE username = '{username}'")

def get_information_from_database():
    with sq.connect("bot.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        return cur.fetchall()

def send_mail():
    send_email(get_information_from_database())