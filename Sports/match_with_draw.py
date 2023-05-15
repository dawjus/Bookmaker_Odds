from Sports.match import Match

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
            self.probabilities += self._count_probabilities_one_event(self.draw_odds)
        except TypeError:
            self.probabilities = 'Too little information about this match'

    @staticmethod
    def createDataFrame(matches):
        df = Match.createDataFrame(matches)
        draw_column = [match.draw_odds for match in matches]
        df.insert(2, 'Draw', draw_column)
        return df