from enum import Enum, auto

class Color(Enum):
    RED = auto()
    BLUE = auto()
    GREEN = auto()
    YELLOW = auto()
    BLACK = auto()
    
class CardType(Enum):
    NUMBER = auto()
    SKIP = auto()
    REVERSE = auto()
    DRAW_TWO = auto()
    WILD = auto()
    WILD_DRAW = auto()

class Card:
    def __init__(self, color: Color, card_type: CardType, value: int = None):
        self.color = color
        self.card_type = card_type
        self.value = value  # For NUMBER cards, value is the number; otherwise, None

    def __str__(self):
        if self.card_type == CardType.NUMBER:
            return f"[{self.value} {self.color.name}]"
        return f"[{self.card_type.name} {self.color.name}]"

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return (self.color == other.color and 
                self.card_type == other.card_type and 
                self.value == other.value)
        
    def __repr__(self):
        if self.card_type == CardType.NUMBER:
            return f"<Card {self.color.name} {self.value}>"
        return f"<Card {self.color.name} {self.card_type.name}>"
    
    def is_wild(self):
        return self.card_type in (CardType.WILD, CardType.WILD_DRAW)
    
    def can_be_played_on(self, top_card):
        if self.is_wild():
            return True
        if top_card.is_wild():
            return True
        return  (   self.color == top_card.color or 
                    self.card_type == top_card.card_type or 
                    (   self.card_type == CardType.NUMBER and 
                        top_card.card_type == CardType.NUMBER and 
                        self.value == top_card.value
                    )
                )
                
        