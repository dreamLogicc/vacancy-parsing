import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://gb.ru/courses/it'


session = requests.session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.5.715 Yowser/2.5 Safari/537.36',
    'Accept-Language': 'ru,en;q=0.9'
}

request = session.get(url)
html = request.text

soup = BeautifulSoup(html, 'html5lib')

cards = soup.select('a.card_full_link')

courses = []
for card in cards:
    try:
        request = session.get(card.get('href'), timeout=3)
        html = request.text
        soup = BeautifulSoup(html, 'html.parser')

        print(soup.select('h1.gkb-promo__title.ui-text-heading--2.ui-text--bold')[0].text)
        print(soup.select('div.gkb-promo__tag-wrapper.promo-tech__wrapper')[0].text)
        courses.append({
            'name': soup.select('h1.gkb-promo__title.ui-text-heading--2.ui-text--bold')[0].text,
            'skills': soup.select('div.gkb-promo__tag-wrapper.promo-tech__wrapper')[0].text
        })
    except Exception as ex:
        print(ex)

courses = pd.DataFrame.from_dict(courses)
courses.to_csv('geekbrains_courses.csv', index=False)

