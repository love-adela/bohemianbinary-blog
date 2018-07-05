from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Date
import sqlite3
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

engine = create_engine("sqlite:///history.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class History(Base):
    __tablename__ = 'histories'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)

    def __init__(self, date, open_price, high_price, low_price, close_price):
        self.date = date
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price

    def __repr__(self):
        return "<History(date='%s', open_price ='%f', high_price='%f', low_price='%f', close_price='%f')>" % (
            self.date, self.open_price, self.high_price, self.low_price, self.close_price)


def add(date, open_price, high_price, low_price, close_price):
    h1 = History(date=date, open_price=open_price, high_price=high_price, low_price=low_price, close_price=close_price)
    session.add(h1)


def commit():
    session.commit()


session = Session()
for row in session.query(History).order_by(asc(History.date)).all():
    print(f"low: {row.low_price} / high: {row.high_price} / open: {row.open_price} / close: {row.close_price} "
          f"/ date: {row.date}")


session = Session()
result = session.query(History).order_by(asc(History.date)).all()
data = []
index = []
for row in result:
    index.append(row.date)
    data.append(row.close_price)

ts = pd.Series(data, index=index)
ts.plot()

low_price = []
high_price = []
open_price = []
close_price = []
index = []

session = Session()
for row in session.query(History).order_by(asc(History.date)).all():
    low_price.append(row.low_price)
    high_price.append(row.high_price)
    open_price.append(row.open_price)
    close_price.append(row.close_price)
    index.append(pd.Timestamp(row.date))

prices = {
    'low': low_price,
    'high': high_price,
    'open': open_price,
    'close': close_price
}

# print(prices)

df = pd.DataFrame(prices, index=index)
df.plot()

gap = []
half_gap = []

for i in range(0, len(prices['low'])):
    gap_row = prices['high'][i] - prices['low'][i]
    half_gap_row = gap_row * 0.5

    gap.append(gap_row)
    half_gap.append(half_gap_row)

prices['gap'] = gap
prices['half_gap'] = half_gap

# print(prices)

df = pd.DataFrame(prices, index=index)
df.plot()


target = [-1]
for i in range(1, len(prices['low'])):
    target_row = prices['open'][i] + prices['gap'][i - 1]
    target.append(target_row)


prices['target'] = target

df = pd.DataFrame({'close' : prices['close'], 'target' : prices['target']}, index)
df.plot()


