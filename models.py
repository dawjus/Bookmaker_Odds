from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
engine = create_engine('sqlite:///matches.db')

class Football(Base):
    __tablename__ = 'football'
    id = Column(Integer, primary_key=True)
    id_match = Column(String(100))
    name =Column(String(100))
    home = Column(String(100))
    draw = Column(String(100))
    away = Column(String(100))
    date = Column(Date)
    probability = Column(String(100))

class Handball(Base):
    __tablename__ = 'handball'
    id = Column(Integer, primary_key=True)
    id_match = Column(String(100))
    name =Column(String(100))
    home = Column(String(100))
    draw = Column(String(100))
    away = Column(String(100))
    date = Column(Date)
    probability = Column(String(100))

class Basketball(Base):
    __tablename__ = 'basketball'
    id = Column(Integer, primary_key=True)
    id_match = Column(String(100))
    name =Column(String(100))
    home = Column(String(100))
    away = Column(String(100))
    date = Column(Date)
    probability = Column(String(100))

Base.metadata.create_all(engine)