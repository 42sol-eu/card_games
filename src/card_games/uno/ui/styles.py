"""
CSS styles and styling utilities for UNO game interface.
"""

from nicegui import ui


class UnoStyles:
    """Manages CSS styles for the UNO game interface."""
    
    @staticmethod
    def setup_custom_css():
        """Add custom CSS for enhanced card animations and styling."""
        ui.add_head_html("""
        <style>
            .uno-card {
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                cursor: pointer;
                border-radius: 12px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                margin: 0 4px;
            }
            
            .uno-card:hover {
                transform: translateY(-8px) scale(1.05);
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
                z-index: 10;
            }
            
            .uno-card-disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            
            .uno-card-disabled:hover {
                transform: none;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            
            .card-row {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 8px;
                padding: 20px;
                min-height: 200px;
            }
            
            .game-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 0 0 20px 20px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }
            
            .wild-card-gradient {
                background: linear-gradient(45deg, #ef4444, #3b82f6, #10b981, #f59e0b);
                background-size: 300% 300%;
                animation: gradientShift 3s ease infinite;
            }
            
            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            .player-turn-glow {
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0%, 100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7); }
                50% { box-shadow: 0 0 0 8px rgba(59, 130, 246, 0); }
            }
        </style>
        """)
