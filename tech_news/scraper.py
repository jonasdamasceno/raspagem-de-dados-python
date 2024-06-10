import requests
import time
from parsel import Selector

from tech_news.database import create_news


# Requisito 1
def fetch(url, timeout=10):
    headers = {"User-Agent": "Fake user-agent"}
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except (
        requests.RequestException
    ) as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        time.sleep(1)


# Requisito 2
def scrape_updates(html_content):
    if not html_content:
        return []

    try:
        selector = Selector(text=html_content)
        links = selector.css(".cs-overlay-link::attr(href)").extract()
        return links
    except Exception as e:
        print(f"An error occurred while scraping updates: {e}")
        return []


# Requisito 3
def scrape_next_page_link(html_content):
    try:
        data = Selector(text=html_content)
        return data.css(".next::attr(href)").get()
    except ValueError:
        return None


# Requisito 4
def scrape_news(html_content):
    data = Selector(text=html_content)

    return {
        "url": data.css('link[rel="canonical"]::attr(href)').get(),
        "title": data.css("h1.entry-title::text").get().strip(),
        "timestamp": data.css(".meta-date::text").get(),
        "writer": data.css(".author a::text").get(),
        "reading_time": int(
            data.css(".meta-reading-time::text").get().split()[0]
        ),
        "summary": "".join(data.xpath("(//p)[1]//text()").getall()).strip(),
        "category": data.css(".category-style .label::text").get(),
    }


# Requisito 5
def get_tech_news(amount):
    base_url = "https://blog.betrybe.com"
    news_list = []

    while len(news_list) < amount:
        request = fetch(base_url)
        urls = scrape_updates(request)

        for url in urls:
            data = fetch(url)
            news_list.append(scrape_news(data))

            if len(news_list) >= amount:
                break

        base_url = scrape_next_page_link(request)

        if base_url is None:
            break

    create_news(news_list)
    return news_list
