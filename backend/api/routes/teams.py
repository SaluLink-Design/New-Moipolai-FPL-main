"""
Teams API Routes
"""
from fastapi import APIRouter, HTTPException
from typing import List
import logging

from models.fpl_models import TeamAnalysis, PlayerPrediction
from services.fpl_api import fpl_client
from services.supabase_client import supabase_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/analyze", response_model=TeamAnalysis)
async def analyze_team(team_data: dict):
    """
    Analyze a team and provide insights.

    Args:
        team_data: Team data including players

    Returns:
        Team analysis with predictions and suggestions
    """
    try:
        logger.info("Analyzing team")

        player_ids = team_data.get("players", [])
        if not player_ids:
            raise HTTPException(status_code=400, detail="No players provided")

        logger.info(f"Fetching player data for {len(player_ids)} players")
        all_players = await fpl_client.get_players()
        logger.info(f"Fetched {len(all_players)} total players from FPL API")

        team_players = [p for p in all_players if p.get("id") in player_ids]
        logger.info(f"Found {len(team_players)} team players")

        if len(team_players) != len(player_ids):
            missing_ids = set(player_ids) - {p.get("id") for p in team_players}
            logger.warning(f"Some players not found: {missing_ids}")
            raise HTTPException(status_code=400, detail=f"Players not found: {missing_ids}")

        team_value = sum(p.get("now_cost", 0) for p in team_players) / 10.0
        predicted_points = sum(_calculate_simple_prediction(p) for p in team_players[:11])
        predicted_bench_points = sum(_calculate_simple_prediction(p) for p in team_players[11:])

        captain_player = max(team_players[:11], key=lambda p: _calculate_simple_prediction(p))
        vice_captain = sorted(
            [p for p in team_players[:11] if p["id"] != captain_player["id"]],
            key=lambda p: _calculate_simple_prediction(p),
            reverse=True
        )[0]

        logger.info("Generating transfer suggestions")
        transfer_suggestions = _generate_transfer_suggestions(team_players, all_players)

        analysis_data = {
            "team_value": round(team_value, 1),
            "free_transfers": team_data.get("free_transfers", 1),
            "bank": team_data.get("bank", 0.0),
            "players": player_ids,
            "captain_id": captain_player["id"],
            "vice_captain_id": vice_captain["id"],
            "predicted_gameweek_points": round(predicted_points, 1),
            "predicted_bench_points": round(predicted_bench_points, 1),
            "transfer_suggestions": transfer_suggestions,
            "captain_suggestion": _create_player_prediction(captain_player),
            "vice_captain_suggestion": _create_player_prediction(vice_captain),
            "bench_order": player_ids[11:]
        }

        logger.info("Team analysis complete, saving to database")
        # Save to database in background without blocking response
        try:
            analysis_id = await supabase_service.save_team_analysis(analysis_data)
            logger.info(f"Team analysis saved with ID: {analysis_id}")
        except Exception as save_error:
            logger.error(f"Failed to save analysis to database: {save_error}")
            # Don't fail the response if database save fails

        return TeamAnalysis(**analysis_data)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing team: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/captain")
async def get_captain_suggestion(team_data: dict):
    """
    Get captain recommendation for a team.

    Args:
        team_data: Team data

    Returns:
        Captain and vice-captain suggestions
    """
    try:
        logger.info("Getting captain suggestion")

        player_ids = team_data.get("players", [])[:11]
        if not player_ids:
            raise HTTPException(status_code=400, detail="No players provided")

        all_players = await fpl_client.get_players()
        team_players = [p for p in all_players if p.get("id") in player_ids]

        captain_player = max(team_players, key=lambda p: _calculate_simple_prediction(p))
        vice_captain = sorted(
            [p for p in team_players if p["id"] != captain_player["id"]],
            key=lambda p: _calculate_simple_prediction(p),
            reverse=True
        )[0]

        return {
            "captain": _create_player_prediction(captain_player),
            "vice_captain": _create_player_prediction(vice_captain)
        }

    except Exception as e:
        logger.error(f"Error getting captain suggestion: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bench")
