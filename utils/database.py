import sqlite3
from config import SEED_WEIGHT

gen_db_text = """CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY UNIQUE NOT NULL, 
    balance REAL DEFAULT (0) NOT NULL ON CONFLICT REPLACE, 
    seeds INTEGER DEFAULT (0) NOT NULL ON CONFLICT REPLACE, 
    balance_withdrawal REAL NOT NULL ON CONFLICT REPLACE DEFAULT (0)
    );"""

def connect_db():
    return sqlite3.connect("DB.db")

def open_db():
    with connect_db() as db:
        cur = db.cursor()
        cur.execute(gen_db_text)

def get_balance(user_id):
    with connect_db() as db:
        cur = db.cursor()
        data = cur.execute("SELECT balance FROM users WHERE id = ?", [user_id]).fetchone()[0]
        return data
    
def get_seeds(user_id):
    with connect_db() as db:
        cur = db.cursor()
        data = cur.execute("SELECT seeds FROM users WHERE id = ?", [user_id]).fetchone()[0]
        return data
    
def check_reg_user(user_id):
    """ Если есть в базе -> True \n
        Если нет в базе -> False"""
    with connect_db() as db:
        cur = db.cursor()
        try:
            cur.execute("SELECT id FROM users WHERE id = ?", [user_id]).fetchone()[0]
            return True
        except:
            return False
        
def reg_user(user_id):
    with connect_db() as db:
        cur = db.cursor()
        try:
            cur.execute("INSERT INTO users (id) VALUES (?)", [user_id]).fetchone()
        except:
            pass

def add_balance_by_seeds():
    with connect_db() as db:
        cur = db.cursor()
        data = cur.execute("SELECT id, seeds FROM users", ).fetchall()
        for i in data:
            user_id = i[0]
            seed_balance = i[-1] * SEED_WEIGHT
            cur.execute("UPDATE users SET balance = balance + ? WHERE id = ?", [seed_balance, user_id])
        return data

def add_seeds(user_id, count):
    with connect_db() as db:
        cur = db.cursor()
        cur.execute("UPDATE users SET seeds = seeds + ? WHERE id = ?", [count, user_id])

def reset_balance(user_id):
    with connect_db() as db:
        cur = db.cursor()
        cur.execute("UPDATE users SET balance_withdrawal = balance_withdrawal + (SELECT balance FROM users WHERE id = ?) WHERE id = ?", [user_id, user_id])
        cur.execute("UPDATE users SET balance = 0 WHERE id = ?", [user_id])

def restore_balance(user_id):
    with connect_db() as db:
        cur = db.cursor()
        cur.execute("UPDATE users SET balance = balance + (SELECT balance_withdrawal FROM users WHERE id = ?) WHERE id = ?", [user_id, user_id])
        cur.execute("UPDATE users SET balance_withdrawal = 0 WHERE id = ?", [user_id])

def reset_balance_withdrawal(user_id):
    with connect_db() as db:
        cur = db.cursor()
        cur.execute("UPDATE users SET balance_withdrawal = 0 WHERE id = ?", [user_id])

def check_balance_withdrawal(user_id):
    with connect_db() as db:
        cur = db.cursor()
        balance_withdrawal=cur.execute("SELECT balance_withdrawal FROM users WHERE id = ?", [user_id]).fetchone()[0]
        if balance_withdrawal == "0" or balance_withdrawal == 0:
            return True
        return False

if __name__ == "__main__":
    print(reset_balance(123))