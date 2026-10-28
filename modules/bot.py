import asyncio
import html
from aiogram import Bot,  Dispatcher, Router, F
from aiogram.enums import ParseMode
import config
from database.db import get_approved_news, update_news_status, update_telegram_message_id, update_news_grade
from aiogram.client.default import DefaultBotProperties
import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

router = Router() 

@router.callback_query(F.data.startswith("rate:"))
async def heandle_vate(callback: CallbackQuery):
    parts = callback.data.split(":")
    vote_type = parts[1]
    news_id = int(parts[2])
    
    if vote_type =="like":
        update_news_grade(grade=1, news_id=news_id)
        btn_text = "✅ Ты оценил: 👍"
    else:
        update_news_grade(grade=-1, news_id=news_id)
        btn_text = "✅ Ты оценил: 👎"
    new_kb = InlineKeyboardMarkup(inline_keyboard=[[
                
                InlineKeyboardButton(text=btn_text, callback_data="ignore")
            ]])
    await callback.message.edit_reply_markup(reply_markup=new_kb)
    await callback.answer(f"Голос {vote_type} учтен!")
        


async def send_aler(bot: Bot, token: str = config.API_KEY_TG, id_chat: int = config.ADMIN_CHAT_ID):

    approved_news = get_approved_news()
    if not approved_news:
        logging.info("Нет новых одобренных новостей для отправки.")
        return
    
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
        
    
    
