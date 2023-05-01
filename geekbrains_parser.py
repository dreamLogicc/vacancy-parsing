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

cards = soup.select('div.direction-card.ui-col-md-6.ui-col-xxxl-6')

courses = []
for card in cards:
    information = {
        'name': card.select('div.direction-card__title')[0].text,
        'skills': card.select('div.direction-card__tags')[0].getText(separator=u',')
    }
    courses.append(information)

courses = pd.DataFrame.from_dict(courses)
courses.to_csv('geekbrains_courses.csv', index=False)

