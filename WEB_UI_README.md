# 🎮 UNO Game - Modern Web UI

Welcome to the enhanced UNO card game with a beautiful web-based interface built using NiceGUI!

## ✨ Features

### 🎨 Modern Visual Design
- **Gradient Backgrounds**: Beautiful color gradients throughout the interface
- **Card Animations**: Smooth hover effects and play animations
- **Responsive Layout**: Works on desktop, tablet, and mobile devices
- **Color-Coded Cards**: Each card color has its unique styling

### 🎯 Enhanced Gameplay
- **Real-time Updates**: Game state updates instantly for all players
- **Visual Feedback**: Clear indicators for playable cards and current player
- **Smart Notifications**: Success, error, and info messages with appropriate styling
- **Forced Draw Handling**: Clear visual indicators for special card effects

### 🌈 Special Card Effects
- **Wild Cards**: Animated gradient backgrounds with color picker dialog
- **+2 and +4 Cards**: Visual warnings and stacking capabilities
- **Direction Changes**: Clear direction indicators with arrow symbols
- **UNO Warnings**: Special alerts when players have few cards left

### 🎪 Interactive Elements
- **Hover Effects**: Cards lift and scale when hovered
- **Click Animations**: Smooth transitions when playing cards
- **Color Picker**: Beautiful modal dialog for wild card color selection
- **Winner Celebration**: Animated winner announcement page

## 🚀 How to Run

### Option 1: Using the Main Entry Point
```bash
python -m src.card_games.main uno --interface web
```

### Option 2: Using the Launcher Script
```bash
python launch_ui.py
```

### Option 3: Direct Import
```python
from src.card_games.uno.ui import UnoUI
ui = UnoUI()
ui.run(port=8081)
```

## 🎮 How to Play

1. **Start Game**: Enter 2-4 player names on the landing page
2. **Play Cards**: Click on playable cards in your hand (highlighted in green)
3. **Draw Cards**: Click the draw pile when you can't play
4. **Wild Cards**: Choose colors using the beautiful color picker
5. **Special Cards**: Handle +2, +4, Skip, and Reverse cards
6. **Win**: First player to empty their hand wins!

## 🛠️ Technical Features

- **NiceGUI Framework**: Modern Python web UI framework
- **CSS Animations**: Custom CSS for smooth transitions
- **Responsive Design**: Tailwind CSS classes for responsive layout
- **State Management**: Real-time game state updates
- **Error Handling**: Graceful error handling and user feedback

## 🎨 UI Components

### Landing Page
- Gradient title with animated text
- Clean player input forms
- Input validation with user feedback

### Game Board
- **Left Sidebar**: Other players with card counts and UNO warnings
- **Center Area**: Top card display and draw pile with animations
- **Right Sidebar**: Current player's hand with playable card indicators

### Card Styling
- **Red Cards**: Red background with white text
- **Blue Cards**: Blue background with white text  
- **Green Cards**: Green background with white text
- **Yellow Cards**: Yellow background with black text
- **Wild Cards**: Animated rainbow gradient

### Winner Page
- Animated winner announcement
- Final game statistics
- Options to start new game or play again

## 🔧 Development Notes

The UI is built with modern web technologies:
- **Backend**: Python with NiceGUI
- **Frontend**: HTML/CSS/JavaScript (automatically handled by NiceGUI)
- **Styling**: Tailwind CSS classes with custom animations
- **State**: Reactive UI updates based on game state changes

## 📱 Mobile Support

The interface is fully responsive and works great on:
- Desktop computers
- Tablets (portrait and landscape)
- Mobile phones (optimized touch interface)

## 🎯 Future Enhancements

Potential improvements for future versions:
- Multiplayer network support
- Sound effects and background music
- Tournament mode with multiple rounds
- Custom card themes and backgrounds
- Player statistics and achievements
- AI opponents with different difficulty levels

Enjoy playing UNO with this modern, beautiful web interface! 🎉
