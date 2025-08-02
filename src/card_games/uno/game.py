"""
Uno card game implementation.

This module contains the core game logic for Uno, including card definitions,
game state management, and game rules.
"""

import random
from enum import Enum
from typing import List, Dict, Optional, Tuple


class Color(Enum):
    """Enum for card colors in Uno."""
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    WILD = "black"


class CardType(Enum):
    """Enum for card types in Uno."""
    NUMBER = "number"
    SKIP = "skip"
    REVERSE = "reverse"
    DRAW_TWO = "draw_two"
    WILD = "wild"
    WILD_DRAW = "WILD_DRAW"


class Card:
    """Represents a single Uno card."""
    
    def __init__(self, color: Color, card_type: CardType, value: Optional[int] = None):
        self.color = color
        self.type = card_type
        self.value = value

    def __str__(self):
        if self.type == CardType.NUMBER:
            return f"{self.value}"
        elif self.type == CardType.WILD:
            return "🌈"
        elif self.type == CardType.WILD_DRAW:
            return "🌈+4"
        else:
            return self.type.value.replace("_", " ").title()

    def get_display_color(self) -> str:
        """Get the color for display purposes."""
        if self.color == Color.WILD:
            return "black"
        return self.color.value
    
    def get_sort_key(self) -> tuple:
        """Get sorting key for cards: (color_order, type_order, value)."""
        # Color order: RED, BLUE, GREEN, YELLOW, WILD
        color_order = {
            Color.RED: 0,
            Color.BLUE: 1, 
            Color.GREEN: 2,
            Color.YELLOW: 3,
            Color.WILD: 4
        }
        
        # Type order: NUMBER, SKIP, REVERSE, DRAW_TWO, WILD, WILD_DRAW
        type_order = {
            CardType.NUMBER: 0,
            CardType.SKIP: 1,
            CardType.REVERSE: 2, 
            CardType.DRAW_TWO: 3,
            CardType.WILD: 4,
            CardType.WILD_DRAW: 5
        }
        
        return (
            color_order.get(self.color, 999),
            type_order.get(self.type, 999),
            self.value if self.value is not None else 999
        )

    def to_dict(self):
        """Convert card to dictionary representation."""
        return {
            "color": self.color.value,
            "type": self.type.value,
            "value": self.value,
            "display": str(self),
            "display_color": self.get_display_color()
        }


