#!/usr/bin/env python3
"""
UNO Game Demo Script

This script demonstrates both the CLI and Web UI versions of the UNO game.
"""

import sys
import time
import subprocess
from pathlib import Path

def print_banner():
    """Print a nice banner."""
    print("=" * 60)
    print("🎮 UNO CARD GAME - DEMO SHOWCASE 🎮")
    print("=" * 60)
    print()
    print("Welcome to the enhanced UNO card game!")
    print("This demo showcases both interface options:")
    print()
    print("1. 💻 CLI Interface - Rich terminal-based gameplay")
    print("2. 🌐 Web Interface - Modern browser-based UI")
    print()

def demo_cli():
    """Demo the CLI interface."""
    print("🎯 CLI INTERFACE DEMO")
    print("-" * 30)
    print()
    print("Features of the CLI interface:")
    print("✅ Rich text formatting with colors")
    print("✅ ASCII art card displays")
    print("✅ Beautiful card layouts")
    print("✅ Interactive command prompts")
    print("✅ Full game logic support")
    print()
    
    response = input("Would you like to try the CLI version? (y/n): ").strip().lower()
    if response == 'y':
        print("\n🚀 Launching CLI interface...")
        try:
            subprocess.run([sys.executable, "-m", "src.card_games.main", "uno", "--interface", "cli"], 
                         cwd=Path(__file__).parent)
        except KeyboardInterrupt:
            print("\n👋 CLI demo ended.")
    else:
        print("📝 CLI demo skipped.")

def demo_web():
    """Demo the web interface."""
    print("\n🌐 WEB INTERFACE DEMO") 
    print("-" * 30)
    print()
    print("Features of the Web interface:")
    print("✅ Beautiful gradient backgrounds")
    print("✅ Animated card hover effects")
    print("✅ Responsive design (mobile & desktop)")
    print("✅ Real-time game state updates")
    print("✅ Color-coded cards with smooth transitions")
    print("✅ Enhanced visual feedback")
    print("✅ Wild card color picker dialog")
    print("✅ Winner celebration page")
    print()
    
    response = input("Would you like to try the Web interface? (y/n): ").strip().lower()
    if response == 'y':
        print("\n🚀 Launching Web interface...")
        print("🌐 Server will start on http://localhost:8080")
        print("📱 Interface works on mobile devices too!")
        print("🎯 Press Ctrl+C in terminal to stop the server")
        print()
        
        try:
            # Import and run the web UI
            from src.card_games.uno.ui_simple import UnoUI
            ui = UnoUI()
            ui.run(port=8080)
        except ImportError:
            print("❌ NiceGUI not installed. Install with: pip install nicegui")
        except KeyboardInterrupt:
            print("\n👋 Web demo ended.")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("📝 Web demo skipped.")

def show_comparison():
    """Show comparison between interfaces."""
    print("\n📊 INTERFACE COMPARISON")
    print("-" * 30)
    print()
    print("CLI Interface:")
    print("  🎯 Best for: Terminal lovers, quick games")
    print("  ✅ Pros: Fast, lightweight, ASCII art")
    print("  ❌ Cons: Terminal-only, no mouse support")
    print()
    print("Web Interface:")
    print("  🎯 Best for: Visual experience, multiple devices")
    print("  ✅ Pros: Beautiful UI, mobile support, animations")
    print("  ❌ Cons: Requires browser, slightly more resources")
    print()

def main():
    """Main demo function."""
    print_banner()
    
    print("What would you like to do?")
    print("1. 💻 Try CLI Interface")
    print("2. 🌐 Try Web Interface") 
    print("3. 📊 View Comparison")
    print("4. 🚀 Launch Quick Web Demo")
    print("5. ❌ Exit")
    print()
    
    while True:
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            demo_cli()
            break
        elif choice == "2":
            demo_web()
            break
        elif choice == "3":
            show_comparison()
            print("\nChoose an interface to try:")
            continue
        elif choice == "4":
            print("\n🚀 Quick Web Demo Launch...")
            try:
                subprocess.run([sys.executable, "launch_ui.py"], cwd=Path(__file__).parent)
            except KeyboardInterrupt:
                print("\n👋 Demo ended.")
            break
        elif choice == "5":
            print("\n👋 Thanks for checking out UNO!")
            print("🎮 Try running: python launch_ui.py")
            break
        else:
            print("❌ Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("🔧 Please check your installation.")
