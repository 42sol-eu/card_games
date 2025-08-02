"""
Game header and discard pile components for UNO game interface.
"""

from nicegui import ui

from .base import UnoUIBase
from .components import CardComponents
from ..game import Color


class GameHeader:
    """Handles the game header display."""
    
    def __init__(self, ui_instance: UnoUIBase):
        self.ui = ui_instance

    def create(self):
        """Create the header with game information."""
        with ui.element('div').classes("game-header"):
            with ui.row().classes("w-full items-center justify-between"):
                
                # Left side - Current player and direction
                self._create_current_player_info()
                
                # Center - Top card and recent played cards
                self._create_center_cards()
                
                # Right side - Other players and draw pile
                self._create_controls()

    def _create_current_player_info(self):
        """Create current player and direction display."""
        with ui.column().classes("gap-2"):
            ui.label(f"🎯 Current Turn").classes("text-lg font-semibold opacity-80")
            ui.label(f"{self.ui.current_player}").classes("text-2xl font-bold")
            
            direction_icon = "↻" if self.ui.game.direction == 1 else "↺"
            ui.label(f"Direction: {direction_icon}").classes("text-lg")

    def _create_center_cards(self):
        """Create center area with top card and recent cards."""
        with ui.column().classes("items-center gap-2"):
            ui.label("🎯 Current Card").classes("text-lg font-semibold opacity-80")
            self._create_header_top_card()
            
            # Show recent played cards (discard pile preview)
            if len(self.ui.game.discard_pile) > 1:
                ui.label("📚 Recent Cards").classes("text-sm font-semibold opacity-70 mt-2")
                self._create_discard_pile_preview()

    def _create_controls(self):
        """Create right side controls."""
        with ui.column().classes("gap-2 items-end"):
            ui.label("👥 Other Players").classes("text-lg font-semibold opacity-80")
            
            # Other players info (compact)
            player_counts = self.ui.game.get_player_counts()
            other_players = [(name, count) for name, count in player_counts.items() if name != self.ui.player_name]
            
            for name, count in other_players:
                player_class = "text-lg font-bold" + (" text-yellow-300" if count == 1 else " text-white")
                status = "🚨 UNO!" if count == 1 else f"{count} cards"
                ui.label(f"{name}: {status}").classes(player_class)
            
            # Controls row
            with ui.row().classes("items-center gap-2 mt-2"):
                ui.label("🂠 Draw Pile").classes("text-sm opacity-80")
                ui.button(f"Draw ({len(self.ui.game.draw_pile)})", on_click=self._draw_card).classes("bg-white/20 hover:bg-white/30 text-white font-bold py-2 px-4 rounded-lg")
                ui.button("📚 Show All Cards", on_click=self._show_discard_pile).classes("bg-white/20 hover:bg-white/30 text-white font-bold py-2 px-4 rounded-lg")
                ui.button("🔄 Back to Lobby", on_click=self._back_to_lobby).classes("bg-white/20 hover:bg-white/30 text-white font-bold py-2 px-4 rounded-lg")

    def _create_header_top_card(self):
        """Create a compact top card display for the header."""
        top_card = self.ui.game.get_top_card()
        style = self.ui.color_styles.get(top_card.color, self.ui.color_styles[Color.RED])
        
        if top_card.color == Color.WILD:
            if self.ui.game.current_color:
                # Show wild card with the chosen color as background
                current_style = self.ui.color_styles.get(self.ui.game.current_color, self.ui.color_styles[Color.RED])
                card_class = f"w-20 h-28 {current_style['bg']} {current_style['text']} rounded-lg shadow-lg flex flex-col items-center justify-center border-2 {current_style['border']}"
            else:
                card_class = "w-20 h-28 rounded-lg shadow-lg flex flex-col items-center justify-center border-2 border-purple-300 wild-card-gradient"
        else:
            card_class = f"w-20 h-28 {style['bg']} {style['text']} rounded-lg shadow-lg flex flex-col items-center justify-center border-2 {style['border']}"
        
        with ui.card().classes(card_class):
            ui.label(CardComponents.get_card_display_text(top_card)).classes("text-xl font-bold")
            
            if top_card.color == Color.WILD and self.ui.game.current_color:
                ui.label(f"Wild → {self.ui.game.current_color.value.title()}").classes("text-xs font-bold bg-white/30 px-2 py-1 rounded")
            elif top_card.color != Color.WILD:
                ui.label(top_card.color.value.title()).classes("text-xs font-bold bg-white/20 px-1 rounded")

    def _create_discard_pile_preview(self):
        """Create a small preview of recent cards in the discard pile."""
        # Show last 3-4 cards (excluding the top card which is shown separately)
        recent_cards = self.ui.game.discard_pile[-5:-1] if len(self.ui.game.discard_pile) > 4 else self.ui.game.discard_pile[:-1]
        recent_cards.reverse()  # Show most recent first
        
        with ui.row().classes("gap-1 justify-center"):
            for i, card in enumerate(recent_cards):
                if i >= 4:  # Limit to 4 cards max
                    break
                CardComponents.create_mini_card(card, i, self.ui.color_styles)

    def _show_discard_pile(self):
        """Show the full discard pile in a dialog."""
        self.ui._active_dialog = True
        
        with ui.dialog() as dialog, ui.card().classes("w-full max-w-4xl p-6"):
            ui.label("📚 All Played Cards").classes("text-2xl font-bold text-center mb-4")
            ui.label(f"Total cards played: {len(self.ui.game.discard_pile)}").classes("text-lg text-center mb-4 text-gray-600")
            
            # Show cards in reverse order (most recent first)
            discard_cards = list(reversed(self.ui.game.discard_pile))
            
            with ui.scroll_area().classes("w-full h-96"):
                with ui.grid(columns=8).classes("gap-2 p-4"):
                    for i, card in enumerate(discard_cards):
                        CardComponents.create_discard_card(card, len(discard_cards) - i, self.ui.color_styles)  # Show position from start
            
            with ui.row().classes("w-full justify-center mt-4"):
                def close_dialog():
                    self.ui._active_dialog = False
                    dialog.close()
                
                ui.button("Close", on_click=close_dialog).classes("bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded")
        
        dialog.open()

    def _draw_card(self):
        """Draw cards - only if it's the viewing player's turn."""
        # This will be moved to card_actions.py
        pass

    def _back_to_lobby(self):
        """Return to lobby page."""
        self.ui.game_stage = 'lobby'
        ui.navigate.to('/lobby')
