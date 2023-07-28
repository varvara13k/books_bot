from datetime import datetime
import requests
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base, relationship
from database.models import *
from  datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
import json

class DatabaseConnector:
    USERNAME = "schecksu"
    connection_string = f"postgresql+psycopg2://{USERNAME}:@localhost:5432/{USERNAME}"
    engine = create_engine(connection_string)
    def add(self,book):
        with Session(self.engine) as session:
            try:
                new_record = Book(**book, date_added=datetime.now(), date_deleted = None)
                session.add(new_record)
                session.commit()
            except IntegrityError:
                session.rollback()
                return False
            book_id = new_record.book_id
            return book_id


    def delete(self, id):
        with Session(self.engine) as session:
            borrow = session.query(Borrow).filter_by(book_id=id, date_end=None).first()
            if borrow:
                return False
            else:
                book = session.query(Book).filter_by(book_id=id).first()
                book.date_deleted = datetime.now()
                session.commit()
                return True


    def list_books(self):
        with Session(self.engine) as session:
            query = session.query(Book).all()
            lst = []
            for q in query:
                lst.append({"title": q.title, "author": q.author, "published": q.published, "date_deleted": q.date_deleted})
            return lst
    

    def borrow(self, user_id, book):
        with Session(self.engine) as session:
            book_to_borrow = Book(**book)
            borrowed = session.query(Borrow).filter_by(book_id=book_to_borrow.book_id, date_end=None).first()
            if borrowed:
                return False
            else:
                new_borrow = Borrow(book_id=book_to_borrow.book_id, date_start=datetime.now(), user_id=user_id)
                session.add(new_borrow)
                session.commit()
                return new_borrow.borrow_id



    def get_book(self, bk_title, bk_author, bk_published):
        with Session(self.engine) as session:
            bk_title = bk_title.lower()
            bk_author = bk_author.lower()
            try:
                book = session.query(Book).filter(func.lower(Book.title) == bk_title, func.lower(Book.author) == bk_author.lower(),  Book.published == bk_published).first()
            except NoResultFound:
                return None
            else:
                if book is None:
                    return None
                else:
                    return book.book_id


    def get_borrow(self, user_id):
        with Session(self.engine) as session:
            borrow = session.query(Borrow).filter(Borrow.user_id == user_id, Borrow.date_end == None).first()
            if borrow is not None:
                return borrow.borrow_id
            else:
                return False


    def retrieve(self, borrow_id):
        with Session(self.engine) as session:
            borrow = session.query(Borrow).get(borrow_id)
            if not borrow:
                return False
            if borrow.date_end is not None:
                return False
            borrow.date_end = datetime.now()
            session.commit()
            return True

    def get_book_stats(self, book_id):
        with Session(self.engine) as session:
            borrows = session.query(models.Borrow).filter_by(book_id=book_id).all()
            if borrows is not None:
                result = []
                for borrow in borrows:
                    record = {
                        "borrow_id": borrow.borrow_id,
                        "book_id": borrow.book_id,
                        "date_start": datetime.strftime(borrow.date_start, format="%Y-%m-%d"),
                        "user_id": borrow.user_id
                    }
                    if borrow.date_end is not None:
                        record["date_end"] = datetime.strftime(borrow.date_end, format="%Y-%m-%d")
                    else:
                        record["date_end"] = None
                    result.append(record)
                return result
            else:
                return False

dba = DatabaseConnector()
# print(dba.add({"title": "A", "author": "B", "published": "2000"}))