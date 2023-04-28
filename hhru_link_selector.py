from lib2to3.pgen2 import driver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--ignore-certificate-errors')

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

def parse(start_link):

    link = start_link

    html = []
    try:
        while True:
            driver.get(link)
            driver.implicitly_wait(2)

            link = driver.find_element(By.LINK_TEXT, "дальше").get_attribute('href')

            actions = ActionChains(driver)
            actions.move_to_element(driver.find_element(By.LINK_TEXT, "дальше")).click()
            actions.perform()

            html.append(driver.page_source)

            if not driver.find_element(By.LINK_TEXT, "дальше"):
                raise Exception('Element is not on page')

    except Exception as ex:
        print(f'Error: {ex}')
    driver.quit()

    return html
