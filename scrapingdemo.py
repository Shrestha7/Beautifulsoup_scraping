from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import re
import pandas as pd
import pyodbc

ACCESSCODE = "nibl"
USERNAME = "nibl_api_user"
PASSWORD = "Nibl&456789"

LOGIN_URL = "https://www.neabilling.com/userpanel/verifyAdmin.asp"
REPORT_URL = "https://www.neabilling.com/userpanel/report_writer/report_detail.asp"


def main():
    session_requests = requests.session()

    # Create payload
    payload = {
        "branch_code": ACCESSCODE,
        "EName": USERNAME,
        "EPass": PASSWORD,
        "shid": 830,
        "IP_Country_Name": "",
        "enable_IP": "",
        "Login": ""
    }

    # Perform login
    result = session_requests.post(LOGIN_URL,
                                   data=payload,
                                   headers=dict(referer=LOGIN_URL))
    #print(result.text)
    yesterday_date = datetime.today() - timedelta(1)
    yesterday_date = yesterday_date.strftime('%m/%d/%Y')
    # Create payload
    payload = {
        "ctr0": yesterday_date,
        "clmVar0": "@FromDate",
        "ctr1": yesterday_date,
        "clmVar1": "@ToDate",
        "ctr2": "",
        "clmVar2": "@Offcode",
        "ctrLen": 3,
        "report_id": 440,
        "report_name": "BranchWise Paid Report - Partner"
    }
    # Scrape url
    result = session_requests.post(REPORT_URL,
                                   data=payload,
                                   headers=dict(referer=REPORT_URL))

    soup = BeautifulSoup(result.content, "html.parser")
    table = soup.find_all("table", {"class": "sortable"})[0]
    rows = table.find_all("tr")
    row_list = list()
    td_row = list()
    for tr in rows:
        td = tr.find_all('td')
        td_row = []
        for i in td:
            if len(i.find_all('span')) > 0:
                span = i.find("span")["onclick"]
                arr = re.split("-!-", span)
                td_row.append(arr[2].replace("@off_code=",""))
            else:
                td_row.append(i.text.strip())
        row_list.append(td_row)

    del row_list[0]
    del row_list[-1]
    del row_list[-1]

    #Connecting DB
    server = 'IT27' 
    database = 'DotNetCoreDemo' 
    username = 'sa' 
    password = 'D@t@b@$e20!9' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

    #Checking If Data Already Exists of that day
    cursor.execute("Select 1 From NEA_BILL_DATA WHERE PAID_DATE = '"+ row_list[0][0] +"'")
    row = cursor.fetchone()
    if row == None:
        var_string = ', '.join('?' * len(row_list[0]))
        query_string = 'INSERT INTO NEA_BILL_DATA VALUES (%s);' % var_string
        for row in row_list:
            cursor.execute(query_string, row)
        cnxn.commit()
    cnxn.close()

if __name__ == '__main__':
    main()
