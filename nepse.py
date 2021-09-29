from typing import Any, cast
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options

banks = [143,131,132,133,134,135,136,137,138,139,140,141,142,144,145,171,238,255,341,348,357,359,397,517,532,562,605]

for bankid in banks:

    URL = "https://newweb.nepalstock.com/company/detail/" + str(bankid)

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome('./chromedriver', options=options)
    html = Any
    try:
        driver.get(URL)
        html = driver.page_source
    except:
        print("Bank not found. Bank ID: "+ str(bankid))
        continue

    time.sleep(5)

    soup = BeautifulSoup(html,"html.parser")
    parsed_table = soup.find_all('table')
    table = any
    if(len(parsed_table) > 0):
        table = parsed_table[0]
        rows = table.find_all('tr')

        ltp_data = []
        index = 0
        for tr in rows:
            if index == 3:
                ltp_data =  [span.text.strip() for span in tr.find_all("span")]
                break
            index = index + 1

        if len(ltp_data) > 0:
            print(bankid,float(ltp_data[0].replace(",","")), float(ltp_data[1].replace(",","")), float(ltp_data[2].replace("(","").replace(")","").replace("%","")))
            