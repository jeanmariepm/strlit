import os
import psycopg2
from sqlalchemy import create_engine, text
from pprint import pprint

DATABASE_URL = os.environ.get('DATABASE_URL')


def start():
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(text("select * from stock"))
        pprint(result.all())


if __name__ == '__main__':
    start()
