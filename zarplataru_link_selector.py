from lib2to3.pgen2 import driver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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
            driver.implicitly_wait(20)

            link = driver.find_element(By.CSS_SELECTOR, "a.button_3D6Qp.next_d7TPs.btn-group-item_2S3uV.btn_29r4R.medium_Vx2fa.basic_2Qi2P").get_attribute('href')

            actions = ActionChains(driver)
            actions.move_to_element(driver.find_element(By.CSS_SELECTOR, "a.button_3D6Qp.next_d7TPs.btn-group-item_2S3uV.btn_29r4R.medium_Vx2fa.basic_2Qi2P")).click()
            actions.perform()

            html.append(driver.page_source)

            if not driver.find_element(By.CSS_SELECTOR, "a.button_3D6Qp.next_d7TPs.btn-group-item_2S3uV.btn_29r4R.medium_Vx2fa.basic_2Qi2P"):
                raise Exception('Element is not on page')
    except Exception as ex:
        print(f'Error: {ex}')
    driver.quit()

    return html