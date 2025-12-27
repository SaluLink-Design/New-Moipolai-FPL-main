"""
In-memory data cache service for fast access to player data.
Caches FPL data in memory to avoid repeated slow API calls.
Includes fallback demo data for development/testing.
"""
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Minimal demo data for fallback
DEMO_PLAYERS = [
    {"id": 352, "web_name": "Haaland", "element_type": 4, "team": 1, "form": 8.5, "points_per_game": 6.2, "total_points": 186, "now_cost": 900, "status": "a", "minutes": 1800},
    {"id": 333, "web_name": "Son", "element_type": 3, "team": 6, "form": 8.0, "points_per_game": 5.8, "total_points": 174, "now_cost": 800, "status": "a", "minutes": 1900},
    {"id": 141, "web_name": "Mount", "element_type": 3, "team": 2, "form": 7.5, "points_per_game": 5.1, "total_points": 153, "now_cost": 700, "status": "a", "minutes": 1600},
    {"id": 308, "web_name": "Martinelli", "element_type": 3, "team": 1, "form": 7.2, "points_per_game": 4.9, "total_points": 147, "now_cost": 650, "status": "a", "minutes": 1500},
    {"id": 5, "web_name": "De Bruyne", "element_type": 3, "team": 8, "form": 6.8, "points_per_game": 4.6, "total_points": 138, "now_cost": 850, "status": "a", "minutes": 1400},
    {"id": 254, "web_name": "Salah", "element_type": 3, "team": 10, "form": 7.1, "points_per_game": 5.0, "total_points": 150, "now_cost": 900, "status": "a", "minutes": 1700},
    {"id": 405, "web_name": "Alvarez", "element_type": 4, "team": 8, "form": 6.5, "points_per_game": 4.3, "total_points": 129, "now_cost": 700, "status": "a", "minutes": 1300},
    {"id": 88, "web_name": "Odegaard", "element_type": 3, "team": 1, "form": 6.8, "points_per_game": 4.7, "total_points": 141, "now_cost": 750, "status": "a", "minutes": 1600},
    {"id": 427, "web_name": "Jota", "element_type": 3, "team": 10, "form": 6.2, "points_per_game": 4.1, "total_points": 123, "now_cost": 700, "status": "a", "minutes": 1200},
    {"id": 306, "web_name": "Neto", "element_type": 3, "team": 16, "form": 6.0, "points_per_game": 4.0, "total_points": 120, "now_cost": 650, "status": "a", "minutes": 1400},
    {"id": 14, "web_name": "Shaw", "element_type": 2, "team": 11, "form": 5.8, "points_per_game": 3.5, "total_points": 105, "now_cost": 550, "status": "a", "minutes": 1700},
    {"id": 286, "web_name": "Dias", "element_type": 2, "team": 8, "form": 5.5, "points_per_game": 3.2, "total_points": 96, "now_cost": 500, "status": "a", "minutes": 1800},
    {"id": 328, "web_name": "Van Dijk", "element_type": 2, "team": 10, "form": 5.6, "points_per_game": 3.3, "total_points": 99, "now_cost": 520, "status": "a", "minutes": 1800},
    {"id": 251, "web_name": "Ramsdale", "element_type": 1, "team": 1, "form": 5.2, "points_per_game": 2.8, "total_points": 84, "now_cost": 430, "status": "a", "minutes": 1800},
    {"id": 195, "web_name": "Alisson", "element_type": 1, "team": 10, "form": 5.1, "points_per_game": 2.7, "total_points": 81, "now_cost": 430, "status": "a", "minutes": 1800},
]


class DataCacheService:
    """In-memory cache for FPL data with fallback support."""

    def __init__(self):
        self.players_cache: Optional[List[Dict[str, Any]]] = None
        self.teams_cache: Optional[List[Dict[str, Any]]] = None
        self.cache_timestamp: Optional[datetime] = None
        self.cache_ttl_seconds: int = 3600  # 1 hour
    
    def set_players(self, players: List[Dict[str, Any]]):
        """Cache player data."""
        self.players_cache = players
        self.cache_timestamp = datetime.now()
        logger.info(f"Cached {len(players)} players in memory")
    
    def get_players(self) -> Optional[List[Dict[str, Any]]]:
        """Get cached players if still fresh."""
        if self.players_cache and self.cache_timestamp:
            age = (datetime.now() - self.cache_timestamp).total_seconds()
            if age < self.cache_ttl_seconds:
                logger.debug(f"Returning {len(self.players_cache)} cached players")
                return self.players_cache
        return None
    
    def set_teams(self, teams: List[Dict[str, Any]]):
        """Cache team data."""
        self.teams_cache = teams
        logger.info(f"Cached {len(teams)} teams in memory")
    
    def get_teams(self) -> Optional[List[Dict[str, Any]]]:
        """Get cached teams."""
        return self.teams_cache
    
    def is_fresh(self) -> bool:
        """Check if cache is still fresh."""
        if not self.cache_timestamp:
            return False
        age = (datetime.now() - self.cache_timestamp).total_seconds()
        return age < self.cache_ttl_seconds
    
    def clear(self):
        """Clear the cache."""
        self.players_cache = None
        self.teams_cache = None
        self.cache_timestamp = None
        logger.info("Cache cleared")

    def get_demo_players(self) -> List[Dict[str, Any]]:
        """Get demo player data for fallback/testing."""
        return DEMO_PLAYERS


# Global cache instance
data_cache = DataCacheService()
