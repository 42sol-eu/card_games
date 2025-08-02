from nicegui import ui

def show_game_selector_dialog(game):
    with ui.dialog() as dialog, ui.card():
        ui.label('Choose a game:')
        game_input = ui.select(['UNO'], value='UNO')
        with ui.row():
            ui.button('OK', on_click=lambda: (game.set_game(game_input.value), dialog.close()))
            ui.button('Cancel', on_click=dialog.close)
    dialog.open()

# Example usage:
def on_game_selected(selected_game):
    ui.notify(f'Selected game: {selected_game}')

