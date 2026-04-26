# Snake and Ladder Game

A two player terminal based Snake and Ladder game built in python as a final project for **CMPSC 132 – Programming and Computation 2**.

---

## Project Description

This is a classic 2-player Snake & Ladder game that runs entirely in the terminal. Players take turns rolling a dice, moving across a 1–100 board, climbing ladders, and sliding down snakes. The first player to land *exactly* on cell 100 wins!

The project demonstrates fundamental Python concepts and data structures including dictionaries, lists, loops, conditionals, functions, and input validation.

---

## Rules

The game uses a 10×10 board (cells 1–100) and a standard 6-sided dice.

- Each player begins with their counter on cell 1 and takes turns rolling the dice.
- After rolling, the player moves their counter forward by the number shown on the dice.
- Ladders — landing on the bottom of a ladder lifts the player straight up to the top.
- Snakes — landing on a snake's head sends the player sliding down to its tail.
- Turns alternate fairly between players.
- Rolling a 6 earns the player a bonus roll. However, a single turn is capped at a maximum of 3 rolls — so if a player rolls 6, 6, 6, their turn ends and play passes to the next player.
- If a roll would move a player past cell 100, the move is considered invalid and the player stays in their current position. For example, a player on cell 99 must roll exactly 1 to win; any higher roll keeps them on 99.
- When a player reaches cell 100, they finish the game. The program tracks and displays the final rankings (1st, 2nd, 3rd, …) once all players have completed the board.

---

## Requirements

- Python 3.8 or higher
- No external libraries required (uses only the built-in `random` module)

---

## How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cmpsc132-snake-ladder.git
   cd snake-and-ladder
   ```

2. **Run the game**
   ```bash
   python game.py
   ```

3. **Follow the on-screen prompts** to play!

---

## Data Structures Used

| Structure | Purpose |
|-----------|---------|
| `dict` | Stores snake mappings (head → tail) |
| `dict` | Stores ladder mappings (bottom → top) |
| `dict` / `list` | Tracks each player's current position |

**Example:**
```python
snakes  = {16: 6, 48: 30, 62: 19, 95: 75}
ladders = {3: 22, 20: 38, 36: 44, 71: 91}
```

---

## File Structure

```
snake-and-ladder/
├── snake_ladder.py    # Main game file
└── README.md          # Project documentation
```

---

## Author

**Ved Bhattathiripad**
CMPSC 132 – Spring 2026
Pennsylvania State University

---

## License

This project was created for educational purposes as part of CMPSC 132.
