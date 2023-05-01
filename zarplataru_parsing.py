import zarplataru_link_selector
from bs4 import BeautifulSoup
import pandas as pd
from lib2to3.pgen2 import driver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = 'https://russia.zarplata.ru/vacancy/razrabotchik'
html_docs = zarplataru_link_selector.parse(start_link=URL)

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

links = []
for doc in html_docs:
    soup = BeautifulSoup(doc, 'html5lib')
    a_tags = soup.select('a.vacancy-title.vacancy-title_23EUM')
    for tag in a_tags:
        links.append('https://russia.zarplata.ru' + tag.get('href'))

vacancy_info = []
for link in links:

    try:
        driver.get(link)
        driver.implicitly_wait(20)
        WebDriverWait(driver, timeout=15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ui.button.button__q_qh")))

        html = driver.page_source
        soup = BeautifulSoup(html, 'html5lib')

        info = {
            'link': link,
            'name': soup.select('h1.ui.header.medium.header_2ehhw')[0].text,
            'salary': soup.select('div.salary_7tPJD')[0].text,
            'expirience': soup.select('div.descriptions_wVg5R')[0].text.split(',')[1],
            'conditions': soup.select('div.descriptions_wVg5R')[0].text.split(',')[0] + ',' + soup.select('div.descriptions_wVg5R')[0].text.split(',')[2],
            'skills': soup.select('div.info_393bj')[0].text if len(soup.select('div.info_393bj')) != 0 else None 
        }
        vacancy_info.append(info)
    except Exception as ex:
        print(ex)

vacancy_info = pd.DataFrame.from_dict(vacancy_info)
vacancy_info.to_csv('zarplataru_vacancy.csv')
