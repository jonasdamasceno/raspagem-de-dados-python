import requests
import time
from parsel import Selector


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
    """Seu código deve vir aqui"""
    raise NotImplementedError


# Requisito 4
def scrape_news(html_content):
    """Seu código deve vir aqui"""
    raise NotImplementedError


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
    raise NotImplementedError
