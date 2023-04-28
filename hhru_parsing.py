import hhru_link_selector
from bs4 import BeautifulSoup
import html5lib
import requests
import pandas as pd

URL = 'https://hh.ru/search/vacancy?area=1&professional_role=156&professional_role=160&professional_role=10&professional_role=12&professional_role=150&professional_role=25&professional_role=165&professional_role=34&professional_role=36&professional_role=73&professional_role=155&professional_role=96&professional_role=164&professional_role=104&professional_role=157&professional_role=107&professional_role=112&professional_role=113&professional_role=148&professional_role=114&professional_role=116&professional_role=121&professional_role=124&professional_role=125&professional_role=126&useTopFilterCatalog=true&page=0&disableBrowserCache=true'
html_docs = hhru_link_selector.parse(start_link=URL)

session = requests.session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.5.715 Yowser/2.5 Safari/537.36',
    'Accept-Language': 'ru,en;q=0.9'
}

links = []
for doc in html_docs:
    soup = BeautifulSoup(doc, 'html5lib')
    a_tags = soup.select('a.serp-item__title')
    for tag in a_tags:
        links.append(tag.get('href'))

vacancy_info = []
for link in links:

    try:
        request = session.get(link)
        html = request.text    

        soup = BeautifulSoup(html, 'html5lib')

        info = {
            'link': link,
            'name': soup.select('h1.bloko-header-section-1')[0].text,
            'salary': soup.select('span.bloko-header-section-2.bloko-header-section-2_lite')[0].text,
            'expirience': soup.select('p.vacancy-description-list-item')[0].text,
            'conditions': soup.select('p.vacancy-description-list-item')[1].text,
            'skills': soup.select('div.bloko-tag-list')[0].getText(separator=u',') 
                    if len(soup.select('div.bloko-tag-list')) > 0  
                    else None,
        }
        vacancy_info.append(info)
    except Exception as ex:
        print(ex)

vacancy_info = pd.DataFrame.from_dict(vacancy_info)
vacancy_info.to_csv('hhru_vacancy.csv')