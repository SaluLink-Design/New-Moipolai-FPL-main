"""
Supabase client service for database operations
"""
from typing import Optional, List, Dict, Any
from supabase import create_client, Client
from config import settings
import logging

logger = logging.getLogger(__name__)


class SupabaseService:
    """Service for interacting with Supabase database."""

    def __init__(self):
        self.client: Optional[Client] = None

    async def connect(self):
        """Initialize Supabase client."""
        try:
            if settings.supabase_url and settings.supabase_anon_key:
                self.client = create_client(
                    settings.supabase_url,
                    settings.supabase_anon_key
                )
                logger.info("Supabase client initialized successfully")
            else:
                logger.warning("Supabase credentials not configured")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            raise

    async def disconnect(self):
        """Cleanup Supabase client."""
        self.client = None
        logger.info("Supabase client disconnected")

    # Player operations
    async def upsert_players(self, players: List[Dict[str, Any]]) -> bool:
        """Bulk upsert players data."""
        try:
            if not self.client:
                logger.warning("Supabase client not initialized")
                return False

            response = self.client.table("players").upsert(players).execute()
            logger.info(f"Upserted {len(players)} players")
            return True
        except Exception as e:
            logger.error(f"Failed to upsert players: {e}")
            return False

    async def get_players(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get players with optional filters."""
        try:
            if not self.client:
                return []

            query = self.client.table("players").select("*")

            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)

            response = query.execute()
            return response.data
        except Exception as e:
            logger.error(f"Failed to get players: {e}")
            return []

    # Team operations
    async def upsert_teams(self, teams: List[Dict[str, Any]]) -> bool:
        """Bulk upsert teams data."""
        try:
            if not self.client:
                return False

            response = self.client.table("teams").upsert(teams).execute()
            logger.info(f"Upserted {len(teams)} teams")
            return True
        except Exception as e:
            logger.error(f"Failed to upsert teams: {e}")
            return False

    async def get_teams(self) -> List[Dict[str, Any]]:
        """Get all teams."""
        try:
            if not self.client:
                return []

            response = self.client.table("teams").select("*").execute()
            return response.data
        except Exception as e:
            logger.error(f"Failed to get teams: {e}")
            return []

    # Fixture operations
    async def upsert_fixtures(self, fixtures: List[Dict[str, Any]]) -> bool:
        """Bulk upsert fixtures data."""
        try:
            if not self.client:
                return False

            response = self.client.table("fixtures").upsert(fixtures).execute()
            logger.info(f"Upserted {len(fixtures)} fixtures")
            return True
        except Exception as e:
            logger.error(f"Failed to upsert fixtures: {e}")
            return False

    async def get_fixtures(self, gameweek: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get fixtures, optionally filtered by gameweek."""
        try:
            if not self.client:
                return []

            query = self.client.table("fixtures").select("*")
            if gameweek:
                query = query.eq("event", gameweek)

            response = query.execute()
            return response.data
        except Exception as e:
            logger.error(f"Failed to get fixtures: {e}")
            return []

    # Gameweek operations
    async def upsert_gameweeks(self, gameweeks: List[Dict[str, Any]]) -> bool:
        """Bulk upsert gameweeks data."""
        try:
            if not self.client:
                return False

            response = self.client.table("gameweeks").upsert(gameweeks).execute()
            logger.info(f"Upserted {len(gameweeks)} gameweeks")
            return True
        except Exception as e:
            logger.error(f"Failed to upsert gameweeks: {e}")
            return False

    async def get_current_gameweek(self) -> Optional[Dict[str, Any]]:
        """Get the current gameweek."""
        try:
            if not self.client:
                return None

            response = self.client.table("gameweeks").select("*").eq("is_current", True).maybeSingle().execute()
            return response.data
        except Exception as e:
            logger.error(f"Failed to get current gameweek: {e}")
            return None

    # Prediction operations
    async def save_predictions(self, predictions: List[Dict[str, Any]]) -> bool:
        """Save player predictions."""
        try:
            if not self.client:
                return False

            response = self.client.table("player_predictions").upsert(predictions).execute()
            logger.info(f"Saved {len(predictions)} predictions")
            return True
        except Exception as e:
            logger.error(f"Failed to save predictions: {e}")
            return False

    async def get_predictions(self, gameweek_id: int) -> List[Dict[str, Any]]:
        """Get predictions for a specific gameweek."""
        try:
            if not self.client:
                return []

            response = self.client.table("player_predictions").select("*").eq("gameweek_id", gameweek_id).execute()
            return response.data
        except Exception as e:
            logger.error(f"Failed to get predictions: {e}")
            return []

    # Team analysis operations
    async def save_team_analysis(self, analysis: Dict[str, Any]) -> Optional[str]:
        """Save team analysis and return the ID."""
        try:
            if not self.client:
                return None

            response = self.client.table("team_analyses").insert(analysis).execute()
            if response.data:
                logger.info(f"Saved team analysis: {response.data[0]['id']}")
                return response.data[0]["id"]
            return None
        except Exception as e:
            logger.error(f"Failed to save team analysis: {e}")
            return None

    async def get_team_analysis(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific team analysis by ID."""
        try:
            if not self.client:
                return None

            response = self.client.table("team_analyses").select("*").eq("id", analysis_id).maybeSingle().execute()
            return response.data
        except Exception as e:
            logger.error(f"Failed to get team analysis: {e}")
            return None

    # Cache metadata operations
    async def update_cache_metadata(self, cache_key: str, data_type: str, ttl_seconds: int = 3600):
        """Update cache metadata to track data freshness."""
        try:
            if not self.client:
                return

            from datetime import datetime, timedelta

            metadata = {
                "cache_key": cache_key,
                "data_type": data_type,
                "last_updated": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow() + timedelta(seconds=ttl_seconds)).isoformat()
            }

            self.client.table("cache_metadata").upsert(metadata).execute()
        except Exception as e:
            logger.error(f"Failed to update cache metadata: {e}")

    async def check_cache_freshness(self, cache_key: str) -> bool:
        """Check if cached data is still fresh."""
        try:
            if not self.client:
                return False

            from datetime import datetime

            response = self.client.table("cache_metadata").select("expires_at").eq("cache_key", cache_key).maybeSingle().execute()

            if not response.data:
                return False

            expires_at = datetime.fromisoformat(response.data["expires_at"].replace("Z", "+00:00"))
            return datetime.utcnow().replace(tzinfo=expires_at.tzinfo) < expires_at
        except Exception as e:
            logger.error(f"Failed to check cache freshness: {e}")
            return False


# Global service instance
supabase_service = SupabaseService()
