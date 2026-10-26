from dotenv import load_dotenv
import os

load_dotenv()
models_pool = [
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-3.1-flash-lite",
    "gemini-3-flash",
    "gemini-2.5-flash"
]
url_news = [
    # --- ИИ-лаборатории и техногиганты ---
    "https://openai.com/news/rss.xml",
    "https://blog.google/innovation-and-ai/technology/ai/rss/",
    "https://deepmind.google/blog/rss.xml",
    "https://huggingface.co/blog/feed.xml",
    "https://bair.berkeley.edu/blog/feed.xml",

    # --- Хардкорная разработка, холивары языков и архитектура (Добавлено) ---
    "https://hnrss.org/best",                     # Hacker News (только лучшие посты сообщества)
    "https://lobste.rs/rss",                      # Lobsters — статьи про Rust, C++, Linux и архитектуру без воды
    "https://blog.cloudflare.com/rss/",           # Инженерный блог Cloudflare (эталонные разборы сбоев и сетей)
    "https://feeds.arstechnica.com/arstechnica/index", # Ars Technica — глубокие разборы железа, науки и IT

    # --- Разработка и IT (Россия + Мир) ---
    "https://habr.com/ru/rss/articles/top/",       
    
    
    
    "https://techcrunch.com/category/artificial-intelligence/feed/",

    # --- Мировая повестка (Global News) ---
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.theguardian.com/world/rss",
    "https://feeds.content.dowjones.io/public/rss/RSSWorldNews",
]
API_KEY_TG = os.getenv("API_KEY_TG")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
DB_PATH = os.getenv("DB_PATH", "database/news.db")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:4b")
API_KEY_GEMINI = os.getenv("API_GEMINI")
if (not API_KEY_TG) or (not ADMIN_CHAT_ID):
    raise ValueError("Нету апи или тг айди")

ADMIN_CHAT_ID = int(ADMIN_CHAT_ID)