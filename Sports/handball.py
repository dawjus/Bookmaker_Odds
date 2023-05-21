from Sports.match_with_draw import MatchWithDraw
from models import Handball_db as table_handball
from models import engine
from sqlalchemy.orm import sessionmaker

class Handball(MatchWithDraw):
    def __init__(self, id):
        super().__init__(id)
        self.path = 'https://www.flashscore.com/'

    def add_to_database(self):
        return table_handball(id_match=str(self.id), name=str(self.match_name), home=str(self.home_team_win_odds),
                 draw=str(self.draw_odds), away=str(self.away_team_win_odds), probability=str(self.probabilities),
                 date=self.date)
