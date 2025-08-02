# card_games
A package for card games - teaching children how to code 

## Installation

### Option 1: Using pip (recommended)
```bash
# Install from local directory
pip install -e .

# Or with web UI support
pip install -e ".[ui]"
```

### Option 2: Direct execution
If you don't want to install the package, you can run it directly:
```bash
python -m src.card_games.uno.cli
```

## Games

### UNO
Uno is a popular card game that is easy to learn and fun for all ages. The objective of the game is to be the first player to get rid of all your cards. Players take turns matching a card from their hand with the top card of the discard pile by color or number. Special action cards add excitement and strategy to the game.

#### Running the game

**Using the entry point (recommended):**
```bash
# Show available commands
card-games --help

# Play Uno with CLI (default)
card-games uno

# Play Uno with web interface
card-games uno --interface web

# Play Uno CLI with preset number of players
card-games uno --players 3

# Short form
card-games uno -i web
card-games uno -p 2
```

**Direct module execution:**
```bash
# CLI version
python -m src.card_games.uno_cli

# Web version (requires nicegui)
python -m src.card_games.main uno --interface web
```

#### Card Types in UNO:

**Number Cards (0-9):**
- Red, Blue, Green, Yellow
- 0: One per color
- 1-9: Two per color

**Action Cards:**
- Skip: Skip the next player's turn
- Reverse: Reverse the direction of play
- Draw Two: Next player draws 2 cards and loses their turn

**Wild Cards:**
- Wild: Change the color, player chooses new color
- Wild Draw Four: Change color and next player draws 4 cards

## Project Structure

```
card_games/
├── src/
│   └── card_games/
│       ├── __init__.py
|       ├── uno/
│       │   ├── __init__.py     # Package initialization
│       │   ├── game.py          # Core game logic
│       │   ├── cli.py          # Command-line interface
│       │   ├── ui.py           # Web interface (requires nicegui)
│       │   └── main.py         # Main entry point
├── pyproject.toml
├── README.md
└── LICENSE
```

## Development

This project uses a modern Python package structure with the source code in `src/card_games/`. The games are designed to be both educational and fun, demonstrating various programming concepts like:

- Object-oriented design
- Enums and type hints
- Game state management
- User interface design (both CLI and web)
- Package structure and distribution
