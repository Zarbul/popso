from urllib.parse import urlparse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from src.news.models import News

URL = 'https://seller.ozon.ru/news/'


def parse(browser):
    html = browser.page_source
    bulk_list = list()
    bs_obj = BeautifulSoup(html, 'lxml')

    news_cards = bs_obj.find_all('div', class_='news-card')
    for new in news_cards:
        name = new.find('h3', class_='news-card__title').text.strip()
        print(name)

        link = new.find('a', class_='news-card__link')['href']
        domain = urlparse(URL)
        link = ('{d.scheme}://{d.netloc}'.format(d=domain)) + link
        print(link)
        publish_date = new.find('span', class_='news-card__date').text
        print(publish_date)
        #
        browser.get(link)
        news_card = browser.page_source
        news_card_soup = BeautifulSoup(news_card, 'lxml')
        description = news_card_soup.find('section', class_='new-section').find('p').text.strip()
        print(description)
        try:
            tags = news_card_soup.find('div', class_='page-info__topic-value').text.strip().split(', ')
            tags = [a for a in tags]
            tags.append('#Ozon')
            #
            print(tags)
        except:
            tags = ['#Ozon',]
            print(tags)
        bulk_list.append(News(channel='ozon', name=name, description=description, publish_date=publish_date, tag=tags))
    News.objects.bulk_create(bulk_list)
    browser.quit()


def get_browser():

    try:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        browser_options = webdriver.ChromeOptions()
        browser_options.add_argument('--disable-blink-features=AutomationControlled')
        browser_options.add_argument(f'user-agent={user_agent}')
        browser = webdriver.Chrome(options=browser_options)

        browser.get(URL)
        # timeout in 30 seconds
        el = WebDriverWait(browser, 60).until(
            ec.presence_of_element_located((By.XPATH, "//section[@class='news-list']")))
        return browser
    except:
        return False


def ozon():
    browser = get_browser()
    parse(browser)


if __name__ == "__main__":
    ozon()
