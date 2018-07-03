# coding: utf-8

import datetime
import requests
from bs4 import BeautifulSoup
import db
import sqlite3
import json

response = requests.get('https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20170626&end=20180626')
soup = BeautifulSoup(response.content, 'html.parser')
wrap = soup.find('div', {'id': 'historical-data'})
table = wrap.find('table')

data = table.text
print(data)
jsonD = json.dumps(datgi
jsonL = json.loads(jsonD)
#data = []

for tr in table.find_all('tr'):
    tds = list(tr.find_all('td'))
    if len(tds) == 0:
        continue
    date = tds[0].text
    open_price = tds[1].text
    high_price = tds[2].text
    low_price = tds[3].text
    close_price = tds[4].text
    db.add(date, open_price, high_price, low_price, close_price)

db.commit()
