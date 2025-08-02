"""
Game page functionality for UNO game interface.
"""

from nicegui import ui

from .base import UnoUIBase
from .heartbeat import HeartbeatManager
from .game_header import GameHeader
from .card_actions import CardActions, HandDisplay


class GamePage:
    """Handles the main game page where UNO is played."""
    
    def __init__(self, ui_instance: UnoUIBase):
        self.ui = ui_instance
        self.game_header = GameHeader(ui_instance)
        self.card_actions = CardActions(ui_instance)
        self.hand_display = HandDisplay(ui_instance, self.card_actions)
        
        # Connect the draw card action to the header
        self.game_header._draw_card = self.card_actions.draw_card

    def show(self):
        """Stage 3: Game page - Show the actual UNO game for this player."""
        # Check for game over
        if self.ui.game and self.ui.game.is_game_over():
            self._show_winner_page()
            return
        
        # Check if player name is valid
        if not self.ui.player_name or self.ui.player_name not in UnoUIBase._lobby_players:
            self.ui.game_stage = 'landing'
            ui.navigate.to('/')
            return
        
        with ui.column().classes("w-full min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50"):
            
            # Game header container (will be updated)
            game_header_container = ui.column().classes("w-full")
            
            # Main content area container (will be updated)
            main_content_container = ui.column().classes("flex-grow")
            
            def update_game_display():
                """Update the entire game display."""
                # Send heartbeat for current player
                HeartbeatManager.send_heartbeat(self.ui.player_name)
                if self.ui._active_dialog:
                    return
                
                # Check for game over first
                if self.ui.game and self.ui.game.is_game_over():
                    ui.navigate.to(f'/uno-{UnoUIBase._game_hash}')  # This will trigger winner page
                    return
                
                # Update current player
                if self.ui.game:
                    self.ui.current_player = self.ui.game.get_current_player()
                
                # Clear and rebuild header
                game_header_container.clear()
                with game_header_container:
                    self.game_header.create()
                
                # Clear and rebuild main content
                main_content_container.clear()
                with main_content_container:
                    self._create_main_content()
            
            # Initial display
            update_game_display()

            # Auto-refresh 
            ui.timer(2.0, update_game_display)

    def _create_main_content(self):
        """Create the main game content area."""
        with ui.column().classes("flex-grow p-6"):
            # Player status
            is_my_turn = self.ui.current_player == self.ui.player_name
            if is_my_turn:
                ui.label(f"🎯 Your Turn, {self.ui.player_name}!").classes("text-3xl font-bold text-center mb-6 text-green-600 animate-pulse")
                
                # Show forced draw warning for current player
                if self.ui.game.forced_draw > 0:
                    ui.label(f"⚠️ You must draw {self.ui.game.forced_draw} cards or play +2 to stack!").classes("text-xl font-bold text-center mb-4 text-red-600 bg-red-100 p-3 rounded-lg")
            else:
                ui.label(f"🕐 Waiting for {self.ui.current_player}'s turn...").classes("text-2xl font-bold text-center mb-6 text-gray-600")
            
            # Player's hand
            ui.label(f"🎴 Your Hand ({len(self.ui.game.get_player_hand(self.ui.player_name))} cards)").classes("text-xl font-bold mb-4")
            self.hand_display.create_horizontal_hand()

    def _show_winner_page(self):
        """Display winner page."""
        with ui.column().classes("w-full min-h-screen bg-gradient-to-br from-yellow-50 to-orange-50 flex items-center justify-center p-4"):
            with ui.card().classes("w-full max-w-2xl mx-auto p-12 bg-white/90 shadow-2xl text-center"):
                
                ui.html(f"""
                    <div class="mb-8">
                        <h1 class="text-6xl font-bold bg-gradient-to-r from-yellow-400 to-red-500 bg-clip-text text-transparent mb-4">
                            🎉 WINNER! 🎉
                        </h1>
                        <h2 class="text-4xl font-bold text-gray-800 mb-4">
                            {self.ui.game.winner}
                        </h2>
                        <p class="text-xl text-gray-600">Congratulations!</p>
                    </div>
                """)
                
                # Final scores
                with ui.card().classes("p-6 bg-blue-50 mb-6"):
                    ui.label("📊 Final Scores").classes("text-xl font-bold text-center mb-4")
                    
                    player_counts = self.ui.game.get_player_counts()
                    for name, count in player_counts.items():
                        status = "🏆 Winner" if name == self.ui.game.winner else f"{count} cards left"
                        ui.label(f"{name}: {status}").classes("text-lg text-center")
                
                # Action buttons
                with ui.row().classes("gap-4 justify-center"):
                    ui.button("🎮 New Game", on_click=self._new_game).classes("p-3 text-lg font-bold bg-blue-500 text-white hover:bg-blue-600")
                    ui.button("🔄 Play Again", on_click=self._play_again).classes("p-3 text-lg font-bold bg-green-500 text-white hover:bg-green-600")

    def _new_game(self):
        """Start a completely new game."""
        UnoUIBase._game_instance = None
        self.ui.player_name = None
        # Clear global game state
        UnoUIBase._lobby_players.clear()
        UnoUIBase._player_heartbeats.clear()
        UnoUIBase._game_started = False
        UnoUIBase._game_hash = None
        # Redirect to landing page
        ui.navigate.to('/')

    def _play_again(self):
        """Play again with same players."""
        # Reset to lobby with same players
        UnoUIBase._game_started = False
        UnoUIBase._game_hash = None
        UnoUIBase._game_instance = None
        # Reset all players to not ready but keep heartbeats
        for player in UnoUIBase._lobby_players:
            UnoUIBase._lobby_players[player] = False
        ui.navigate.to('/lobby')
