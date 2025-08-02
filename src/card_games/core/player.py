"""
player.py
This module defines the Player class, which represents a player in a card game.
The Player class manages the player's name and their hand of cards, and provides
methods to add, remove, and display cards in the hand.
"""

class Player:
    """
    Represents a player in a card game.
    Attributes:
        name (str): The name of the player.
        hand (list): The list of cards currently held by the player.
    """
    def __init__(self, name, hand=None):
        """
        Initializes a Player instance.
        Args:
            name (str): The name of the player.
            hand (list, optional): The initial hand of cards. Defaults to an empty list.
        """
        self.name = name
        self.hand = hand if hand is not None else []

    def add_card(self, card):
        """
        Adds a card to the player's hand.
        Args:
            card: The card to be added to the hand.
        """
        self.hand.append(card)

    def remove_card(self, card):
        """
        Removes a card from the player's hand if it exists.
        Args:
            card: The card to be removed from the hand.
        Returns:
            The removed card if it was in the hand, otherwise None.
        """
        if card in self.hand:
            self.hand.remove(card)
            return card
        return None

    def show_hand(self):
        """
        Returns the current hand of the player.
        Returns:
            list: The list of cards in the player's hand.
        """
        return self.hand

    def __str__(self):
        """
        Returns a string representation of the player.
        Returns:
            str: A string describing the player and their hand.
        """
        return f"Player({self.name}, Hand: {self.hand})"