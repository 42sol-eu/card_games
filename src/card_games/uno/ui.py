"""
Uno game user interface using NiceGUI.

This module provides a modern web-based UI for playing Uno games with 
beautiful card animations, responsive design, and smooth gameplay.
"""

try:
    from nicegui import ui, app
    from nicegui.events import MouseEventArguments
except ImportError:
    print("NiceGUI not installed. Install with: pip install nicegui")
    ui = None
    app = None

from .game import UnoGame, Card, Color, CardType
from typing import List, Optional
import asyncio


class UnoUI:
    """Modern web-based user interface for Uno game with enhanced visuals."""
    
    def __init__(self):
        if ui is None:
            raise ImportError("NiceGUI is required for the UI. Install with: pip install nicegui")
        
        self.game = None
        self.player_names = []
        self.current_player = None
        self.color_choices = []
        self.game_container = None
        self.hand_container = None
        self.players_container = None
        self.top_card_container = None
        
        # Color mappings for beautiful card styling
        self.color_styles = {
            Color.RED: {"bg": "bg-red-500", "text": "text-white", "border": "border-red-600", "hover": "hover:bg-red-600"},
            Color.BLUE: {"bg": "bg-blue-500", "text": "text-white", "border": "border-blue-600", "hover": "hover:bg-blue-600"},
            Color.GREEN: {"bg": "bg-green-500", "text": "text-white", "border": "border-green-600", "hover": "hover:bg-green-600"},
            Color.YELLOW: {"bg": "bg-yellow-400", "text": "text-black", "border": "border-yellow-500", "hover": "hover:bg-yellow-500"},
            Color.WILD: {"bg": "bg-gradient-to-br from-purple-500 to-pink-500", "text": "text-white", "border": "border-purple-600", "hover": "hover:from-purple-600 hover:to-pink-600"}
        }
        
        self._setup_custom_css()

    def _setup_custom_css(self):
        """Add custom CSS for enhanced card animations and styling."""
        ui.add_head_html("""
        <style>
            .uno-card {
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                cursor: pointer;
                border-radius: 12px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            }
            
            .uno-card:hover {
                transform: translateY(-8px) scale(1.05);
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
                z-index: 10;
            }
            
            .uno-card-disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            
            .uno-card-disabled:hover {
                transform: none;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            }
            
            .card-play-animation {
                animation: cardPlay 0.6s ease-out forwards;
            }
            
            @keyframes cardPlay {
                0% { transform: scale(1) rotate(0deg); opacity: 1; }
                50% { transform: scale(1.2) rotate(5deg); opacity: 0.8; }
                100% { transform: scale(0.8) rotate(0deg); opacity: 0; }
            }
            
            .draw-pile-shake {
                animation: shake 0.5s ease-in-out;
            }
            
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-5px); }
                75% { transform: translateX(5px); }
            }
            
            .player-turn-indicator {
                animation: pulse 2s infinite;
                border-radius: 12px;
            }
            
            @keyframes pulse {
                0%, 100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7); }
                50% { box-shadow: 0 0 0 10px rgba(59, 130, 246, 0); }
            }
            
            .wild-card-gradient {
                background: linear-gradient(45deg, #ef4444, #3b82f6, #10b981, #f59e0b);
                background-size: 400% 400%;
                animation: gradientShift 3s ease infinite;
            }
            
            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            .notification-success {
                background: linear-gradient(135deg, #10b981, #059669);
                color: white;
                border-radius: 8px;
                padding: 12px 16px;
                box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.3);
            }
            
            .notification-error {
                background: linear-gradient(135deg, #ef4444, #dc2626);
                color: white;
                border-radius: 8px;
                padding: 12px 16px;
                box-shadow: 0 10px 15px -3px rgba(239, 68, 68, 0.3);
            }
        </style>
        """)

    def show_landing_page(self):
        """Display an enhanced landing page for setting up a game."""
        ui.colors(primary='#3b82f6')
        
        with ui.column().classes("w-full min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4"):
            # Game title with enhanced styling
            with ui.card().classes("w-full max-w-2xl mx-auto p-8 bg-white/80 backdrop-blur-sm shadow-2xl"):
                ui.html("""
                    <div class="text-center mb-8">
                        <h1 class="text-6xl font-bold bg-gradient-to-r from-red-500 via-blue-500 to-green-500 bg-clip-text text-transparent mb-4">
                        UNO GAME
                        </h1>
                        <p class="text-xl text-gray-600">Modern Web-Based Card Game Experience</p>
                    </div>
                """).classes("mb-6")

                # Player setup section
                with ui.card().classes("p-6 bg-gradient-to-r from-indigo-50 to-blue-50 border border-indigo-200"):
                    ui.label("👥 Player Setup").classes("text-2xl font-bold text-center mb-4 text-indigo-800")
                    ui.label("Enter 2-4 player names to start your game").classes("text-center mb-6 text-gray-600")

                    self.player_inputs = []
                    with ui.grid(columns=2).classes("w-full gap-4"):
                        for i in range(4):
                            with ui.column().classes("gap-2"):
                                self.player_inputs.append(
                                    ui.input(
                                        label=f"🎯 Player {i+1}",
                                        placeholder=f"Enter player {i+1} name"
                                    ).classes("w-full").props("outlined dense")
                                )

                # Start game button
                def start_game():
                    self.player_names = [input.value.strip() for input in self.player_inputs if input.value.strip()]
                    
                    if len(self.player_names) < 2:
                        ui.notify("Need at least 2 players to start!", type='negative', position='top')
                        return
                    
                    if len(set(self.player_names)) != len(self.player_names):
                        ui.notify("Player names must be unique!", type='negative', position='top')
                        return

                    ui.notify(f"Starting game with {len(self.player_names)} players!", type='positive', position='top')
                    self.game = UnoGame(self.player_names)
                    self.current_player = self.game.get_current_player()
                    self.show_game_page()

                ui.button(
                    "🚀 Start Game", 
                    on_click=start_game
                ).classes("w-full mt-6 p-4 text-xl font-bold bg-gradient-to-r from-green-500 to-blue-500 text-white hover:from-green-600 hover:to-blue-600 transition-all duration-300 transform hover:scale-105")

    def show_game_page(self):
        """Display the enhanced main game interface."""
        ui.clear()
        
        # Check for game over
        if self.game.is_game_over():
            self._show_winner_page()
            return
        
        # Main game layout with background
        with ui.column().classes("w-full min-h-screen bg-gradient-to-br from-green-50 via-blue-50 to-purple-50"):
            
            # Game header
            with ui.card().classes("w-full p-4 bg-white/90 backdrop-blur-sm shadow-lg"):
                with ui.row().classes("w-full items-center justify-between"):
                    # Current player indicator
                    current_player_class = "player-turn-indicator bg-gradient-to-r from-blue-500 to-purple-500 text-white p-4 rounded-lg font-bold text-xl"
                    ui.label(f"🎯 {self.current_player}'s Turn").classes(current_player_class)
                    
                    # Game direction
                    direction_icon = "↻" if self.game.direction == 1 else "↺" 
                    ui.label(f"Direction: {direction_icon}").classes("text-2xl font-bold text-gray-600")
                    
                    # Forced draw warning
                    if self.game.forced_draw > 0:
                        ui.label(f"⚠️ Must draw {self.game.forced_draw} cards!").classes("text-red-600 font-bold text-xl bg-red-100 p-2 rounded-lg")

            # Main game area
            with ui.row().classes("w-full flex-grow gap-6 p-6"):
                
                # Left sidebar - Other players
                self._create_players_sidebar()
                
                # Center - Game board
                self._create_game_board()
                
                # Right sidebar - Current player's hand
                self._create_player_hand()

    def _create_players_sidebar(self):
        """Create the left sidebar showing other players."""
        with ui.column().classes("w-80 gap-4"):
            ui.label("👥 Other Players").classes("text-2xl font-bold text-center text-gray-800 mb-4")
            
            player_counts = self.game.get_player_counts()
            for name, count in player_counts.items():
                if name != self.current_player:
                    # Player card with animation
                    card_class = "p-4 bg-white/80 backdrop-blur-sm shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                    with ui.card().classes(card_class):
                        ui.label(f"🎮 {name}").classes("text-lg font-bold text-gray-800")
                        ui.label(f"Cards: {count}").classes("text-xl text-blue-600 font-semibold")
                        
                        # Show warning if player has few cards
                        if count == 1:
                            ui.label("🚨 UNO!").classes("text-red-600 font-bold animate-pulse")
                        elif count <= 3:
                            ui.label("⚠️ Few cards left").classes("text-orange-600 font-semibold")

    def _create_game_board(self):
        """Create the central game board with top card and draw pile."""
        with ui.column().classes("flex-grow items-center gap-8"):
            
            # Top card display
            with ui.column().classes("items-center gap-4"):
                ui.label("🎯 Top Card").classes("text-2xl font-bold text-gray-800")
                
                top_card = self.game.get_top_card()
                self._create_top_card_display(top_card)
            
            # Draw pile
            with ui.column().classes("items-center gap-4"):
                ui.label("🂠 Draw Pile").classes("text-xl font-bold text-gray-700")
                
                def draw_card():
                    self._handle_draw_card()
                
                draw_pile_class = "w-32 h-48 bg-gradient-to-br from-gray-600 to-gray-800 text-white font-bold text-lg rounded-xl shadow-lg cursor-pointer hover:shadow-2xl transition-all duration-300 transform hover:scale-105 flex flex-col items-center justify-center"
                
                with ui.card().classes(draw_pile_class).on('click', draw_card):
                    ui.label("DRAW").classes("text-2xl font-bold")
                    ui.label(f"{len(self.game.draw_pile)} cards").classes("text-sm")

    def _create_top_card_display(self, card: Card):
        """Create an enhanced display for the top card."""
        style = self.color_styles.get(card.color, self.color_styles[Color.RED])
        
        # Special styling for wild cards
        if card.color == Color.WILD:
            if self.game.current_color:
                current_style = self.color_styles.get(self.game.current_color, self.color_styles[Color.RED])
                card_class = f"w-40 h-60 rounded-xl shadow-2xl flex flex-col items-center justify-center border-4 {current_style['border']} wild-card-gradient"
            else:
                card_class = "w-40 h-60 rounded-xl shadow-2xl flex flex-col items-center justify-center border-4 border-purple-600 wild-card-gradient"
        else:
            card_class = f"w-40 h-60 {style['bg']} {style['text']} rounded-xl shadow-2xl flex flex-col items-center justify-center border-4 {style['border']}"
        
        with ui.card().classes(card_class):
            # Card symbol/number
            ui.label(str(card)).classes("text-4xl font-bold mb-2")
            
            # Color name for wild cards
            if card.color == Color.WILD and self.game.current_color:
                ui.label(f"Color: {self.game.current_color.value.title()}").classes("text-sm font-semibold bg-white/20 px-2 py-1 rounded")
            elif card.color != Color.WILD:
                ui.label(card.color.value.title()).classes("text-sm font-semibold bg-white/20 px-2 py-1 rounded")

    def _create_player_hand(self):
        """Create the right sidebar showing current player's hand."""
        with ui.column().classes("w-80 gap-4"):
            ui.label(f"🃏 {self.current_player}'s Hand").classes("text-2xl font-bold text-center text-gray-800")
            
            hand = self.game.get_player_hand(self.current_player)
            ui.label(f"Cards: {len(hand)}").classes("text-lg text-center text-gray-600 mb-4")
            
            # Sort hand for better organization
            sorted_hand = sorted(hand, key=lambda card: card.get_sort_key())
            
            with ui.scroll_area().classes("h-[600px] p-2"):
                for i, card in enumerate(sorted_hand):
                    original_index = hand.index(card)
                    self._create_hand_card(card, original_index, i)

    def _create_hand_card(self, card: Card, original_index: int, display_index: int):
        """Create a single card in the player's hand."""
        style = self.color_styles.get(card.color, self.color_styles[Color.RED])
        playable = self._is_card_playable(card)
        
        # Card styling based on playability
        if playable:
            if card.color == Color.WILD:
                card_class = f"uno-card w-full h-24 wild-card-gradient text-white rounded-xl shadow-lg flex items-center justify-between p-4 mb-2 border-2 border-green-400"
            else:
                card_class = f"uno-card w-full h-24 {style['bg']} {style['text']} rounded-xl shadow-lg flex items-center justify-between p-4 mb-2 border-2 border-green-400 {style['hover']}"
        else:
            card_class = f"uno-card-disabled w-full h-24 bg-gray-300 text-gray-500 rounded-xl shadow-lg flex items-center justify-between p-4 mb-2 border-2 border-gray-400"
        
        with ui.card().classes(card_class):
            # Card info
            with ui.column().classes("gap-1"):
                ui.label(f"#{display_index + 1}").classes("text-xs font-bold opacity-70")
                ui.label(str(card)).classes("text-xl font-bold")
                if card.color != Color.WILD:
                    ui.label(card.color.value.title()).classes("text-xs font-semibold")
            
            # Play button
            if playable:
                def play_card(idx=original_index):
                    self._handle_play_card(idx)
                
                play_btn_class = "bg-white/20 hover:bg-white/30 text-current font-bold py-2 px-4 rounded-lg transition-all duration-300 transform hover:scale-105"
                ui.button("PLAY", on_click=play_card).classes(play_btn_class)

    def _handle_play_card(self, card_index: int):
        """Handle playing a card with enhanced feedback."""
        hand = self.game.get_player_hand(self.current_player)
        card = hand[card_index]
        
        # Handle wild cards
        if card.type in (CardType.WILD, CardType.WILD_DRAW):
            self._show_color_picker(card_index)
            return
        
        # Handle forced draw scenario
        if self.game.forced_draw > 0:
            if card.type == CardType.DRAW_TWO:
                # Allow stacking +2 cards
                success, message = self.game.play_card(
                    list(self.game.players.keys()).index(self.current_player),
                    card_index
                )
                if success:
                    ui.notify(f"Stacked +2! Next player must draw {self.game.forced_draw} cards!", type='positive')
                else:
                    ui.notify(message or "Cannot play that card!", type='negative')
            else:
                ui.notify(f"You must draw {self.game.forced_draw} cards first or play a +2 to stack!", type='warning')
                return
        else:
            # Normal card play
            success, message = self.game.play_card(
                list(self.game.players.keys()).index(self.current_player),
                card_index
            )
            
            if success:
                if message:  # Win message
                    ui.notify(message, type='positive')
                else:
                    ui.notify(f"Played {card}!", type='positive')
            else:
                ui.notify(message or "Cannot play that card!", type='negative')
        
        self.update_game_state()

    def _handle_draw_card(self):
        """Handle drawing cards with enhanced feedback."""
        if self.game.forced_draw > 0:
            # Handle forced draw
            drawn = self.game.handle_forced_draw(list(self.game.players.keys()).index(self.current_player))
            ui.notify(f"Drew {len(drawn)} cards due to special card effect!", type='info')
        else:
            # Normal draw
            drawn = self.game.draw_card(list(self.game.players.keys()).index(self.current_player))
            ui.notify(f"Drew {len(drawn)} card{'s' if len(drawn) > 1 else ''}!", type='info')
        
        self.game._next_turn()
        self.update_game_state()

    def _show_color_picker(self, card_index: int):
        """Show an enhanced color picker dialog for wild cards."""
        with ui.dialog() as dialog, ui.card().classes("p-6 bg-white/95 backdrop-blur-sm"):
            ui.label("🌈 Choose a Color").classes("text-3xl font-bold text-center mb-6 bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent")

            with ui.grid(columns=2).classes("gap-6 justify-center"):
                colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]
                
                for color in colors:
                    style = self.color_styles[color]
                    
                    def on_color_select(c=color, idx=card_index):
                        success, message = self.game.play_card(
                            list(self.game.players.keys()).index(self.current_player),
                            idx,
                            c
                        )
                        if success:
                            if message:  # Win message
                                ui.notify(message, type='positive')
                            else:
                                ui.notify(f"Played wild card! Color changed to {c.value.title()}!", type='positive')
                            dialog.close()
                            self.update_game_state()
                        else:
                            ui.notify(message or "Couldn't play that card!", type='negative')
                    
                    color_btn_class = f"w-24 h-24 {style['bg']} {style['text']} rounded-xl shadow-lg font-bold text-xl transition-all duration-300 transform hover:scale-110 {style['hover']} flex items-center justify-center cursor-pointer"
                    
                    with ui.card().classes(color_btn_class).on('click', lambda c=color: on_color_select(c)):
                        ui.label(color.value.title()).classes("font-bold text-center")

            dialog.open()

    def _show_winner_page(self):
        """Display the winner announcement page."""
        ui.clear()
        
        with ui.column().classes("w-full min-h-screen bg-gradient-to-br from-yellow-50 via-orange-50 to-red-50 flex items-center justify-center p-4"):
            with ui.card().classes("w-full max-w-2xl mx-auto p-12 bg-white/90 backdrop-blur-sm shadow-2xl text-center"):
                
                # Winner announcement with animation
                ui.html(f"""
                    <div class="mb-8">
                        <h1 class="text-7xl font-bold bg-gradient-to-r from-yellow-400 via-orange-500 to-red-500 bg-clip-text text-transparent mb-4 animate-pulse">
                            🎉 WINNER! 🎉
                        </h1>
                        <h2 class="text-4xl font-bold text-gray-800 mb-6">
                            {self.game.winner}
                        </h2>
                        <p class="text-xl text-gray-600">
                            Congratulations on your victory!
                        </p>
                    </div>
                """)
                
                # Game stats
                with ui.card().classes("p-6 bg-gradient-to-r from-blue-50 to-purple-50 mb-6"):
                    ui.label("📊 Final Scores").classes("text-2xl font-bold text-center mb-4")
                    
                    player_counts = self.game.get_player_counts()
                    for name, count in player_counts.items():
                        status = "🏆 Winner" if name == self.game.winner else f"{count} cards remaining"
                        ui.label(f"{name}: {status}").classes("text-lg font-semibold text-center")
                
                # Action buttons
                with ui.row().classes("gap-4 justify-center"):
                    def new_game():
                        self.game = None
                        self.show_landing_page()
                    
                    def same_players():
                        if self.player_names:
                            self.game = UnoGame(self.player_names)
                            self.current_player = self.game.get_current_player()
                            self.show_game_page()
                    
                    ui.button("🎮 New Game", on_click=new_game).classes("p-4 text-lg font-bold bg-gradient-to-r from-blue-500 to-purple-500 text-white hover:from-blue-600 hover:to-purple-600")
                    
                    if self.player_names:
                        ui.button("🔄 Play Again", on_click=same_players).classes("p-4 text-lg font-bold bg-gradient-to-r from-green-500 to-blue-500 text-white hover:from-green-600 hover:to-blue-600")

    def _is_card_playable(self, card: Card) -> bool:
        """Check if a card is playable (enhanced logic)."""
        # During forced draw, only +2 cards can be played (for stacking)
        if self.game.forced_draw > 0:
            return card.type == CardType.DRAW_TWO
        
        # Wild cards are always playable
        if card.type in (CardType.WILD, CardType.WILD_DRAW):
            return True
        
        top_card = self.game.get_top_card()
        
        return (card.color == self.game.current_color or
                card.type == top_card.type or
                (card.type == CardType.NUMBER and top_card.type == CardType.NUMBER and card.value == top_card.value))

    def update_game_state(self):
        """Update the game state and refresh the UI."""
        if self.game and not self.game.is_game_over():
            self.current_player = self.game.get_current_player()
        self.show_game_page()

    def run(self, title: str = "🎮 UNO Game - Modern Web Edition", port: int = 8080, debug: bool = False):
        """Run the enhanced UI application."""
        if ui is None:
            raise ImportError("NiceGUI is required for the UI. Install with: pip install nicegui")
        
        # Setup the initial page
        self.show_landing_page()
        
        # Configure and run the application
        ui.run(
            title=title,
            port=port,
            show=False,  # Don't auto-open browser
            reload=debug,
            favicon="🎮"
        )
