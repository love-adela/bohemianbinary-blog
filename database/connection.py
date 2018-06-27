from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# db settings
dbuser = 'root'
dbpass = 'root'
dbhost = 'localhost'
dbname = 'spiders'

engine = create_engine('sqlite:///history.db' % (dbuser, dbpass, dbhost, dbname), echo=False, pool_recycle=1800)

db = scoped_session(sessionmaker(autocommit=False,
                                 autoflush=False,
                                 bind=engine))
Base = declarative_base()