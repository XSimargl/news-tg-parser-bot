import json
import time
import config
import logging
from google import genai
from google.genai import types


api_gemini = config.API_KEY_GEMINI
models_pool = config.models_pool
client = genai.Client(
    api_key=api_gemini, http_options=types.HttpOptions(timeout=60000)
)

def bouncer_bad_news(news_list: list[dict]):
    batch_for_ai = [{"id": item["id"], "title": item["title"], "summary": item["summary"][:1000]} for item in news_list]
    
    text_for_ai = json.dumps(batch_for_ai, ensure_ascii=False, indent=2)
    models_pool = [
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash",
    
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    
    "gemini-3-flash",
    "gemini-2.5-flash"
]
    BOUNCER_INSTRUCTION = (
    "Ты — суровый Senior Tech Lead и главный редактор закрытого инженерного канала. "
    "На вход ты получишь пачку свежих новостей (их ID, заголовки и краткие описания). "
    "Твоя задача — отсеять информационный мусор и оценить техническую ценность каждой статьи "
    "по шкале от 1 до 10.\n\n"
    "КРИТЕРИИ ВЫСОКОЙ ОЦЕНКИ (8-10 баллов - 'Алмазы'):\n"
    "- Post-mortems (разбор факапов, 'как мы уронили прод и как чинили').\n"
    "- Глубокая архитектура высоконагруженных систем, баз данных и сетей.\n"
    "- Реверс-инжиниринг, хардкорная оптимизация, работа с памятью и железом.\n"
    "- Обоснованные холивары языков (Rust, C++, Python, Go, etc) с техническими аргументами.\n"
    "- Важные для жизни новости, что происходит в реальном мире.\n"
    "- Разбор уязвимостей (CVE) с деталями эксплуатации.\n\n"
    "КРИТЕРИИ МУСОРА (1-4 балла - Сразу на свалку):\n"
    "- 'Топ 10 плагинов...', 'Как установить Git' и прочие джуновские туториалы.\n"
    "- Реклама курсов, школ программирования, вебинаров.\n"
    "- Корпоративные пресс-релизы, меморандумы о партнерствах без технической сути.\n"
    "- Рассуждения об успешном успехе, выгорании и 'как войти в IT'.\n\n"
    "ПРАВИЛО ДУБЛИКАТОВ (КРИТИЧЕСКИ ВАЖНО):\n"
    "Среди новостей могут быть дубликаты (разные сайты написали об одном и том же). "
    "Твоя задача — заметить это! Выбери только ОДИН самый лучший первоисточник и поставь ему "
    "заслуженный балл, а всем остальным копиям этого же события ставь 1 балл.\n\n"
    "ФОРМАТ ОТВЕТА:\n"
    "Верни строго валидный JSON-массив без маркдаун-оберток (без ```json). Только сам массив.\n"
    "Пример: [{\"id\": 15, \"score\": 9}, {\"id\": 16, \"score\": 2}]"
)
    for model_name in models_pool:
        try:
            
            logging.info("Отправлены новости в ИИ вышибалу")
            response = client.models.generate_content(
                model=model_name,
                contents=text_for_ai,
                config=types.GenerateContentConfig(
                    system_instruction=BOUNCER_INSTRUCTION,
                    response_mime_type="application/json",
                    temperature=0.2
                )
                
            )
            ai_scores = json.loads(response.text)
            return ai_scores
        except Exception as e:
            logging.error(f"Произошла ошибка: {e}")
    return ""
    
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
                "Ты — главный редактор дайджеста для любознательного разработчика. "
                "Твоя задача — отсеять информационный мусор и сделать сочную выжимку из интересных материалов.\n\n"
                "ЧТО ПРОПУСКАТЬ (is_positive: true):\n"
                "Мы не ограничиваемся одним языком программирования. Пропускай любые сильные материалы: "
                "разборы на C++, Rust, Python, Go, споры об архитектуре ('почему технология X устарела'), "
                "истории падения серверов, ИИ, железо, научные прорывы, а также важные мировые и технологические новости.\n\n"
                "ЖЕСТКИЙ ЧЕРНЫЙ СПИСОК (is_positive: false):\n"
                "Малейший намек на эти темы — сразу отклоняй (false):\n"
                "- Реклама курсов, вебинаров, буткемпов и школ программирования;\n"
                "- Корпоративные пресс-релизы, пиар брендов, отчеты о мероприятиях и социальные инициативы;\n"
                "- Маркетинг, SEO, воронки продаж, арбитраж трафика, снижение цены лида;\n"
                "- Поверхностные статьи-пустышки ('Топ-5 библиотек для новичка', 'Как установить Git'), "
                "банальные советы про успешный успех и выгорание.\n\n"
                "ЯЗЫК И ПЕРЕВОД:\n"
                "Если оригинал на английском языке, переведи смысл и напиши итоговое резюме "
                "исключительно на грамотном русском языке.\n\n"
                "ПРАВИЛА ДЛЯ ПОЛЯ short_review (строго 3 коротких абзаца для Telegram):\n"
                "Обязательно разделяй 3 смысловых части переносами строк (\\n\\n). "
                "Каждый абзац должен начинаться с буллита (•), чтобы пост читался легко за 3 секунды.\n"
                "• Суть и контекст (1-2 предложения): О чем речь, какая проблема решается или что произошло.\n"
                "• Главные детали (2-3 предложения): Ключевые технические факты, аргументы автора (например, почему "
                "один язык оказался быстрее другого) или суть события. Без воды и мелких версий пакетов.\n"
                "• Вывод (1-2 предложение): Главный итог, практическая польза или к чему это приведет.\n\n"
                "СТИЛЬ (КРИТИЧЕСКИ ВАЖНО):\n"
                "Категорически запрещены штампы: «В статье рассказывается», «Автор делится», «Статья посвящена», "
                "«Рассматривается», «материал». Пиши сразу по делу, живым языком.\n\n"
                "ФОРМАТ ОТВЕТА:\n"
                "Верни строго валидный JSON без маркдаун-оберток, корректно экранируя переносы строк (\\n):\n"
                "{\"is_positive\": true/false, \"short_review\": \"• Текст...\\n\\n• Текст...\\n\\n• Текст...\"}"
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

