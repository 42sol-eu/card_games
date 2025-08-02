"""
Reusable UI components for UNO game interface.
"""

from nicegui import ui

from ..game import Card, Color, CardType


class CardComponents:
    """Components for displaying UNO cards."""
    
    @staticmethod
    def get_card_display_text(card: Card) -> str:
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

    @staticmethod
    def get_mini_card_text(card: Card) -> str:
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

    @staticmethod
    def create_mini_card(card: Card, index: int, color_styles: dict):
        """Create a very small card display for the discard pile preview."""
        style = color_styles.get(card.color, color_styles[Color.RED])
        
        if card.color == Color.WILD:
            card_class = "w-8 h-12 wild-card-gradient text-white rounded text-xs flex items-center justify-center border"
        else:
            card_class = f"w-8 h-12 {style['bg']} {style['text']} rounded text-xs flex items-center justify-center border {style['border']}"
        
        with ui.card().classes(card_class):
            ui.label(CardComponents.get_mini_card_text(card)).classes("font-bold")

    @staticmethod
    def create_discard_card(card: Card, play_number: int, color_styles: dict):
        """Create a card display for the discard pile dialog."""
        style = color_styles.get(card.color, color_styles[Color.RED])
        
        if card.color == Color.WILD:
            # For wild cards in discard pile, try to show with the color it was played as
            card_class = "w-16 h-24 wild-card-gradient text-white rounded-lg shadow flex flex-col items-center justify-center border-2 border-purple-300"
        else:
            card_class = f"w-16 h-24 {style['bg']} {style['text']} rounded-lg shadow flex flex-col items-center justify-center border-2 {style['border']}"
        
        with ui.card().classes(card_class):
            # Play order number (small, at top)
            ui.label(f"#{play_number}").classes("text-xs opacity-70")
            
            # Card display
            ui.label(CardComponents.get_card_display_text(card)).classes("text-lg font-bold")
            
            # Color (small, at bottom)
            if card.color != Color.WILD:
                ui.label(card.color.value[:1].upper()).classes("text-xs font-semibold")
            else:
                ui.label("W").classes("text-xs font-semibold")


class DialogComponents:
    """Reusable dialog components."""
    
    @staticmethod
    def create_confirmation_dialog(title: str, message: str, on_confirm, on_cancel=None):
        """Create a confirmation dialog."""
        with ui.dialog() as dialog, ui.card():
            ui.label(title).classes("text-lg font-bold mb-4")
            if message:
                ui.label(message).classes("text-sm text-gray-600 mb-4")
            
            with ui.row().classes("gap-4"):
                def confirm():
                    on_confirm()
                    dialog.close()
                
                def cancel():
                    if on_cancel:
                        on_cancel()
                    dialog.close()
                
                ui.button("Yes", on_click=confirm).classes("bg-red-500 text-white")
                ui.button("Cancel", on_click=cancel).classes("bg-gray-500 text-white")
        
        return dialog
