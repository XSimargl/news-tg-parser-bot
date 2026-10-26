import sqlite3
import config


def init_db(db_path: str = config.DB_PATH):
    with sqlite3.connect(db_path) as conn:
        
        cursor = conn.cursor()
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT ,
                    link TEXT UNIQUE,
                    published TEXT,
                    summary TEXT,
                    full_text TEXT,
                    id_TG_messenge INTEGER,
                    title_ru TEXT DEFAULT NULL,
                    grade INTEGER DEFAULT 0
                            CHECK (grade IN (0, 1, -1)),
                    score INTEGER DEFAULT 0,
                    status  VARCHAR(20) NOT NULL DEFAULT 'raw'
                            CHECK (status IN ('raw', 'selected', 'approved', 'rejected', 'sent')),
                    ai_summary TEXT)""")
    conn.close()
    
    
def save_news(news_list: list[dict],db_path: str = config.DB_PATH):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for item in news_list:
            cursor.execute("""INSERT OR IGNORE INTO news (title, link, published, summary)
            VALUES (?, ?, ?, ?)""", (item['title'], item['link'], item['published'], item['summary']))
    conn.close()
    
def get_selected_news(db_path: str = config.DB_PATH):
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
                        SELECT id, title, link, summary, score 
                        FROM news 
                        WHERE status = 'selected' 
                        ORDER BY score DESC 
                        LIMIT 1
                    """)
        row = cursor.fetchone()
        
    conn.close()
    if row:
        return dict(row)
    else:
        return None
    
    
def  update_news_status(news_id: int, status: str, ai_summary: str, full_text: str, title_ru: str  | None = None, db_path: str = config.DB_PATH):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE news SET status = ?, ai_summary = ?, full_text = ?, title_ru = ? WHERE id = ?", (status, ai_summary, full_text, title_ru, news_id))
    conn.close()
    
def get_approved_news(db_path: str = config.DB_PATH):
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, link, ai_summary, title_ru  FROM news WHERE status = 'approved'")
        rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def clean_old_news(keep_limit: int = 500, db_path: str = config.DB_PATH):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        cursor.execute("""DELETE FROM news
                       WHERE id NOT IN(
                           SELECT id FROM news ORDER BY id DESC LIMIT ?)""", (keep_limit,))
        deleted_count = cursor.rowcount
    conn.close()
    return deleted_count

def get_raw_news_all(db_path: str = config.DB_PATH):
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, summary FROM news WHERE status = 'raw' LIMIT 50")
        rows = cursor.fetchall()
    conn.close()
    if rows:
        return [dict(row) for row in rows]
    else:
        return []
    
def update_bouncer_score(news_id: int, status: str, score: int | None = None, db_path: str = config.DB_PATH):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE news SET status = ?, score = ? WHERE id = ?", (status, score, news_id))
    conn.close()
    
def update_telegram_message_id(news_id: int, message_id: int, status: str | None = None,db_path: str = config.DB_PATH ):
    with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE news SET status = ?, id_TG_messenge = ? WHERE id = ?", (  status, message_id,  news_id))
    conn.close()
    
def update_news_grade(news_id: int, grade: int | None = None,db_path: str = config.DB_PATH):
    
    with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE news SET grade = ? WHERE id = ?", ( grade, news_id))
    conn.close()