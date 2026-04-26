import random

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
    
class MovingEntity:
    """
    In order to create any moving entity, like a snake or ladder etc.
    """
    
    def __init__(self, end_pos=None):
        self.end_pos = end_pos # end pos where player will be sent on the board
        self.desc = None # description of moving entity

    def set_description(self, desc):
        self.desc = desc
    
    def get_end_pos(self):
        if self.end_pos == None:
            raise Exception("no_end_position_defined")
        return self.end_pos

class Snake(MovingEntity):
    """
    Snake Entity
    """
    
    def __init__(self, end_pos=None):
        super().__init__(end_pos)
        self.desc = "Snake"
    
class Ladder(MovingEntity):
    """
    Ladder Entity
    """
    
    def __init__(self, end_pos=None):
        super().__init__(end_pos)
        self.desc = "Ladder"

class Board:
    def __init__(self, size):
        self.size = size
        self.board = {}
    
    def get_size(self):
        return self.size
    
    def set_moving_entity(self, pos, moving_entity):
        self.board[pos] = moving_entity
    
    def get_next_pos(self, player_pos):
        if player_pos > self.size:
            return player_pos 
        if player_pos not in self.board:
            return player_pos
        return self.board[player_pos].get_end_pos()
    
    def at_last_pos(self, pos):
        return pos == self.size

class Dice:
    def __init__(self, sides):
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)