if __name__ == "__main__":
    test_news = [
    {
        "id": 142,
        "title": "How we migrated from Kubernetes back to bare metal and saved $2M",
        "summary": "After 4 years of struggling with K8s cluster maintenance and skyrocketing AWS bills, our infrastructure team decided to migrate back to a fleet of bare metal servers managed by Nomad. Here is a detailed post-mortem with architecture schemes and cost breakdown."
    },
    {
        "id": 143,
        "title": "React 19 RC is finally here: React Compiler in action",
        "summary": "The React team has announced the Release Candidate for React 19. It includes the new React Compiler, which automatically memoizes your code, dropping the need for useMemo and useCallback in most cases."
    },
    {
        "id": 144,
        "title": "Топ-5 платных курсов по Python для новичков (Скидки внутри!)",
        "summary": "Хотите войти в IT, но не знаете с чего начать? Мы собрали для вас лучшие интенсивы и школы программирования, которые обещают трудоустройство за 3 месяца. Переходите по ссылке и забирайте профессию мечты."
    },
    {
        "id": 145,
        "title": "Уязвимость в популярном пакете npm позволяет выполнить произвольный код",
        "summary": "Исследователи безопасности обнаружили критическую RCE-уязвимость (CVE-2026-9876) в библиотеке, которая скачивается более 2 млн раз в неделю. Проблема кроется в отсутствии санитизации инпутов при парсинге JSON. Рекомендуется срочно обновиться."
    },
    {
        "id": 146,
        "title": "Meta releases Llama 5 architecture details: 10x faster inference",
        "summary": "Meta AI engineering team published a new paper detailing the underlying architecture of Llama 5. By utilizing a novel sparse MoE routing algorithm and custom Triton kernels, they achieved a 10x reduction in memory bandwidth bottlenecks."
    }
]
    print(bouncer_bad_news(test_news))
    