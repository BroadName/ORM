import sqlalchemy as sq
import configparser
from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Stock, Shop, Sale


config = configparser.ConfigParser()
config.read('config.ini')
user = config['params']['user']
password = config['params']['password']
host = config['params']['host']
port = config['params']['port']

DSN = f'postgresql://{user}:{password}@localhost:{port}/postgres_db'
engine = sq.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()


def find_info(publisher=input()):

    if publisher.isdigit():
        counter = 0
        for q in session.query(Book.title,
                            Shop.name,
                            Sale.price,
                            Sale.date_sale).\
                                join(Publisher).\
                                    join(Stock).\
                                        join(Shop).\
                                            join(Sale).\
                                                filter(Book.publisher_id == publisher).all():
            for title in q:
                if counter < 3:
                    print(f'{title} | ', end='')
                    counter += 1
                else:
                    print(f'{title}', end='\n')
                    counter = 0
            # print(*q)
    elif publisher:
        counter = 0
        for q in session.query(Book.title,
                               Shop.name,
                               Sale.price,
                               Sale.date_sale). \
                                    join(Publisher). \
                                        join(Stock). \
                                            join(Shop). \
                                                join(Sale). \
                                                    filter(Publisher.name == publisher).all():
            for title in q:
                if counter < 3:
                    print(f'{title} | ', end='')
                    counter += 1
                else:
                    print(f'{title}', end='\n')
                    counter = 0
    else:
        print('You have input a wrong data.\nYou need to input just publisher name or his id.\nTry again!')
        find_info(input())


find_info()
