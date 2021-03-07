class DisplayScores:
    def __init__(self, settings):
        self.settings = settings
        self.show_scores_menu = False
        self.reset_stats()
        self.high_score = 0
        self.level = 1
        self.ships_left = self.score = None

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
