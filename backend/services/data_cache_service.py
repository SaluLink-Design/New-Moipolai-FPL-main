"""
In-memory data cache service for fast access to player data.
Caches FPL data in memory to avoid repeated slow API calls.
"""
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


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


# Global cache instance
data_cache = DataCacheService()
