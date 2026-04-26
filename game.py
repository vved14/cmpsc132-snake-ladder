import random

snakes = {98: 79, 96: 75, 93: 73, 87: 24, 64: 60, 62: 19, 54: 39, 17: 7}
ladders = {80: 100, 71: 91, 51: 67, 28: 84, 21: 42, 9: 31, 4: 14, 2: 38}

class GamePlayer:

    def __init__(self, _id):
        self._id = _id
        self.rank = -1
        self.position = 1

    def set_position(self, pos):
        self.position = pos
    
    def set_rank(self, rank):
        self.rank = rank

    def get_pos(self):
        return self.position
    
    def get_rank(self):
        return self.rank



