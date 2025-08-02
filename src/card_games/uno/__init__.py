# card_games.uno package

"""
This package contains modules and classes for implementing the Uno card game.
"""

__version__ = "2025.0.1"
__author__ = "42sol.eu"

from .game import UnoGame, Card, Color, CardType
from .cli import UnoCLI

try:
    # Optional import for UI (requires nicegui)
    from .ui import UnoUI
    __all__ = ['UnoGame', 'Card', 'Color', 'CardType', 'UnoCLI', 'UnoUI']
except ImportError:
    __all__ = ['UnoGame', 'Card', 'Color', 'CardType', 'UnoCLI']
    
