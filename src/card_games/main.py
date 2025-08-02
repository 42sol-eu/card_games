#!/usr/bin/env python3
"""
Main entry point for the Card Games package.

This module provides a command-line interface with subcommands for different games and interfaces.
"""

import argparse
import sys
from .uno.cli import UnoCLI


def main():
    """Main entry point with subcommands."""
    parser = argparse.ArgumentParser(
        description="Card Games - Teaching children how to code",
        prog="card-games"
    )
    
    # Add version argument
    parser.add_argument(
        "--version", 
        action="version", 
        version="%(prog)s 2025.0.1"
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        title="Commands",
        description="Choose a game to play"
    )
    
    # Uno subcommand
    uno_parser = subparsers.add_parser(
        "uno",
        help="Play Uno card game",
        description="Start an Uno game with CLI or web interface"
    )
    
    uno_parser.add_argument(
        "--interface", "-i",
        choices=["cli", "web"],
        default="cli",
        help="Choose interface type (default: cli)"
    )
    
    uno_parser.add_argument(
        "--players", "-p",
        type=int,
        choices=[2, 3, 4],
        help="Number of players (for CLI mode)"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no command provided, show help
    if not args.command:
        parser.print_help()
        return
    
    # Handle uno command
    if args.command == "uno":
        if args.interface == "cli":
            cli = UnoCLI()
            if args.players:
                # Pre-set number of players if specified
                cli.preset_players = args.players
            cli.play()
        elif args.interface == "web":
            try:
                from .uno.ui_simple import UnoUI
                print("Starting Uno web interface...")
                print("Open your browser to http://localhost:8080")
                ui = UnoUI()
                ui.run()
            except ImportError:
                print("❌ Web UI requires NiceGUI. Install with:")
                print("   pip install card-games[ui]")
                print("   or: pip install nicegui")
                print("\n🎮 Falling back to CLI interface...")
                cli = UnoCLI()
                if args.players:
                    cli.preset_players = args.players
                cli.play()


if __name__ == "__main__":
    main()
