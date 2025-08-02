#!/usr/bin/env python3
"""
Launcher script for the UNO web UI.
"""

import sys
import os

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

try:
    from card_games.uno.ui_simple import UnoUI
    
    if __name__ == "__main__":
        print("Starting UNO Web UI...")
        ui = UnoUI()
        ui.run()
        
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all dependencies are installed:")
    print("pip install nicegui")
except Exception as e:
    print(f"Error starting UI: {e}")
    import traceback
    traceback.print_exc()
