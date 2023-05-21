from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import StaticPool

Base = declarative_base()
engine = create_engine('sqlite:///matches.db', connect_args={'check_same_thread': False},
    poolclass=StaticPool)

class Football_db(Base):
    __tablename__ = 'football'
    id = Column(Integer, primary_key=True)
    id_match = Column(String(100))
    name =Column(String(100))
    home = Column(String(100))
    draw = Column(String(100))
    away = Column(String(100))
    date = Column(Date)
    probability = Column(String(100))

    def __init__(self, id_match, name, home, draw, away, date, probability):
        self.id_match = id_match
        self.name = name
        self.home = home
        self.draw = draw
        self.away = away
        self.date = date
        self.probability = probability

class Handball_db(Base):
    __tablename__ = 'handball'
    id = Column(Integer, primary_key=True)
    id_match = Column(String(100))
    name =Column(String(100))
    home = Column(String(100))
    draw = Column(String(100))
    away = Column(String(100))
    date = Column(Date)
    probability = Column(String(100))

    def __init__(self, id_match, name, home, draw, away, date, probability):
        self.id_match = id_match
        self.name = name
        self.home = home
        self.draw = draw
        self.away = away
        self.date = date
        self.probability = probability

class Basketball_db(Base):
    __tablename__ = 'basketball'
    id = Column(Integer, primary_key=True)
    id_match = Column(String(100))
    name =Column(String(100))
    home = Column(String(100))
    away = Column(String(100))
    date = Column(Date)
    probability = Column(String(100))

    def __init__(self, id_match, name, home, away, date, probability):
        self.id_match = id_match
        self.name = name
        self.home = home
        self.away = away
        self.date = date
        self.probability = probability

Base.metadata.create_all(engine)