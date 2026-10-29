import feedparser
from bs4 import BeautifulSoup
import httpx
import logging
import trafilatura
from curl_cffi import requests
from urllib.parse import urljoin
from curl_cffi.requests.errors import RequestsError
def get_rss_news(rss_url: str, limit: int):
    
   
    try:
        response = requests.get(rss_url, impersonate="chrome",  timeout=10.0)
       
        response.raise_for_status()
        raw_data = feedparser.parse(response.text)
        
    except RequestsError as e:
       logging.error(f"Ошибка с парсингом: {e}") 
       return []
    news_list = []
    
    if raw_data.entries:
        for item in raw_data.entries[:limit]:
            raw_html = ""
            if "content" in item and len(item.content) > 0:
                raw_html = item.content[0].get("value", "")
            if not raw_html:
                raw_html = item.get("summary", "")
            raw_link = item.get("link", "")
            safe_link = urljoin(rss_url, raw_link)
            if raw_html:
                clean_summary = BeautifulSoup(raw_html, "html.parser").get_text(separator=" ", strip=True)
            else:
                clean_summary = ""
            news_data  = {

                "title": item.get("title"),

                "link": safe_link,

                "published": item.get("published"),
                "summary": clean_summary
            }
            
            news_list.append(news_data)  
    return news_list

def get_article_text(url: str) -> str:
    try:
        downlodr = requests.get(url, impersonate="chrome", timeout=15.0)
    
        if (downlodr.status_code == 200) and ("html" in downlodr.headers.get("Content-Type", "").lower()):
            text = trafilatura.extract(
                    downlodr.text,
                    include_comments=False,
                    include_tables=True,
                    output_format="markdown"
                )
            if text:
                return text[:20000]
                
        else:
            logging.error(f"Не удолось скачать статью: {url}")
            return ""
    
    except RequestsError as e:
        logging.error(f"Сетевая ошибка при скачивании статьи {url}: {e}")
        return ""
    return ""
        
if __name__ == "__main__":
    a = get_rss_news("https://habr.com/ru/rss/articles/", 5)
    print(a)