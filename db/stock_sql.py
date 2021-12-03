import os
import psycopg2
from sqlalchemy import create_engine, text, schema, Table
from sqlalchemy.orm import sessionmaker
from db.models import Stock, Member
from pprint import pprint
import pandas as pd


class StockSql:
    def __init__(self):
        self.DATABASE_URL = os.environ.get('DATABASE_URL')
        if self.DATABASE_URL.startswith("postgres://"):
            self.DATABASE_URL = self.DATABASE_URL.replace(
                "postgres://", "postgresql://", 1)
        self.engine = create_engine(self.DATABASE_URL)
        self.connection = self.engine.connect()
        self.session = sessionmaker(bind=self.engine)(bind=self.engine)
        return

    def findTicker(self, company):
        try:
            (ticker,) = self.session.query(Stock.symbol).filter(
                Stock.company.ilike(f'%{company}%')).first()
            return ticker
        except:
            pprint('DB ERROR or company not found')
            return None

    def fetchMember(self, username):
        try:
            member = self.session.query(Member).filter(
                Member.username.ilike(f'%{username}%')).first()
            return member
        except Exception as ex:
            pprint('DB ERROR or member not found', ex)
            return None

    def listMembers(self):
        try:
            members = pd.read_sql("SELECT * FROM member", self.connection)
            pprint(members)
            return members
        except Exception as ex:
            pprint('DB ERROR or member not found', ex)
            return None

    def register(self, username, password):
        try:
            member = Member(username=username, password=password)
            self.session.add(member)
            self.session.commit()
            return member
        except Exception as ex:
            pprint('DB ERROR ', ex)
            return None

    def load_symbols(self):
        table = pd.read_html(
            'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        mycols = table[0][['Symbol', 'Security']]
        mycols = mycols.rename(
            columns={"Symbol": "symbol", "Security": "company"})
        mycolsDict = mycols.to_dict(orient='records')
        self.startSession()
        metadata = schema.MetaData(self.engine)
        table = Table('stock', metadata, autoload=True)
        self.connection.execute(table.insert(), mycolsDict)
        self.session.commit()


if __name__ == '__main__':
    ss = StockSql()
    ss.load_symbols()
    pprint(ss.findTicker('Nike'))
