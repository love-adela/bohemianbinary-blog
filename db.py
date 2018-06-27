from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

engine = create_engine('sqlite:///history.db')
Base = declarative_base()
session = Session(bind=engine)
Session = sessionmaker(bind=engine)


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


def save(date, open_price, high_price, low_price, close_price):
    h1 = History(date=date, open_price=open_price, high_price=high_price, low_price=low_price, close_price=close_price)
    session.add(h1)

'''
print(repr(History.__table__))
print(repr(History.__mapper__))


# Creating Data
h1 = History(date="Jun 25, 2018", open_price=455.94, high_price=470.34, low_price=448.90, close_price=460.31)
h2 = History(date="Jun 24, 2018", open_price=474.77, high_price=475.36, low_price=426.47, close_price=457.67)

# print(h1)
# print(h2.id)

session.add(h1)
session.add(h2)

'''