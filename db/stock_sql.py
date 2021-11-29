import os
import psycopg2
from sqlalchemy import create_engine, text, schema, Table
from sqlalchemy.orm import sessionmaker
from db.models import Stock
from pprint import pprint
import pandas as pd

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


def findTicker(company):
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session(bind=engine)
    (ticker,) = session.query(Stock.symbol).filter(
        Stock.company.like(f'%{company}%')).first()
    return ticker


def load_symbols():
    table = pd.read_html(
        'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    mycols = table[0][['Symbol', 'Security']]
    mycols = mycols.rename(
        columns={"Symbol": "symbol", "Security": "company"})
    mycolsDict = mycols.to_dict(orient='records')
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session(bind=engine)
    metadata = schema.MetaData(engine)
    table = Table('stock', metadata, autoload=True)
    conn.execute(table.insert(), mycolsDict)
    session.commit()
    session.close()


if __name__ == '__main__':
    load_symbols()
    pprint(findTicker('Nike'))
