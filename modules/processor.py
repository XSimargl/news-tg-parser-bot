import json
import httpx
import config

url_ollama = config.OLLAMA_URL
model_ollama = config.OLLAMA_MODEL

def news_analis(title: str, text: str):
    user_pront = f"Заголовок: {title}\n\n Текст новости: {text}"
    payload = {
    "model": model_ollama,
    "system": "Ты строгий оценщик IT-новостей. Твоя задача — проверить новость. Целевые темы: Python, SQL, базы данных, Git, Linux, Docker, ИИ, локальные LLM, ML, Data Science, компьютерное железо, Open Source, карьера в IT, поиск работы и прохождение собеседований. Категорически отклоняй (is_positive: false): рекламу курсов, корпоративные пресс-релизы и статьи ради выгоды компании. Верни строго JSON: {\"is_positive\": true/false, \"short_review\": \" краткая суть статьи на русском языке (3–4 предложения с главной мыслью, плюсами и выводами)\"}.",
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