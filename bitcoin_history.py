# coding: utf-8

import requests
from bs4 import BeautifulSoup

response = requests.get('https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20170626&end=20180626')
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table', {'class': 'historical-data'})
data = []

for tr in table.find_all('tr'):
    tds = list(tr.find_all('td'))

    for tr in table.find_all('tr'):
        tds = list(tr.find_all('td'))
        if len(tds) == 0:
            continue
        date = tds[0].text
        open_price = tds[1].text
        high_price = tds[2].text
        low_price = tds[3].text
        close_price = tds[4].text
        data.append([date, open_price, high_price, low_price, close_price])

