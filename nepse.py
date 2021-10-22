import configparser
import time

# from datetime import datetime
from typing import Any

import pandas as pd
import schedule
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# parsering configfile
_config = configparser.ConfigParser()

# reading config file
_config.read("app.config")


# add from app.config
banks_str = _config.get("DEFAULT", "banks")
banks = banks_str.split(",")

update = _config.get("TIMER", "update")

data_list = list()


def main():
    for bankid in banks:

        URL = "https://www.nepalstock.com.np/company/detail/" + str(bankid)

        # to hide browser
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome("./chromedriver", options=options)
        html = Any
        time.sleep(15)
        # if bank not exist
        try:
            driver.get(URL)
            html = driver.page_source
        except:
            print("Bank not found. Bank ID: " + str(bankid))
            continue

        time.sleep(15)

        soup = BeautifulSoup(html, "html.parser")
        parsed_table = soup.find_all("table")
        table = any

        if len(parsed_table) > 0:
            table = parsed_table[0]
            rows = table.find_all("tr")
            bankname = soup.find(class_="company__title--details").find("h1").text
            parser(rows=rows, bankname=bankname)

    export(data_list=data_list)
    #         ltp_data = []
    #         index = 0
    #         for tr in rows:
    #             if index == 3:
    #                 ltp_data = [span.text.strip()
    #                             for span in tr.find_all("span")]
    #                 break
    #             index = index + 1

    # # ltp,change price , change %
    #         if len(ltp_data) > 0:
    #             data_list.append(ltp_data)
    #             print(bankid, float(ltp_data[0].replace(",", "")), float(ltp_data[1].replace(
    #                 ",", "")), float(ltp_data[2].replace("(", "").replace(")", "").replace("%", "")))


def parser(rows, bankname):
    ltp_data = []
    index = 0
    ltp_data.append(bankname)
    for tr in rows:
        if index == 3 or index == 0:
            for span in tr.find_all("span"):
                ltp_data.append(span.text.strip())
        else:
            for th in tr.find_all("td"):
                ltp_data.append(th.text.strip())

        index = index + 1

    # ltp,change price , change %
    if len(ltp_data) > 0 and len(ltp_data[0]) > 0:
        data_list.append(ltp_data)


def export(data_list):

    # Create Pandas Dataframe and print it
    df_bs = pd.DataFrame(
        data_list,
        columns=[
            "Bank Name",
            "As of",
            "Instrument Type",
            "Listing Date",
            "Last Traded Price",
            "Change Price",
            "Change Percentage",
            "Total Traded Quantity",
            "Total Trades",
            "Previous Day Close Price",
            "High Price / Low Price",
            "52 Week High / 52 Week Low",
            "Open Price",
            "Close Price*",
            "Total Listed Shares",
            "Total Paid up Value",
            "Market Capitalization",
            "Notes",
        ],
    )
    df_bs.set_index("Bank Name", inplace=True)
    print(df_bs.head())

    # Exporting the data into csv
    # df_bs.to_csv('nepse-' +
    #              datetime.now().strftime("%d-%m-%Y %H-%M-%S") + '.csv')
    df_bs.to_csv("nepse.csv")

    # To auto update
    schedule.every().seconds.do(main)

    while True:
        schedule.run_pending()
        time.sleep(int(update))


if __name__ == "__main__":
    main()
