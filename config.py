from dotenv import load_dotenv
import os

load_dotenv()

API_KEY_TG = os.getenv("API_KEY_TG")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
DB_PATH = os.getenv("DB_PATH", "database/news.db")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:4b")

if (not API_KEY_TG) or (not ADMIN_CHAT_ID):
    raise ValueError("Нету апи или тг айди")

ADMIN_CHAT_ID = int(ADMIN_CHAT_ID)