#!/usr/bin/env python3
"""
Example script showing how to use the card_games package programmatically.

This demonstrates how to create and interact with an Uno game without the CLI.
"""

import sys
from pathlib import Path

# Add the src directory to the path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from card_games.uno import UnoGame, Color, CardType


def main():
    """Demonstrate programmatic usage of the Uno game."""
    print("=== Uno Game Example ===")
    
    # Create a game with 3 players
    players = ["Alice", "Bob", "Charlie"]
    game = UnoGame(players)
    
    print(f"Players: {', '.join(players)}")
    print(f"Starting card: {game.get_top_card()}")
    print(f"Current color: {game.current_color.value if game.current_color else 'N/A'}")
    print()
    
    # Show initial hands
    for player in players:
        hand = game.get_player_hand(player)
        print(f"{player}'s hand ({len(hand)} cards): {', '.join(str(card) for card in hand)}")
    print()
    
    # Play a few turns automatically
    turns = 0
    max_turns = 10
    
    while not game.is_game_over() and turns < max_turns:
        current_player = game.get_current_player()
        player_index = list(game.players.keys()).index(current_player)
        hand = game.get_player_hand(current_player)
        
        print(f"--- {current_player}'s turn ---")
        print(f"Top card: {game.get_top_card()} ({game.current_color.value if game.current_color else 'N/A'})")
        
        # Handle forced draws
        if game.forced_draw > 0:
            drawn = game.draw_card(player_index, game.forced_draw)
            print(f"{current_player} drew {len(drawn)} cards: {', '.join(str(card) for card in drawn)}")
            game.forced_draw = 0
            game._next_turn()
            turns += 1
            continue
        
        # Try to play a card
        played = False
        for i, card in enumerate(hand):
            if game._is_playable(card):
                # For wild cards, choose a random color
                chosen_color = None
                if card.type in (CardType.WILD, CardType.WILD_DRAW):
                    import random
                    chosen_color = random.choice([Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW])
                    print(f"{current_player} plays {card} and chooses {chosen_color.value}")
                else:
                    print(f"{current_player} plays {card}")
                
                success, message = game.play_card(player_index, i, chosen_color)
                if success:
                    if message:  # Win message
                        print(f"🎉 {message}")
                        return
                    played = True
                    break
        
        if not played:
            # Draw a card
            drawn = game.draw_card(player_index)
            print(f"{current_player} drew: {drawn[0]}")
            game._next_turn()
        
        # Show card counts
        counts = game.get_player_counts()
        print(f"Card counts: {', '.join(f'{name}: {count}' for name, count in counts.items())}")
        print()
        
        turns += 1
    
    if game.is_game_over():
        print(f"🎉 Game Over! Winner: {game.winner}")
    else:
        print(f"Game stopped after {max_turns} turns for demonstration.")


if __name__ == "__main__":
    main()
