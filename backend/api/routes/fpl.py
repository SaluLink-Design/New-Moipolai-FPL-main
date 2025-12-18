"""
FPL Data API Routes
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
import logging

from services.fpl_api import fpl_client
from services.supabase_client import supabase_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/gameweek/current")
async def get_current_gameweek():
    """
    Get current gameweek information.

    Returns:
        Current gameweek data
    """
    try:
        gameweek = await fpl_client.get_current_gameweek()

        if not gameweek:
            return {"error": "No current gameweek found"}

        return gameweek

    except Exception as e:
        logger.error(f"Error getting current gameweek: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gameweek/next")
async def get_next_gameweek():
    """
    Get next gameweek information.

    Returns:
        Next gameweek data
    """
    try:
        gameweek = await fpl_client.get_next_gameweek()

        if not gameweek:
            return {"error": "No next gameweek found"}

        return gameweek

    except Exception as e:
        logger.error(f"Error getting next gameweek: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/players")
async def get_players(
    position: Optional[int] = Query(None, description="Filter by position (1=GK, 2=DEF, 3=MID, 4=FWD)"),
    team: Optional[int] = Query(None, description="Filter by team ID"),
    limit: Optional[int] = Query(None, ge=1, le=1000, description="Limit results")
):
    """
    Get all FPL players.

    Args:
        position: Filter by position
        team: Filter by team
        limit: Limit number of results

    Returns:
        List of players
    """
    try:
        players = await supabase_service.get_players()

        if not players:
            players = await fpl_client.get_players()

        if position:
            players = [p for p in players if p.get("element_type") == position]

        if team:
            players = [p for p in players if p.get("team") == team or p.get("team_id") == team]

        if limit:
            players = players[:limit]

        return players

    except Exception as e:
        logger.error(f"Error getting players: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/players/{player_id}")
async def get_player(player_id: int):
    """
    Get a specific player by ID.

    Args:
        player_id: FPL player ID

    Returns:
        Player data
    """
    try:
        players = await fpl_client.get_players()
        player = next((p for p in players if p.get("id") == player_id), None)

        if not player:
            raise HTTPException(status_code=404, detail="Player not found")

        return player

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting player {player_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/teams")
async def get_teams():
    """
    Get all Premier League teams.

    Returns:
        List of teams
    """
    try:
        teams = await supabase_service.get_teams()

        if not teams:
            teams = await fpl_client.get_teams()

        return teams

    except Exception as e:
        logger.error(f"Error getting teams: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fixtures")
async def get_fixtures(
    gameweek: Optional[int] = Query(None, description="Filter by gameweek")
):
    """
    Get fixtures.

    Args:
        gameweek: Optional gameweek filter

    Returns:
        List of fixtures
    """
    try:
        fixtures = await fpl_client.get_fixtures(gameweek)
        return fixtures

    except Exception as e:
        logger.error(f"Error getting fixtures: {e}")
        raise HTTPException(status_code=500, detail=str(e))
