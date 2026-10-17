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
                    status  VARCHAR(20) NOT NULL DEFAULT 'raw'
                            CHECK (status IN ('raw', 'approved', 'rejected', 'sent')),
                    ai_summary TEXT)""")
    conn.close()
    
    
def save_news(news_list: list[dict],db_path: str = config.DB_PATH):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for item in news_list:
            cursor.execute("""INSERT OR IGNORE INTO news (title, link, published, summary)
            VALUES (?, ?, ?, ?)""", (item['title'], item['link'], item['published'], item['summary']))
    conn.close()
    
def get_raw_news(db_path: str = config.DB_PATH):
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, link, summary FROM news WHERE status = 'raw' LIMIT 1")
        row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    else:
        return None
    
    
def  update_news_status(news_id: int, status: str, ai_summary: str | None = None, db_path: str = config.DB_PATH):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE news SET status = ?, ai_summary = ? WHERE id = ?", (status, ai_summary, news_id))
    conn.close()
    
if __name__ == "__main__":
    init_db()
    test_news = [
        {
            "title": "Вышел Python 3.15 с новым ускорителем",
            "link": "https://example.com/python-3-15",
            "published": "Sat, 17 Oct 2026 15:00:00 GMT",
            "summary": "Разработчики представили новую версию языка с улучшенной производительностью."
        }
    ]
    save_news(test_news)
    print("Новость успешно отправлена в БД!")

    # 4. Проверяем, что она там лежит со статусом 'raw'
    raw_item = get_raw_news()
    print("Достали из базы:", raw_item)