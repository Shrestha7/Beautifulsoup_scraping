from typing import Any, cast
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import pandas as pd
import configparser

# parsering configfile
_config = configparser.ConfigParser()

#reading config file
_config.read('app.config')


#add from app.config
banks_str = _config.get("DEFAULT",'banks')
banks = banks_str.split(",")

data_list = list()
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

# ltp,change price , change %
        if len(ltp_data) > 0:
            data_list.append(ltp_data)
            print(bankid,float(ltp_data[0].replace(",","")), float(ltp_data[1].replace(",","")), float(ltp_data[2].replace("(","").replace(")","").replace("%","")))
            

# Create Pandas Dataframe and print it
df_bs = pd.DataFrame(data_list,columns=['Last Traded Price', 'Change Price', 'Change Percentage'])
df_bs.set_index('Last Traded Price',inplace=True)
print(df_bs.head())

# Exporting the data into csv
df_bs.to_csv('beautifulsoup.csv')