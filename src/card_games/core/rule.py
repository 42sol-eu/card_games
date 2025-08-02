"""rule.py

    This module defines the Rule class, which represents a game rule in a card game.
    It can be used as a base for implementing specific rules.
    Subclasses should override the `is_valid` method to define rule logic.
"""

class Rule:
    """
    Represents a game rule in a card game.

    This class can be used as a base for implementing specific rules.
    Subclasses should override the `is_valid` method to define rule logic.

    Attributes:
        name (str): The name of the rule.
        description (str): A brief description of the rule.
    """

    def __init__(self, name: str, description: str = ""):
        """
        Initializes a Rule instance.

        Args:
            name (str): The name of the rule.
            description (str, optional): A brief description of the rule.
        """
        self.name = name
        self.description = description

    def is_valid(self, game_state, move) -> bool:
        """
        Checks if a move is valid according to this rule.

        Args:
            game_state: The current state of the game.
            move: The move to validate.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        raise NotImplementedError("Subclasses should implement this method.")