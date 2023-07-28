from  datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Book(Base):
    __tablename__ = 'Books'
    book_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    published = Column(Integer, nullable=False)
    date_added = Column(Date, nullable=False)
    date_deleted = Column(Date, nullable=True)


class Borrow(Base):
    __tablename__ = 'Borrows'
    borrow_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('Books.book_id'), nullable=False)
    date_start = Column(DateTime, default=datetime.now(), nullable=False)
    date_end = Column(DateTime, nullable=True)
    user_id = Column(Integer, nullable=False)
    
    # связываем таблицы один-ко-многим
    book = relationship('Book', backref='Borrow')

    # определяем метод для удобного вывода информации
    def __repr__(self):
        return f"<Borrow(id={self.borrow_id}, book_id={self.book_id}, date_start={self.date_start}, date_end={self.date_end}, user_id={self.user_id})>"



#  Base.metadata.create_all(engine)



# добавляем книги в БД

# session.add_all([Books(title='The Great Gatsby', author='F. Scott Fitzgerald', published=1925, date_added='2021-05-01'), 
#                 Books(title='To Kill a Mockingbird', author='Harper Lee', published=1960, date_added='2021-05-01'), 
#                 Books(title='1984', author='George Orwell', published=1949, date_added='2021-05-01'), 
#                 Books(title='Pride and Prejudice', author='Jane Austen', published=1813, date_added='2021-05-01'), 
#                 Books(title='The Catcher in the Rye', author='J.D. Salinger', published=1951, date_added='2021-05-01')])

# session.add_all([Borrow(book_id=1,user_id=1, date_start='2023-01-01'),
#                 Borrow(book_id=2, user_id=1, date_start='2023-02-02'),
#                 Borrow(book_id=3, user_id=1, date_start='2023-03-03'),
#                 Borrow(book_id=4, user_id=1, date_start='2023-04-04'),
#                 Borrow(book_id=5, user_id=1, date_start='2023-05-05')

# ])
# session.commit()

# session.close()

