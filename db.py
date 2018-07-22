from sqlalchemy import create_engine, desc, asc
from sqlalchemy.orm import sessionmaker, session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Text

engine = create_engine("sqlite:///history.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)


def create_db():
    Base.metadata.create_all(engine)


class History(Base):
    __tablename__ = 'histories'

    date = Column(Date, primary_key=True)
    coin_type = Column(Text, primary_key=True)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)

    def __init__(self, date, open_price, high_price, low_price, close_price, coin_type):
        self.date = date
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.coin_type = coin_type

    def __repr__(self):
        return "<History(date='%s', open_price ='%f', high_price='%f', low_price='%f', close_price='%f')>" % (
            self.date, self.open_price, self.high_price, self.low_price, self.close_price)


def add(date, open_price, high_price, low_price, close_price):
    h1 = History(date=date, open_price=open_price, high_price=high_price, low_price=low_price, close_price=close_price)
    session.add(h1)


def commit():
    session.commit()
