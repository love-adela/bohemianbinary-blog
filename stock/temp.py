import db

class CoinRepository:
    def __init__(self, coin_type):
        self.coin_type = coin_type
        self.coin_full_name = {
            'ETH': 'ethereum',
            'BTC':'bitcoin',
            'XRP': 'ripple',
            'BCH': 'bitcoin-cash',
            'EOS': 'eos',
            'XLM': 'stellar',
            'LTC': 'litecoin',
            'ADA': 'cardano',
            'MIOTA': 'iota',
            'USDT': 'tether'
        }[coin_type]

    @staticmethod
    def create_db():
        db.create_db()

    def print_stock(self):
        session = db.Session()
        for row in session.query(db.History).filter_by(db.History.coin_type == self.coin_type)\
            .order_by(db.asc(db.History.date).all()):

