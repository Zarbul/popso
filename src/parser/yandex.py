from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from src.news.models import News

URL = 'https://market.yandex.ru/partners/news'


def get_pade(url):
    session = requests.Session()
    useragent = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Version/13.0.2 Safari/605.1.15',
        'Accept-Language': 'ru',
    }

    request = session.get(url, headers=useragent)
    html = request.text
    return html


def get_news_list(html):
    soup = BeautifulSoup(html, 'lxml')
    news_cards = soup.find_all('div', class_='news-list__item')
    return news_cards


def get_news_data(news_list):
    bulk_list = list()
    for new in news_list[:10]:
        name = new.find('div', class_='news-list__item-header').text

        link = new.find('a', class_='news-list__item-active')['href']
        domain = urlparse(URL)
        link = ('{d.scheme}://{d.netloc}'.format(d=domain)) + link

        news_card = get_pade(link)
        news_card_soup = BeautifulSoup(news_card, 'lxml')
        description = news_card_soup.find('div', class_='news-info__post-body').find('p').text
        publish_date = news_card_soup.find('time', class_='news-info__published-date').text
        tags = news_card_soup.find('div', class_='news-info__tags').find_all('a')
        tags = [a.text for a in tags]
        tags.append('#Yandex')
        bulk_list.append(News(channel='yandex', name=name, description=description, publish_date=publish_date, tag=tags))
    News.objects.bulk_create(bulk_list)


def yandex():
    html = get_pade(URL)
    news_list = get_news_list(html)
    get_news_data(news_list)


if __name__ == "__main__":
    yandex()
