import asyncio
import html
from aiogram import Bot
from aiogram.enums import ParseMode
import config
from database.db import get_approved_news, update_news_status
from aiogram.client.default import DefaultBotProperties

async def send_aler(token: str = config.API_KEY_TG, id_chat: int = config.ADMIN_CHAT_ID):
    approved_news = get_approved_news()
    if not approved_news:
        print("Нет новых одобренных новостей для отправки.")
        return
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    for news in approved_news:
        
        title = html.escape(news["title"])
        link = news["link"]
        ai_summary = html.escape(news["ai_summary"])

        message_text = f"<b>{title}</b>\n\n<i>{ai_summary}</i>\n\n<a href='{link}'>Читать оригинал</a>"
        
        try:
            await bot.send_message(chat_id=id_chat, text=message_text)
            print(f"Отпрлено {news['title']}")
            
            update_news_status(news_id=news["id"], status="sent")
            
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Ошибка при отправке новости {news['id']}: {e}")
        
    await bot.session.close()
    
if __name__ == "__main__":
    asyncio.run(send_aler())