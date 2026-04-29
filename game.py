"""
Snake and Ladder Game
CMPSC 132 - Final Project
 
A multi-player Snake and Ladder game with classic rules.
All data structures (Queue, Stack) and the sorting algorithm are
implemented manually from scratch, no imports from collections.
"""
 
import random
 
class Node:
    """A single link used by the linked-list-based Queue and Stack."""
 
    def __init__(self, data):
        self.data = data
        self.next = None
 
 
class Queue:
    """
    A FIFO queue built from scratch using a singly linked list.
    enqueue adds to the back, dequeue removes from the front,
    and both operations run in O(1) time.
    """
 
    def __init__(self):
        self.front = None
        self.back = None
        self.count = 0
 
    def enqueue(self, data):
        new_node = Node(data)

        if self.back is None:
            self.front = new_node
            self.back = new_node
        else:
            self.back.next = new_node
            self.back = new_node
        self.count += 1
 
    def dequeue(self):
        if self.front is None:
            return None
        data = self.front.data
        self.front = self.front.next

        if self.front is None:
            self.back = None
        self.count -= 1
        return data
 
    def peek(self):
        if self.front is None:
            return None
        return self.front.data
 
    def is_empty(self):
        return self.front is None
 
    def __len__(self):
        return self.count
 
 
class Stack:
    """
    A LIFO stack built from scratch using a singly linked list.
    push and pop both run in O(1) time.
    """
 
    def __init__(self):
        self.top = None
        self.count = 0
 
    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node
        self.count += 1
 
    def pop(self):
        if self.top is None:
            return None
        data = self.top.data
        self.top = self.top.next
        self.count -= 1
        return data
 
    def peek(self):
        if self.top is None:
            return None
        return self.top.data
 
    def is_empty(self):
        return self.top is None
 
    def __len__(self):
        return self.count

def bubble_sort(items, attribute_name, descending=False):
    """
    Sort a list of objects by one of their attributes using bubble sort.
    """
    sorted_items = items[:]   
    n = len(sorted_items)
    pass_num = 0
    is_sorted = False
 
    while pass_num < n and not is_sorted:
        swapped = False
        j = 0
        while j < n - pass_num - 1:
            value_a = getattr(sorted_items[j], attribute_name)
            value_b = getattr(sorted_items[j + 1], attribute_name)
 
            if descending:
                needs_swap = value_a < value_b
            else:
                needs_swap = value_a > value_b
 
            if needs_swap:
                temp = sorted_items[j]
                sorted_items[j] = sorted_items[j + 1]
                sorted_items[j + 1] = temp
                swapped = True
            j += 1
 
        if not swapped:
            is_sorted = True
        pass_num += 1
 
    return sorted_items
 
# ---------------------------------------------------------------
# Game classes
# ---------------------------------------------------------------
 
class GamePlayer:
    """Represents a single player in the game."""
 
    def __init__(self, player_id, name=None):
        self.player_id = player_id
        self.name = name if name else f"Player {player_id + 1}"
        self.position = 1     # everyone starts on square 1
        self.rank = -1        # -1 means still playing; gets set when they finish
        # tracking some basic stats for the end-of-game summary
        self.total_rolls = 0
        self.snakes_hit = 0
        self.ladders_climbed = 0
 
    def __str__(self):
        return f"{self.name} (pos: {self.position}, rank: {self.rank})"
 
 
class MovingEntity:
    """Base class for snakes and ladders, anything that moves a player."""
 
    def __init__(self, start_pos, end_pos, description="Entity"):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.description = description
 
    def get_end_pos(self):
        return self.end_pos
 
    def get_description(self):
        return self.description
 
 
class Snake(MovingEntity):
    """A snake sends the player from a higher square down to a lower one."""
 
    def __init__(self, head, tail):
        if head <= tail:
            raise ValueError("Snake's head must be higher than its tail")
        super().__init__(head, tail, "Snake")
 
 
class Ladder(MovingEntity):
    """A ladder sends the player from a lower square up to a higher one."""
 
    def __init__(self, bottom, top):
        if top <= bottom:
            raise ValueError("Ladder's top must be higher than its bottom")
        super().__init__(bottom, top, "Ladder")
 
 
