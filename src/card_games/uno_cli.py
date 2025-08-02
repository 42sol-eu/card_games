"""
Command-line interface for Uno game with Rich formatting.

This module provides a beautiful text-based interface for playing Uno games.
"""

from .uno import UnoGame, Card, Color, CardType
from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.columns import Columns
from rich.align import Align
from rich import box
from rich.style import Style


class UnoCLI:
    """Command-line interface for Uno game with Rich formatting."""
    
    def __init__(self):
        self.game = None
        self.preset_players = None  # Allow preset number of players
        self.console = Console()
        self._current_sorted_hand = []  # Store sorted hand for card selection
        
        # Color mapping for cards
        self.color_map = {
            Color.RED: "red",
            Color.BLUE: "blue", 
            Color.GREEN: "green",
            Color.YELLOW: "yellow1",  # Pure bright yellow
            Color.WILD: "magenta"
        }

    def _create_full_card_panel(self, card: Card, style_prefix: str = "green") -> Panel:
        """Create a full-sized card panel with ASCII art."""
        card_content = Text()
        
        # Format card value/type with ASCII art
        if card.type == CardType.NUMBER:
            ascii_number = self._create_ascii_number(card.value)
            card_content = ascii_number
            if card.color != Color.WILD:
                color_name = card.color.value.lower()
                card_content.append(f"\n{color_name}", style="bold white")
        elif card.type == CardType.WILD:
            ascii_symbol = self._create_ascii_symbol("?")
            card_content = ascii_symbol
        elif card.type == CardType.WILD_DRAW:
            ascii_symbol = self._create_ascii_symbol("+4")
            card_content = ascii_symbol
        else:
            card_value = str(card).upper()
            if card.color != Color.WILD:
                color_name = card.color.value.lower()
                if "DRAW TWO" in card_value:
                    ascii_symbol = self._create_ascii_symbol("+2")
                    card_content = ascii_symbol
                    card_content.append(f"\n{color_name}", style="bold white")
                elif "REVERSE" in card_value:
                    ascii_symbol = self._create_ascii_symbol("<-")
                    card_content = ascii_symbol
                    card_content.append(f"\n{color_name}", style="bold white")
                elif "SKIP" in card_value:
                    ascii_symbol = self._create_ascii_symbol("!")
                    card_content = ascii_symbol
                    card_content.append(f"\n{color_name}", style="bold white")
                else:
                    card_content.append(f"\n{card_value}\n\n{color_name}", style="bold white")
            else:
                if "DRAW TWO" in card_value:
                    ascii_symbol = self._create_ascii_symbol("+2")
                    card_content = ascii_symbol
                elif "REVERSE" in card_value:
                    ascii_symbol = self._create_ascii_symbol("<-")
                    card_content = ascii_symbol
                elif "SKIP" in card_value:
                    ascii_symbol = self._create_ascii_symbol("!")
                    card_content = ascii_symbol
                else:
                    card_content.append(f"\n{card_value}\n", style="bold white")
        
        # Determine background color
        if card.color != Color.WILD:
            background_color = self.color_map.get(card.color, "white")
        else:
            background_color = "magenta"
        
        # Create card panel
        return Panel(
            Align.center(card_content),
            style=f"{style_prefix} on {background_color}",
            width=14,
            height=8
        )

    def _create_ascii_number(self, number: int) -> Text:
        """Create ASCII art representation of a number for card values."""
        # ASCII art patterns for numbers 0-9 (5 rows high, calculator style)
        ascii_patterns = {
            0: [
                " ███ ",
                "█   █",
                "█   █",
                "█   █",
                " ███ "
            ],
            1: [
                "  █  ",
                " ██  ",
                "  █  ",
                "  █  ",
                " ███ "
            ],
            2: [
                " ███ ",
                "    █",
                " ███ ",
                "█    ",
                "█████"
            ],
            3: [
                " ███ ",
                "    █",
                " ███ ",
                "    █",
                " ███ "
            ],
            4: [
                "█   █",
                "█   █",
                "█████",
                "    █",
                "    █"
            ],
            5: [
                "█████",
                "█    ",
                "████ ",
                "    █",
                "████ "
            ],
            6: [
                " ███ ",
                "█    ",
                "████ ",
                "█   █",
                " ███ "
            ],
            7: [
                "█████",
                "    █",
                "   █ ",
                "  █  ",
                " █   "
            ],
            8: [
                " ███ ",
                "█   █",
                " ███ ",
                "█   █",
                " ███ "
            ],
            9: [
                " ███ ",
                "█   █",
                " ████",
                "    █",
                " ███ "
            ]
        }
        
        if number < 10:
            pattern = ascii_patterns.get(number, [" ███ ", "█   █", "█   █", "█   █", " ███ "])
            return Text("\n".join(pattern), style="bold white")
        else:
            # For multi-digit numbers, combine patterns
            digits = [int(d) for d in str(number)]
            lines = ["", "", "", "", ""]
            for i, digit in enumerate(digits):
                digit_pattern = ascii_patterns.get(digit, [" ███ ", "█   █", "█   █", "█   █", " ███ "])
                for line_idx in range(5):
                    if i > 0:  # Add space between digits
                        lines[line_idx] += " "
                    lines[line_idx] += digit_pattern[line_idx]
            return Text("\n".join(lines), style="bold white")

    def _create_ascii_symbol(self, symbol: str) -> Text:
        """Create ASCII art representation of UNO card symbols."""
        # ASCII art patterns for UNO symbols (5 rows high)
        symbol_patterns = {
            "+2": [
                "     ███ ",
                "  █     █",
                " ███ ███ ",
                "  █  █   ",
                "    ████ "
            ],
            "+4": [
                "    █   █",
                " █  █   █",
                "███ █████",
                " █      █",
                "        █"
            ],
            "<-": [
                "   █     ",
                "  ██     ",
                " ███████ ",
                "  ██     ",
                "   █     "
            ],
            "!": [
                "  ███  ",
                "  ███  ",
                "  ███  ",
                "       ",
                "  ███  "
            ],
            "?": [
                "  ███ ",
                " █   █",
                "   ██ ",
                "      ",
                "   ██ "
            ]
        }
        
        pattern = symbol_patterns.get(symbol, [" ███ ", "█   █", "█   █", "█   █", " ███ "])
        return Text("\n".join(pattern), style="bold white")

    def play(self):
        """Start and play a game of Uno."""
        # Welcome banner
        welcome_panel = Panel(
            Text("🎮 Welcome to UNO! 🎮", style="bold cyan", justify="center"),
            box=box.DOUBLE,
            style="cyan"
        )
        self.console.print(welcome_panel)
        self.console.print()
        
        # Get player names
        player_names = self._get_player_names()
        
        # Start the game
        self.game = UnoGame(player_names)
        
        # Game start info
        start_info = f"🎯 Game started with players: {', '.join(player_names)}\n"
        start_info += f"🃏 Starting card: {self._format_card_display(self.game.get_top_card())}"
        
        start_panel = Panel(start_info, title="Game Started", style="green")
        self.console.print(start_panel)
        self.console.print()
        
        # Main game loop
        while not self.game.is_game_over():
            self._play_turn()
        
        # Winner announcement
        winner_panel = Panel(
            Text(f"🎉 Game Over! Winner: {self.game.winner} 🎉", style="bold gold1", justify="center"),
            box=box.DOUBLE,
            style="gold1"
        )
        self.console.print(winner_panel)

    def _format_card_display(self, card: Card) -> Text:
        """Format a card for rich display with colors."""
        color_style = self.color_map.get(card.color, "white")
        
        # Special formatting for different card types
        if card.type == CardType.NUMBER:
            display_text = f"{card.value}"
        elif card.type == CardType.WILD:
            display_text = "? WILD"
            color_style = "rainbow"
        elif card.type == CardType.WILD_DRAW:
            display_text = "+4 WILD"
            color_style = "rainbow"
        else:
            card_str = str(card).upper()
            if "DRAW TWO" in card_str:
                display_text = "+2"
            elif "REVERSE" in card_str:
                display_text = "<-"
            elif "SKIP" in card_str:
                display_text = "!"
            else:
                display_text = card_str
        
        return Text(display_text, style=f"bold {color_style}")
    
    def _create_card_panel(self, card: Card, playable: bool = True) -> Panel:
        """Create a panel representation of a card."""
        card_text = self._format_card_display(card)
        
        # Add playability indicator
        if playable:
            border_style = "green"
            suffix = " ✓"
        else:
            border_style = "red"
            suffix = " ✗"
        
        card_content = Text()
        card_content.append_text(card_text)
        card_content.append(suffix, style=f"bold {border_style}")
        
        color_style = self.color_map.get(card.color, "white")
        return Panel(
            Align.center(card_content),
            style=color_style,
            width=12,
            height=3
        )
    def _get_player_names(self) -> List[str]:
        """Get player names from user input with rich prompts."""
        players = []
        
        if self.preset_players:
            info_panel = Panel(
                f"Enter names for {self.preset_players} players:",
                title="Player Setup",
                style="blue"
            )
            self.console.print(info_panel)
            
            for i in range(self.preset_players):
                while True:
                    name = Prompt.ask(f"[bold cyan]Player {i+1} name[/bold cyan]").strip()
                    if name:
                        players.append(name)
                        break
                    self.console.print("[red]Please enter a valid name.[/red]")
            return players
        
        info_panel = Panel(
            "Enter player names (2-4 players). Press Enter with empty name to finish.",
            title="Player Setup",
            style="blue"
        )
        self.console.print(info_panel)
        
        for i in range(4):
            name = Prompt.ask(f"[bold cyan]Player {i+1} name[/bold cyan]", default="").strip()
            if not name:
                break
            players.append(name)
        
        if len(players) < 2:
            self.console.print("[red]Need at least 2 players![/red]")
            return self._get_player_names()
        
        return players

    def _play_turn(self):
        """Play a single turn with rich formatting."""
        current_player = self.game.get_current_player()
        
        # Turn header
        turn_panel = Panel(
            Text(f"🎯 {current_player}'s Turn", style="bold cyan", justify="center"),
            style="cyan"
        )
        self.console.print(turn_panel)
        
        # Game state display
        self._display_game_state()
        
        # Handle forced draw
        if self.game.forced_draw > 0:
            current_player = self.game.get_current_player()
            hand = self.game.get_player_hand(current_player)
            
            # Check if player has any +2 cards to stack
            has_draw_two = any(card.type == CardType.DRAW_TWO for card in hand)
            
            if has_draw_two:
                warning_panel = Panel(
                    f"⚠️  You must draw {self.game.forced_draw} cards!\n💡 Or play a +2 card to stack and pass to next player",
                    title="Forced Draw - Stack Option Available",
                    style="yellow"
                )
                self.console.print(warning_panel)
                
                # Show player's hand so they can see their +2 cards
                self._display_player_hand(current_player)
                
                # Get player action - they can play a +2 or draw
                action = Prompt.ask(
                    f"\n[bold yellow]Choose action[/bold yellow]: [cyan][1-{len(hand)}][/cyan] to play card (only +2 allowed), [cyan]'d'[/cyan] to draw {self.game.forced_draw} cards"
                ).strip().lower()
                
                if action == 'd':
                    # Player chooses to draw
                    drawn = self.game.handle_forced_draw(self.game.current_player)
                    
                    # Display all drawn cards as full-sized cards
                    self.console.print(Text("Drew cards:", style="bold yellow"))
                    
                    # Create panels for each drawn card
                    card_panels = [self._create_full_card_panel(card, "yellow") for card in drawn]
                    
                    # Display cards in columns
                    cards_row = Columns(card_panels, width=14, expand=False)
                    self.console.print(cards_row)
                    
                    # Pause to let player see the drawn cards
                    Prompt.ask("Press Enter to continue", default="")
                    
                    self.game._next_turn()
                    return
                else:
                    # Player tries to play a card (must be +2)
                    try:
                        display_index = int(action) - 1
                        if 0 <= display_index < len(self._current_sorted_hand):
                            # Get the card from the sorted hand
                            card = self._current_sorted_hand[display_index]
                            # Find the original index in the unsorted hand
                            original_hand = self.game.get_player_hand(current_player)
                            card_index = original_hand.index(card)
                            
                            success, message = self.game.play_card(self.game.current_player, card_index)
                            
                            if success:
                                if message:  # Win message
                                    win_panel = Panel(
                                        Text(f"🎉 {message}", style="bold gold1", justify="center"),
                                        style="gold1"
                                    )
                                    self.console.print(win_panel)
                                else:
                                    played_text = Text("Played: ")
                                    played_text.append_text(self._format_card_display(card))
                                    stack_text = Text(f" (Stacked! Next player must draw {self.game.forced_draw} cards)")
                                    played_text.append_text(stack_text)
                                    played_panel = Panel(played_text, style="green")
                                    self.console.print(played_panel)
                                return
                            else:
                                error_panel = Panel(f"❌ {message}", style="red")
                                self.console.print(error_panel)
                                self._play_turn()  # Try again
                                return
                        else:
                            self.console.print("[red]Invalid card number![/red]")
                            self._play_turn()  # Try again
                            return
                    except ValueError:
                        self.console.print("[red]Invalid input![/red]")
                        self._play_turn()  # Try again
                        return
            else:
                # No +2 cards, must draw
                warning_panel = Panel(
                    f"⚠️  You must draw {self.game.forced_draw} cards!",
                    title="Forced Draw",
                    style="red"
                )
                self.console.print(warning_panel)
                
                Prompt.ask("Press Enter to draw cards", default="")
                drawn = self.game.handle_forced_draw(self.game.current_player)
                
                # Display all drawn cards as full-sized cards
                self.console.print(Text("Drew cards:", style="bold yellow"))
                
                # Create panels for each drawn card
                card_panels = [self._create_full_card_panel(card, "yellow") for card in drawn]
                
                # Display cards in columns
                cards_row = Columns(card_panels, width=14, expand=False)
                self.console.print(cards_row)
                
                # Pause to let player see the drawn cards
                Prompt.ask("Press Enter to continue", default="")
                
                self.game._next_turn()
                return
        
        # Show player's hand
        self._display_player_hand(current_player)
        
        # Get player action
        hand = self.game.get_player_hand(current_player)
        action = Prompt.ask(
            f"\n[bold green]Choose action[/bold green]: [cyan][1-{len(hand)}][/cyan] to play card, [cyan]'1,2,3'[/cyan] for multiple cards, [cyan]'d'[/cyan] to draw, [cyan]'q'[/cyan] to quit"
        ).strip().lower()
        
        if action == 'q':
            self.console.print("[yellow]Thanks for playing![/yellow]")
            exit()
        elif action == 'd':
            drawn = self.game.draw_card(self.game.current_player)
            drawn_card = drawn[0]
            
            # Create full-sized card display for the drawn card
            drawn_card_panel = self._create_full_card_panel(drawn_card, "yellow")
            drawn_card_panel.title = "Drew Card"
            
            self.console.print(Align.center(drawn_card_panel))
            
            # Pause to let player see the drawn card
            Prompt.ask("Press Enter to continue", default="")
            
            self.game._next_turn()
        else:
            try:
                # Check if action contains commas (multiple cards)
                if ',' in action:
                    # Multiple cards selected
                    card_numbers = [int(x.strip()) for x in action.split(',')]
                    display_indices = [n - 1 for n in card_numbers]
                    
                    # Validate all indices
                    if not all(0 <= i < len(self._current_sorted_hand) for i in display_indices):
                        self.console.print("[red]Invalid card number(s)![/red]")
                        self._play_turn()  # Try again
                        return
                    
                    # Get the cards from the sorted hand
                    cards_to_play = [self._current_sorted_hand[i] for i in display_indices]
                    
                    # Find the original indices in the unsorted hand
                    original_hand = self.game.get_player_hand(current_player)
                    card_indices = []
                    
                    for card in cards_to_play:
                        # Find the card in the original hand (handle duplicates by removing found cards)
                        temp_hand = original_hand.copy()
                        for idx, temp_card in enumerate(temp_hand):
                            if (temp_card.type == card.type and 
                                temp_card.color == card.color and 
                                temp_card.value == card.value):
                                # Find the actual index in the original hand
                                actual_idx = original_hand.index(temp_card)
                                card_indices.append(actual_idx)
                                original_hand[actual_idx] = None  # Mark as used
                                break
                    
                    # Handle wild cards (only if single card)
                    chosen_color = None
                    if len(cards_to_play) == 1 and cards_to_play[0].type in (CardType.WILD, CardType.WILD_DRAW):
                        chosen_color = self._choose_color()
                    
                    success, message = self.game.play_multiple_cards(self.game.current_player, card_indices, chosen_color)
                    
                    if success:
                        if message:  # Win message
                            win_panel = Panel(
                                Text(f"🎉 {message}", style="bold gold1", justify="center"),
                                style="gold1"
                            )
                            self.console.print(win_panel)
                        else:
                            played_text = Text("Played: ")
                            for i, card in enumerate(cards_to_play):
                                if i > 0:
                                    played_text.append(", ")
                                played_text.append_text(self._format_card_display(card))
                            played_panel = Panel(played_text, style="green")
                            self.console.print(played_panel)
                    else:
                        error_panel = Panel(f"❌ {message}", style="red")
                        self.console.print(error_panel)
                        self._play_turn()  # Try again
                else:
                    # Single card selected
                    display_index = int(action) - 1
                    if 0 <= display_index < len(self._current_sorted_hand):
                        # Get the card from the sorted hand
                        card = self._current_sorted_hand[display_index]
                        # Find the original index in the unsorted hand
                        original_hand = self.game.get_player_hand(current_player)
                        card_index = original_hand.index(card)
                        
                        # Handle wild cards
                        chosen_color = None
                        if card.type in (CardType.WILD, CardType.WILD_DRAW):
                            chosen_color = self._choose_color()
                        
                        success, message = self.game.play_card(self.game.current_player, card_index, chosen_color)
                        
                        if success:
                            if message:  # Win message
                                win_panel = Panel(
                                    Text(f"🎉 {message}", style="bold gold1", justify="center"),
                                    style="gold1"
                                )
                                self.console.print(win_panel)
                            else:
                                played_text = Text("Played: ")
                                played_text.append_text(self._format_card_display(card))
                                played_panel = Panel(played_text, style="green")
                                self.console.print(played_panel)
                        else:
                            error_panel = Panel(f"❌ {message}", style="red")
                            self.console.print(error_panel)
                            self._play_turn()  # Try again
                    else:
                        self.console.print("[red]Invalid card number![/red]")
                        self._play_turn()  # Try again
            except ValueError:
                self.console.print("[red]Invalid input! Use numbers like '1' or '1,2,3'[/red]")
                self._play_turn()  # Try again

    def _display_game_state(self):
        """Display the current game state with top card, draw pile, and other players."""
        current_player = self.game.get_current_player()
        
        # Create top card display with colored background
        top_card = self.game.get_top_card()
        
        # Format top card content with ASCII art for numbers
        top_card_text = Text()
        
        if top_card.type == CardType.NUMBER:
            # Use ASCII art for number cards
            ascii_number = self._create_ascii_number(top_card.value)
            top_card_text = ascii_number
        elif top_card.type == CardType.WILD:
            # Use ASCII art for WILD symbol
            ascii_symbol = self._create_ascii_symbol("?")
            top_card_text = ascii_symbol
        elif top_card.type == CardType.WILD_DRAW:
            # Use ASCII art for +4 symbol
            ascii_symbol = self._create_ascii_symbol("+4")
            top_card_text = ascii_symbol
        else:
            # Use ASCII art for other card types
            card_value = str(top_card).upper()
            if "DRAW TWO" in card_value:
                ascii_symbol = self._create_ascii_symbol("+2")
                top_card_text = ascii_symbol
            elif "REVERSE" in card_value:
                ascii_symbol = self._create_ascii_symbol("<-")
                top_card_text = ascii_symbol
            elif "SKIP" in card_value:
                ascii_symbol = self._create_ascii_symbol("!")
                top_card_text = ascii_symbol
            else:
                top_card_text.append(f"\n{card_value}\n", style="bold white")
        
        # Always add color name - for wild cards, show the current chosen color
        if top_card.type in (CardType.WILD, CardType.WILD_DRAW):
            # For wild cards, show the chosen color
            color_name = self.game.current_color.value.lower()
            top_card_text.append(f"\n{color_name}", style="bold white")
            background_color = self.color_map.get(self.game.current_color, "magenta")
        elif top_card.color != Color.WILD:
            color_name = top_card.color.value.lower()
            top_card_text.append(f"\n{color_name}", style="bold white")
            background_color = self.color_map.get(top_card.color, "white")
        else:
            background_color = "magenta"
        
        top_card_panel = Panel(
            Align.center(top_card_text),
            title="🎯 Top Card",
            style=f"green on {background_color}",
            width=20,
            height=8  # Increased height to accommodate ASCII art
        )
        
        # Create draw pile display
        draw_pile_content = Text()
        draw_pile_content.append(f"{len(self.game.draw_pile)} cards", style="bold blue")
        
        draw_pile_panel = Panel(
            Align.center(draw_pile_content),
            title="🂠 Draw Pile",
            style="blue",
            width=20,
            height=8  # Match top card height
        )
                
        # Create other players display
        player_counts = self.game.get_player_counts()
        other_players = [(name, count) for name, count in player_counts.items() if name != current_player]
        
        if other_players:
            # Create horizontal layout: Player1: X cards | Player2: Y cards
            players_text = Text()
            for i, (name, count) in enumerate(other_players):
                if i > 0:
                    players_text.append(" | ", style="dim")
                players_text.append(f"{name}: ", style="cyan")
                players_text.append(f"{count} cards", style="yellow1")
            
            other_players_panel = Panel(
                Align.center(players_text),
                title="👥 Other Players",
                style="dim",
                width=40,
                height=8  # Match top card height
            )
        else:
            other_players_panel = Panel(
                Align.center(Text("No other players", style="dim")),
                title="👥 Other Players",
                style="dim",
                width=40,
                height=8  # Match top card height
            )
        
        # Arrange in columns: Top Card, Draw Pile, Direction, Other Players
        game_state = Columns([top_card_panel, draw_pile_panel, other_players_panel], expand=False)
        self.console.print(game_state)
        
    def _display_player_hand(self, current_player: str):
        """Display the current player's hand horizontally with framed cards."""
        hand = self.game.get_player_hand(current_player)
        
        # Sort the hand by color and number
        sorted_hand = sorted(hand, key=lambda card: card.get_sort_key())
        
        # Store the sorted hand for later use in card selection
        self._current_sorted_hand = sorted_hand
        
        hand_title = f"🃏 {current_player}'s Hand ({len(sorted_hand)} cards)"
        hand_panel = Panel(hand_title, style="black")
        self.console.print(hand_panel)
        
        # Create framed card displays
        card_panels = []
        for i, card in enumerate(sorted_hand):
            # Use display index (i+1) instead of original index
            playable = self._is_card_playable(card)
            
            # Create card content without number (number will be above)
            card_content = Text()
            
            # Format card value/type with ASCII art for numbers
            if card.type == CardType.NUMBER:
                # Use ASCII art for number cards
                ascii_number = self._create_ascii_number(card.value)
                card_content = ascii_number
                if card.color != Color.WILD:
                    color_name = card.color.value.lower()
                    card_content.append(f"\n{color_name}", style="bold white")
            elif card.type == CardType.WILD:
                # Use ASCII art for WILD symbol
                ascii_symbol = self._create_ascii_symbol("?")
                card_content = ascii_symbol
            elif card.type == CardType.WILD_DRAW:
                # Use ASCII art for +4 symbol
                ascii_symbol = self._create_ascii_symbol("+4")
                card_content = ascii_symbol
            else:
                # Use ASCII art for other card types
                card_value = str(card).upper()
                if card.color != Color.WILD:
                    color_name = card.color.value.lower()
                    if "DRAW TWO" in card_value:
                        ascii_symbol = self._create_ascii_symbol("+2")
                        card_content = ascii_symbol
                        card_content.append(f"\n{color_name}", style="bold white")
                    elif "REVERSE" in card_value:
                        ascii_symbol = self._create_ascii_symbol("<-")
                        card_content = ascii_symbol
                        card_content.append(f"\n{color_name}", style="bold white")
                    elif "SKIP" in card_value:
                        ascii_symbol = self._create_ascii_symbol("!")
                        card_content = ascii_symbol
                        card_content.append(f"\n{color_name}", style="bold white")
                    else:
                        card_content.append(f"\n{card_value}\n\n{color_name}", style="bold white")
                else:
                    if "DRAW TWO" in card_value:
                        ascii_symbol = self._create_ascii_symbol("+2")
                        card_content = ascii_symbol
                    elif "REVERSE" in card_value:
                        ascii_symbol = self._create_ascii_symbol("<-")
                        card_content = ascii_symbol
                    elif "SKIP" in card_value:
                        ascii_symbol = self._create_ascii_symbol("!")
                        card_content = ascii_symbol
                    else:
                        card_content.append(f"\n{card_value}\n", style="bold white")
            
            # Determine background color and border style
            if card.color != Color.WILD:
                background_color = self.color_map.get(card.color, "white")
            else:
                background_color = "magenta"
            
            border_style = "green" if playable else "red"
            
            # Create card number label above the card (using display index for playing)
            display_index = i + 1
            card_number = Text(f"[{display_index}]", style="bold white", justify="center")
            
            # Create a small panel for each card with colored background
            card_panel = Panel(
                Align.center(card_content),
                style=f"{border_style} on {background_color}",
                width=14,
                height=8  # Increased height to accommodate ASCII art
            )
            
            # Combine number and card panel
            card_with_number = Align.center(
                Text.from_markup(f"[bold white]\\[{display_index}][/bold white]\n") + 
                Text(" ") # This will be replaced by the panel in columns
            )
            
            card_panels.append((f"[{display_index}]", card_panel))
        
        # Display cards in rows, maximum 10 cards per row for better spacing
        cards_per_row = 10
        for i in range(0, len(card_panels), cards_per_row):
            row_data = card_panels[i:i+cards_per_row]
            
            # Create number labels row
            number_labels = []
            panels_only = []
            
            for number_label, panel in row_data:
                number_labels.append(Text(number_label, style="bold white", justify="center"))
                panels_only.append(panel)
            
            # Display number labels
            numbers_row = Columns(number_labels, width=14, expand=False)
            self.console.print(numbers_row)
            
            # Display the card panels
            cards_row = Columns(panels_only, width=14, expand=False)
            self.console.print(cards_row)
            
            # Add spacing between rows if there are more cards
            if i + cards_per_row < len(card_panels):
                self.console.print()
    
    def _display_other_players(self, current_player: str):
        """Display other players' card counts."""
        player_counts = self.game.get_player_counts()
        other_players = [(name, count) for name, count in player_counts.items() if name != current_player]
        
        if other_players:
            # Create table for other players
            table = Table(title="👥 Other Players", style="dim")
            table.add_column("Player", style="cyan")
            table.add_column("Cards", justify="center", style="yellow")
            
            for name, count in other_players:
                table.add_row(name, str(count))
            
            self.console.print(table)
    
    def _is_card_playable(self, card: Card) -> bool:
        """Check if a card is playable (for display purposes)."""
        top_card = self.game.get_top_card()
        
        if card.type in (CardType.WILD, CardType.WILD_DRAW):
            return True
        
        return (card.color == self.game.current_color or
                card.type == top_card.type or
                (card.type == CardType.NUMBER and top_card.type == CardType.NUMBER and card.value == top_card.value))

    def _choose_color(self) -> Color:
        """Let player choose a color for wild cards with rich interface."""
        colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]
        
        # Create color choice table
        table = Table(title="🌈 Choose a Color", style="bold")
        table.add_column("Number", justify="center", style="dim")
        table.add_column("Color", justify="center")
        
        for i, color in enumerate(colors):
            color_style = self.color_map[color]
            color_text = Text(color.value.capitalize(), style=f"bold {color_style}")
            table.add_row(str(i+1), color_text)
        
        self.console.print(table)
        
        while True:
            try:
                choice = IntPrompt.ask("[bold green]Enter color number[/bold green]", choices=["1", "2", "3", "4"])
                return colors[choice - 1]
            except (ValueError, IndexError):
                self.console.print("[red]Invalid choice! Please enter 1-4.[/red]")


def main():
    """Main entry point for CLI game."""
    cli = UnoCLI()
    cli.play()


if __name__ in {"__main__", "__mp_main__"}:
    main()
