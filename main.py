from database.db import init_db, save_news, get_raw_news, update_news_status
from modules.fetcher import get_rss_news, get_article_text
from modules.processor import news_analis
from modules.bot import send_aler
import config
import json
import asyncio


def main():
    init_db()
    news_list = get_rss_news("https://habr.com/ru/rss/articles/", limit=3)
    save_news(news_list)
    
    
    
        
    while True:
        news = get_raw_news()
        if not news:
            print("Все новости оброботоны")
            break
        print(f"Обрабатываем новость: {news['title']}")
        full_text = get_article_text(news["link"])
        news["summary"] = full_text
        if full_text:
            print("ИИ думает")
            ai_result = news_analis(news["title"], news["summary"])
            if ai_result["is_positive"]:
                new_status = "approved"
            else:
                new_status = "rejected"
            update_news_status(news_id=news["id"], status=new_status, ai_summary=ai_result["short_review"])
            print(f"Ответ от ИИ: {ai_result["short_review"]}")
            print(f"Новость успешно обновлена в БД со статусом '{new_status}'!")
            
        else:
            print("Текст не найден, помечаем как rejected...\n")
            update_news_status(
                news_id=news["id"], 
                status="rejected", 
                ai_summary="Ошибка скачивания текста"
            )
    asyncio.run(send_aler())
    

if __name__ == "__main__":
    main()