async def get_bench_order(team_data: dict):
    """
    Get optimal bench order.

    Args:
        team_data: Team data

    Returns:
        Optimal bench order
    """
    try:
        logger.info("Optimizing bench order")

        player_ids = team_data.get("players", [])[11:]
        if not player_ids:
            return {"bench_order": []}

        all_players = await fpl_client.get_players()
        bench_players = [p for p in all_players if p.get("id") in player_ids]

        bench_players.sort(key=lambda p: _calculate_simple_prediction(p), reverse=True)

        return {
            "bench_order": [p["id"] for p in bench_players]
        }

    except Exception as e:
        logger.error(f"Error optimizing bench: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _calculate_simple_prediction(player: dict) -> float:
    """Calculate simple prediction based on form and recent points."""
    form = float(player.get("form", 0) or 0)
    points_per_game = float(player.get("points_per_game", 0) or 0)
    total_points = player.get("total_points", 0)

    if total_points < 10:
        return form * 1.2

    return (form * 0.6 + points_per_game * 0.4) * 1.1


def _create_player_prediction(player: dict) -> dict:
    """Create a player prediction object."""
    expected_points = _calculate_simple_prediction(player)

    return {
        "player_id": player["id"],
        "player_name": player.get("web_name", ""),
        "team": str(player.get("team", "")),
        "position": _get_position_name(player.get("element_type", 0)),
        "expected_points": round(expected_points, 1),
        "expected_points_floor": round(expected_points * 0.6, 1),
        "expected_points_ceiling": round(expected_points * 1.4, 1),
        "start_probability": 0.85 if player.get("minutes", 0) > 200 else 0.65,
        "expected_minutes": min(90, player.get("minutes", 0) / max(player.get("event_points", 1), 1)),
        "rotation_risk": 0.2 if player.get("minutes", 0) > 500 else 0.4,
        "injury_risk": 0.1 if player.get("status") == "a" else 0.6,
        "confidence_score": 0.7,
        "key_factors": [
            f"Form: {player.get('form', 0)}",
            f"Points: {player.get('total_points', 0)}",
            f"Price: £{player.get('now_cost', 0) / 10.0}m"
        ],
        "fixture_difficulty": 3,
        "opponent": "TBD"
    }


def _get_position_name(element_type: int) -> str:
    """Get position name from element_type."""
    positions = {1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}
    return positions.get(element_type, "UNK")


def _generate_transfer_suggestions(team_players: List[dict], all_players: List[dict]) -> List[dict]:
    """Generate basic transfer suggestions."""
    suggestions = []

    worst_performers = sorted(team_players[:11], key=lambda p: _calculate_simple_prediction(p))[:3]

    best_alternatives = sorted(
        [p for p in all_players if p["id"] not in [tp["id"] for tp in team_players]],
        key=lambda p: _calculate_simple_prediction(p),
        reverse=True
    )[:10]

    for i, player_out in enumerate(worst_performers[:2]):
        for player_in in best_alternatives[:3]:
            if player_in.get("element_type") == player_out.get("element_type"):
                cost_diff = (player_in.get("now_cost", 0) - player_out.get("now_cost", 0)) / 10.0

                if abs(cost_diff) <= 3.0:
                    points_out = _calculate_simple_prediction(player_out)
                    points_in = _calculate_simple_prediction(player_in)
                    gain = points_in - points_out

                    if gain > 0.5:
                        suggestions.append({
                            "player_out_id": player_out["id"],
                            "player_out_name": player_out.get("web_name", ""),
                            "player_in_id": player_in["id"],
                            "player_in_name": player_in.get("web_name", ""),
                            "expected_points_gain": round(gain, 1),
                            "expected_points_gain_5gw": round(gain * 5, 1),
                            "transfer_cost": 0,
                            "net_cost_change": round(cost_diff, 1),
                            "category": "overall" if i == 0 else "differential",
                            "risk_level": "low" if gain > 2 else "medium",
                            "risk_score": 0.3,
                            "reasoning": f"Upgrade to higher form player with {gain:.1f} point advantage",
                            "key_factors": [
                                f"{player_in.get('web_name')} form: {player_in.get('form', 0)}",
                                f"{player_out.get('web_name')} form: {player_out.get('form', 0)}",
                                f"Cost difference: £{cost_diff:.1f}m"
                            ]
                        })
                        break

    return suggestions[:5]
