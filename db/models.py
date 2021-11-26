from sqlalchemy import Column, DateTime, String, Integer, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True)
    company = Column(String)

    def __repr__(self):
        return f"id:{self.id}, symbol:{self.symbol}, compant:{self.company}"
