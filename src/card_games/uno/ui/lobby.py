"""
Lobby page functionality for UNO game interface.
"""

import hashlib
import time
from nicegui import ui

from .base import UnoUIBase
from .heartbeat import HeartbeatManager
from .components import DialogComponents
from ..game import UnoGame


class LobbyPage:
    """Handles the lobby page where players ready up and start games."""
    
    def __init__(self, ui_instance: UnoUIBase):
        self.ui = ui_instance

    def show(self):
        """Stage 2: Lobby page - Show players and ready status."""
        # Ensure current player is in the lobby dict
        if self.ui.player_name and self.ui.player_name not in UnoUIBase._lobby_players:
            UnoUIBase._lobby_players[self.ui.player_name] = False
            HeartbeatManager.send_heartbeat(self.ui.player_name)
            
        with ui.column().classes("w-full min-h-screen bg-gradient-to-br from-purple-50 to-pink-50 p-4"):
            with ui.card().classes("w-full max-w-2xl mx-auto p-8 bg-white/90 backdrop-blur-sm shadow-2xl"):
                ui.html("""
                    <div class="text-center mb-8">
                        <h1 class="text-4xl font-bold bg-gradient-to-r from-purple-500 to-pink-500 bg-clip-text text-transparent mb-4">
                            🎮 Game Lobby 🎮
                        </h1>
                        <p class="text-lg text-gray-600">Players joining the game</p>
                    </div>
                """)

                # Player status
                ui.label(f"Welcome, {self.ui.player_name}!").classes("text-2xl font-bold text-center mb-6 text-purple-600")
                
                # Players list container
                players_container = ui.column().classes("w-full mb-6")
                
                # Ready button for this player
                ready_button_container = ui.row().classes("w-full justify-center mb-4")
                
                # Start game button (only visible if conditions are met)
                start_button_container = ui.row().classes("w-full justify-center")
                
                def clear_lobby():
                    """Clear all players from lobby with confirmation."""
                    def confirm_clear():
                        UnoUIBase._lobby_players.clear()
                        UnoUIBase._player_heartbeats.clear()
                        ui.notify("Cleared all players from lobby", type='info')
                        self.ui._active_dialog = False
                        update_lobby_display()
                    
                    def cancel_clear():
                        self.ui._active_dialog = False
                    
                    self.ui._active_dialog = True
                    dialog = DialogComponents.create_confirmation_dialog(
                        "Clear all players from lobby?",
                        "This will remove all players including yourself.",
                        confirm_clear,
                        cancel_clear
                    )
                    dialog.open()
                
                def update_lobby_display():
                    """Update the lobby display with current players."""
                    # Send heartbeat for current player
                    HeartbeatManager.send_heartbeat(self.ui.player_name)
                    
                    # Remove inactive players
                    players_removed = HeartbeatManager.remove_inactive_players()
                    
                    # Safety check: if current player was removed, re-add them
                    if self.ui.player_name and self.ui.player_name not in UnoUIBase._lobby_players:
                        UnoUIBase._lobby_players[self.ui.player_name] = False
                        HeartbeatManager.send_heartbeat(self.ui.player_name)
                        ui.notify(f"Re-added {self.ui.player_name} to lobby", type='info')
                    
                    players_container.clear()
                    ready_button_container.clear()
                    start_button_container.clear()
                    
                    self._create_players_list(players_container)
                    self._create_ready_button(ready_button_container, update_lobby_display)
                    self._create_start_button(start_button_container, clear_lobby)

                # Initial display
                update_lobby_display()
                
                # Auto-refresh every 2 seconds
                ui.timer(2.0, update_lobby_display)

    def _create_players_list(self, container):
        """Create the players list display."""
        with container:
            ui.label("Players in Lobby:").classes("text-xl font-bold mb-4")
            ui.label(f"⏰ Auto-remove inactive players after {UnoUIBase._heartbeat_timeout} seconds").classes("text-sm text-gray-500 mb-4")
            
            for player, ready in UnoUIBase._lobby_players.items():
                status_icon = "✅" if ready else "⏳"
                status_text = "Ready" if ready else "Not Ready"
                color_class = "text-green-600" if ready else "text-orange-600"
                
                # Check connection status
                connection_icon, connection_text = HeartbeatManager.get_connection_status(player)
                
                # Create a row for each player with status and remove button
                with ui.row().classes("w-full items-center justify-between mb-2 p-2 bg-gray-50 rounded-lg"):
                    with ui.column().classes("flex-grow"):
                        ui.label(f"{status_icon} {player} - {status_text}").classes(f"text-lg {color_class}")
                        ui.label(f"{connection_icon} {connection_text}").classes("text-xs text-gray-500")
                    
                    # Remove button (only for other players, not yourself)
                    if player != self.ui.player_name:
                        self._create_remove_button(player)
                    else:
                        # Empty space to maintain alignment
                        ui.label("").classes("w-16")

    def _create_remove_button(self, player_to_remove: str):
        """Create remove button for a player."""
        def remove_player():
            def confirm_remove():
                if player_to_remove in UnoUIBase._lobby_players:
                    del UnoUIBase._lobby_players[player_to_remove]
                if player_to_remove in UnoUIBase._player_heartbeats:
                    del UnoUIBase._player_heartbeats[player_to_remove]
                ui.notify(f"Removed {player_to_remove} from lobby", type='info')
                self.ui._active_dialog = False
            
            def cancel_remove():
                self.ui._active_dialog = False
            
            self.ui._active_dialog = True
            dialog = DialogComponents.create_confirmation_dialog(
                f"Remove {player_to_remove} from lobby?",
                None,
                confirm_remove,
                cancel_remove
            )
            dialog.open()
        
        ui.button(
            "🗑️ Remove",
            on_click=remove_player
        ).classes("bg-red-400 hover:bg-red-500 text-white text-sm px-2 py-1 rounded")

    def _create_ready_button(self, container, update_callback):
        """Create the ready button for the current player."""
        with container:
            current_ready = UnoUIBase._lobby_players.get(self.ui.player_name, False)
            
            def toggle_ready():
                # Ensure player is in lobby dict
                if self.ui.player_name not in UnoUIBase._lobby_players:
                    UnoUIBase._lobby_players[self.ui.player_name] = False
                
                UnoUIBase._lobby_players[self.ui.player_name] = not UnoUIBase._lobby_players[self.ui.player_name]
                ui.notify(f"You are {'ready' if UnoUIBase._lobby_players[self.ui.player_name] else 'not ready'}!", type='positive')
                update_callback()
            
            button_text = "❌ Not Ready" if current_ready else "✅ Ready Up"
            button_class = "bg-red-500 hover:bg-red-600" if current_ready else "bg-green-500 hover:bg-green-600"
            
            ui.button(
                button_text,
                on_click=toggle_ready
            ).classes(f"p-3 text-lg font-bold {button_class} text-white transition-all duration-300")

    def _create_start_button(self, container, clear_lobby_callback):
        """Create the start game button."""
        with container:
            ready_players = [name for name, ready in UnoUIBase._lobby_players.items() if ready]
            
            if len(ready_players) >= 2 and len(ready_players) == len(UnoUIBase._lobby_players):
                def start_game():
                    # Create game with ready players
                    player_names = list(UnoUIBase._lobby_players.keys())
                    self.ui.game = UnoGame(player_names)
                    UnoUIBase._game_started = True
                    self.ui.current_player = self.ui.game.get_current_player()
                    
                    # Generate unique game hash
                    game_data = f"{'-'.join(sorted(player_names))}-{int(time.time())}"
                    UnoUIBase._game_hash = hashlib.md5(game_data.encode()).hexdigest()[:8]
                    
                    self.ui.game_stage = 'game'
                    
                    ui.notify("Game starting!", type='positive')
                    ui.navigate.to(f'/uno-{UnoUIBase._game_hash}')  # Navigate to game page
                
                ui.button(
                    f"🎮 Start Game ({len(ready_players)} players)",
                    on_click=start_game
                ).classes("p-4 text-xl font-bold bg-gradient-to-r from-blue-500 to-purple-500 text-white hover:from-blue-600 hover:to-purple-600 transition-all duration-300")
            
            elif len(UnoUIBase._lobby_players) < 2:
                ui.label("Need at least 2 players to start").classes("text-lg text-gray-600 italic")
                
                # Add clear lobby button if there are players but not enough
                if len(UnoUIBase._lobby_players) > 0:
                    ui.button(
                        "🧹 Clear All Players",
                        on_click=clear_lobby_callback
                    ).classes("p-2 text-sm font-bold bg-gray-400 hover:bg-gray-500 text-white transition-all duration-300 mt-2")
            
            else:
                not_ready = [name for name, ready in UnoUIBase._lobby_players.items() if not ready]
                ui.label(f"Waiting for: {', '.join(not_ready)}").classes("text-lg text-orange-600")
                
                # Add clear lobby button for lobby management
                ui.button(
                    "🧹 Clear All Players",
                    on_click=clear_lobby_callback
                ).classes("p-2 text-sm font-bold bg-gray-400 hover:bg-gray-500 text-white transition-all duration-300 mt-2")
