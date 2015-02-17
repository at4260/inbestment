# Purpose: create the database and tables
# to create initial table:
    # python -i model.py
    # engine = create_engine("sqlite:///portfolio.db", echo=True)
    # Base.metadata.create_all(engine)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

engine = create_engine("sqlite:///portfolio.db", echo=True)
session = scoped_session(sessionmaker(bind=engine, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class Ticker(Base):
    __tablename__ = "tickers"

    id = Column(Integer, primary_key = True)
    ticker_symbol = Column(String(8), nullable=False)
    ticker_name = Column(String(100), nullable=False)
    
    def __repr__(self):
        return "<Ticker ID=%s Symbol=%s Name=%s>" % (self.id, self.ticker_symbol, self.ticker_name)

class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True)
    ticker_symbol = Column(String(8), ForeignKey('tickers.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    # FIXME- chose nullable because not every day may have a stock price (market closed), may not be true though
    close_price = Column(Integer, nullable=True)

    ticker_price = relationship("Ticker",
            backref=backref("prices", order_by=id))

    def __repr__(self):
        return "<Ticker Symbol=%s Date=%s Close Price=%d>" % (self.ticker_symbol, self.date, self.close_price)

### End class declarations
def main():
    """In case we need this for something"""

if __name__ == "__main__":
    main()
