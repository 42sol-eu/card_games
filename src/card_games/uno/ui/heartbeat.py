"""
Heartbeat system and player management for UNO game interface.
"""

import time
from nicegui import ui

from .base import UnoUIBase


class HeartbeatManager:
    """Manages player heartbeats and inactive player removal."""
    
    @staticmethod
    def send_heartbeat(player_name: str):
        """Send heartbeat for current player to show they're still active."""
        if player_name:
            UnoUIBase._player_heartbeats[player_name] = time.time()

    @staticmethod
    def remove_inactive_players():
        """Remove players who haven't sent a heartbeat in the timeout period."""
        current_time = time.time()
        inactive_players = []
        
        for player_name, last_heartbeat in UnoUIBase._player_heartbeats.items():
            if current_time - last_heartbeat > UnoUIBase._heartbeat_timeout:
                inactive_players.append(player_name)
        
        for player_name in inactive_players:
            if player_name in UnoUIBase._lobby_players:
                del UnoUIBase._lobby_players[player_name]
            if player_name in UnoUIBase._player_heartbeats:
                del UnoUIBase._player_heartbeats[player_name]
            
            # Don't show notification for every inactive player removal
            # as it could be noisy - just clean them up silently
        
        return len(inactive_players) > 0  # Return True if any players were removed

    @staticmethod
    def get_connection_status(player_name: str) -> tuple:
        """Get connection status for a player."""
        current_time = time.time()
        last_heartbeat = UnoUIBase._player_heartbeats.get(player_name, 0)
        time_since_heartbeat = current_time - last_heartbeat
        
        # Add connection indicator
        if time_since_heartbeat > UnoUIBase._heartbeat_timeout * 0.7:  # 70% of timeout
            return "🔴", "Poor Connection"  # Red for poor connection
        elif time_since_heartbeat > UnoUIBase._heartbeat_timeout * 0.4:  # 40% of timeout
            return "🟡", "Weak Connection"  # Yellow for weak connection
        else:
            return "🟢", "Connected"  # Green for good connection
