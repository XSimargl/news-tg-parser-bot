from dotenv import load_dotenv
import os

load_dotenv()
models_pool = [
    
    "gemini-3.5-flash",
    
    "gemini-3.0-flash",
    "gemini-2.5-flash",
    
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash"
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