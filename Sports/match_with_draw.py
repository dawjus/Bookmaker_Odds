from Sports.match import Match
from sqlalchemy.orm import sessionmaker
from models import engine
import pandas as pd

class MatchWithDraw(Match):
    def __init__(self, id):
        super().__init__(id)
        self.draw_odds = []
        self.key = {0: self.home_team_win_odds,  1 : self.draw_odds,
                    2:  self.away_team_win_odds}
        self.possibilities = 3

    def convert_string_odds_to_array(self):
        super().convert_string_odds_to_array()
        self.draw_odds = self._process_odds(self.draw_odds)

    def set_probabilities(self):
        super().set_probabilities()
        try:
            self.probabilities = round(self.probabilities +self._count_probabilities_one_event(self.draw_odds),4)
        except TypeError:
            self.probabilities = 'Too little information about this match'

    @staticmethod
    def create_data_frame(db, amount, selectDate):
        Session = sessionmaker(bind=engine)
        session = Session()
        database = session.query(db).filter_by(date=selectDate)
        data = {'Match': [match.name for match in database],
                'Home': [match.home for match in database],
                'Draw': [match.draw for match in database],
                'Away': [match.away for match in database],
                'Probability': [match.probability for match in database],
                'URL': [match.id_match[4:] for match in database]
                }
        df = pd.DataFrame(data)
        df['URL'] = df['URL'].apply(lambda x: f'<a href="https://www.flashscore.com/match/{x}">{"Match Details"}</a>')
        return df.sort_values('Probability').head(amount)

