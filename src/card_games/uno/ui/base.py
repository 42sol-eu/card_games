"""
Base UI class and shared utilities for UNO game interface.
"""

from typing import Optional
from nicegui import ui, app

from ..game import UnoGame, Card, Color, CardType


class UnoUIBase:
    """Base class for UNO UI with shared state and utilities."""
    
    # Global game state (shared across all sessions)
    _lobby_players = {}  # {player_name: ready_status}
    _player_heartbeats = {}  # {player_name: last_heartbeat_timestamp}
    _game_started = False
    _game_hash = None  # Current game session hash
    _game_instance = None  # Shared game instance
    _heartbeat_timeout = 30  # Remove players after 30 seconds of inactivity
    
    def __init__(self):
        self._active_dialog = False
        self.current_player = None
        
        # Color mappings for beautiful card styling
        self.color_styles = {
            Color.RED: {"bg": "bg-red-500", "text": "text-white", "border": "border-red-600"},
            Color.BLUE: {"bg": "bg-blue-500", "text": "text-white", "border": "border-blue-600"},
            Color.GREEN: {"bg": "bg-green-500", "text": "text-white", "border": "border-green-600"},
            Color.YELLOW: {"bg": "bg-yellow-400", "text": "text-black", "border": "border-yellow-500"},
            Color.WILD: {"bg": "bg-gradient-to-br from-purple-500 to-pink-500", "text": "text-white", "border": "border-purple-600"}
        }
    
    @property
    def game(self):
        """Get the shared game instance."""
        return UnoUIBase._game_instance
    
    @game.setter
    def game(self, value):
        """Set the shared game instance."""
        UnoUIBase._game_instance = value
    
    @property
    def player_name(self):
        """Get the player name for this session."""
        return app.storage.user.get('player_name')
    
    @player_name.setter
    def player_name(self, value):
        """Set the player name for this session."""
        app.storage.user['player_name'] = value
    
    @property
    def game_stage(self):
        """Get the current game stage for this session."""
        return app.storage.user.get('game_stage', 'landing')  # landing, lobby, game
    
    @game_stage.setter
    def game_stage(self, value):
        """Set the current game stage for this session."""
        app.storage.user['game_stage'] = value

    def update_game_state(self):
        """Update the game state and refresh UI."""
        if self.game and not self.game.is_game_over():
            self.current_player = self.game.get_current_player()
        # The timer will handle the UI refresh automatically
