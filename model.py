"""
This file creates the database and schema for the tables.

To create the initial table:
    python -i model.py
    engine = create_engine("sqlite:///database.db", echo=True)
    Base.metadata.create_all(engine)
"""


from sqlalchemy import create_engine, ForeignKey, Column
from sqlalchemy import Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

engine = create_engine("sqlite:///database.db", echo=True)
session = scoped_session(sessionmaker(
    bind=engine, autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = session.query_property()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(50), nullable=False)
    password = Column(String(10), nullable=False)
    income = Column(Integer, nullable=True)
    company_401k = Column(String(1), nullable=True)
    company_match = Column(String(1), nullable=True)
    match_percent = Column(Integer, nullable=True)
    match_salary = Column(Integer, nullable=True)
    risk_profile_id = Column(
        Integer, ForeignKey('risk_profs.id'), nullable=True)

    banking = relationship(
        "UserBanking", backref=backref("user", order_by=id))
    risk_profile = relationship(
        "RiskProfile", backref=backref("users", order_by=id))

    def __repr__(self):
        return "<User ID=%s Email=%s Password=%s Income=%s \
            Risk Profile ID=%s>" % (self.id, self.email,
                                    self.password, self.income,
                                    self.risk_profile_id)


class UserBanking(Base):
    __tablename__ = "u_bank"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    inputted_assets = Column(Integer, nullable=True)
    checking_amt = Column(Integer, nullable=True)
    savings_amt = Column(Integer, nullable=True)
    IRA_amt = Column(Integer, nullable=True)
    comp401k_amt = Column(Integer, nullable=True)
    investment_amt = Column(Integer, nullable=True)

    def __repr__(self):
        return "<User ID=%s Asset=%s Checkings=%s>" % (
            self.user_id, self.inputted_assets, self.checking_amt)


class RiskProfile(Base):
    __tablename__ = "risk_profs"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)

    allocation = relationship(
        "ProfileAllocation", backref=backref("risk_profile", order_by=id))

    def __repr__(self):
        return "<Risk Profile ID=%s Name=%s>" % (self.id, self.name)


class ProfileAllocation(Base):
    __tablename__ = "prof_allocs"

    id = Column(Integer, primary_key=True)
    risk_profile_id = Column(
        Integer, ForeignKey('risk_profs.id'), nullable=False)
    ticker_id = Column(String(8), ForeignKey('tickers.id'), nullable=False)
    ticker_weight_percent = Column(Integer, nullable=False)

    ticker = relationship(
        "Ticker", backref=backref("profile_allocations", order_by=id))

    def __repr__(self):
        return "<Risk Profile ID=%s Ticker ID=%s Ticker Weight=%s>" % (
            self.risk_profile_id, self.ticker_id,
            self.ticker_weight_percent)


class Ticker(Base):
    __tablename__ = "tickers"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(8), nullable=False)
    name = Column(String(100), nullable=False)
    category = Column(String(100), nullable=True)

    price = relationship(
        "Price", backref=backref("ticker", order_by=id))

    def __repr__(self):
        return "<Ticker ID=%s Symbol=%s Name=%s Category=%s>" % (
            self.id, self.symbol, self.name, self.category)


class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True)
    ticker_id = Column(Integer, ForeignKey('tickers.id'), nullable=False)
    date = Column(Date, nullable=False)
    close_price = Column(Integer, nullable=False)
    percent_change = Column(Integer, nullable=True)

    def __repr__(self):
        return "<Ticker ID=%s Date=%s Close Price=%d>" % (
            self.ticker_id, self.date, self.close_price)


def main():
    pass

if __name__ == "__main__":
    main()
