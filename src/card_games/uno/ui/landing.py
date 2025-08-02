"""
Landing page functionality for UNO game interface.
"""

import time
from nicegui import ui

from .base import UnoUIBase
from .heartbeat import HeartbeatManager


class LandingPage:
    """Handles the landing page where players enter their names."""
    
    def __init__(self, ui_instance: UnoUIBase):
        self.ui = ui_instance

    def show(self):
        """Stage 1: Landing page - Choose a player name."""
        # Create main container for this session
        with ui.column().classes("w-full min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4"):
            with ui.card().classes("w-full max-w-lg mx-auto p-8 bg-white/90 backdrop-blur-sm shadow-2xl"):
                # Game title
                ui.html("""
                    <div class="text-center mb-8">
                        <h1 class="text-6xl font-bold bg-gradient-to-r from-red-500 via-blue-500 to-green-500 bg-clip-text text-transparent mb-4">
                             UNO GAME - Landing Page
                        </h1>
                        <p class="text-xl text-gray-600">Enter your name to join the game</p>
                    </div>
                """)

                # Name input
                name_input = ui.input(
                    label="🎯 Your Name",
                    placeholder="Enter your player name"
                ).classes("w-full mb-4").props("outlined")

                def join_lobby():
                    name = name_input.value.strip()
                    if not name:
                        ui.notify("Please enter your name!", type='warning')
                        return
                    
                    if name in UnoUIBase._lobby_players:
                        ui.notify("Name already taken! Choose another name.", type='warning')
                        return
                    
                    # Add player to lobby
                    self.ui.player_name = name
                    UnoUIBase._lobby_players[name] = False  # Not ready yet
                    HeartbeatManager.send_heartbeat(name)  # Initialize heartbeat
                    self.ui.game_stage = 'lobby'
                    
                    ui.notify(f"Welcome {name}! Joining lobby...", type='positive')
                    # Navigate to lobby page
                    ui.navigate.to('/lobby')

                # Join button
                ui.button(
                    "🚀 Join Game Lobby", 
                    on_click=join_lobby
                ).classes("w-full p-4 text-xl font-bold bg-gradient-to-r from-green-500 to-blue-500 text-white hover:from-green-600 hover:to-blue-600 transition-all duration-300")
