"""
Simplified UNO game user interface using NiceGUI.

This module provides a beautiful web-based UI for playing Uno games with 
enhanced styling and smooth gameplay.
"""

import sys
import os
import hashlib
import time
from typing import List, Optional

try:
    from nicegui import ui, app
except ImportError:
    print("NiceGUI not installed. Install with: pip install nicegui")
    ui = None
    app = None

# Handle imports for both module and standalone execution
try:
    from .game import UnoGame, Card, Color, CardType
except ImportError:
    try:
        from game import UnoGame, Card, Color, CardType
    except ImportError:
        # If running as standalone, try to import from parent directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        from uno.game import UnoGame, Card, Color, CardType


class UnoUI:
    """Simple but beautiful web-based user interface for Uno game."""
    
    def __init__(self):
        if ui is None:
            raise ImportError("NiceGUI is required for the UI. Install with: pip install nicegui")
        self._active_dialog = False
        # Global game state (shared across all sessions)
        if not hasattr(UnoUI, '_lobby_players'):
            UnoUI._lobby_players = {}  # {player_name: ready_status}
            UnoUI._player_heartbeats = {}  # {player_name: last_heartbeat_timestamp}
            UnoUI._game_started = False
            UnoUI._game_hash = None  # Current game session hash
            UnoUI._game_instance = None  # Shared game instance
            UnoUI._heartbeat_timeout = 30  # Remove players after 30 seconds of inactivity
        
        self.current_player = None
        
        # Color mappings for beautiful card styling
        self.color_styles = {
            Color.RED: {"bg": "bg-red-500", "text": "text-white", "border": "border-red-600"},
            Color.BLUE: {"bg": "bg-blue-500", "text": "text-white", "border": "border-blue-600"},
            Color.GREEN: {"bg": "bg-green-500", "text": "text-white", "border": "border-green-600"},
            Color.YELLOW: {"bg": "bg-yellow-400", "text": "text-black", "border": "border-yellow-500"},
            Color.WILD: {"bg": "bg-gradient-to-br from-purple-500 to-pink-500", "text": "text-white", "border": "border-purple-600"}
        }
        self._setup_custom_css()
    
    @property
    def game(self):
        """Get the shared game instance."""
        return UnoUI._game_instance
    
    @game.setter
    def game(self, value):
        """Set the shared game instance."""
        UnoUI._game_instance = value
    
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

    def _setup_custom_css(self):
        """Add custom CSS for enhanced card animations and styling."""
        ui.add_head_html("""
        <style>
            .uno-card {
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                cursor: pointer;
                border-radius: 12px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                margin: 0 4px;
            }
            
            .uno-card:hover {
                transform: translateY(-8px) scale(1.05);
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
                z-index: 10;
            }
            
            .uno-card-disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            
            .uno-card-disabled:hover {
                transform: none;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            
            .card-row {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 8px;
                padding: 20px;
                min-height: 200px;
            }
            
            .game-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 0 0 20px 20px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }
            
            .wild-card-gradient {
                background: linear-gradient(45deg, #ef4444, #3b82f6, #10b981, #f59e0b);
                background-size: 300% 300%;
                animation: gradientShift 3s ease infinite;
            }
            
            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            .player-turn-glow {
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0%, 100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7); }
                50% { box-shadow: 0 0 0 8px rgba(59, 130, 246, 0); }
            }
        </style>
        """)

    def _send_heartbeat(self):
        """Send heartbeat for current player to show they're still active."""
        if self.player_name:
            UnoUI._player_heartbeats[self.player_name] = time.time()

    def _remove_inactive_players(self):
        """Remove players who haven't sent a heartbeat in the timeout period."""
        current_time = time.time()
        inactive_players = []
        
        for player_name, last_heartbeat in UnoUI._player_heartbeats.items():
            if current_time - last_heartbeat > UnoUI._heartbeat_timeout:
                inactive_players.append(player_name)
        
        for player_name in inactive_players:
            if player_name in UnoUI._lobby_players:
                del UnoUI._lobby_players[player_name]
            if player_name in UnoUI._player_heartbeats:
                del UnoUI._player_heartbeats[player_name]
            
            # Don't show notification for every inactive player removal
            # as it could be noisy - just clean them up silently
        
        return len(inactive_players) > 0  # Return True if any players were removed

    def _show_landing_page(self):
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
                    
                    if name in UnoUI._lobby_players:
                        
                        ui.notify("Name already taken! Choose another name.", type='warning')
                        
                        return
                    
                    # Add player to lobby
                    self.player_name = name
                    UnoUI._lobby_players[name] = False  # Not ready yet
                    UnoUI._player_heartbeats[name] = time.time()  # Initialize heartbeat
                    self.game_stage = 'lobby'
                    
                    ui.notify(f"Welcome {name}! Joining lobby...", type='positive')
                    # Navigate to lobby page
                    ui.navigate.to('/lobby')

                # Join button
                ui.button(
                    "🚀 Join Game Lobby", 
                    on_click=join_lobby
                ).classes("w-full p-4 text-xl font-bold bg-gradient-to-r from-green-500 to-blue-500 text-white hover:from-green-600 hover:to-blue-600 transition-all duration-300")

    def _show_lobby_page(self):
        """Stage 2: Lobby page - Show players and ready status."""
        # Ensure current player is in the lobby dict
        if self.player_name and self.player_name not in UnoUI._lobby_players:
            UnoUI._lobby_players[self.player_name] = False
            UnoUI._player_heartbeats[self.player_name] = time.time()  # Initialize heartbeat
            
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
                ui.label(f"Welcome, {self.player_name}!").classes("text-2xl font-bold text-center mb-6 text-purple-600")
                
                # Players list container
                players_container = ui.column().classes("w-full mb-6")
                
                # Ready button for this player
                ready_button_container = ui.row().classes("w-full justify-center mb-4")
                
                # Start game button (only visible if conditions are met)
                start_button_container = ui.row().classes("w-full justify-center")
                
                def clear_lobby():
                    """Clear all players from lobby with confirmation."""
                    with ui.dialog() as dialog, ui.card():
                        self._active_dialog = True
                        ui.label("Clear all players from lobby?").classes("text-lg font-bold mb-4")
                        ui.label("This will remove all players including yourself.").classes("text-sm text-gray-600 mb-4")
                        with ui.row().classes("gap-4"):
                            def confirm_clear():
                                UnoUI._lobby_players.clear()
                                UnoUI._player_heartbeats.clear()
                                ui.notify("Cleared all players from lobby", type='info')
                                self._active_dialog = False
                                update_lobby_display()
                                dialog.close()
                            
                            ui.button("Yes, Clear All", on_click=confirm_clear).classes("bg-red-500 text-white")
                            ui.button("Cancel", on_click=dialog.close).classes("bg-gray-500 text-white")
                    dialog.open()
                
                def update_lobby_display():
                    """Update the lobby display with current players."""
                    # Send heartbeat for current player
                    self._send_heartbeat()
                    
                    # Remove inactive players
                    players_removed = self._remove_inactive_players()
                    
                    # Safety check: if current player was removed, re-add them
                    if self.player_name and self.player_name not in UnoUI._lobby_players:
                        UnoUI._lobby_players[self.player_name] = False
                        UnoUI._player_heartbeats[self.player_name] = time.time()
                        ui.notify(f"Re-added {self.player_name} to lobby", type='info')
                    
                    players_container.clear()
                    ready_button_container.clear()
                    start_button_container.clear()
                    
                    with players_container:
                        ui.label("Players in Lobby:").classes("text-xl font-bold mb-4")
                        ui.label(f"⏰ Auto-remove inactive players after {UnoUI._heartbeat_timeout} seconds").classes("text-sm text-gray-500 mb-4")
                        
                        current_time = time.time()
                        for player, ready in UnoUI._lobby_players.items():
                            status_icon = "✅" if ready else "⏳"
                            status_text = "Ready" if ready else "Not Ready"
                            color_class = "text-green-600" if ready else "text-orange-600"
                            
                            # Check connection status
                            last_heartbeat = UnoUI._player_heartbeats.get(player, 0)
                            time_since_heartbeat = current_time - last_heartbeat
                            
                            # Add connection indicator
                            if time_since_heartbeat > UnoUI._heartbeat_timeout * 0.7:  # 70% of timeout
                                connection_icon = "🔴"  # Red for poor connection
                                connection_text = "Poor Connection"
                            elif time_since_heartbeat > UnoUI._heartbeat_timeout * 0.4:  # 40% of timeout
                                connection_icon = "🟡"  # Yellow for weak connection
                                connection_text = "Weak Connection"
                            else:
                                connection_icon = "🟢"  # Green for good connection
                                connection_text = "Connected"
                            
                            # Create a row for each player with status and remove button
                            with ui.row().classes("w-full items-center justify-between mb-2 p-2 bg-gray-50 rounded-lg"):
                                with ui.column().classes("flex-grow"):
                                    ui.label(f"{status_icon} {player} - {status_text}").classes(f"text-lg {color_class}")
                                    ui.label(f"{connection_icon} {connection_text}").classes("text-xs text-gray-500")
                                
                                # Remove button (only for other players, not yourself)
                                if player != self.player_name:
                                    def remove_player(player_to_remove=player):
                                        with ui.dialog() as dialog, ui.card():
                                            self._active_dialog = True

                                            ui.label(f"Remove {player_to_remove} from lobby?").classes("text-lg font-bold mb-4")
                                            with ui.row().classes("gap-4"):
                                                def confirm_remove():
                                                    if player_to_remove in UnoUI._lobby_players:
                                                        del UnoUI._lobby_players[player_to_remove]
                                                    if player_to_remove in UnoUI._player_heartbeats:
                                                        del UnoUI._player_heartbeats[player_to_remove]
                                                    ui.notify(f"Removed {player_to_remove} from lobby", type='info')
                                                    self._active_dialog = False

                                                    update_lobby_display()
                                                    dialog.close()
                                                
                                                ui.button("Yes, Remove", on_click=confirm_remove).classes("bg-red-500 text-white")
                                                ui.button("Cancel", on_click=dialog.close).classes("bg-gray-500 text-white")
                                        dialog.open()
                                    
                                    ui.button(
                                        "🗑️ Remove",
                                        on_click=remove_player
                                    ).classes("bg-red-400 hover:bg-red-500 text-white text-sm px-2 py-1 rounded")
                                else:
                                    # Empty space to maintain alignment
                                    ui.label("").classes("w-16")
                    
                    # Ready button for current player
                    with ready_button_container:
                        current_ready = UnoUI._lobby_players.get(self.player_name, False)
                        
                        def toggle_ready():
                            # Ensure player is in lobby dict
                            if self.player_name not in UnoUI._lobby_players:
                                UnoUI._lobby_players[self.player_name] = False
                            
                            UnoUI._lobby_players[self.player_name] = not UnoUI._lobby_players[self.player_name]
                            ui.notify(f"You are {'ready' if UnoUI._lobby_players[self.player_name] else 'not ready'}!", type='positive')
                            update_lobby_display()
                        
                        button_text = "❌ Not Ready" if current_ready else "✅ Ready Up"
                        button_class = "bg-red-500 hover:bg-red-600" if current_ready else "bg-green-500 hover:bg-green-600"
                        
                        ui.button(
                            button_text,
                            on_click=toggle_ready
                        ).classes(f"p-3 text-lg font-bold {button_class} text-white transition-all duration-300")
                    
                    # Start game button (only if 2+ players and all ready)
                    with start_button_container:
                        ready_players = [name for name, ready in UnoUI._lobby_players.items() if ready]
                        
                        if len(ready_players) >= 2 and len(ready_players) == len(UnoUI._lobby_players):
                            def start_game():
                                # Create game with ready players
                                player_names = list(UnoUI._lobby_players.keys())
                                self.game = UnoGame(player_names)
                                UnoUI._game_started = True
                                self.current_player = self.game.get_current_player()
                                
                                # Generate unique game hash
                                game_data = f"{'-'.join(sorted(player_names))}-{int(time.time())}"
                                UnoUI._game_hash = hashlib.md5(game_data.encode()).hexdigest()[:8]
                                
                                self.game_stage = 'game'
                                
                                ui.notify("Game starting!", type='positive')
                                ui.navigate.to(f'/uno-{UnoUI._game_hash}')  # Navigate to game page
                            
                            ui.button(
                                f"🎮 Start Game ({len(ready_players)} players)",
                                on_click=start_game
                            ).classes("p-4 text-xl font-bold bg-gradient-to-r from-blue-500 to-purple-500 text-white hover:from-blue-600 hover:to-purple-600 transition-all duration-300")
                        
                        elif len(UnoUI._lobby_players) < 2:
                            ui.label("Need at least 2 players to start").classes("text-lg text-gray-600 italic")
                            
                            # Add clear lobby button if there are players but not enough
                            if len(UnoUI._lobby_players) > 0:
                                ui.button(
                                    "🧹 Clear All Players",
                                    on_click=clear_lobby
                                ).classes("p-2 text-sm font-bold bg-gray-400 hover:bg-gray-500 text-white transition-all duration-300 mt-2")
                        
                        else:
                            not_ready = [name for name, ready in UnoUI._lobby_players.items() if not ready]
                            ui.label(f"Waiting for: {', '.join(not_ready)}").classes("text-lg text-orange-600")
                            
                            # Add clear lobby button for lobby management
                            ui.button(
                                "🧹 Clear All Players",
                                on_click=clear_lobby
                            ).classes("p-2 text-sm font-bold bg-gray-400 hover:bg-gray-500 text-white transition-all duration-300 mt-2")

                # Initial display
                update_lobby_display()
                
                # Auto-refresh every
                ui.timer(2.0, update_lobby_display)

    def _show_game_page(self):
        """Stage 3: Game page - Show the actual UNO game for this player."""
        # Check for game over
        if self.game and self.game.is_game_over():
            self._show_winner_page()
            return
        
        # Check if player name is valid
        if not self.player_name or self.player_name not in UnoUI._lobby_players:
            self.game_stage = 'landing'
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
                self._send_heartbeat()
                if self._active_dialog:
                    return
                
                # Check for game over first
                if self.game and self.game.is_game_over():
                    ui.navigate.to(f'/uno-{UnoUI._game_hash}')  # This will trigger winner page
                    return
                
                # Update current player
                if self.game:
                    self.current_player = self.game.get_current_player()
                
                # Clear and rebuild header
                game_header_container.clear()
                with game_header_container:
                    self._create_game_header()
                
                # Clear and rebuild main content
                main_content_container.clear()
                with main_content_container:
                    with ui.column().classes("flex-grow p-6"):
                        # Player status
                        is_my_turn = self.current_player == self.player_name
                        if is_my_turn:
                            ui.label(f"🎯 Your Turn, {self.player_name}!").classes("text-3xl font-bold text-center mb-6 text-green-600 animate-pulse")
                            
                            # Show forced draw warning for current player
                            if self.game.forced_draw > 0:
                                ui.label(f"⚠️ You must draw {self.game.forced_draw} cards or play +2 to stack!").classes("text-xl font-bold text-center mb-4 text-red-600 bg-red-100 p-3 rounded-lg")
                        else:
                            ui.label(f"🕐 Waiting for {self.current_player}'s turn...").classes("text-2xl font-bold text-center mb-6 text-gray-600")
                        
                        # Player's hand
                        ui.label(f"🎴 Your Hand ({len(self.game.get_player_hand(self.player_name))} cards)").classes("text-xl font-bold mb-4")
                        self._create_horizontal_hand()
            
            # Initial display
            update_game_display()

            # Auto-refresh 
            ui.timer(2.0, update_game_display)

    def _create_game_header(self):
        """Create the header with game information."""
        with ui.element('div').classes("game-header"):
            with ui.row().classes("w-full items-center justify-between"):
                
                # Left side - Current player and direction
                with ui.column().classes("gap-2"):
                    ui.label(f"🎯 Current Turn").classes("text-lg font-semibold opacity-80")
                    ui.label(f"{self.current_player}").classes("text-2xl font-bold")
                    
                    direction_icon = "↻" if self.game.direction == 1 else "↺"
                    ui.label(f"Direction: {direction_icon}").classes("text-lg")
                
                # Center - Top card and recent played cards
                with ui.column().classes("items-center gap-2"):
                    ui.label("🎯 Current Card").classes("text-lg font-semibold opacity-80")
                    self._create_header_top_card()
                    
                    # Show recent played cards (discard pile preview)
                    if len(self.game.discard_pile) > 1:
                        ui.label("📚 Recent Cards").classes("text-sm font-semibold opacity-70 mt-2")
                        self._create_discard_pile_preview()
                
                # Right side - Other players and draw pile
                with ui.column().classes("gap-2 items-end"):
                    ui.label("👥 Other Players").classes("text-lg font-semibold opacity-80")
                    
                    # Other players info (compact)
                    player_counts = self.game.get_player_counts()
                    other_players = [(name, count) for name, count in player_counts.items() if name != self.player_name]
                    
                    for name, count in other_players:
                        player_class = "text-lg font-bold" + (" text-yellow-300" if count == 1 else " text-white")
                        status = "🚨 UNO!" if count == 1 else f"{count} cards"
                        ui.label(f"{name}: {status}").classes(player_class)
                    
                    # Controls row
                    with ui.row().classes("items-center gap-2 mt-2"):
                        ui.label("🂠 Draw Pile").classes("text-sm opacity-80")
                        ui.button(f"Draw ({len(self.game.draw_pile)})", on_click=self._draw_card).classes("bg-white/20 hover:bg-white/30 text-white font-bold py-2 px-4 rounded-lg")
                        ui.button("📚 Show All Cards", on_click=self._show_discard_pile).classes("bg-white/20 hover:bg-white/30 text-white font-bold py-2 px-4 rounded-lg")
                        ui.button("🔄 Back to Lobby", on_click=self._back_to_lobby).classes("bg-white/20 hover:bg-white/30 text-white font-bold py-2 px-4 rounded-lg")

    def _back_to_lobby(self):
        """Return to lobby page."""
        self.game_stage = 'lobby'
        ui.navigate.to('/lobby')

    def _create_discard_pile_preview(self):
        """Create a small preview of recent cards in the discard pile."""
        # Show last 3-4 cards (excluding the top card which is shown separately)
        recent_cards = self.game.discard_pile[-5:-1] if len(self.game.discard_pile) > 4 else self.game.discard_pile[:-1]
        recent_cards.reverse()  # Show most recent first
        
        with ui.row().classes("gap-1 justify-center"):
            for i, card in enumerate(recent_cards):
                if i >= 4:  # Limit to 4 cards max
                    break
                self._create_mini_card(card, i)

    def _create_mini_card(self, card: Card, index: int):
        """Create a very small card display for the discard pile preview."""
        style = self.color_styles.get(card.color, self.color_styles[Color.RED])
        
        if card.color == Color.WILD:
            if hasattr(self.game, 'card_colors') and card in self.game.card_colors:
                # If we track what color wild cards were played as, use that
                chosen_color = self.game.card_colors.get(card)
                if chosen_color:
                    chosen_style = self.color_styles.get(chosen_color, self.color_styles[Color.RED])
                    card_class = f"w-8 h-12 {chosen_style['bg']} {chosen_style['text']} rounded text-xs flex items-center justify-center border"
                else:
                    card_class = "w-8 h-12 wild-card-gradient text-white rounded text-xs flex items-center justify-center border"
            else:
                card_class = "w-8 h-12 wild-card-gradient text-white rounded text-xs flex items-center justify-center border"
        else:
            card_class = f"w-8 h-12 {style['bg']} {style['text']} rounded text-xs flex items-center justify-center border {style['border']}"
        
        with ui.card().classes(card_class):
            ui.label(self._get_mini_card_text(card)).classes("font-bold")

    def _get_mini_card_text(self, card: Card) -> str:
        """Get abbreviated text for mini cards."""
        if card.type == CardType.NUMBER:
            return str(card.value)
        elif card.type == CardType.WILD:
            return "🌈"
        elif card.type == CardType.WILD_DRAW:
            return "+4"
        elif card.type == CardType.DRAW_TWO:
            return "+2"
        elif card.type == CardType.SKIP:
            return "⊘"
        elif card.type == CardType.REVERSE:
            return "⟲"
        else:
            return "?"

    def _show_discard_pile(self):
        """Show the full discard pile in a dialog."""
        self._active_dialog = True
        
        with ui.dialog() as dialog, ui.card().classes("w-full max-w-4xl p-6"):
            ui.label("📚 All Played Cards").classes("text-2xl font-bold text-center mb-4")
            ui.label(f"Total cards played: {len(self.game.discard_pile)}").classes("text-lg text-center mb-4 text-gray-600")
            
            # Show cards in reverse order (most recent first)
            discard_cards = list(reversed(self.game.discard_pile))
            
            with ui.scroll_area().classes("w-full h-96"):
                with ui.grid(columns=8).classes("gap-2 p-4"):
                    for i, card in enumerate(discard_cards):
                        self._create_discard_card(card, len(discard_cards) - i)  # Show position from start
            
            with ui.row().classes("w-full justify-center mt-4"):
                def close_dialog():
                    self._active_dialog = False
                    dialog.close()
                
                ui.button("Close", on_click=close_dialog).classes("bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded")
        
        dialog.open()

    def _create_discard_card(self, card: Card, play_number: int):
        """Create a card display for the discard pile dialog."""
        style = self.color_styles.get(card.color, self.color_styles[Color.RED])
        
        if card.color == Color.WILD:
            # For wild cards in discard pile, try to show with the color it was played as
            card_class = "w-16 h-24 wild-card-gradient text-white rounded-lg shadow flex flex-col items-center justify-center border-2 border-purple-300"
        else:
            card_class = f"w-16 h-24 {style['bg']} {style['text']} rounded-lg shadow flex flex-col items-center justify-center border-2 {style['border']}"
        
        with ui.card().classes(card_class):
            # Play order number (small, at top)
            ui.label(f"#{play_number}").classes("text-xs opacity-70")
            
            # Card display
            ui.label(self._get_card_display_text(card)).classes("text-lg font-bold")
            
            # Color (small, at bottom)
            if card.color != Color.WILD:
                ui.label(card.color.value[:1].upper()).classes("text-xs font-semibold")
            else:
                ui.label("W").classes("text-xs font-semibold")

    def _create_header_top_card(self):
        """Create a compact top card display for the header."""
        top_card = self.game.get_top_card()
        style = self.color_styles.get(top_card.color, self.color_styles[Color.RED])
        
        if top_card.color == Color.WILD:
            if self.game.current_color:
                # Show wild card with the chosen color as background
                current_style = self.color_styles.get(self.game.current_color, self.color_styles[Color.RED])
                card_class = f"w-20 h-28 {current_style['bg']} {current_style['text']} rounded-lg shadow-lg flex flex-col items-center justify-center border-2 {current_style['border']}"
            else:
                card_class = "w-20 h-28 rounded-lg shadow-lg flex flex-col items-center justify-center border-2 border-purple-300 wild-card-gradient"
        else:
            card_class = f"w-20 h-28 {style['bg']} {style['text']} rounded-lg shadow-lg flex flex-col items-center justify-center border-2 {style['border']}"
        
        with ui.card().classes(card_class):
            ui.label(self._get_card_display_text(top_card)).classes("text-xl font-bold")
            
            if top_card.color == Color.WILD and self.game.current_color:
                ui.label(f"Wild → {self.game.current_color.value.title()}").classes("text-xs font-bold bg-white/30 px-2 py-1 rounded")
            elif top_card.color != Color.WILD:
                ui.label(top_card.color.value.title()).classes("text-xs font-bold bg-white/20 px-1 rounded")

    def _create_horizontal_hand(self):
        """Create the player's hand in a horizontal row."""
        if not self.player_name:
            return
            
        hand = self.game.get_player_hand(self.player_name)
        sorted_hand = sorted(hand, key=lambda card: card.get_sort_key())
        
        for i, card in enumerate(sorted_hand):
            original_index = hand.index(card)
            self._create_horizontal_card(card, original_index, i)

    def _create_horizontal_card(self, card: Card, original_index: int, display_index: int):
        """Create a single card in horizontal layout."""
        style = self.color_styles.get(card.color, self.color_styles[Color.RED])
        playable = self._is_card_playable(card) and (self.current_player == self.player_name)
        
        # Card styling - always show color, but indicate playability with border
        if card.color == Color.WILD:
            if playable:
                card_class = "uno-card w-24 h-36 wild-card-gradient text-white rounded-xl shadow-lg border-4 border-green-400 flex flex-col items-center justify-center"
            else:
                card_class = "uno-card-disabled w-24 h-36 wild-card-gradient text-white rounded-xl shadow-lg border-2 border-gray-400 flex flex-col items-center justify-center opacity-75"
        else:
            if playable:
                card_class = f"uno-card w-24 h-36 {style['bg']} {style['text']} rounded-xl shadow-lg border-4 border-green-400 flex flex-col items-center justify-center"
            else:
                card_class = f"uno-card-disabled w-24 h-36 {style['bg']} {style['text']} rounded-xl shadow-lg border-2 border-gray-400 flex flex-col items-center justify-center opacity-75"
        
        with ui.row():
            with ui.card().classes(card_class) as card_element:
                # Card number (small, at top)
                ui.label(f"#{display_index + 1}").classes("text-xs opacity-70 mb-1")
                
                # Card value (large, center) - use custom display method
                ui.label(self._get_card_display_text(card)).classes("text-2xl font-bold mb-1")
                
                # Color name (small, at bottom) - always show color
                if card.color != Color.WILD:
                    ui.label(card.color.value.title()).classes("text-xs font-semibold")
                else:
                    ui.label("Wild").classes("text-xs font-semibold")
                
                # Play button (only if playable and my turn)
                if playable:
                    ui.button("PLAY", on_click=lambda idx=original_index: self._play_card(idx)).classes("mt-2 bg-white/30 hover:bg-white/50 font-bold py-1 px-2 rounded text-xs")
                
                # Make entire card clickable if playable
                if playable:
                    card_element.on('click', lambda idx=original_index: self._play_card(idx))

    def _play_card(self, card_index: int):
        """Play a card - only if it's the viewing player's turn."""
        if not self.player_name or self.current_player != self.player_name:
            ui.notify("It's not your turn!", type='warning')
            return
            
        hand = self.game.get_player_hand(self.player_name)
        card = hand[card_index]
        
        # Handle wild cards
        if card.type in (CardType.WILD, CardType.WILD_DRAW):
            self._show_color_picker(card_index)
            return
        
        # Handle forced draw
        if self.game.forced_draw > 0:
            if card.type == CardType.DRAW_TWO:
                success, message = self.game.play_card(
                    list(self.game.players.keys()).index(self.player_name),
                    card_index
                )
                if success:
                    # Update current player immediately after successful play
                    self.current_player = self.game.get_current_player()
                    ui.notify(f"Stacked +2! Next player draws {self.game.forced_draw}!", type='positive')
            else:
                ui.notify(f"Must draw {self.game.forced_draw} cards or play +2!", type='warning')
                return
        else:
            success, message = self.game.play_card(
                list(self.game.players.keys()).index(self.player_name),
                card_index
            )
            
            if success:
                # Update current player immediately after successful play
                self.current_player = self.game.get_current_player()
                ui.notify(f"Played {card}!" if not message else message, type='positive')
            else:
                ui.notify(message or "Cannot play that card!", type='negative')
                return  # Don't call update_game_state if the play failed
        
        self.update_game_state()

    def _draw_card(self):
        """Draw cards - only if it's the viewing player's turn."""
        if not self.player_name or self.current_player != self.player_name:
            ui.notify("It's not your turn!", type='warning')
            return
            
        if self.game.forced_draw > 0:
            drawn = self.game.handle_forced_draw(list(self.game.players.keys()).index(self.player_name))
            ui.notify(f"Drew {len(drawn)} cards!", type='info')
        else:
            drawn = self.game.draw_card(list(self.game.players.keys()).index(self.player_name))
            ui.notify(f"Drew {len(drawn)} card!", type='info')
        
        self.game._next_turn()
        # Update current player immediately after turn change
        self.current_player = self.game.get_current_player()
        self.update_game_state()

    def _show_color_picker(self, card_index: int):
        """Show color picker for wild cards."""
        self._active_dialog = True

        with ui.dialog() as dialog, ui.card().classes("p-6"):
            ui.label("🌈 Choose a Color").classes("text-2xl font-bold text-center mb-4")

            # Get current player's hand to count cards by color
            hand = self.game.get_player_hand(self.player_name)
            color_counts = {}
            
            # Count cards by color (excluding wild cards)
            for card in hand:
                if card.color != Color.WILD:
                    color_counts[card.color] = color_counts.get(card.color, 0) + 1

            with ui.grid(columns=2).classes("gap-4"):
                colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]
                
                for color in colors:
                    style = self.color_styles[color]
                    card_count = color_counts.get(color, 0)
                    
                    def select_color(c=color):
                        success, message = self.game.play_card(
                            list(self.game.players.keys()).index(self.player_name),
                            card_index,
                            c
                        )
                        if success:
                            # Update current player immediately after successful play
                            self.current_player = self.game.get_current_player()
                            ui.notify(f"Played wild! Color: {c.value.title()}!" if not message else message, type='positive')
                            dialog.close()
                            self._active_dialog = False
                            self.update_game_state()
                        else:
                            ui.notify(message or "Cannot play that card!", type='negative')                            
                            self._active_dialog = False
                    
                    ui.button(
                        f"{color.value.title()} ({card_count})",
                        on_click=select_color
                    ).classes(f"p-4 {style['bg']} {style['text']} font-bold rounded-lg hover:scale-105 transition-all duration-300 shadow-lg")

            dialog.open()

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
                            {self.game.winner}
                        </h2>
                        <p class="text-xl text-gray-600">Congratulations!</p>
                    </div>
                """)
                
                # Final scores
                with ui.card().classes("p-6 bg-blue-50 mb-6"):
                    ui.label("📊 Final Scores").classes("text-xl font-bold text-center mb-4")
                    
                    player_counts = self.game.get_player_counts()
                    for name, count in player_counts.items():
                        status = "🏆 Winner" if name == self.game.winner else f"{count} cards left"
                        ui.label(f"{name}: {status}").classes("text-lg text-center")
                
                # Action buttons
                with ui.row().classes("gap-4 justify-center"):
                    ui.button("🎮 New Game", on_click=self._new_game).classes("p-3 text-lg font-bold bg-blue-500 text-white hover:bg-blue-600")
                    ui.button("🔄 Play Again", on_click=self._play_again).classes("p-3 text-lg font-bold bg-green-500 text-white hover:bg-green-600")

    def _new_game(self):
        """Start a completely new game."""
        UnoUI._game_instance = None
        self.player_name = None
        # Clear global game state
        UnoUI._lobby_players.clear()
        UnoUI._player_heartbeats.clear()
        UnoUI._game_started = False
        UnoUI._game_hash = None
        # Redirect to landing page
        ui.navigate.to('/')

    def _play_again(self):
        """Play again with same players."""
        # Reset to lobby with same players
        UnoUI._game_started = False
        UnoUI._game_hash = None
        UnoUI._game_instance = None
        # Reset all players to not ready but keep heartbeats
        for player in UnoUI._lobby_players:
            UnoUI._lobby_players[player] = False
        ui.navigate.to('/lobby')

    def _is_card_playable(self, card: Card) -> bool:
        """Check if a card is playable."""
        # Only allow playing if it's the viewing player's turn
        if not self.player_name or self.current_player != self.player_name:
            return False
            
        if self.game.forced_draw > 0:
            return card.type == CardType.DRAW_TWO
        
        if card.type in (CardType.WILD, CardType.WILD_DRAW):
            return True
        
        top_card = self.game.get_top_card()
        return (card.color == self.game.current_color or
                card.type == top_card.type or
                (card.type == CardType.NUMBER and top_card.type == CardType.NUMBER and card.value == top_card.value))

    def update_game_state(self):
        """Update the game state and refresh UI."""
        if self.game and not self.game.is_game_over():
            self.current_player = self.game.get_current_player()
        # The timer will handle the UI refresh automatically

    def _get_card_display_text(self, card: Card) -> str:
        """Get display text for a card with better formatting."""
        if card.type == CardType.NUMBER:
            return str(card.value)
        elif card.type == CardType.WILD:
            return "🌈"
        elif card.type == CardType.WILD_DRAW:
            return "🌈+4"
        elif card.type == CardType.DRAW_TWO:
            return "+2"
        elif card.type == CardType.SKIP:
            return "⊘"
        elif card.type == CardType.REVERSE:
            return "⟲"
        else:
            return str(card)

    def run(self, title: str = "🎮 UNO Game", port: int = 8080, debug: bool = False):
        """Run the UI application."""
        if ui is None:
            raise ImportError("NiceGUI is required for the UI. Install with: pip install nicegui")
        
        # Set up page routes for proper session handling
        @ui.page('/')
        def index_page():
            # Landing page - player name entry
            self._show_landing_page()
        
        @ui.page('/lobby')
        def lobby_page():
            # Check if player has entered name
            if not self.player_name:
                ui.navigate.to('/')
                return
            self._show_lobby_page()
        
        @ui.page('/uno-{game_hash}')
        def game_page(game_hash: str):
            # Check if player is part of this game session
            if not self.player_name or not UnoUI._game_started or UnoUI._game_hash != game_hash:
                ui.navigate.to('/lobby')
                return
            
            if self.game and self.game.is_game_over():
                self._show_winner_page()
            else:
                self._show_game_page()
        
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
