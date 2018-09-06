from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, session
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///memory:', echo=True)
Base = declarative_base
Session = sessionmaker(bind=engine)


def create_db():
    Base.metadata.create_all(engine)


class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    movie_name_en = Column(String(120), primary_key=True)
    movie_name_kr = Column(String(120))
    director_name_en = Column(String(64))
    director_name_kr = Column(String(50))
    actor_name_en = Column(String(64))
    actor_name_kr = Column(String(50))

    def __init__(self, movie_name_en, movie_name_kr, director_name_en, director_name_kr, actor_name_en, actor_name_kr):
        self.movie_name_en = movie_name_en
        self.movie_name_kr = movie_name_kr
        self.director_name_en = director_name_en
        self.director_name_kr = director_name_kr
        self.actor_name_en = actor_name_en
        self.actor_name_kr = actor_name_kr

    def __repr__(self):
        return "<Movie('%s', '%s', '%s', '%s', '%s', '%s')> " \
                        "% (self.movie_name_en, self.movie_name_kr, self.director_name_en, self.director_name_kr,\
                            self.actor_name_en, self.actor_name_kr)"


def commit():
    session.commit()
