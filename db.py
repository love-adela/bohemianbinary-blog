from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

engine = create_engine("sqlite:///history.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class History(Base):
    __tablename__ = 'histories'

    id = Column(Integer, primary_key=True)
    date = Column(String)
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