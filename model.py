""" This file creates the database and schema for the tables. """
# to create initial table:
    # python -i model.py
    # engine = create_engine("sqlite:///database.db", echo=True)
    # Base.metadata.create_all(engine)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

engine = create_engine("sqlite:///database.db", echo=True)
session = scoped_session(sessionmaker(bind=engine, autocommit = False, 
    autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

class Ticker(Base):
    __tablename__ = "tickers"

    id = Column(Integer, primary_key = True)
    symbol = Column(String(8), nullable=False)
    name = Column(String(100), nullable=False)
    
    def __repr__(self):
        return "<Ticker ID=%s Symbol=%s Name=%s>" % (self.id, self.symbol, 
            self.name)

class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True)
    ticker_symbol = Column(String(8), ForeignKey('tickers.id'), nullable=False)
    date = Column(Date, nullable=False)
    close_price = Column(Integer, nullable=False)

    ticker_price = relationship("Ticker",
            backref=backref("prices", order_by=id))

    def __repr__(self):
        return "<Ticker Symbol=%s Date=%s Close Price=%d>" % (self.ticker_symbol, 
            self.date, self.close_price)

class riskProfile(Base):
    __tablename__ = "risk_profiles"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)

    def __repr__(self):
        return "<Risk Profile ID=%s Name=%s>" % (self.id, self.name)

class profileAllocation(Base):
    __tablename__ = "profile_allocations"

    id = Column(Integer, primary_key=True)
    risk_profile_id = Column(Integer, ForeignKey('risk_profiles.id'), nullable=False)
    ticker_symbol = Column(String(8), ForeignKey('tickers.id'), nullable=False)
    ticker_weight_percent = Column(Integer, nullable=False)

    def __repr__(self):
        return "<Risk Profile ID=%s Ticker Symbol=%s Ticker Weight(in percent) \
            =%s>" %(self.risk_profile_id, self.ticker_symbol, 
            self.ticker_weight_percent)

def main():
    pass

if __name__ == "__main__":
    main()
