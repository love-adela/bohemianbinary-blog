import db
import requests
import bs4
import pandas
import datetime

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
