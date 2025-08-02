"""
Simplified UNO game user interface using NiceGUI.

This module provides a beautiful web-based UI for playing Uno games with 
enhanced styling and smooth gameplay.
"""

try:
    from nicegui import ui
except ImportError:
    print("NiceGUI not installed. Install with: pip install nicegui")
    ui = None

from .game import UnoGame, Card, Color, CardType
from typing import List, Optional


class UnoUI:
    """Simple but beautiful web-based user interface for Uno game."""
    
    def __init__(self):
        if ui is None:
            raise ImportError("NiceGUI is required for the UI. Install with: pip install nicegui")
        
        self.game = None
        self.player_names = []
        self.current_player = None
        self.viewing_player = None  # The player this browser view represents
        self.main_container = None
        
        # Color mappings for beautiful card styling
        self.color_styles = {
            Color.RED: {"bg": "bg-red-500", "text": "text-white", "border": "border-red-600"},
            Color.BLUE: {"bg": "bg-blue-500", "text": "text-white", "border": "border-blue-600"},
            Color.GREEN: {"bg": "bg-green-500", "text": "text-white", "border": "border-green-600"},
            Color.YELLOW: {"bg": "bg-yellow-400", "text": "text-black", "border": "border-yellow-500"},
            Color.WILD: {"bg": "bg-gradient-to-br from-purple-500 to-pink-500", "text": "text-white", "border": "border-purple-600"}
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
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            
            .uno-card:hover {
                transform: translateY(-4px) scale(1.02);
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            }
            
            .uno-card-disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            
            .uno-card-disabled:hover {
                transform: none;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
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

    def show_landing_page(self):
        """Display the landing page for setting up a game."""
        with self.main_container:
            self.main_container.clear()
            
            with ui.column().classes("w-full min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4"):
                with ui.card().classes("w-full max-w-2xl mx-auto p-8 bg-white/90 backdrop-blur-sm shadow-2xl"):
                    # Game title
                    ui.html("""
                        <div class="text-center mb-8">
                            <h1 class="text-6xl font-bold bg-gradient-to-r from-red-500 via-blue-500 to-green-500 bg-clip-text text-transparent mb-4">
                                🎮 UNO GAME 🎮
                            </h1>
                            <p class="text-xl text-gray-600">Modern Web-Based Card Game</p>
                        </div>
                    """)

                    # Player setup
                    with ui.card().classes("p-6 bg-gradient-to-r from-indigo-50 to-blue-50 border border-indigo-200 mb-6"):
                        ui.label("👥 Player Setup").classes("text-2xl font-bold text-center mb-4 text-indigo-800")
                        ui.label("Enter 2-4 player names to start").classes("text-center mb-6 text-gray-600")

                        self.player_inputs = []
                        with ui.grid(columns=2).classes("w-full gap-4"):
                            for i in range(4):
                                self.player_inputs.append(
                                    ui.input(
                                        label=f"🎯 Player {i+1}",
                                        placeholder=f"Enter name"
                                    ).classes("w-full").props("outlined")
                                )

                    # Start button
                    ui.button(
                        "🚀 Start Game", 
                        on_click=self._start_game
                    ).classes("w-full p-4 text-xl font-bold bg-gradient-to-r from-green-500 to-blue-500 text-white hover:from-green-600 hover:to-blue-600 transition-all duration-300")

    def _start_game(self):
        """Start a new game."""
        self.player_names = [input.value.strip() for input in self.player_inputs if input.value.strip()]
        
        if len(self.player_names) < 2:
            ui.notify("Need at least 2 players!", type='negative')
            return
        
        if len(set(self.player_names)) != len(self.player_names):
            ui.notify("Player names must be unique!", type='negative')
            return

        ui.notify(f"Starting game with {len(self.player_names)} players!", type='positive')
        self.game = UnoGame(self.player_names)
        self.current_player = self.game.get_current_player()
        self.show_game_page()

    def show_game_page(self):
        """Display the main game interface."""
        with self.main_container:
            self.main_container.clear()
            
            # Check for game over
            if self.game.is_game_over():
                self._show_winner_page()
                return
            
            with ui.column().classes("w-full min-h-screen bg-gradient-to-br from-green-50 via-blue-50 to-purple-50"):
                
                # Game header
                with ui.card().classes("w-full p-4 bg-white/90 backdrop-blur-sm shadow-lg mb-4"):
                    with ui.row().classes("w-full items-center justify-between"):
                        # Current player
                        ui.label(f"🎯 {self.current_player}'s Turn").classes("text-2xl font-bold text-blue-600 player-turn-glow bg-blue-100 px-4 py-2 rounded-lg")
                        
                        # Direction
                        direction_icon = "↻" if self.game.direction == 1 else "↺" 
                        ui.label(f"Direction: {direction_icon}").classes("text-2xl font-bold text-gray-600")
                        
                        # Forced draw warning
                        if self.game.forced_draw > 0:
                            ui.label(f"⚠️ Must draw {self.game.forced_draw} cards!").classes("text-red-600 font-bold text-xl bg-red-100 px-3 py-2 rounded-lg")

                # Main game area
                with ui.row().classes("w-full flex-grow gap-6 p-6"):
                    
                    # Left - Other players
                    with ui.column().classes("w-1/4 gap-4"):
                        ui.label("👥 Other Players").classes("text-xl font-bold text-center mb-4")
                        
                        player_counts = self.game.get_player_counts()
                        for name, count in player_counts.items():
                            if name != self.current_player:
                                with ui.card().classes("p-4 bg-white/80 shadow-lg hover:shadow-xl transition-all duration-300"):
                                    ui.label(f"🎮 {name}").classes("font-bold text-lg")
                                    ui.label(f"Cards: {count}").classes("text-blue-600 font-semibold")
                                    if count == 1:
                                        ui.label("🚨 UNO!").classes("text-red-600 font-bold animate-pulse")
                    
                    # Center - Game board
                    with ui.column().classes("w-2/4 items-center gap-8"):
                        
                        # Top card
                        with ui.column().classes("items-center gap-4"):
                            ui.label("🎯 Current Card").classes("text-xl font-bold")
                            self._create_top_card()
                        
                        # Draw pile
                        with ui.column().classes("items-center gap-4"):
                            ui.label("🂠 Draw Pile").classes("text-lg font-bold")
                            
                            with ui.card().classes("w-28 h-40 bg-gradient-to-br from-gray-600 to-gray-800 text-white cursor-pointer hover:shadow-xl transition-all duration-300 transform hover:scale-105 flex flex-col items-center justify-center").on('click', self._draw_card):
                                ui.label("DRAW").classes("text-lg font-bold")
                                ui.label(f"{len(self.game.draw_pile)}").classes("text-sm")
                    
                    # Right - Player hand
                    with ui.column().classes("w-1/4 gap-4"):
                        ui.label(f"🃏 Your Hand").classes("text-xl font-bold text-center")
                        ui.label(f"Cards: {len(self.game.get_player_hand(self.current_player))}").classes("text-center text-gray-600 mb-4")
                        
                        with ui.scroll_area().classes("h-[500px]"):
                            self._create_player_hand()

    def _create_top_card(self):
        """Create the top card display."""
        top_card = self.game.get_top_card()
        style = self.color_styles.get(top_card.color, self.color_styles[Color.RED])
        
        if top_card.color == Color.WILD:
            if self.game.current_color:
                current_style = self.color_styles.get(self.game.current_color, self.color_styles[Color.RED])
                card_class = f"w-32 h-48 rounded-xl shadow-xl flex flex-col items-center justify-center border-4 {current_style['border']} wild-card-gradient"
            else:
                card_class = "w-32 h-48 rounded-xl shadow-xl flex flex-col items-center justify-center border-4 border-purple-600 wild-card-gradient"
        else:
            card_class = f"w-32 h-48 {style['bg']} {style['text']} rounded-xl shadow-xl flex flex-col items-center justify-center border-4 {style['border']}"
        
        with ui.card().classes(card_class):
            ui.label(str(top_card)).classes("text-3xl font-bold mb-2")
            
            if top_card.color == Color.WILD and self.game.current_color:
                ui.label(f"{self.game.current_color.value.title()}").classes("text-sm font-bold bg-white/20 px-2 py-1 rounded")
            elif top_card.color != Color.WILD:
                ui.label(top_card.color.value.title()).classes("text-sm font-bold bg-white/20 px-2 py-1 rounded")

    def _create_player_hand(self):
        """Create the player's hand display."""
        hand = self.game.get_player_hand(self.current_player)
        sorted_hand = sorted(hand, key=lambda card: card.get_sort_key())
        
        for i, card in enumerate(sorted_hand):
            original_index = hand.index(card)
            self._create_hand_card(card, original_index, i)

    def _create_hand_card(self, card: Card, original_index: int, display_index: int):
        """Create a single card in the hand."""
        style = self.color_styles.get(card.color, self.color_styles[Color.RED])
        playable = self._is_card_playable(card)
        
        if playable:
            if card.color == Color.WILD:
                card_class = "uno-card w-full h-20 wild-card-gradient text-white rounded-lg shadow-lg flex items-center justify-between p-3 mb-2 border-2 border-green-400"
            else:
                card_class = f"uno-card w-full h-20 {style['bg']} {style['text']} rounded-lg shadow-lg flex items-center justify-between p-3 mb-2 border-2 border-green-400"
        else:
            card_class = "uno-card-disabled w-full h-20 bg-gray-300 text-gray-500 rounded-lg shadow-lg flex items-center justify-between p-3 mb-2 border-2 border-gray-400"
        
        with ui.card().classes(card_class):
            with ui.column().classes("gap-1"):
                ui.label(f"#{display_index + 1}").classes("text-xs opacity-70")
                ui.label(str(card)).classes("text-lg font-bold")
                if card.color != Color.WILD:
                    ui.label(card.color.value.title()).classes("text-xs")
            
            if playable:
                ui.button("PLAY", on_click=lambda idx=original_index: self._play_card(idx)).classes("bg-white/20 hover:bg-white/30 font-bold py-1 px-3 rounded")

    def _play_card(self, card_index: int):
        """Play a card."""
        hand = self.game.get_player_hand(self.current_player)
        card = hand[card_index]
        
        # Handle wild cards
        if card.type in (CardType.WILD, CardType.WILD_DRAW):
            self._show_color_picker(card_index)
            return
        
        # Handle forced draw
        if self.game.forced_draw > 0:
            if card.type == CardType.DRAW_TWO:
                success, message = self.game.play_card(
                    list(self.game.players.keys()).index(self.current_player),
                    card_index
                )
                if success:
                    ui.notify(f"Stacked +2! Next player draws {self.game.forced_draw}!", type='positive')
            else:
                ui.notify(f"Must draw {self.game.forced_draw} cards or play +2!", type='warning')
                return
        else:
            success, message = self.game.play_card(
                list(self.game.players.keys()).index(self.current_player),
                card_index
            )
            
            if success:
                ui.notify(f"Played {card}!" if not message else message, type='positive')
            else:
                ui.notify(message or "Cannot play that card!", type='negative')
        
        self.update_game_state()

    def _draw_card(self):
        """Draw cards."""
        if self.game.forced_draw > 0:
            drawn = self.game.handle_forced_draw(list(self.game.players.keys()).index(self.current_player))
            ui.notify(f"Drew {len(drawn)} cards!", type='info')
        else:
            drawn = self.game.draw_card(list(self.game.players.keys()).index(self.current_player))
            ui.notify(f"Drew {len(drawn)} card!", type='info')
        
        self.game._next_turn()
        self.update_game_state()

    def _show_color_picker(self, card_index: int):
        """Show color picker for wild cards."""
        with ui.dialog() as dialog, ui.card().classes("p-6"):
            ui.label("🌈 Choose a Color").classes("text-2xl font-bold text-center mb-4")

            with ui.grid(columns=2).classes("gap-4"):
                colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]
                
                for color in colors:
                    style = self.color_styles[color]
                    
                    def select_color(c=color):
                        success, message = self.game.play_card(
                            list(self.game.players.keys()).index(self.current_player),
                            card_index,
                            c
                        )
                        if success:
                            ui.notify(f"Played wild! Color: {c.value.title()}!" if not message else message, type='positive')
                            dialog.close()
                            self.update_game_state()
                        else:
                            ui.notify(message or "Cannot play that card!", type='negative')
                    
                    ui.button(
                        color.value.title(),
                        on_click=select_color
                    ).classes(f"p-4 {style['bg']} {style['text']} font-bold rounded-lg hover:scale-105 transition-all duration-300")

            dialog.open()

    def _show_winner_page(self):
        """Display winner page."""
        with self.main_container:
            self.main_container.clear()
            
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
                        
                        if self.player_names:
                            ui.button("🔄 Play Again", on_click=self._play_again).classes("p-3 text-lg font-bold bg-green-500 text-white hover:bg-green-600")

    def _new_game(self):
        """Start a completely new game."""
        self.game = None
        self.player_names = []
        self.show_landing_page()

    def _play_again(self):
        """Play again with same players."""
        if self.player_names:
            self.game = UnoGame(self.player_names)
            self.current_player = self.game.get_current_player()
            self.show_game_page()

    def _is_card_playable(self, card: Card) -> bool:
        """Check if a card is playable."""
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
        self.show_game_page()

    def run(self, title: str = "🎮 UNO Game", port: int = 8080, debug: bool = False):
        """Run the UI application."""
        if ui is None:
            raise ImportError("NiceGUI is required for the UI. Install with: pip install nicegui")
        
        # Create the main container
        self.main_container = ui.column().classes("w-full")
        
        # Show the landing page
        self.show_landing_page()
        
        # Run the application
        ui.run(
            title=title,
            port=port,
            show=False,
            reload=debug,
            favicon="🎮"
        )


def main():
    """Main entry point for the UI."""
    ui_app = UnoUI()
    ui_app.run()


if __name__ == "__main__":
    main()
