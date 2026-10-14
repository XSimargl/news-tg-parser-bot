import feedparser


def get_rss_news(rss_url: str):
    count = 0
    raw_data = feedparser.parse(rss_url)
    news_list = []
    if raw_data.bozo == 0:
        for item in raw_data.entries[:5]:
            news_data  = {
                "title": item.title,
                "link": item.link,
                "published": item.published
            }
            news_list.append(news_data)
            count +=1
            if count == 5:
                break
    else:
        print("Ошибка в парсенге")
    return news_list
        
if __name__ == "__main__":
    a = get_rss_news("https://habr.com/ru/rss/404")
    print(a)