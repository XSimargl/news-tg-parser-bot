from database.db import init_db, save_news, get_approved_news, update_news_status, clean_old_news, get_raw_news_all, update_bouncer_score, get_selected_news
from modules.fetcher import get_rss_news, get_article_text
from modules.processor import news_analis, bouncer_bad_news
from modules.bot import send_aler, router
import config
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
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


async def main():
    token = config.API_KEY_TG
    
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    asyncio.create_task(parser_worker(bot))
    await dp.start_polling(bot)



async def parser_worker(bot: Bot):
    init_db()
    while True:
        try:
            #Собераем данные с парсера
            for feed_url in config.url_news:
                logging.info(f"Проверяем RSS: {feed_url}")
                news_list = await asyncio.to_thread(get_rss_news(feed_url, limit=3))
                if news_list: 
                    save_news(news_list)
            
            #Оценивает сырые новости
            raw_news = get_raw_news_all()
            if raw_news:
                logging.info(f"Вышибала анализирует {len(raw_news)} новостей...")
                ai_result = await asyncio.to_thread(bouncer_bad_news(raw_news))
                # Обновляем оценки и статусы в базе
                for item in ai_result:
                    news_id = item["id"]
                    score = item["score"]
                    
                    if score >= 8:
                        update_bouncer_score(news_id=news_id, status="selected", score=score)
                    else:
                        update_bouncer_score(news_id, status="rejected", score=score)
            #глубоко анализирует отобранные новости
            while True:
                news = get_selected_news()
                
                if not news:
                    logging.info("Все новости оброботоны")
                    break
                
                logging.info(f"Обрабатываем новость: {news['title']}")
                full_text = await asyncio.to_thread(get_article_text(news["link"]))
                rss_summary = news.get("summary", "")
                
                if full_text and len(full_text) >= 300:
                    text_to_analyze = full_text
                    logging.info("Успешно скачан полный текст статьи.")
                elif rss_summary and len(rss_summary) >= 80:
                    text_to_analyze = rss_summary
                    logging.info("Полный текст недоступен. Используем запасное описание из RSS.")
                else:    
                    logging.error("Нет текста вообще, помечаем как rejected...")
                    update_news_status(news_id=news["id"], status="rejected", ai_summary="Нет текста", full_text="Нет текста")              
                    continue
                
                
                if text_to_analyze:
                    logging.info("ИИ думает")
                    ai_result = news_analis(news["title"], text_to_analyze)
                    if ai_result["is_positive"] is None:
                        logging.error(f"Остановка конвейера. Причина: {ai_result['short_review']}")
                        break
                    new_status = "approved" if ai_result["is_positive"] else "rejected"
                    update_news_status(news_id=news["id"], status=new_status, ai_summary=ai_result["short_review"], full_text=text_to_analyze, title_ru=ai_result["title_ru"])
                    logging.info(f"Ответ от ИИ: {ai_result['short_review']}") 
                    logging.info(f"Новость успешно обновлена в БД со статусом '{new_status}'!")
                    await asyncio.sleep(3)
                    
                
            await send_aler(bot)
            deleted = clean_old_news(keep_limit=500)
            if deleted > 0:
                logging.info(f"Очистка БД: удалено {deleted} старых записей.")
        except Exception as err:
            logging.error(f"Сбой в главном цикле: {err}")
            
        logging.info("Уходим в спячку на 1 час...")
        await asyncio.sleep(3600)
    

if __name__ == "__main__":
    asyncio.run(main())