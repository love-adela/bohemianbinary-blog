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
            'XRP': 'ripple'
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

    # repo.populate() => repo.populate(datetime.datetime.now(), 365)
    # repo.populate(now) => repo.populate(now, 365)
    # repo.populate(duration=30) => repo.poppulation(datetime.datetime.now(), 30)

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

    def get_data_frame(self):
        session = db.Session()
        open_prices = {}
        high_prices = {}
        low_prices = {}
        close_prices = {}
        for row in session.query(db.History).filter(db.History.coin_type == f'{self.coin_full_name}') \
                .order_by(db.asc(db.History.date)):
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

    # def get_data_as_lists(self):
    #     session = db.Session()
    #     open_prices = []
    #     high_prices = []
    #     low_prices = []
    #     close_prices = []
    #     index = []
    #     for row in session.query(db.History).filter(db.History.coin_type == f'{self.coin_full_name}') \
    #             .order_by(db.asc(db.History.date)):
    #         open_prices.append(row.open_price)
    #         high_prices.append(row.high_price)
    #         low_prices.append(row.low_price)
    #         close_prices.append(row.close_price)
    #         index.append(row.date)
    #     return (
    #         index,
    #         {
    #             'open': open_prices,
    #             'high': high_prices,
    #             'low': low_prices,
    #             'close': close_prices
    #         }
    #     )
