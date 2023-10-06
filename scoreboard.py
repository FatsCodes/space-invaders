class Scoreboard:
    def __init__(self):
        self.score = 0

    def gain_point(self, points=1):
        self.score += points

    def lose_point(self, points=1):
        self.score -= points

    def game_over(self):
        return self.score <= 0

