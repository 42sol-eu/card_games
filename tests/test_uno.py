"""
Basic tests for the Uno game implementation.
"""

import sys
from pathlib import Path
import unittest

# Add the src directory to the path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from card_games import UnoGame, Card, Color, CardType


class TestUnoGame(unittest.TestCase):
    """Test cases for the Uno game."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.players = ["Alice", "Bob"]
        self.game = UnoGame(self.players)
    
    def test_game_initialization(self):
        """Test that the game initializes correctly."""
        self.assertEqual(len(self.game.players), 2)
        self.assertIn("Alice", self.game.players)
        self.assertIn("Bob", self.game.players)
        
        # Each player should have 7 cards
        for player in self.players:
            self.assertEqual(len(self.game.get_player_hand(player)), 7)
        
        # There should be a card on the discard pile
        self.assertTrue(len(self.game.discard_pile) >= 1)
        
        # Current color should be set
        self.assertIsNotNone(self.game.current_color)
    
    def test_card_playability(self):
        """Test card playability logic."""
        # Create test cards
        red_5 = Card(Color.RED, CardType.NUMBER, 5)
        blue_5 = Card(Color.BLUE, CardType.NUMBER, 5)
        red_skip = Card(Color.RED, CardType.SKIP)
        wild = Card(Color.WILD, CardType.WILD)
        
        # Set up a known state
        self.game.discard_pile = [red_5]
        self.game.current_color = Color.RED
        
        # Test playability
        self.assertTrue(self.game._is_playable(blue_5))  # Same number
        self.assertTrue(self.game._is_playable(red_skip))  # Same color
        self.assertTrue(self.game._is_playable(wild))  # Wild card
        
        # Test non-playable card
        blue_skip = Card(Color.BLUE, CardType.SKIP)
        self.assertFalse(self.game._is_playable(blue_skip))  # Different color and type
    
    def test_deck_creation(self):
        """Test that the deck is created correctly.""" 
        deck = self.game._create_deck()
        
        # Standard Uno deck has 108 cards
        self.assertEqual(len(deck), 108)
        
        # Count specific card types
        number_cards = [card for card in deck if card.type == CardType.NUMBER]
        wild_cards = [card for card in deck if card.type == CardType.WILD]
        wild_draw_four_cards = [card for card in deck if card.type == CardType.WILD_DRAW_FOUR]
        
        # Should have 76 number cards (19 per color: 1 zero + 2 each of 1-9)
        self.assertEqual(len(number_cards), 76)
        
        # Should have 4 wild cards and 4 wild draw four cards
        self.assertEqual(len(wild_cards), 4)
        self.assertEqual(len(wild_draw_four_cards), 4)
    
    def test_card_creation(self):
        """Test card creation and string representation."""
        # Test number card
        card = Card(Color.RED, CardType.NUMBER, 5)
        self.assertEqual(str(card), "5")
        self.assertEqual(card.get_display_color(), "red")
        
        # Test wild card
        wild = Card(Color.WILD, CardType.WILD)
        self.assertEqual(str(wild), "🌈")
        self.assertEqual(wild.get_display_color(), "black")
        
        # Test action card
        skip = Card(Color.BLUE, CardType.SKIP)
        self.assertEqual(str(skip), "Skip")
        self.assertEqual(skip.get_display_color(), "blue")


class TestCard(unittest.TestCase):
    """Test cases for individual cards."""
    
    def test_card_to_dict(self):
        """Test card dictionary conversion."""
        card = Card(Color.RED, CardType.NUMBER, 7)
        card_dict = card.to_dict()
        
        expected = {
            "color": "red",
            "type": "number", 
            "value": 7,
            "display": "7",
            "display_color": "red"
        }
        
        self.assertEqual(card_dict, expected)


if __name__ == "__main__":
    unittest.main()
