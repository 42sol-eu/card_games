"""
Main UNO UI class and application routing.
"""

from nicegui import ui

from .base import UnoUIBase
from .styles import UnoStyles
from .landing import LandingPage
from .lobby import LobbyPage
from .game_page import GamePage


class UnoUI(UnoUIBase):
    """Main UNO UI class that coordinates all pages and functionality."""
    
    def __init__(self):
        super().__init__()
        if ui is None:
            raise ImportError("NiceGUI is required for the UI. Install with: pip install nicegui")
        
        # Set up custom CSS
        UnoStyles.setup_custom_css()
        
        # Initialize page handlers
        self.landing_page = LandingPage(self)
        self.lobby_page = LobbyPage(self)
        self.game_page = GamePage(self)

    def run(self, title: str = "🎮 UNO Game", port: int = 8080, debug: bool = False):
        """Run the UI application."""
        if ui is None:
            raise ImportError("NiceGUI is required for the UI. Install with: pip install nicegui")
        
        # Set up page routes for proper session handling
        @ui.page('/')
        def index_page():
            # Landing page - player name entry
            self.landing_page.show()
        
        @ui.page('/lobby')
        def lobby_page():
            # Check if player has entered name
            if not self.player_name:
                ui.navigate.to('/')
                return
            self.lobby_page.show()
        
        @ui.page('/uno-{game_hash}')
        def game_page(game_hash: str):
            # Check if player is part of this game session
            if not self.player_name or not UnoUIBase._game_started or UnoUIBase._game_hash != game_hash:
                ui.navigate.to('/lobby')
                return
            
            if self.game and self.game.is_game_over():
                self.game_page._show_winner_page()
            else:
                self.game_page.show()
        
        # Run the application
        ui.run(
            title=title,
            port=port,
            show=False,
            reload=debug,
            favicon="🎮",
            storage_secret="uno_game_secret_key_2024"  # Required for session storage
        )


def main():
    """Main entry point for the UI."""
    ui_app = UnoUI()
    ui_app.run()


if __name__ == "__main__":
    main()
