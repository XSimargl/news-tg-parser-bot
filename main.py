from database.db import init_db, save_news, get_raw_news, update_news_status
from modules.fetcher import get_rss_news, get_article_text
import config




def main():
    init_db()
    news_list = get_rss_news("https://habr.com/ru/rss/articles/", limit=3)
    save_news(news_list)
    news = get_raw_news()
    print(news)
    

if __name__ == "__main__":
    main()