"""
FPL API Client - Handles all interactions with the official FPL API
"""
import httpx
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from config import settings

logger = logging.getLogger(__name__)


def convert_to_supabase_format(data: Dict[str, Any], data_type: str) -> Dict[str, Any]:
    """Convert FPL API data to Supabase schema format."""
    if data_type == "player":
        return {
            "id": data.get("id"),
            "web_name": data.get("web_name", ""),
            "first_name": data.get("first_name", ""),
            "second_name": data.get("second_name", ""),
            "team_id": data.get("team"),
            "team_code": data.get("team_code"),
            "element_type": data.get("element_type"),
            "status": data.get("status", "a"),
            "chance_of_playing_next_round": data.get("chance_of_playing_next_round"),
            "chance_of_playing_this_round": data.get("chance_of_playing_this_round"),
            "now_cost": data.get("now_cost", 0),
            "cost_change_start": data.get("cost_change_start", 0),
            "cost_change_event": data.get("cost_change_event", 0),
            "form": float(data.get("form", 0) or 0),
            "points_per_game": float(data.get("points_per_game", 0) or 0),
            "total_points": data.get("total_points", 0),
            "event_points": data.get("event_points", 0),
            "minutes": data.get("minutes", 0),
            "goals_scored": data.get("goals_scored", 0),
            "assists": data.get("assists", 0),
            "clean_sheets": data.get("clean_sheets", 0),
            "goals_conceded": data.get("goals_conceded", 0),
            "own_goals": data.get("own_goals", 0),
            "penalties_saved": data.get("penalties_saved", 0),
            "penalties_missed": data.get("penalties_missed", 0),
            "yellow_cards": data.get("yellow_cards", 0),
            "red_cards": data.get("red_cards", 0),
            "saves": data.get("saves", 0),
            "bonus": data.get("bonus", 0),
            "bps": data.get("bps", 0),
            "influence": float(data.get("influence", 0) or 0),
            "creativity": float(data.get("creativity", 0) or 0),
            "threat": float(data.get("threat", 0) or 0),
            "ict_index": float(data.get("ict_index", 0) or 0),
            "selected_by_percent": float(data.get("selected_by_percent", 0) or 0),
            "transfers_in": data.get("transfers_in", 0),
            "transfers_out": data.get("transfers_out", 0),
            "transfers_in_event": data.get("transfers_in_event", 0),
            "transfers_out_event": data.get("transfers_out_event", 0),
            "expected_goals": float(data.get("expected_goals", 0) or 0) if data.get("expected_goals") else None,
            "expected_assists": float(data.get("expected_assists", 0) or 0) if data.get("expected_assists") else None,
            "expected_goal_involvements": float(data.get("expected_goal_involvements", 0) or 0) if data.get("expected_goal_involvements") else None,
            "expected_goals_conceded": float(data.get("expected_goals_conceded", 0) or 0) if data.get("expected_goals_conceded") else None,
        }
    elif data_type == "team":
        return {
            "id": data.get("id"),
            "name": data.get("name", ""),
            "short_name": data.get("short_name", ""),
            "code": data.get("code"),
            "strength": data.get("strength", 0),
            "strength_overall_home": data.get("strength_overall_home", 0),
            "strength_overall_away": data.get("strength_overall_away", 0),
            "strength_attack_home": data.get("strength_attack_home", 0),
            "strength_attack_away": data.get("strength_attack_away", 0),
            "strength_defence_home": data.get("strength_defence_home", 0),
            "strength_defence_away": data.get("strength_defence_away", 0),
            "played": data.get("played", 0),
            "win": data.get("win", 0),
            "draw": data.get("draw", 0),
            "loss": data.get("loss", 0),
            "points": data.get("points", 0),
            "position": data.get("position", 0),
            "form": float(data.get("form", 0) or 0) if data.get("form") else None,
        }
    elif data_type == "gameweek":
        return {
            "id": data.get("id"),
            "name": data.get("name", ""),
            "deadline_time": data.get("deadline_time"),
            "is_previous": data.get("is_previous", False),
            "is_current": data.get("is_current", False),
            "is_next": data.get("is_next", False),
            "finished": data.get("finished", False),
            "average_entry_score": data.get("average_entry_score"),
            "highest_score": data.get("highest_score"),
            "highest_scoring_entry": data.get("highest_scoring_entry"),
            "chip_plays": data.get("chip_plays"),
        }
    elif data_type == "fixture":
        return {
            "id": data.get("id"),
            "event": data.get("event"),
            "team_h": data.get("team_h"),
            "team_a": data.get("team_a"),
            "team_h_score": data.get("team_h_score"),
            "team_a_score": data.get("team_a_score"),
            "team_h_difficulty": data.get("team_h_difficulty", 0),
            "team_a_difficulty": data.get("team_a_difficulty", 0),
            "kickoff_time": data.get("kickoff_time"),
            "started": data.get("started", False),
            "finished": data.get("finished", False),
            "finished_provisional": data.get("finished_provisional", False),
            "stats": data.get("stats"),
        }
    return data


