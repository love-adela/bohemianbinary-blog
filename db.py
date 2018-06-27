import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///history.db')
Base = declarative_base()


class History(Base):
    __tablename__ = "histories"

    id = Column(Integer, primary_key=True)
    date = Column(String)
    open_price = Column(float)
    high_price = Column(float)
    low_price = Column(float)
    close_price = Column(float)


def __repr__(self):
    return "<User(open_price ='%f', hight_price='%f', low_price='%f', close_price='%f')>" % (
        self.date, self.open_price, self.high_price, self.low_price, self.close_price)
