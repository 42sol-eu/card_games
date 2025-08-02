"""
Card actions and game interactions for UNO game interface.
"""

from nicegui import ui

from .base import UnoUIBase
from .components import CardComponents
from ..game import Card, Color, CardType


class CardActions:
    """Handles card playing and game actions."""
    
    def __init__(self, ui_instance: UnoUIBase):
        self.ui = ui_instance

    def draw_card(self):
        """Draw cards - only if it's the viewing player's turn."""
        if not self.ui.player_name or self.ui.current_player != self.ui.player_name:
            ui.notify("It's not your turn!", type='warning')
            return
        
        player_index = self.ui.get_player_index()
        if player_index == -1:
            ui.notify("Player not found in game!", type='error')
            return
            
        if self.ui.game.forced_draw > 0:
            drawn = self.ui.game.handle_forced_draw(player_index)
            ui.notify(f"Drew {len(drawn)} cards!", type='info')
        else:
            drawn = self.ui.game.draw_card(player_index)
            info = '( '
            for card in drawn:
                info += f'{str(card)} '
            info += ' )'
            ui.notify(f"Drew {len(drawn)} {info} card!", type='info')
        
        self.ui.game._next_turn()
        # Update current player immediately after turn change
        self.ui.current_player = self.ui.game.get_current_player()
        self.ui.update_game_state()

    def play_card(self, card_index: int):
        """Play a card - only if it's the viewing player's turn."""
        if not self.ui.player_name or self.ui.current_player != self.ui.player_name:
            ui.notify("It's not your turn!", type='warning')
            return
        
        player_index = self.ui.get_player_index()
        if player_index == -1:
            ui.notify("Player not found in game!", type='error')
            return
            
        hand = self.ui.game.get_player_hand(self.ui.player_name)
        card = hand[card_index]
        
        # Handle wild cards
        if card.type in (CardType.WILD, CardType.WILD_DRAW):
            self._show_color_picker(card_index)
            return
        
        # Handle forced draw
        if self.ui.game.forced_draw > 0:
            if card.type == CardType.DRAW_TWO:
                success, message = self.ui.game.play_card(
                    player_index,
                    card_index
                )
                if success:
                    # Update current player immediately after successful play
                    self.ui.current_player = self.ui.game.get_current_player()
                    ui.notify(f"Stacked +2! Next player draws {self.ui.game.forced_draw}!", type='positive')
            else:
                ui.notify(f"Must draw {self.ui.game.forced_draw} cards or play +2!", type='warning')
                return
        else:
            success, message = self.ui.game.play_card(
                player_index,
                card_index
            )
            
            if success:
                # Update current player immediately after successful play
                self.ui.current_player = self.ui.game.get_current_player()
                ui.notify(f"Played {card}!" if not message else message, type='positive')
            else:
                ui.notify(message or "Cannot play that card!", type='negative')
                return  # Don't call update_game_state if the play failed
        
        self.ui.update_game_state()

    def is_card_playable(self, card: Card) -> bool:
        """Check if a card is playable."""
        # Only allow playing if it's the viewing player's turn
        if not self.ui.player_name or self.ui.current_player != self.ui.player_name:
            return False
            
        if self.ui.game.forced_draw > 0:
            return card.type == CardType.DRAW_TWO
        
        if card.type in (CardType.WILD, CardType.WILD_DRAW):
            return True
        
        top_card = self.ui.game.get_top_card()
        return (card.color == self.ui.game.current_color or
                card.type == top_card.type or
                (card.type == CardType.NUMBER and top_card.type == CardType.NUMBER and card.value == top_card.value))

    def _show_color_picker(self, card_index: int):
        """Show color picker for wild cards."""
        self.ui._active_dialog = True
        
        player_index = self.ui.get_player_index()
        if player_index == -1:
            ui.notify("Player not found in game!", type='error')
            self.ui._active_dialog = False
            return

        with ui.dialog() as dialog, ui.card().classes("p-6"):
            ui.label("🌈 Choose a Color X").classes("text-2xl font-bold text-center mb-4")

            # Get current player's hand to count cards by color
            hand = self.ui.game.get_player_hand(self.ui.player_name)
            color_counts = {}
            
            # Count cards by color (excluding wild cards)
            for card in hand:
                if card.color != Color.WILD:
                    color_counts[card.color] = color_counts.get(card.color, 0) + 1

            with ui.grid(columns=2).classes("gap-4"):
                colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]
                
                for color in colors:
                    style = self.ui.color_styles[color]
                    card_count = color_counts.get(color, 0)
                    
                    def select_color(c=color):
                        success, message = self.ui.game.play_card(
                            player_index,
                            card_index,
                            c
                        )
                        if success:
                            # Update current player immediately after successful play
                            self.ui.current_player = self.ui.game.get_current_player()
                            ui.notify(f"Played wild! Color: {c.value.title()}!" if not message else message, type='positive')
                            dialog.close()
                            self.ui._active_dialog = False
                            self.ui.update_game_state()
                        else:
                            ui.notify(message or "Cannot play that card!", type='negative')                            
                            self.ui._active_dialog = False
                    
                    ui.button(
                        f"{color.value.title()} ({card_count})",
                        on_click=select_color
                    ).classes(f"p-4 {style['bg']} {style['text']} font-bold rounded-lg hover:scale-105 transition-all duration-300 shadow-lg")

            dialog.open()


class HandDisplay:
    """Handles displaying and interacting with player's hand."""
    
    def __init__(self, ui_instance: UnoUIBase, card_actions: CardActions):
        self.ui = ui_instance
        self.card_actions = card_actions

    def create_horizontal_hand(self):
        """Create the player's hand in a horizontal row."""
        if not self.ui.player_name:
            return
            
        hand = self.ui.game.get_player_hand(self.ui.player_name)
        sorted_hand = sorted(hand, key=lambda card: card.get_sort_key())
        
        with ui.row().classes("flex-wrap justify-center gap-2 p-4"):
            for i, card in enumerate(sorted_hand):
                original_index = hand.index(card)
                self._create_horizontal_card(card, original_index, i)

    def _create_horizontal_card(self, card: Card, original_index: int, display_index: int):
        """Create a single card in horizontal layout."""
        style = self.ui.color_styles.get(card.color, self.ui.color_styles[Color.RED])
        playable = self.card_actions.is_card_playable(card) and (self.ui.current_player == self.ui.player_name)
        
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
        
        with ui.card().classes(card_class) as card_element:
            # Card number (small, at top)
            ui.label(f"#{display_index + 1}").classes("text-xs opacity-70 mb-1")
            
            # Card value (large, center) - use custom display method
            ui.label(CardComponents.get_card_display_text(card)).classes("text-2xl font-bold mb-1")
            
            # Color name (small, at bottom) - always show color
            if card.color != Color.WILD:
                ui.label(card.color.value.title()).classes("text-xs font-semibold")
            else:
                ui.label("Wild").classes("text-xs font-semibold")
            
            # Play button (only if playable and my turn)
            if playable:
                ui.button("PLAY", on_click=lambda idx=original_index: self.card_actions.play_card(idx)).classes("mt-2 bg-white/30 hover:bg-white/50 font-bold py-1 px-2 rounded text-xs")
            
            # Make entire card clickable if playable
            if playable:
                card_element.on('click', lambda idx=original_index: self.card_actions.play_card(idx))
