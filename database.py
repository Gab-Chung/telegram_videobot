from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///video.db")
base = declarative_base()


class User(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    telegram_id = Column(Integer)
    username = Column(String)
    user_firstname = Column(String)
    user_lastname = Column(String)


class search(base):
    __tablename__ = "search"
    id = Column(Integer, primary_key = True)
    text = Column(String)
    keyword = Column(String)