class Board:
    """The game board, which uses a dictionary for O(1) snake/ladder lookups."""
 
    def __init__(self, size=100):
        self.size = size
        # dict maps a square number -> the entity that starts there
        # this gives constant-time lookup when checking if a square has a snake/ladder
        self.entities = {}
 
    def get_size(self):
        return self.size
 
    def add_entity(self, entity):
        if entity.start_pos < 1 or entity.start_pos > self.size:
            raise ValueError(f"Position {entity.start_pos} is off the board")
        if entity.end_pos < 1 or entity.end_pos > self.size:
            raise ValueError(f"Position {entity.end_pos} is off the board")
        if entity.start_pos in self.entities:
            raise ValueError(f"Square {entity.start_pos} already has an entity")
        self.entities[entity.start_pos] = entity
 
    def resolve_position(self, position):
        """
        After a move, see if the landing square has a snake or ladder.
        Returns (final_position, entity_type) where entity_type is None if nothing.
        """
        if position in self.entities:
            entity = self.entities[position]
            return entity.get_end_pos(), entity.get_description()
        return position, None
 
    def is_winning_position(self, position):
        return position == self.size
 
 
class Dice:
    """A simple dice with a configurable number of sides."""
 
    def __init__(self, sides=6):
        self.sides = sides
 
    def roll(self):
        return random.randint(1, self.sides)
 
 
class Game:
    """Main game controller that ties players, board, and dice together."""
 
    def __init__(self, board, dice, player_names):
        self.board = board
        self.dice = dice
        self.players = [GamePlayer(i, name) for i, name in enumerate(player_names)]
 
        # use our own Queue for turn rotation
        self.turn_queue = Queue()
        for player in self.players:
            self.turn_queue.enqueue(player)
 
        # use our own Stack for move history
        self.move_history = Stack()
 
        self.next_rank = 1
        self.consecutive_sixes = 0
 
    def is_game_over(self):
        """The game ends when at most one player is still playing."""
        active_players = [p for p in self.players if p.rank == -1]
        return len(active_players) <= 1
 
    def take_turn(self, player):
        """
        Run one turn for the given player.
        Returns True if the player should roll again (rolled a 6), False otherwise.
        """
        roll = self.dice.roll()
        player.total_rolls += 1
        print(f"\n{player.name} rolled a {roll}")
 
        # track three-in-a-row sixes -- if they get three, they lose this turn
        keep_going = True
        if roll == 6:
            self.consecutive_sixes += 1
            if self.consecutive_sixes >= 3:
                print(f"   Three 6s in a row! Turn forfeit.")
                self.consecutive_sixes = 0
                keep_going = False
        else:
            self.consecutive_sixes = 0
 
        result = False  # default return value -- "no extra turn"
 
        # only proceed with movement if the turn wasn't forfeited
        if keep_going:
            new_position = player.position + roll
 
            # overshoot rule: if rolling would go past the final square, stay put
            if new_position > self.board.get_size():
                print(f"   Cannot move past {self.board.get_size()} -- staying at {player.position}")
                # they still get another turn if they rolled a 6
                result = (roll == 6)
            else:
                # check if the landing square has a snake or ladder
                final_position, entity_type = self.board.resolve_position(new_position)
 
                # push this move onto the history stack
                self.move_history.push({
                    "player": player.name,
                    "from": player.position,
                    "to": final_position,
                    "roll": roll,
                    "entity": entity_type
                })
 
                if entity_type == "Snake":
                    player.snakes_hit += 1
                    print(f"   Snake! Slid from {new_position} down to {final_position}")
                elif entity_type == "Ladder":
                    player.ladders_climbed += 1
                    print(f"   Ladder! Climbed from {new_position} up to {final_position}")
                else:
                    print(f"   Moved from {player.position} to {final_position}")
 
                player.position = final_position
 
                # check win condition
                if self.board.is_winning_position(player.position):
                    player.rank = self.next_rank
                    self.next_rank += 1
                    print(f"   *** {player.name} reached {self.board.get_size()}! Finished rank #{player.rank} ***")
                    result = False  # finished, don't roll again
                else:
                    # rolling a 6 earns another turn
                    result = (roll == 6)
 
        return result
 
    def play(self):
        """The main game loop"""
        print("=" * 50)
        print("       SNAKE AND LADDER GAME")
        print("=" * 50)
        self.print_board_info()
 
        while not self.is_game_over():
            # peek at the player at the front of the queue without removing them yet
            current_player = self.turn_queue.peek()
 
            keep_turn = self.take_turn(current_player)
 
            # if they didn't earn another turn, rotate them to the back
            # (and only re-enqueue if they're still playing, a winner gets removed)
            if not keep_turn:
                self.turn_queue.dequeue()
                if current_player.rank == -1:
                    self.turn_queue.enqueue(current_player)
 
            self.print_state()
 
        # whoever's left automatically gets the last rank
        for p in self.players:
            if p.rank == -1:
                p.rank = self.next_rank
                self.next_rank += 1
 
        self.print_results()
 
    def print_board_info(self):
        """Show all snakes and ladders before the game starts."""
        # collect just snakes and just ladders into separate lists
        all_snakes = []
        all_ladders = []
        for entity in self.board.entities.values():
            if isinstance(entity, Snake):
                all_snakes.append(entity)
            elif isinstance(entity, Ladder):
                all_ladders.append(entity)
 
        # sort each one by start position using our manual bubble sort
        sorted_snakes = bubble_sort(all_snakes, "start_pos")
        sorted_ladders = bubble_sort(all_ladders, "start_pos")
 
        print(f"\nBoard size: 1 to {self.board.get_size()}")
        print(f"\nSnakes ({len(sorted_snakes)}):")
        for s in sorted_snakes:
            print(f"   {s.start_pos} -> {s.end_pos}")
        print(f"\nLadders ({len(sorted_ladders)}):")
        for l in sorted_ladders:
            print(f"   {l.start_pos} -> {l.end_pos}")
        print()
 
    def print_state(self):
        """Show current standings, sorted by board position."""
        print("--- Current State ---")
        sorted_players = bubble_sort(self.players, "position", descending=True)
        for p in sorted_players:
            if p.rank != -1:
                status = f"finished (rank {p.rank})"
            else:
                status = f"position {p.position}"
            print(f"   {p.name}: {status}")
        print()
 
    def print_results(self):
        """Final results screen with stats for each player."""
        print("\n" + "=" * 50)
        print("              FINAL RESULTS")
        print("=" * 50)
 
        # ranked from best (rank 1) to worst, using our manual bubble sort
        ranked = bubble_sort(self.players, "rank")
        for p in ranked:
            print(f"\nRank #{p.rank}: {p.name}")
            print(f"   Final position: {p.position}")
            print(f"   Total rolls:    {p.total_rolls}")
            print(f"   Snakes hit:     {p.snakes_hit}")
            print(f"   Ladders climbed: {p.ladders_climbed}")
 
        print(f"\nTotal moves played in game: {len(self.move_history)}")
        print("=" * 50)
 
 
