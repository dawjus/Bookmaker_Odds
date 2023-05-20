from models import Basketball_db, Handball_db, Football_db
from Sports.football import Football
from Sports.basketball import Basketball
from Sports.handball import Handball
from enum import Enum

class SportEnum(Enum):
    BASKETBALL = ('Basketball', Basketball_db, Basketball)
    FOOTBALL = ('Football', Football_db, Football)
    HANDBALL = ('Handball', Handball_db, Handball)

    def __init__(self, value, db, sport_object):
        self._value = value
        self._db = db
        self._sport_object = sport_object

    @property
    def value(self):
        return self._value

    @property
    def db(self):
        return self._db

    @property
    def sport_object(self):
        return self._sport_object