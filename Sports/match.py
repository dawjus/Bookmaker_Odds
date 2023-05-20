import re
import pandas as pd
from sqlalchemy.orm import sessionmaker
from models import engine

class Match:
    def __init__(self, id):
        self.id = id
        self._name = None
        self.home_team_win_odds = []
        self.away_team_win_odds = []
        self.probabilities = None
        self.key = {0: self.home_team_win_odds, 1 : self.away_team_win_odds}
        self.possibilities = 2
        self.url = 'https://www.flashscore.pl'
        self.url_name = 'Match details'
        self._date = None


    @property
    def match_name(self):
        return self._name

    @match_name.setter
    def match_name(self, val):
        cut_val = re.split(r"\|", val, 2)
        self._name = cut_val[1]

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, val):
        self._date = val


#    def _process_odds(self, odds_list):
#        odds_list = list(filter(lambda x: x != '', odds_list))
#        new_odds_list = []
#        for k in range(len(odds_list)):
#            odds_list[k] = re.findall(r'\d+\.\d+', odds_list[k])
#            if len(odds_list[k]) > 1:
#                new_odds_list.append(odds_list[k][1])
#        return new_odds_list

    def _process_odds(self, odds_list):
        odds_list = list(filter(lambda x: x != '', odds_list))
        new_odds_list = []
        for k in range(len(odds_list)):
            odds_list[k] = re.findall(r'\d+\.\d+', odds_list[k])
            if len(odds_list[k]) > 1:
                new_odds_list.append(odds_list[k][1])
        return new_odds_list


    def sequence_on_page(self, count, val):
        self.key[count % self.possibilities].append(float(val))


    def convert_string_odds_to_array(self):
        self.home_team_win_odds = self._process_odds(self.home_team_win_odds)
        self.away_team_win_odds = self._process_odds(self.away_team_win_odds)

    def set_probabilities(self):
        try:
            self.probabilities = round(self._count_probabilities_one_event(self.home_team_win_odds) +\
                                 self._count_probabilities_one_event(self.away_team_win_odds),4)
        except TypeError:
            self.probabilities = 'Too little information about a match'

    def _count_probabilities_one_event(self, odds_list):
        if odds_list:
            return 1/max(odds_list)
        else: return None

    def get_probabilities(self):
        return self.probabilities

    @staticmethod
    def create_data_frame(db, amount, selectDate):
        Session = sessionmaker(bind=engine)
        session = Session()
        database = session.query(db).filter_by(date=selectDate)
        data = {'Match': [match.name for match in database],
                'Home': [match.home for match in database],
                'Away': [match.away for match in database],
                'Probability': [match.probability for match in database],
                'URL': [match.id_match[4:] for match in database]
                }
        df = pd.DataFrame(data)
        df['URL'] = df['URL'].apply(lambda x: f'<a href="https://www.flashscore.com/match/{x}">{"Match Details"}</a>')
        return df.sort_values('Probability').head(amount)


    def id_from_url(self):
        self.id_to_print = self.id[4:]
        return self.id_to_print

