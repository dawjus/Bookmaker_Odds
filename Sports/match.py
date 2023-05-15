import re
import pandas as pd

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

    def _process_odds(self, odds_list):
        odds_list = list(filter(lambda x: x != '', odds_list))
        for k in range(len(odds_list)):
            odds_list[k] = re.findall(r'\d+\.\d+', odds_list[k])
            if len(odds_list[k]) > 1:
                odds_list[k] = float(odds_list[k][1])
            else:
                odds_list[k] = -1
        return odds_list


    def sequence_on_page(self, count, val):
        self.key[count % self.possibilities].append(val)


    def convert_string_odds_to_array(self):
        self.home_team_win_odds = self._process_odds(self.home_team_win_odds)
        self.away_team_win_odds = self._process_odds(self.away_team_win_odds)

    def set_probabilities(self):
        try:
            self.probabilities = self._count_probabilities_one_event(self.home_team_win_odds) +\
                                 self._count_probabilities_one_event(self.away_team_win_odds)
        except TypeError:
            self.probabilities = 'Too little information about a match'

    def _count_probabilities_one_event(self, odds_list):
        if odds_list:
            return 1/max(odds_list)
        else: return None

    def get_probabilities(self):
        return self.probabilities

    def delete_match(self):
        pass

    @staticmethod
    def createDataFrame(matches):
        data = {
            'Match': [match.match for match in matches],
            'Home': [match.home_team_win_odds for match in matches],
            'Away': [match.away_team_win_odds for match in matches],
            'Probability': [match.get_probabilities() for match in matches],
            'URL': [match.id_from_url() for match in matches]
        }
        df = pd.DataFrame(data)
        df['URL'] = df['URL'].apply(lambda x: f'<a href="https://www.flashscore.com/match/{x}">{"Match Details"}</a>')
        return df

    def id_from_url(self):
        self.id_to_print = self.id[4:]
        return self.id_to_print

