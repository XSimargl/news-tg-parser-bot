import json
import time
import config
import logging
from google import genai
from google.genai import types


api_gemini = config.API_KEY_GEMINI
models_pool = config.models_pool
client = genai.Client(
    api_key=api_gemini
)
def news_analis(title: str, text: str):
    
    user_pront = f"Заголовок: {title}\n\n Текст новости: {text}"
    
    for model_name in models_pool:
        try:
            logging.info(f"Отправка новости в ИИ, модель: {model_name}")
            response = client.models.generate_content(
                model= model_name,
                contents= user_pront,
                config=types.GenerateContentConfig(
                    system_instruction=(
                    "Ты — главный редактор IT-дайджеста. Твоя задача — отфильтровать статью и написать "
                    "емкое превью для разработчиков.\n\n"
                    "ЦЕЛЕВЫЕ ТЕМЫ (is_positive: true):\n"
                    "Python, SQL, базы данных, Git, Linux, Docker, ИИ, LLM, ML, Data Science, "
                    "компьютерное железо, архитектура, Open Source, карьера в IT, поиск работы и собеседования.\n\n"
                    "ЧЕРНЫЙ СПИСОК (is_positive: false):\n"
                    "Реклама курсов, корпоративные пресс-релизы, маркетинг, SEO, воронки продаж, "
                    "снижение цены лида/заявки, социальные инициативы .\n\n"
                    "ПРАВИЛА ДЛЯ ПОЛЯ short_review (строго 5-7 предложения по трехчастной структуре):\n"
                    "1. Суть и контекст (1 предложение): Что именно вышло или какую инженерную проблему решали. "
                    "Напиши так, чтобы суть сразу понял даже тот, кто впервые слышит название проекта или инструмента.\n"
                    "2. Как устроено и главный результат (1–2 предложения): Выдели только 1–2 ключевых технических факта "
                    "или архитектурных решения и поясни, почему это важно или круто. Не перечисляй второстепенные цифры, "
                    "случайные версии пакетов и мелкие метрики — оставь только главное.\n"
                    "3. Итог и практическая польза (1 предложение): Главный вывод автора или что конкретно читатель "
                    "может забрать из статьи в свою практику (готовый код, схему, разбор ошибок).\n\n"
                    "СТИЛЬ:\n"
                    "Категорически запрещены штампы: «В статье рассказывается», «Автор делится», «Статья посвящена», "
                    "«Рассматривается». Пиши сразу по делу, живым инженерным языком.\n\n"
                    "ФОРМАТ ОТВЕТА:\n"
                    "Верни строго валидный JSON без маркдаун-оберток:\n"
                    "{\"is_positive\": true/false, \"short_review\": \"текст превью\"}"
                    ),
                    response_mime_type="application/json",
                    temperature=0.4
                    )
                )
            ai_text = response.text
            return json.loads(ai_text)
            
        except Exception as e:
            logging.warning(f"Модель {model_name} не справилась ({e}), пробуем следующую...")
            time.sleep(2)
    return {"is_positive": None, "short_review": "Ошибка обработки"}