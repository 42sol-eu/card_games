# UNO Game UI - Modular Structure

The UNO game UI has been refactored from a single large file (`ui_simple.py`) into a modular structure for better maintainability and readability.

## File Structure

```
src/card_games/uno/ui/
├── __init__.py          # Package initialization
├── main.py              # Main entry point and routing
├── base.py              # Base UI class and shared utilities
├── styles.py            # CSS styles and styling utilities
├── components.py        # Reusable UI components (cards, dialogs)
├── heartbeat.py         # Heartbeat and player management system
├── landing.py           # Landing page functionality
├── lobby.py             # Lobby page functionality
├── game_page.py         # Game page functionality
├── game_header.py       # Game header and discard pile components
└── card_actions.py      # Card playing and game actions
```

## Module Breakdown

### 1. `base.py` - Core Foundation
- **UnoUIBase**: Base class with shared state and properties
- **Global State Management**: Player lobbies, heartbeats, game instances
- **Properties**: player_name, game_stage, game instance management
- **Utilities**: update_game_state, color_styles definitions

### 2. `styles.py` - Visual Styling
- **UnoStyles**: Static CSS management class
- **Custom CSS**: Card animations, gradients, responsive design
- **Animations**: Hover effects, pulse animations, gradients
- **Theming**: Game header styling, card styling classes

### 3. `components.py` - Reusable Components
- **CardComponents**: Card display utilities and mini-card creation
- **DialogComponents**: Confirmation dialogs and modal management
- **Display Methods**: Card text formatting, abbreviations
- **UI Builders**: Mini cards, discard pile cards, dialog creators

### 4. `heartbeat.py` - Player Management
- **HeartbeatManager**: Player activity tracking
- **Connection Status**: Real-time connection indicators (🟢🟡🔴)
- **Inactive Removal**: Automatic cleanup of disconnected players
- **Timeout Management**: 30-second inactivity detection

### 5. `landing.py` - Entry Point
- **LandingPage**: Player name entry and validation
- **Name Validation**: Duplicate name prevention
- **Navigation**: Smooth transition to lobby
- **Welcome Flow**: User onboarding experience

### 6. `lobby.py` - Pre-Game Setup
- **LobbyPage**: Player readiness and game start management
- **Player Management**: Individual/bulk player removal
- **Ready System**: Player readiness states and validation
- **Game Creation**: Game instance creation and hash generation

### 7. `game_page.py` - Main Gameplay
- **GamePage**: Primary game interface coordination
- **Game Flow**: Turn management and game state updates
- **Winner Detection**: Game over handling and winner display
- **Auto-refresh**: Real-time game state synchronization

### 8. `game_header.py` - Game Information Display
- **GameHeader**: Current game state display
- **Player Info**: Turn indicators, direction, player counts
- **Card Display**: Top card, recent cards, discard pile
- **Controls**: Draw button, discard pile viewer, lobby return

### 9. `card_actions.py` - Game Interactions
- **CardActions**: Card playing logic and validations
- **HandDisplay**: Player hand visualization and interaction
- **Color Picker**: Wild card color selection with strategic info
- **Game Rules**: Playability validation, forced draw handling

### 10. `main.py` - Application Orchestration
- **UnoUI**: Main application class inheriting from UnoUIBase
- **Routing**: Page navigation and URL handling
- **Session Management**: Player session persistence
- **Application Lifecycle**: Startup, routing, shutdown

## Key Improvements

### 1. **Separation of Concerns**
- Each file has a single, well-defined responsibility
- UI logic separated from game logic
- Styling isolated from functionality

### 2. **Maintainability**
- Smaller, focused files are easier to understand and modify
- Clear module boundaries reduce coupling
- Centralized shared state management

### 3. **Reusability**
- Common components can be reused across different pages
- Utility functions centralized in appropriate modules
- Consistent styling and behavior patterns

### 4. **Testability**
- Individual modules can be tested in isolation
- Clear interfaces between components
- Reduced complexity in each module

### 5. **Scalability**
- Easy to add new features without modifying existing code
- Clear extension points for new functionality
- Modular architecture supports growth

## Usage

### Running the Modular Version
```bash
python run_ui_modular.py
```

### Importing Components
```python
from src.card_games.uno.ui import UnoUI, main
from src.card_games.uno.ui.components import CardComponents
from src.card_games.uno.ui.heartbeat import HeartbeatManager
```

## Migration Notes

- **Backward Compatibility**: The original `ui_simple.py` remains functional
- **API Consistency**: External interfaces remain the same
- **Configuration**: Same port (8080) and settings
- **Features**: All existing features preserved and enhanced

## Development Guidelines

1. **Single Responsibility**: Each module should have one clear purpose
2. **Minimal Coupling**: Modules should depend on interfaces, not implementations
3. **Consistent Naming**: Use descriptive names that match the module's purpose
4. **Documentation**: Each module should have clear docstrings
5. **Error Handling**: Graceful degradation and informative error messages

This modular structure makes the codebase more professional, maintainable, and extensible while preserving all existing functionality.
