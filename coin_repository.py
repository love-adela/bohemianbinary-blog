import db
import bs4
import requests
import datetime


def print_stock():
    session = db.Session()
    for row in session.query(db.History).order_by(db.asc(db.History.date)).all():
        print(f"low: {row.low_price} / high: {row.high_price} / open: {row.open_price} / close: {row.close_price} "
              f"/ date: {row.date}")


def populate():
    session = db.Session()
    response = requests.get('https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20170626&end=20180626')
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    wrap = soup.find('div', {'id': 'historical-data'})
    table = wrap.find('table')
    for tr in table.find_all('tr'):
        tds = list(tr.find_all('td'))
        if len(tds) == 0:
            continue
        date = datetime.datetime.strptime(tds[0].text, "%b %d, %Y")
        open_price = tds[1].text
        high_price = tds[2].text
        low_price = tds[3].text
        close_price = tds[4].text
        session.add(db.History(date, open_price, high_price, low_price, close_price))
    session.commit()


def get_data():
    session = db.Session()
    open_prices = {}
    high_prices = {}
    low_prices = {}
    close_prices = {}
    for row in session.query(db.History).order_by(db.asc(db.History.date)):
        open_prices[row.date] = row.open_price
        high_prices[row.date] = row.high_price
        low_prices[row.date] = row.low_price
        close_prices[row.date] = row.close_price
    return {
        'open': open_prices,
        'high': high_prices,
        'low': low_prices,
        'close': close_prices
    }


def get_data_as_lists():
    session = db.Session()
    open_prices = []
    high_prices = []
    low_prices = []
    close_prices = []
    index = []
    for row in session.query(db.History).order_by(db.asc(db.History.date)):
        open_prices.append(row.open_price)
        high_prices.append(row.high_price)
        low_prices.append(row.low_price)
        close_prices.append(row.close_price)
        index.append(row.date)
    return (
        index,
        {
            'open': open_prices,
            'high': high_prices,
            'low': low_prices,
            'close': close_prices
        }
    )
