#!/usr/bin/env python3
"""
Main entry point for the Card Games package.

This script allows you to run different games and interfaces.
"""

import sys
import argparse
from pathlib import Path

# Add the src directory to the path so we can import our package
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from card_games.uno.cli import UnoCLI


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Card Games - Teaching children how to code")
    parser.add_argument("game", choices=["uno"], help="Game to play")
    parser.add_argument("--ui", choices=["cli", "web"], default="cli", 
                        help="User interface type (default: cli)")
    
    args = parser.parse_args()
    
    if args.game == "uno":
        if args.ui == "cli":
            cli = UnoCLI()
            cli.play()
        elif args.ui == "web":
            try:
                from card_games.uno.ui import UnoUI
                ui = UnoUI()
                ui.show_landing_page()
                ui.run()
            except ImportError:
                print("Web UI requires NiceGUI. Install with: pip install nicegui")
                print("Falling back to CLI interface...")
                cli = UnoCLI()
                cli.play()


if __name__ in {"__main__", "__mp_main__"}:
    main()
