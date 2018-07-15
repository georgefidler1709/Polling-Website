from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, joinedload
from sqlalchemy import create_engine
from sqlalchemy.inspection import inspect
from random import randint

ids = set()
def newid():
    num = randint(2**31, 2**33)
    while num in ids:
        num = randint(2**31, 2**33)
    ids.add(num)
    return num


engine = create_engine('sqlite:///data/survey_database.db')
Base = declarative_base()
