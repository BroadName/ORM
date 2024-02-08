import sqlalchemy as sq
import configparser
import json
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Stock, Shop, Sale

config = configparser.ConfigParser()
config.read('config.ini')
user = config['params']['user']
password = config['params']['password']
host = config['params']['host']
port = config['params']['port']

DSN = f'postgresql://{user}:{password}@localhost:{port}/postgres_db'
engine = sq.create_engine(DSN)

create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()
session.close()


def filing_db():
    with open('tests_data.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)

        for query in json_data:
            model = {'publisher': Publisher,
                     'shop': Shop,
                     'book': Book,
                     'stock': Stock,
                     'sale': Sale}[query.get('model')]
            session.add(model(**query.get('fields')))
    session.commit()
    session.close()


filing_db()