class FPLAPIClient:
    """Client for interacting with the Fantasy Premier League API."""

    def __init__(self):
        self.base_url = settings.fpl_api_base_url
        self.client: Optional[httpx.AsyncClient] = None
        self._bootstrap_data: Optional[Dict] = None
        self._bootstrap_timestamp: Optional[datetime] = None
        self._supabase_service = None
        
    async def initialize(self):
        """Initialize the HTTP client."""
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=30.0,
            headers={
                "User-Agent": "FPL-AI-Model/1.0"
            }
        )

        # Import here to avoid circular dependency
        from services.supabase_client import supabase_service
        self._supabase_service = supabase_service

        logger.info("FPL API client initialized")
        
    async def close(self):
        """Close the HTTP client."""
        if self.client:
            await self.client.aclose()
            logger.info("FPL API client closed")
    
    async def check_health(self) -> bool:
        """Check if the FPL API is accessible."""
        try:
            response = await self.client.get("/bootstrap-static/")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"FPL API health check failed: {e}")
            return False

    async def _sync_bootstrap_to_supabase(self):
        """Sync bootstrap data to Supabase."""
        try:
            if not self._bootstrap_data or not self._supabase_service:
                return

            # Sync players
            players_data = self._bootstrap_data.get("elements", [])
            if players_data:
                players_formatted = [convert_to_supabase_format(p, "player") for p in players_data]
                await self._supabase_service.upsert_players(players_formatted)
                await self._supabase_service.update_cache_metadata("bootstrap_players", "players", settings.fpl_cache_ttl)

            # Sync teams
            teams_data = self._bootstrap_data.get("teams", [])
            if teams_data:
                teams_formatted = [convert_to_supabase_format(t, "team") for t in teams_data]
                await self._supabase_service.upsert_teams(teams_formatted)
                await self._supabase_service.update_cache_metadata("bootstrap_teams", "teams", settings.fpl_cache_ttl)

            # Sync gameweeks
            gameweeks_data = self._bootstrap_data.get("events", [])
            if gameweeks_data:
                gameweeks_formatted = [convert_to_supabase_format(gw, "gameweek") for gw in gameweeks_data]
                await self._supabase_service.upsert_gameweeks(gameweeks_formatted)
                await self._supabase_service.update_cache_metadata("bootstrap_gameweeks", "gameweeks", settings.fpl_cache_ttl)

            logger.info("Successfully synced bootstrap data to Supabase")
        except Exception as e:
            logger.error(f"Failed to sync bootstrap data to Supabase: {e}")
    
    async def get_bootstrap_static(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Get bootstrap-static data (general game information).
        This includes: events, teams, elements (players), element_types (positions).
        
        Args:
            force_refresh: Force refresh even if cached data is available
            
        Returns:
            Dictionary containing bootstrap data
        """
        # Check cache
        if not force_refresh and self._bootstrap_data and self._bootstrap_timestamp:
            cache_age = datetime.now() - self._bootstrap_timestamp
            if cache_age < timedelta(seconds=settings.fpl_cache_ttl):
                logger.debug("Returning cached bootstrap data")
                return self._bootstrap_data
        
        try:
            logger.info("Fetching bootstrap-static data from FPL API")
            response = await self.client.get("/bootstrap-static/")
            response.raise_for_status()
            
            self._bootstrap_data = response.json()
            self._bootstrap_timestamp = datetime.now()

            logger.info(f"Bootstrap data fetched successfully. "
                       f"Players: {len(self._bootstrap_data.get('elements', []))}, "
                       f"Teams: {len(self._bootstrap_data.get('teams', []))}")

            # Sync data to Supabase in background
            if self._supabase_service:
                await self._sync_bootstrap_to_supabase()

            return self._bootstrap_data
            
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch bootstrap data: {e}")
            raise
    
    async def get_players(self, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """
        Get all players (elements) from bootstrap data.
        
        Returns:
            List of player dictionaries
        """
        bootstrap = await self.get_bootstrap_static(force_refresh)
        return bootstrap.get("elements", [])
    
    async def get_teams(self, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """
        Get all teams from bootstrap data.
        
        Returns:
            List of team dictionaries
        """
        bootstrap = await self.get_bootstrap_static(force_refresh)
        return bootstrap.get("teams", [])
    
    async def get_gameweeks(self, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """
        Get all gameweeks (events) from bootstrap data.
        
        Returns:
            List of gameweek dictionaries
        """
        bootstrap = await self.get_bootstrap_static(force_refresh)
        return bootstrap.get("events", [])
    
    async def get_current_gameweek(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """
        Get the current gameweek.
        
        Returns:
            Current gameweek dictionary or None
        """
        gameweeks = await self.get_gameweeks(force_refresh)
        for gw in gameweeks:
            if gw.get("is_current", False):
                return gw
        return None
    
    async def get_next_gameweek(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """
        Get the next gameweek.
        
        Returns:
            Next gameweek dictionary or None
        """
        gameweeks = await self.get_gameweeks(force_refresh)
        for gw in gameweeks:
            if gw.get("is_next", False):
                return gw
        return None
    
    async def get_fixtures(self, gameweek: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get fixtures, optionally filtered by gameweek.
        
        Args:
            gameweek: Optional gameweek number to filter by
            
        Returns:
            List of fixture dictionaries
        """
        try:
            url = "/fixtures/"
            if gameweek:
                url += f"?event={gameweek}"
            
            logger.info(f"Fetching fixtures{f' for GW{gameweek}' if gameweek else ''}")
            response = await self.client.get(url)
            response.raise_for_status()
            
            fixtures = response.json()
            logger.info(f"Fetched {len(fixtures)} fixtures")

            # Sync fixtures to Supabase
            if self._supabase_service and fixtures:
                fixtures_formatted = [convert_to_supabase_format(f, "fixture") for f in fixtures]
                await self._supabase_service.upsert_fixtures(fixtures_formatted)
                cache_key = f"fixtures_gw{gameweek}" if gameweek else "fixtures_all"
                await self._supabase_service.update_cache_metadata(cache_key, "fixtures", settings.fpl_cache_ttl)

            return fixtures
            
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch fixtures: {e}")
            raise
    
    async def get_player_summary(self, player_id: int) -> Dict[str, Any]:
        """
        Get detailed summary for a specific player.
        Includes history and upcoming fixtures.
        
        Args:
            player_id: FPL player ID
            
        Returns:
            Player summary dictionary
        """
        try:
            logger.debug(f"Fetching summary for player {player_id}")
            response = await self.client.get(f"/element-summary/{player_id}/")
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch player {player_id} summary: {e}")
            raise
    
    async def get_user_team(self, team_id: int, gameweek: Optional[int] = None) -> Dict[str, Any]:
        """
        Get a user's team for a specific gameweek.
        
        Args:
            team_id: FPL team ID
            gameweek: Optional gameweek number (defaults to current)
            
        Returns:
            Team data dictionary
        """
        try:
            url = f"/entry/{team_id}/"
            if gameweek:
                url += f"event/{gameweek}/picks/"
            
            logger.info(f"Fetching team {team_id}{f' for GW{gameweek}' if gameweek else ''}")
            response = await self.client.get(url)
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch team {team_id}: {e}")
            raise
    
    async def get_player_by_name(self, name: str, fuzzy: bool = True) -> Optional[Dict[str, Any]]:
        """
        Find a player by name.
        
        Args:
            name: Player name to search for
            fuzzy: Whether to use fuzzy matching
            
        Returns:
            Player dictionary or None if not found
        """
        players = await self.get_players()
        
        # Exact match first
        for player in players:
            web_name = player.get("web_name", "")
            full_name = f"{player.get('first_name', '')} {player.get('second_name', '')}".strip()
            
            if name.lower() in [web_name.lower(), full_name.lower()]:
                return player
        
        # Fuzzy match if enabled
        if fuzzy:
            from rapidfuzz import fuzz, process
            
            player_names = {
                f"{p.get('web_name', '')}": p for p in players
            }
            
            match = process.extractOne(
                name,
                player_names.keys(),
                scorer=fuzz.ratio,
                score_cutoff=settings.fuzzy_match_threshold
            )
            
            if match:
                matched_name, score, _ = match
                logger.info(f"Fuzzy matched '{name}' to '{matched_name}' (score: {score})")
                return player_names[matched_name]
        
        logger.warning(f"Player not found: {name}")
        return None


# Global FPL client instance
fpl_client = FPLAPIClient()
