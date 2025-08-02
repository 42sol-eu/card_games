"""
Card Games Package - Teaching children how to code through game development.

This package contains implementations of popular card games.
"""

__version__ = "0.1.0"
__author__ = "Card Games Project"

from .uno import UnoGame, Card, Color, CardType
from .uno.cli import UnoCLI

# Optional import for UI (requires nicegui)
from .uno import *

try:
    from .uno.ui import UnoUI
    __all__ = ['UnoGame', 'Card', 'Color', 'CardType', 'UnoCLI', 'UnoUI']   
except ImportError:
    __all__ = ['UnoGame', 'Card', 'Color', 'CardType', 'UnoCLI']
