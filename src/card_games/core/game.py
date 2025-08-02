"""
core/game.py
This module defines the CoreGame class, which provides the foundational logic for implementing card games.
It manages players, the deck, turn order, and the basic game lifecycle (start, end, next turn).
Game-specific logic such as dealing cards should be implemented by subclasses.
"""
import random

class CoreGame:
    """
    CoreGame is a base class representing the core logic for a card game.
    Attributes:
        players    def __init__(self, players=None, deck=None):
        self.players = players if players is not None else []
        self.deck = deck
        self.current_player_index = 0
        self.is_active = False
    """

    def start(self):
        """Start the game.

        Raises:
            ValueError: If players or deck are not set.
        """
        if not self.players or not self.deck:
            raise ValueError("Players and deck must be set before starting the game.")
        self.is_active = True
        self.current_player_index = 0
        self.shuffle_deck()
        self.deal_cards()

    def shuffle_deck(self):
        """Shuffle the deck of cards."""
        random.shuffle(self.deck)

    def deal_cards(self):
        """Deal cards to players.
        This method should be overridden by subclasses to implement game-specific dealing logic.
        """
        raise NotImplementedError("Subclasses must implement deal_cards method.")

    def next_turn(self):
        """Advance to the next player's turn."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def end(self):
        """End the game."""
        self.is_active = False

    def get_current_player(self):
        """Get the current player."""
        return self.players[self.current_player_index]