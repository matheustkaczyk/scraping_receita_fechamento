from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver as webdriver_seleniumwire
from dotenv import load_dotenv
from datetime import datetime
from pandas import DataFrame
import os
import time
import json

from index import (
    login_index,
    main_index,
    consulting_index,
)

def fetchData(YEAR_TARGET):
    load_dotenv()

    PASSWORD = os.environ.get('PASSWORD')
    CNPJ = os.environ.get('CNPJ_OWN')
    URL = 'https://receita.pr.gov.br/login'

    PARSED_DATE = f"01/01/{YEAR_TARGET} ~ 31/12/{YEAR_TARGET}"

    options = Options()
    options.add_experimental_option("prefs", {
        "download.default_directory": os.getcwd(),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    driver = webdriver_seleniumwire.Chrome(options=options)

    driver.maximize_window()
    driver.get(URL)

    # Login
    login_input = driver.find_element(By.XPATH, login_index['login_xpath'])
    login_password = driver.find_element(By.XPATH, login_index['password_xpath'])
    login_submit = driver.find_element(By.XPATH, login_index['submit_login'])

    login_input.send_keys(CNPJ)
    login_password.send_keys(PASSWORD)
    login_submit.click()

    time.sleep(2)

    # Logado, tela principal
    main_wrapper = driver.find_element(By.XPATH, main_index['nf_wrapper'])
    main_wrapper.click()

    time.sleep(.5)

    main_consulting = driver.find_element(By.XPATH, main_index['nf_consulting'])
    main_consulting.click()

    time.sleep(1)

    # Tela de consulta
    consulting_select = driver.find_element(
        By.XPATH, consulting_index['consulting_select'])
    # consulting_filter_select = driver.find_element(
    #     By.XPATH, consulting_index['consulting_filter_select'])
    consulting_submit = driver.find_element(
        By.XPATH, consulting_index['consulting_submit'])

    consulting_select.click()

    consulting_select_opt = driver.find_element(
        By.XPATH,
        '//*[@id="app"]/div[1]/article/div[2]/div[1]/div[1]/div/select/option[2]'
        )

    # time.sleep(.5)

    consulting_select_opt.click()

    # consulting_filter_select = Select(driver.find_element(
    #     By.XPATH, consulting_index['consulting_filter_select']))
    # consulting_filter_select.select_by_visible_text('Destinatário')

    time.sleep(.5)

    # consulting_target_cnpj_input = driver.find_element(
    #     By.XPATH, consulting_index['consulting_target_cnpj_input'])
    # consulting_target_cnpj_input.send_keys(CNPJ_target)

    consulting_date_input = driver.find_element(
        By.XPATH, consulting_index['consulting_date'])
    consulting_date_input.send_keys(PARSED_DATE)

    time.sleep(.5)

    consulting_submit.click()

    time.sleep(.5)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Captura dos dados
    partial_data = []

    for requests in driver.requests:
        if (requests.url == 'https://nfae.fazenda.pr.gov.br/nfae/api/nfae?acao=LISTAR'):
            partial_data.append(requests.response.body)

    time.sleep(2)

    parsing = json.loads(partial_data[0])
    # final_json = json.dumps(parsing)

    # json_data = json.loads(final_json)

    with open(f'data_{YEAR_TARGET}.json', 'w') as file:
        json.dump(parsing, file)

    driver.quit()

# if __name__ == '__main__':
#     fetchData('2023')