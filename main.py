from database.db import init_db, save_news, get_raw_news, update_news_status, clean_old_news
from modules.fetcher import get_rss_news, get_article_text
from modules.processor import news_analis
from modules.bot import send_aler
import config
import json
import asyncio
import logging
import time
from logging.handlers import RotatingFileHandler
file_handler = RotatingFileHandler(
    "service.log", 
    maxBytes=5 * 1024 * 1024, 
    backupCount=1, 
    encoding="utf-8"
)
stream_handler = logging.StreamHandler()
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(message)s", 
    handlers=[file_handler, stream_handler]
)
def main():
    init_db()
    while True:
        try:
            logging.info("Идем на Хабр за свежими новостями...")
            news_list = get_rss_news("https://habr.com/ru/rss/articles/", limit=3)
            save_news(news_list)
            
        
        
            
            while True:
                news = get_raw_news()
                if not news:
                    logging.info("Все новости оброботоны")
                    break
                logging.info(f"Обрабатываем новость: {news['title']}")
                full_text = get_article_text(news["link"])
                news["summary"] = full_text
                if full_text:
                    logging.info("ИИ думает")
                    ai_result = news_analis(news["title"], news["summary"])
                    if ai_result["is_positive"] is None:
                        logging.error(f"Остановка конвейера. Причина: {ai_result['short_review']}")
                        break
                    new_status = "approved" if ai_result["is_positive"] else "rejected"
                    update_news_status(news_id=news["id"], status=new_status, ai_summary=ai_result["short_review"])
                    logging.info(f"Ответ от ИИ: {ai_result["short_review"]}")
                    logging.info(f"Новость успешно обновлена в БД со статусом '{new_status}'!")
                    
                else:
                    logging.error("Текст не найден, помечаем как rejected...\n")
                    update_news_status(
                        news_id=news["id"], 
                        status="rejected", 
                        ai_summary="Ошибка скачивания текста"
                    )
            asyncio.run(send_aler())
            deleted = clean_old_news(keep_limit=500)
            if deleted > 0:
                logging.info(f"Очистка БД: удалено {deleted} старых записей.")
        except Exception as err:
            logging.error(f"Сбой в главном цикле: {err}")
            
        logging.info("Уходим в спячку на 1 час...")
        time.sleep(3600)
    

if __name__ == "__main__":
    main()