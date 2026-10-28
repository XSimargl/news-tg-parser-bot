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
  "https://habr.com/ru/rss/articles/?fl=ru",
  "https://habr.com/ru/rss/news/?fl=ru",
  "https://www.linux.org.ru/section-rss.jsp?section=1",
  "https://feed.infoq.com/",
  "https://thenewstack.io/feed/",
  "https://lwn.net/headlines/rss",
  "https://news.ycombinator.com/rss",
  "https://martinfowler.com/feed.atom",
  "https://github.blog/feed/",
  "https://github.blog/changelog/feed/",
  "https://blog.cloudflare.com/rss/",
  "https://kubernetes.io/feed.xml",
  "https://www.docker.com/feed/",
  "https://blog.python.org/rss.xml",
  "https://blog.rust-lang.org/feed.xml",
  "https://go.dev/blog/feed.atom",
  "https://www.postgresql.org/news.rss",
  "https://huggingface.co/blog/feed.xml",
  "https://pytorch.org/blog/feed/",
  "https://research.google/blog/rss/",
  "https://3dnews.ru/news/rss/",
  "https://3dnews.ru/cpu/rss/",
  "https://www.ixbt.com/export/news/rss.xml",
  "https://www.ixbt.com/export/articles/rss.xml",
  "https://overclockers.ru/rss/news.rss",
  "https://servernews.ru/news/rss/",
  "https://www.tomshardware.com/feeds.xml",
  "https://www.techpowerup.com/rss/news",
  "https://www.techpowerup.com/rss/reviews",
  "https://www.techspot.com/backend.xml",
  "https://www.techspot.com/reviews.xml",
  "https://www.phoronix.com/rss.php",
  
  "https://www.servethehome.com/feed/",
  "https://chipsandcheese.com/feed",
  "https://www.storagereview.com/feed",
  "https://www.gsmarena.com/rss-news-reviews.php3",
  "https://www.androidauthority.com/feed",
  "https://videocardz.com/feed",
  "https://feeds.arstechnica.com/arstechnica/index",
  "https://www.theregister.com/headlines.atom",
  "https://techcrunch.com/feed/",
  "https://www.wired.com/feed/rss",
  "https://www.technologyreview.com/feed/",
  "https://spectrum.ieee.org/feeds/feed.rss",
  "https://www.bleepingcomputer.com/feed/",
  "https://krebsonsecurity.com/feed/",
  "https://www.schneier.com/feed/atom/",
  "https://feeds.feedburner.com/TheHackersNews",
  "https://www.securitylab.ru/_services/export/rss/",
  "https://www.cnews.ru/inc/rss/news.xml",
  "https://xakep.ru/feed/",
  
  
  "https://feeds.bbci.co.uk/news/world/rss.xml",
  "https://feeds.bbci.co.uk/news/business/rss.xml",
  "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
  "https://rss.dw.com/xml/rss-ru-all",
  "https://rss.dw.com/xml/rss-en-all",
  "https://www.france24.com/en/rss",
  "https://feeds.npr.org/1004/rss.xml",
  "https://www.interfax.ru/rss",
  "https://rssexport.rbc.ru/rbcnews/news/30/full.rss",
  "https://www.kommersant.ru/rss/news.xml",
  "https://www.nature.com/nature.rss",
  "https://www.sciencenews.org/feed",
  "https://nplus1.ru/rss"
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