class UnoGame:
    """Main game logic for Uno."""
    
    def __init__(self, player_names: List[str]):
        self.players = {name: {"hand": [], "score": 0} for name in player_names}
        self.current_player = 0
        self.direction = 1
        self.discard_pile: List[Card] = []
        self.draw_pile: List[Card] = self._create_deck()
        self.current_color: Optional[Color] = None
        self.game_started = False
        self.winner = None
        self.forced_draw = 0  # Number of cards to draw due to special cards

        self._deal_cards()
        self._start_game()

    def _create_deck(self) -> List[Card]:
        """Create a full Uno deck with all cards."""
        deck = []
        colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]

        # Number cards (0-9), with 0 appearing once and 1-9 appearing twice per color
        for color in colors:
            deck.append(Card(color, CardType.NUMBER, 0))  # Only one 0 per color
            for value in range(1, 10):
                deck.append(Card(color, CardType.NUMBER, value))
                deck.append(Card(color, CardType.NUMBER, value))

        # Action cards (2 of each per color)
        for color in colors:
            for _ in range(2):
                deck.append(Card(color, CardType.SKIP))
                deck.append(Card(color, CardType.REVERSE))
                deck.append(Card(color, CardType.DRAW_TWO))

        # Wild cards (4 of each)
        for _ in range(4):
            deck.append(Card(Color.WILD, CardType.WILD))
            deck.append(Card(Color.WILD, CardType.WILD_DRAW))

        random.shuffle(deck)
        return deck

    def _deal_cards(self):
        """Deal 7 cards to each player."""
        for player in self.players:
            self.players[player]["hand"] = self.draw_pile[:7]
            self.draw_pile = self.draw_pile[7:]

    def _start_game(self):
        """Start the game by placing the first card on the discard pile."""
        for i, card in enumerate(self.draw_pile):
            if card.type != CardType.WILD and card.type != CardType.WILD_DRAW:
                self.discard_pile.append(self.draw_pile.pop(i))
                self.current_color = self.discard_pile[-1].color
                self.game_started = True
                return

    def draw_card(self, player_index: int, count: int = 1) -> List[Card]:
        """Draw cards for a player."""
        drawn_cards = []
        for _ in range(count):
            if not self.draw_pile:
                self._reshuffle_discard_pile()
            if self.draw_pile:
                card = self.draw_pile.pop(0)
                player_name = list(self.players.keys())[player_index]
                self.players[player_name]["hand"].append(card)
                drawn_cards.append(card)
        return drawn_cards

    def handle_forced_draw(self, player_index: int) -> List[Card]:
        """Handle forced draw (from +2 or +4 cards) and reset the forced_draw counter."""
        if self.forced_draw == 0:
            return []
        
        drawn_cards = self.draw_card(player_index, self.forced_draw)
        # Reset forced_draw after cards are drawn
        self.forced_draw = 0
        return drawn_cards

    def _reshuffle_discard_pile(self):
        """Reshuffle the discard pile into the draw pile when needed."""
        top_card = self.discard_pile.pop()
        self.draw_pile = self.discard_pile
        self.discard_pile = [top_card]
        random.shuffle(self.draw_pile)

    def play_card(self, player_index: int, card_index: int, chosen_color: Optional[Color] = None) -> Tuple[bool, Optional[str]]:
        """Attempt to play a card from a player's hand."""
        return self.play_multiple_cards(player_index, [card_index], chosen_color)

    def play_multiple_cards(self, player_index: int, card_indices: List[int], chosen_color: Optional[Color] = None) -> Tuple[bool, Optional[str]]:
        """Attempt to play multiple cards from a player's hand (same number and color only)."""
        player_name = list(self.players.keys())[player_index]
        hand = self.players[player_name]["hand"]
        
        # Get the cards to be played
        cards_to_play = [hand[i] for i in sorted(card_indices)]
        
        # Validate that all cards are the same (number and color)
        if len(cards_to_play) > 1:
            first_card = cards_to_play[0]
            
            # Only allow multiple cards for number cards of same color and value
            if first_card.type != CardType.NUMBER:
                return False, "Can only play multiple cards of the same number"
            
            for card in cards_to_play[1:]:
                if (card.type != CardType.NUMBER or 
                    card.color != first_card.color or 
                    card.value != first_card.value):
                    return False, "All cards must be the same number and color"

        # Use the first card for playability check
        first_card = cards_to_play[0]

        # Special case: Allow +2 cards to be played when forced_draw > 0 (stacking rule)
        if self.forced_draw > 0:
            if first_card.type == CardType.DRAW_TWO and len(cards_to_play) == 1:
                # Player can stack a +2 card to pass the draw to the next player
                self.current_color = first_card.color
                self.discard_pile.append(self.players[player_name]["hand"].pop(card_indices[0]))
                self.forced_draw += 2  # Add 2 more cards to the forced draw
                
                if not self.players[player_name]["hand"]:
                    self.winner = player_name
                    return True, f"{player_name} wins!"
                
                self._next_turn()
                return True, None
            else:
                return False, "You must draw cards first or play a single +2 card to stack!"

        if self._is_playable(first_card):
            if first_card.type in (CardType.WILD, CardType.WILD_DRAW) and not chosen_color:
                return False, "Must choose color for wild card"

            # Wild cards can only be played one at a time
            if first_card.type in (CardType.WILD, CardType.WILD_DRAW) and len(cards_to_play) > 1:
                return False, "Can only play one wild card at a time"

            # Set the color based on the card type
            if first_card.type == CardType.WILD or first_card.type == CardType.WILD_DRAW:
                self.current_color = chosen_color
            else:
                self.current_color = first_card.color

            # Remove cards from hand (in reverse order to maintain correct indices)
            for card_index in sorted(card_indices, reverse=True):
                played_card = self.players[player_name]["hand"].pop(card_index)
                self.discard_pile.append(played_card)

            # Handle special card effects (only for the first card since they're all the same)
            self._handle_special_card(first_card)

            if not self.players[player_name]["hand"]:
                self.winner = player_name
                return True, f"{player_name} wins!"

            self._next_turn()
            return True, None

        return False, "Card is not playable"

    def _is_playable(self, card: Card) -> bool:
        """Check if a card can be played on the current top card."""
        top_card = self.discard_pile[-1]

        if card.type in (CardType.WILD, CardType.WILD_DRAW):
            if top_card.type in (CardType.WILD, CardType.WILD_DRAW):
                # Wild cards can always be played on top of wild cards
                return False
            
            return True

        return (    card.color == self.current_color or
                    (card.type == CardType.NUMBER and top_card.type == CardType.NUMBER and card.value == top_card.value) or
                    (card.type != CardType.NUMBER and top_card.type == card.type)
                )

    def _handle_special_card(self, card: Card):
        """Handle the effects of special cards."""
        if card.type == CardType.SKIP:
            self._next_turn()
        elif card.type == CardType.REVERSE:
            self.direction *= -1
        elif card.type == CardType.DRAW_TWO:
            next_player = (self.current_player + self.direction) % len(self.players)
            self.forced_draw = 2
        elif card.type == CardType.WILD_DRAW:
            next_player = (self.current_player + self.direction) % len(self.players)
            self.forced_draw = 4

    def _next_turn(self):
        """Move to the next player's turn."""
        self.current_player = (self.current_player + self.direction) % len(self.players)
        # Note: Don't reset forced_draw here - it should persist until the affected player draws

    def get_current_player(self) -> str:
        """Get the name of the current player."""
        return list(self.players.keys())[self.current_player]

    def get_player_hand(self, player_name: str) -> List[Card]:
        """Get a player's hand."""
        return self.players[player_name]["hand"]

    def get_top_card(self) -> Card:
        """Get the top card of the discard pile."""
        return self.discard_pile[-1]

    def get_player_counts(self) -> Dict[str, int]:
        """Get the number of cards each player has."""
        return {name: len(self.players[name]["hand"]) for name in self.players}

    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.winner is not None
