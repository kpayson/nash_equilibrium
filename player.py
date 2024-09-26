import random

class Player:
    def __init__(self, id):
        self.id = id
        self.prefs = [0.5]
        self.total_score = 0
        self.num_games_played = 0
        random.seed()
    
    def all_preferences(self):
        return self.prefs
    
    def current_preference(self):
        return self.prefs[-1]
    
    def choose_strategy(self):
        return 1 if random.uniform(0, 1) < self.current_preference() else 0
            
    def update(self, score):
        self.total_score += score
        self.num_games_played += 1
        avg = self.total_score / self.num_games_played
        new_weight = self.current_preference() + (score - avg) / 100
        if new_weight > 1:
            self.prefs.append(1)
        elif new_weight < 0:
            self.prefs.append(0)
        else:
            self.prefs.append(new_weight)
