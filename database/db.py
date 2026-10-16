import sqlite3
import config


def init_db(DB_PATH: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   title TEXT ,
                   link TEXT UNIQUE,
                   published TEXT,
                   summary TEXT,
                   status  VARCHAR(20) NOT NULL DEFAULT 'raw'
                        CHECK (status IN ('raw', 'approved', 'rejected')))""")
    conn.commit()
    conn.close()