# ---------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------
 
def get_int_in_range(prompt, low, high):
    """Get an integer from the user, retrying until they enter something valid."""
    valid_value = None
    has_valid_input = False
    while not has_valid_input:
        user_input = input(prompt)
        try:
            value = int(user_input)
            if low <= value <= high:
                valid_value = value
                has_valid_input = True
            else:
                print(f"Please enter a number between {low} and {high}.")
        except ValueError:
            print("That's not a number. Try again.")
    return valid_value
 
 
def get_player_names(count):
    """Ask for each player's name, allowing them to use a default."""
    names = []
    i = 0
    while i < count:
        name = input(f"Enter name for Player {i + 1} (or press Enter for default): ").strip()
        if name == "":
            name = f"Player {i + 1}"
        names.append(name)
        i += 1
    return names
 
 
def create_default_board():
    """Build a standard 100-square Snake & Ladder board."""
    board = Board(100)
 
    # standard snake placements (head, tail)
    snakes = [(16, 6), (47, 26), (49, 11), (56, 53), (62, 19),
              (64, 60), (87, 24), (93, 73), (95, 75), (98, 78)]
    for head, tail in snakes:
        board.add_entity(Snake(head, tail))
 
    # standard ladder placements (bottom, top)
    ladders = [(1, 38), (4, 14), (9, 31), (21, 42), (28, 84),
               (36, 44), (51, 67), (71, 91), (80, 100)]
    for bottom, top in ladders:
        board.add_entity(Ladder(bottom, top))
 
    return board
 
 
def main():
    """Program entry point."""
    print("Welcome to Snake & Ladder!\n")
 
    player_count = get_int_in_range("Enter number of players (2-4): ", 2, 4)
    player_names = get_player_names(player_count)
 
    board = create_default_board()
    dice = Dice(6)
    game = Game(board, dice, player_names)
    game.play()
 
 
if __name__ == "__main__":
    main()
 