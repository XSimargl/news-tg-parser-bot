import json
import httpx
import config

url_ollama = config.OLLAMA_URL
model_ollama = config.OLLAMA_MODEL

def news_analis(title: str, text: str):
    user_pront = f"Заголовок: {title}\n\n Текст новости: {text}"
    payload = {
    "model": model_ollama,
    "system": (
        "Ты строгий оценщик IT-новостей. Целевые темы: Python, SQL, БД, Git, Linux, Docker, ИИ, "
        "локальные LLM, ML, DS, компьютерное железо, Open Source, карьера и поиск работы. "
        "Категорически отклоняй (is_positive: false): маркетинг, SEO, контекстную рекламу, воронки продаж, лиды и конверсии, корпоративный PR и социальные инициативы. "
        "Если новость подходит, напиши short_review (4-6 предложений) по трем строгим правилам: "
        "1. КАТЕГОРИЧЕСКИ ЗАПРЕЩЕН канцелярит («В статье рассказывается», «Автор делится», «Статья анализирует»). Пиши сразу по сути, живо и с легкой инженерной иронией. "
        "2. Требуется фактура: обязательно вытаскивай конкретные названия технологий, стек, метрики производительности, цифры ускорения или размер кодовой базы. "
        "3. Последним предложением обязательно напиши, что лежит по ссылке, начиная со слова «Внутри: » (например: «Внутри: готовый скрипт миграции, схема БД и разбор граблей с памятью»). "
        "Верни строго JSON: {\"is_positive\": true/false, \"short_review\": \"текст отзыва\"}."
    ),
    "prompt": user_pront,
    "stream": False,
    "format": "json",
    "options": {"num_ctx": 8192, "temperature": 0.2}
}
    try:
        resp = httpx.post(url_ollama, json=payload, timeout=300.0)
        resp.raise_for_status()
        
        ai_text = resp.json()["response"]
        
        return json.loads(ai_text)
    except Exception as e:
        print(f"Ошибка при обращении к нейросети: {e}")
       
        return {"is_positive": None, "short_review": "Ошибка обработки"}