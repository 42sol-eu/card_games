"""
Uno game user interface using NiceGUI.

This module provides a web-based UI for playing Uno games.
"""

try:
    from nicegui import ui
except ImportError:
    print("NiceGUI not installed. Install with: pip install nicegui")
    ui = None

from .game import UnoGame, Card, Color, CardType
from typing import List, Optional


class UnoUI:
    """Web-based user interface for Uno game."""
    
    def __init__(self):
        if ui is None:
            raise ImportError("NiceGUI is required for the UI. Install with: pip install nicegui")
        
        self.game = None
        self.player_names = []
        self.current_player = None
        self.color_choices = []

    def show_landing_page(self):
        """Display the initial landing page for setting up a game."""
        with ui.card().classes("w-full max-w-md mx-auto p-6"):
            ui.label("Uno Game").classes("text-3xl font-bold text-center mb-6")

            with ui.card().classes("p-4 mb-4"):
                ui.label("Enter player names (2-4 players):").classes("mb-2")

                self.player_inputs = []
                for i in range(4):
                    self.player_inputs.append(
                        ui.input(
                            label=f"Player {i+1}",
                            placeholder=f"Player {i+1} name"
                        ).classes("mb-2")
                    )

            def start_game():
                self.player_names = [input.value for input in self.player_inputs if input.value]
                if len(self.player_names) < 2:
                    ui.notify("Need at least 2 players!")
                    return

                self.game = UnoGame(self.player_names)
                self.current_player = self.game.get_current_player()
                self.show_game_page()

            ui.button("Start Game", on_click=start_game).classes("w-full bg-blue-500 text-white p-2")

    def show_game_page(self):
        """Display the main game interface."""
        ui.clear()

        with ui.row().classes("w-full max-w-4xl mx-auto p-2 gap-4"):
            # Left side - other players
            with ui.column().classes("w-1/4 gap-2"):
                ui.label("Players").classes("text-xl font-bold mb-2")

                player_counts = self.game.get_player_counts()
                for name, count in player_counts.items():
                    if name != self.current_player:
                        with ui.card().classes("p-2"):
                            ui.label(name).classes("font-bold")
                            ui.label(f"Cards: {count}").classes("text-center")

            # Middle - game area
            with ui.column().classes("w-2/4 gap-4 items-center"):
                # Current player and direction
                with ui.card().classes("w-full p-4"):
                    ui.label(f"Current Player: {self.current_player}").classes("text-2xl font-bold text-center")
                    ui.label(f"Direction: {'↻' if self.game.direction == 1 else '↺'}").classes("text-xl text-center")

                # Discard pile (top card)
                with ui.card().classes("w-32 h-48 bg-gray-200 flex flex-col items-center justify-center"):
                    top_card = self.game.get_top_card()
                    ui.label(str(top_card)).classes(f"text-4xl font-bold text-{top_card.get_display_color()}-600")

                # Draw pile
                def draw_card():
                    if self.game.forced_draw > 0:
                        drawn = self.game.draw_card(
                            list(self.game.players.keys()).index(self.current_player),
                            self.game.forced_draw
                        )
                        self.game.forced_draw = 0
                        ui.notify(f"Drew {len(drawn)} cards!")
                    else:
                        drawn = self.game.draw_card(
                            list(self.game.players.keys()).index(self.current_player)
                        )
                        ui.notify(f"Drew 1 card!")

                    self.update_game_state()

                with ui.card().classes("w-32 h-24 bg-gray-300 flex items-center justify-center cursor-pointer") as draw_pile:
                    ui.label("Draw Pile").classes("text-xl font-bold")
                    ui.label(f"Cards: {len(self.game.draw_pile)}").classes("text-sm")
                    draw_pile.on('click', draw_card)

                if self.game.forced_draw > 0:
                    ui.notify(f"You must draw {self.game.forced_draw} cards!").classes("text-red-600")

            # Right side - current player's hand
            with ui.column().classes("w-1/4"):
                ui.label("Your Hand").classes("text-xl font-bold mb-2 text-center")

                hand = self.game.get_player_hand(self.current_player)
                with ui.scroll_area().classes("h-[600px] p-2"):
                    for i, card in enumerate(hand):
                        with ui.card().classes(f"w-24 h-36 mb-2 bg-{card.get_display_color()}-100"):
                            ui.label(str(card)).classes(f"text-3xl font-bold text-{card.get_display_color()}-800 text-center")

                            if card.type in (CardType.WILD, CardType.WILD_DRAW_FOUR):
                                def on_wild_click(card_idx=i):
                                    self.show_color_picker(card_idx)

                                ui.button("Play", on_click=lambda: on_wild_click(i)).classes("mt-2")
                            else:
                                def on_card_click(card_idx=i):
                                    success, message = self.game.play_card(
                                        list(self.game.players.keys()).index(self.current_player),
                                        card_idx
                                    )
                                    if success:
                                        self.update_game_state()
                                    else:
                                        ui.notify(message or "Can't play that card!")

                                ui.button("Play", on_click=lambda: on_card_click(i)).classes("mt-2")

    def show_color_picker(self, card_index: int):
        """Show a dialog for choosing colors when playing wild cards."""
        with ui.dialog() as dialog:
            ui.label("Choose a color:").classes("text-xl font-bold mb-4")

            with ui.row().classes("justify-center gap-4"):
                for color in [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]:
                    with ui.card().classes(f"w-20 h-20 flex flex-col items-center justify-center bg-{color.value}-500 rounded-lg cursor-pointer"):
                        def on_color_select(c=color, idx=card_index):
                            success, message = self.game.play_card(
                                list(self.game.players.keys()).index(self.current_player),
                                idx,
                                c
                            )
                            if success:
                                self.update_game_state()
                                dialog.close()
                            else:
                                ui.notify(message or "Couldn't play that card!")

                        ui.button("", on_click=lambda: on_color_select()).classes("w-full h-full")
                        ui.label(color.value.capitalize()).classes("text-white font-bold")

            dialog.open()

    def update_game_state(self):
        """Update the game state and refresh the UI."""
        self.current_player = self.game.get_current_player()
        self.show_game_page()

    def run(self, title: str = "Uno Game", port: int = 8080):
        """Run the UI application."""
        if ui is None:
            raise ImportError("NiceGUI is required for the UI. Install with: pip install nicegui")
        
        ui.run(title=title, port=port, native=True)
