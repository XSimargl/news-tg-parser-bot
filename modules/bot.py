import asyncio
import html
from aiogram import Bot
from aiogram.enums import ParseMode
import config
from database.db import get_approved_news, update_news_status, update_telegram_message_id
from aiogram.client.default import DefaultBotProperties
import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



async def send_aler(token: str = config.API_KEY_TG, id_chat: int = config.ADMIN_CHAT_ID):

    approved_news = get_approved_news()
    if not approved_news:
        logging.info("Нет новых одобренных новостей для отправки.")
        return
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    for news in approved_news:
        kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="👍", callback_data=f"rate:like:{news['id']}"),
            InlineKeyboardButton(text="👎", callback_data=f"rate:dislike:{news['id']}")
        ]])
        title = html.escape(news["title_ru"])
        link = news["link"]
        ai_summary = html.escape(news["ai_summary"])

        message_text = f"<b>{title}</b>\n\n<i>{ai_summary}</i>\n\n<a href='{link}'>Читать оригинал</a>"
        
        try:
            sent_messang = await bot.send_message(chat_id=id_chat, text=message_text, reply_markup=kb)
            logging.info(f"Отпрлено {news['title']}")
            
           
            update_telegram_message_id(news_id=news['id'], message_id=sent_messang.message_id, status="sent")
            
            await asyncio.sleep(1)
        except Exception as e:
            logging.error(f"Ошибка при отправке новости {news['id']}: {e}")
        
    await bot.session.close()
    
if __name__ == "__main__":
    asyncio.run(send_aler())