import db
import requests
import bs4
import datetime
import pandas


class CoinRepository:
    def __init__(self, coin_type):
        self.coin_type = coin_type
        self.coin_full_name = {
            'ETH': 'ethereum',
            'BTC': 'bitcoin',
            'XRP': 'ripple',
            'BCH': 'bitcoin_cash',
            'EOS': 'eos',
            'XLM': 'stellar',
            'LTC': 'lite_coin',
            'ADA': 'cardano',
            'MIOTA': 'iota',
            'USDT': 'tether'
        }[coin_type]

    @staticmethod
    def create_db():
        db.create_db()

    def print_stock(self):
        session = db.Session()
        for row in session.query(db.History).filter(db.History.coin_type == self.coin_type). \
                order_by(db.asc(db.History.date)).all():
            print(f"low: {row.low_price} / high: {row.high_price} / open: {row.open_price} / close: {row.close_price} "
                  f"/ date: {row.date}")

    def update_stock(self, end_date=datetime.datetime.now(), duration=365):
        start_date = end_date - datetime.timedelta(duration)
        session = db.Session()
        response = requests.get(
            f"https://coinmarketcap.com/currencies/{self.coin_full_name}/historical-data/"
            f"?start={start_date.strftime('%Y%m%d')}&end={end_date.strftime('%Y%m%d')}")
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
            session.merge(db.History(date, open_price, high_price, low_price, close_price, f'{self.coin_full_name}'))
        session.commit()

    def get_data_frame(self, end_date=datetime.datetime.now(), duration=365):
        start_date = end_date - datetime.timedelta(duration)

        session = db.Session()
        open_prices = {}
        high_prices = {}
        low_prices = {}
        close_prices = {}

        query = self.query_data(session, start_date, end_date)
        if query.count() > 0:
            got_start_date, got_end_date = query[0].date, query[-1].date

            is_same_start_date = start_date != got_start_date
            is_same_end_date = end_date != got_end_date

            if is_same_start_date or is_same_end_date:
                self.update_stock(end_date, duration)
                query = self.query_data(session, start_date, end_date)
        else:
            query = self.query_data(session, start_date, end_date)

        for row in query:
            open_prices[row.date] = row.open_price
            high_prices[row.date] = row.high_price
            low_prices[row.date] = row.low_price
            close_prices[row.date] = row.close_price
        return pandas.DataFrame({
            'open': open_prices,
            'high': high_prices,
            'low': low_prices,
            'close': close_prices
        })

    def query_data(self, session, start_date, end_date):
        return session.query(db.History)\
            .filter(db.History.coin_type == f'{self.coin_full_name}')\
            .filter(db.History.date >= start_date)\
            .filter(db.History.date <= end_date)\
            .order_by(db.asc(db.History.date))
