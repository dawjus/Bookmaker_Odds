from Sports.match import Match
from models import Basketball_db  as table_basketball
from models import engine
from sqlalchemy.orm import sessionmaker

class Basketball(Match):
    def __init__(self, id):
        super().__init__(id)
        self.path = 'https://www.flashscore.com/basketball/'

    def add_to_database(self):
        return table_basketball(id_match=str(self.id), name=str(self.match_name), home=str(self.home_team_win_odds),
                away=str(self.away_team_win_odds), probability=str(self.probabilities),
                 date=self.date)

    def delete_from_database(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        session.query(table_basketball).filter(table_basketball.id_match == self.id).delete(synchronize_session=False)
        session.commit()