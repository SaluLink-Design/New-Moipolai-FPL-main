"""
Pydantic models for FPL data structures
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class FPLPlayer(BaseModel):
    """FPL Player model."""
    id: int
    web_name: str
    first_name: str
    second_name: str
    team: int
    team_code: int
    element_type: int  # 1=GK, 2=DEF, 3=MID, 4=FWD
    
    # Current status
    status: str  # a=available, d=doubtful, i=injured, s=suspended, u=unavailable
    chance_of_playing_next_round: Optional[int] = None
    chance_of_playing_this_round: Optional[int] = None
    
    # Pricing
    now_cost: int  # Price in tenths (e.g., 100 = £10.0m)
    cost_change_start: int
    cost_change_event: int
    
    # Form and stats
    form: str
    points_per_game: str
    total_points: int
    event_points: int
    
    # Performance metrics
    minutes: int
    goals_scored: int
    assists: int
    clean_sheets: int
    goals_conceded: int
    own_goals: int
    penalties_saved: int
    penalties_missed: int
    yellow_cards: int
    red_cards: int
    saves: int
    bonus: int
    bps: int  # Bonus points system
    
    # Advanced stats
    influence: str
    creativity: str
    threat: str
    ict_index: str
    
    # Ownership
    selected_by_percent: str
    transfers_in: int
    transfers_out: int
    transfers_in_event: int
    transfers_out_event: int
    
    # Expected stats (if available)
    expected_goals: Optional[str] = None
    expected_assists: Optional[str] = None
    expected_goal_involvements: Optional[str] = None
    expected_goals_conceded: Optional[str] = None
    
    @property
    def price(self) -> float:
        """Get price in millions."""
        return self.now_cost / 10.0
    
    @property
    def position(self) -> str:
        """Get position name."""
        positions = {1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}
        return positions.get(self.element_type, "UNK")


class FPLTeam(BaseModel):
    """FPL Team (Premier League club) model."""
    id: int
    name: str
    short_name: str
    code: int
    
    # Strength ratings
    strength: int
    strength_overall_home: int
    strength_overall_away: int
    strength_attack_home: int
    strength_attack_away: int
    strength_defence_home: int
    strength_defence_away: int
    
    # Performance
    played: int
    win: int
    draw: int
    loss: int
    points: int
    position: int
    
    # Form
    form: Optional[str] = None


class FPLFixture(BaseModel):
    """FPL Fixture model."""
    id: int
    event: Optional[int] = None  # Gameweek number
    team_h: int  # Home team ID
    team_a: int  # Away team ID
    team_h_score: Optional[int] = None
    team_a_score: Optional[int] = None
    
    # Difficulty ratings
    team_h_difficulty: int
    team_a_difficulty: int
    
    # Timing
    kickoff_time: Optional[datetime] = None
    started: bool = False
    finished: bool = False
    finished_provisional: bool = False
    
    # Stats
    stats: Optional[List] = None


class FPLGameweek(BaseModel):
    """FPL Gameweek (Event) model."""
    id: int
    name: str
    deadline_time: datetime
    
    # Status
    is_previous: bool
    is_current: bool
    is_next: bool
    finished: bool
    
    # Stats
    average_entry_score: Optional[int] = None
    highest_score: Optional[int] = None
    highest_scoring_entry: Optional[int] = None
    
    # Chip usage
    chip_plays: Optional[List] = None


class PlayerPrediction(BaseModel):
    """Predicted performance for a player."""
    player_id: int
    player_name: str
    team: str
    position: str
    
    # Predictions
    expected_points: float
    expected_points_floor: float  # Conservative estimate
    expected_points_ceiling: float  # Optimistic estimate
    
    # Minutes prediction
    start_probability: float  # 0-1
    expected_minutes: float
    
    # Risk assessment
    rotation_risk: float  # 0-1, higher = more risk
    injury_risk: float  # 0-1, higher = more risk
    
    # Confidence
    confidence_score: float  # 0-1
    
    # Explanation
    key_factors: List[str] = Field(default_factory=list)
    fixture_difficulty: Optional[int] = None
    opponent: Optional[str] = None


class TransferSuggestion(BaseModel):
    """Transfer suggestion model."""
    player_out_id: int
    player_out_name: str
    player_in_id: int
    player_in_name: str
    
    # Impact
    expected_points_gain: float  # For next gameweek
    expected_points_gain_5gw: float  # For next 5 gameweeks
    
    # Cost
    transfer_cost: int  # 0 for free transfer, 4 for hit
    net_cost_change: float  # Price difference
    
    # Category
    category: str  # overall, differential, budget, long_term, safe, gamble
    
    # Risk
    risk_level: str  # low, medium, high
    risk_score: float  # 0-1
    
    # Explanation
    reasoning: str
    key_factors: List[str] = Field(default_factory=list)


class TeamAnalysis(BaseModel):
    """Analysis of a user's FPL team."""
    team_value: float
    free_transfers: int
    bank: float
    
    # Current team
    players: List[int]  # Player IDs
    captain_id: Optional[int] = None
    vice_captain_id: Optional[int] = None
    
    # Predictions
    predicted_gameweek_points: float
    predicted_bench_points: float
    
    # Suggestions
    transfer_suggestions: List[TransferSuggestion]
    captain_suggestion: Optional[PlayerPrediction] = None
    vice_captain_suggestion: Optional[PlayerPrediction] = None
    bench_order: List[int] = Field(default_factory=list)  # Player IDs in order


class OCRResult(BaseModel):
    """Result from OCR processing."""
    success: bool
    players_detected: List[str] = Field(default_factory=list)
    confidence_scores: List[float] = Field(default_factory=list)
    
    # Matched players
    matched_players: List[FPLPlayer] = Field(default_factory=list)
    unmatched_names: List[str] = Field(default_factory=list)
    
    # Validation
    is_valid_team: bool = False
    validation_errors: List[str] = Field(default_factory=list)
    
    # Formation
    formation: Optional[str] = None  # e.g., "3-4-3"
