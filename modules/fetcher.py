import feedparser
from bs4 import BeautifulSoup
import httpx
import logging
import trafilatura

def get_rss_news(rss_url: str, limit: int):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = httpx.get(rss_url, headers=headers, timeout=10.0)
        response.raise_for_status()
        raw_data = feedparser.parse(response.text)
        
    except httpx.HTTPError as e:
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
            
            
            if raw_html:
                clean_summary = BeautifulSoup(raw_html, "html.parser").get_text(separator=" ", strip=True)
            else:
                clean_summary = ""
            news_data  = {

                "title": item.get("title"),

                "link": item.get("link"),

                "published": item.get("published"),
                "summary": clean_summary
            }
            
            news_list.append(news_data)  
    return news_list

def get_article_text(url: str) -> str:
    downlodr = trafilatura.fetch_url(url)
    
    if not downlodr:
        logging.error(f"Не удолось скачать статью: {url}")
        return ""
    
    text = trafilatura.extract(
        downlodr,
        include_comments=False,
        include_tables=True,
        output_format="markdown"
    )
    if text:
        return text
    return ""
        
if __name__ == "__main__":
    a = get_rss_news("https://habr.com/ru/rss/articles/", 5)
    print(a)