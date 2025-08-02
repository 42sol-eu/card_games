from nicegui import ui
from card_games import __version__

from card_games.core.ui import show_game_selector_dialog, on_game_selected

from nicegui import ui

class Game(ui.element):
    """A simple game class to demonstrate UI functionality."""
    def __init__(self, name):
        self.name = None
        self.players = {}

    def set_game(self, game_name):
        """Set the game name."""
        self.name = game_name
        ui.notify(f'Game set to: {game_name}', type='positive')
        game_panel.refresh()
        player_panel.refresh()

    def get_player_hand(self, player_name):
        """Get the hand of a player."""
        return self.players.get(player_name, [])

    def get_game_name(self):
        """Get the current game name."""
        return self.name if self.name else "No game selected"
        
    def add_player(self, player_name):
        if player_name and player_name.strip().rstrip() and player_name not in self.players:
            self.players[player_name.strip()] = []
            return True
        return False

    def remove_player(self, player_name):
        """Remove a player from the game."""
        ui.notify(f'Removing player: {player_name}', type='info')
        
        if player_name in self.players:
            del self.players[player_name]
            ui.notify(f'Player "{player_name}" removed!', type='positive')
            player_panel.refresh()
            return True


    def __str__(self):
        name = self.name
        if not name:
            return "No game selected"
        return f"{name}"
game = Game(None)


def remove_player(e):
    """Remove a player from the game."""
    global game
    # e.sender is the chip component; its label is the player name
    player_name = e.sender.text if hasattr(e.sender, 'text') else e.sender.value
    if game.remove_player(player_name):
        ui.notify(f'Player "{player_name}" removed!', type='positive')
        player_panel.refresh()

@ui.refreshable
def game_panel() -> None:
    global game
    ui.label(str(game)).classes('text-2xl font-bold text-center my-4')

@ui.refreshable
def player_panel() -> None:
    """Display the players."""
    global game
    ui.label(f"Players:").classes('text-lg text-center my-4')
    if game and game.players:
        
        with ui.row().classes('text-lg text-center my-4'):
            for player in game.players.keys():
                player_button = ui.chip(f"{player}",selectable=True, removable=True,  icon='star', on_value_change=remove_player).classes('text-lg text-center my-4')
                # TODO: remove_player is not working
                if game.name:
                    player_button.enable()
                else:
                    player_button.disable()
    else:
        ui.label("No players added yet").classes('text-lg text-center my-4 text-gray-500')

@ui.page('/')
def page_layout():
    global game 
    
    with ui.row():
        ui.button(icon='sports_esports', on_click=lambda: show_game_selector_dialog(game)).tooltip('select game').classes('text-2xl font-bold text-center my-2')
        ui.label('Game:').classes('text-2xl font-bold text-center my-4')
        game_panel()
    with ui.row():
        player_panel()

    with ui.row().classes('items-center justify-center'):
        def add_player_and_refresh():
            player_name = player_input.value
            if game.add_player(player_name):
                player_input.value = ''  # Clear input
                player_panel.refresh()
                ui.notify(f'Player "{player_name.strip()}" added!', type='positive')
            elif player_name and player_name.strip():
                ui.notify('Player already exists!', type='warning')
            else:
                ui.notify('Please enter a valid player name!', type='warning')
        
        ui.button(icon='add', on_click=add_player_and_refresh).tooltip('Add player').classes('my-1')
        player_input = ui.input(label='Player Name', placeholder='Enter player name').classes('my-4')
        
    
    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        ui.label('Card Games Home')
        ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')
    with ui.left_drawer(top_corner=True, bottom_corner=True).style('background-color: #d7e3f4'):
        ui.label('LEFT DRAWER')
    with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
        ui.label('RIGHT DRAWER')
    with ui.footer().style('background-color: #3874c8'):
        ui.label(f'Version: {__version__}')

ui.link('show page with fancy layout', page_layout)


ui.run()