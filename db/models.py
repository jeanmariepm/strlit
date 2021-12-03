from sqlalchemy import Column, DateTime, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True)
    company = Column(String)

    def __repr__(self):
        return f"id:{self.id}, symbol:{self.symbol}, compant:{self.company}"


class Member(Base):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String, nullable=False)
    is_su = Column(Boolean, default=False)

    def __repr__(self):
        return f"id:{self.id}, username:{self.username}, is_su:{self.is_su}"
