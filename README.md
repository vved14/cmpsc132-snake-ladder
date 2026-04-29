# Snake and Ladder Game

A terminal-based Snake and Ladder game written in Python. Built as my final project for CMPSC 132 - Programming and Computation 2.

## What It Does

This is a Snake and Ladder game for 2 to 4 players. You take turns rolling a dice and moving along a board with squares numbered 1 to 100. Land on a ladder and you climb up. Land on a snake and you slide down. The first player to land exactly on square 100 wins.

The game also tracks stats for each player like total rolls, snakes hit, and ladders climbed. When everyone finishes, it prints out the final ranking with each player's stats.

## Rules

The board has 100 squares and the dice has 6 sides.

- Every player starts on square 1.
- On your turn, you roll the dice and move forward by that many squares.
- If you land on the bottom of a ladder, you climb to the top.
- If you land on the head of a snake, you slide down to its tail.
- Players take turns one after the other.
- Rolling a 6 lets you go again. But three sixes in a row ends your turn instead.
- You have to land exactly on 100 to win. If your roll would take you past 100, you stay where you are. So if you are on 97 and you roll a 5, you stay on 97 because 102 is off the board.
- Once you reach 100, you finish and get a rank. The game keeps going until only one player is left, and that player gets the last rank.

## Requirements

You need Python 3.8 or higher. The game only uses the built-in `random` module, so there is nothing extra to install.

## How to Run

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/cmpsc132-snake-ladder.git
   cd snake-and-ladder
   ```

2. Run the game:
   ```
   python snake_and_ladder.py
   ```

3. Type the number of players, enter each player's name, and play.

## Data Structures Used

I built the data structures myself instead of importing them from a library. Here is what I used:

| Structure | What it does in the game |
|-----------|--------------------------|
| Queue (linked list) | Holds the players in turn order. After someone takes their turn, they go to the back of the line. |
| Stack (linked list) | Saves every move that happens during the game so we can show how many moves were played at the end. |
| Dictionary | Stores the snakes and ladders on the board. The key is the square where the snake or ladder starts. |
| List | Holds all the players and their stats. |

The Queue and Stack both use a Node class to build a linked list. The Queue keeps a `front` pointer and a `back` pointer, so adding to the back and removing from the front both run in O(1) time. The Stack only needs a `top` pointer because everything goes in and out from the same end.

The dictionary on the Board class is what makes snake and ladder lookups fast. When a player lands on a square, the program just checks if that square is a key in the dictionary. If it is, the player gets sent to wherever that snake or ladder leads.

Example of how the board stores them:
```python
board.entities = {16: Snake(16, 6), 4: Ladder(4, 14), ...}
```

## Algorithm Used

I wrote a bubble sort from scratch to sort the players. It runs in two places: during the game when showing the current standings (sorted by who is furthest along the board), and at the end when showing the final results (sorted by rank). I also added the early-exit trick, where if the sort goes through a full pass without swapping anything, it stops because the list is already sorted.

## File Structure

```
snake-and-ladder/
├── snake_and_ladder.py    # main game file
└── README.md              # this file
```

## Author

Ved Bhattathiripad
CMPSC 132 - Spring 2026
Pennsylvania State University

## License

This is a school project for CMPSC 132. Educational use only.
