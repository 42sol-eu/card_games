#!/usr/bin/env python3
"""
Quick launcher for the UNO web UI.

This script launches the modern NiceGUI-based UNO game interface.
"""

def main():
    """Launch the UNO web UI."""
    try:
        from src.card_games.uno.ui_simple import UnoUI
        
        print("🎮 Starting UNO Web Interface...")
        print("✨ Features:")
        print("   • Beautiful card animations")
        print("   • Responsive design")
        print("   • Real-time game updates")
        print("   • Modern UI with gradients and effects")
        print("   • Color-coded cards")
        print("   • Smooth transitions and hover effects")
        print()
        print("🌐 Web interface will open at: http://localhost:8080")
        print("📱 The interface is mobile-friendly!")
        print()
        print("🎯 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Create and run the UI
        ui = UnoUI()
        ui.run(
            title="🎮 UNO Game - Modern Web Edition",
            port=8080,
            debug=False
        )
        
    except ImportError as e:
        print("❌ Error: NiceGUI is not installed!")
        print()
        print("📦 Install with one of these commands:")
        print("   pip install nicegui")
        print("   or")
        print("   pip install card-games[ui]")
        print()
        print("🎮 Alternative: Use the CLI version with:")
        print("   python -m src.card_games.uno.cli")
        
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for playing UNO!")
        print("🎮 Game server stopped.")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("🔧 Please check your installation and try again.")


if __name__ == "__main__":
    main()
