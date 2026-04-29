import sqlite3
import pandas as pd
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        description TEXT,
        amount REAL,
        category TEXT,
        balance REAL
    )
    """)

    conn.close()


def save_data(df):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("transactions", conn, if_exists="replace", index=False)
    conn.close()
