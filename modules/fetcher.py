import feedparser
from bs4 import BeautifulSoup
import httpx

def get_rss_news(rss_url: str, limit: int):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = httpx.get(rss_url, headers=headers, timeout=10.0)
        raw_data = feedparser.parse(response.text)
        response.raise_for_status()
    except httpx.HTTPError as e:
       print("Ебать а тут ошибка с парсингм") 
       return []
    news_list = []
    
    if raw_data.entries:
        for item in raw_data.entries[:limit]:
            raw_data_summary = item.get("summary")
            
            if raw_data_summary:
                clean_summary = BeautifulSoup(raw_data_summary, "html.parser").get_text(separator=" ", strip=True)
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
        
if __name__ == "__main__":
    a = get_rss_news("https://habr.com/ru/rss/articles/", 5)
    print(a)