import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Client-Info, Apikey",
};

interface TeamAnalysisRequest {
  players: number[];
  free_transfers?: number;
  bank?: number;
}

interface PlayerData {
  id: number;
  web_name: string;
  team: number;
  element_type: number;
  now_cost: number;
  form: string;
  points_per_game: string;
  total_points: number;
  minutes: number;
  status: string;
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, {
      status: 200,
      headers: corsHeaders,
    });
  }

  try {
    const { players, free_transfers = 1, bank = 0 }: TeamAnalysisRequest = await req.json();

    if (!players || players.length === 0) {
      return new Response(
        JSON.stringify({ error: "No players provided" }),
        {
          status: 400,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        }
      );
    }

    const fplResponse = await fetch("https://fantasy.premierleague.com/api/bootstrap-static/");
    const fplData = await fplResponse.json();
    const allPlayers: PlayerData[] = fplData.elements;

    const teamPlayers = allPlayers.filter(p => players.includes(p.id));

    if (teamPlayers.length !== players.length) {
      return new Response(
        JSON.stringify({ error: "Some players not found" }),
        {
          status: 400,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        }
      );
    }

    const calculatePrediction = (player: PlayerData): number => {
      const form = parseFloat(player.form || "0");
      const ppg = parseFloat(player.points_per_game || "0");
      if (player.total_points < 10) return form * 1.2;
      return (form * 0.6 + ppg * 0.4) * 1.1;
    };

    const getPositionName = (elementType: number): string => {
      const positions: Record<number, string> = { 1: "GK", 2: "DEF", 3: "MID", 4: "FWD" };
      return positions[elementType] || "UNK";
    };

    const createPlayerPrediction = (player: PlayerData) => {
      const expectedPoints = calculatePrediction(player);
      return {
        player_id: player.id,
        player_name: player.web_name,
        team: String(player.team),
        position: getPositionName(player.element_type),
        expected_points: Math.round(expectedPoints * 10) / 10,
        expected_points_floor: Math.round(expectedPoints * 0.6 * 10) / 10,
        expected_points_ceiling: Math.round(expectedPoints * 1.4 * 10) / 10,
        start_probability: player.minutes > 200 ? 0.85 : 0.65,
        expected_minutes: Math.min(90, player.minutes / Math.max(1, player.total_points || 1)),
        rotation_risk: player.minutes > 500 ? 0.2 : 0.4,
        injury_risk: player.status === "a" ? 0.1 : 0.6,
        confidence_score: 0.7,
        key_factors: [
          `Form: ${player.form}`,
          `Points: ${player.total_points}`,
          `Price: £${player.now_cost / 10}m`
        ],
        fixture_difficulty: 3,
        opponent: "TBD"
      };
    };

    const teamValue = teamPlayers.reduce((sum, p) => sum + p.now_cost, 0) / 10;
    const predictedPoints = teamPlayers.slice(0, 11).reduce((sum, p) => sum + calculatePrediction(p), 0);
    const predictedBenchPoints = teamPlayers.slice(11).reduce((sum, p) => sum + calculatePrediction(p), 0);

    const startingEleven = teamPlayers.slice(0, 11);
    const captainPlayer = startingEleven.reduce((best, p) =>
      calculatePrediction(p) > calculatePrediction(best) ? p : best
    );
    const viceCaptain = startingEleven
      .filter(p => p.id !== captainPlayer.id)
      .reduce((best, p) => calculatePrediction(p) > calculatePrediction(best) ? p : best);

    const worstPerformers = [...startingEleven]
      .sort((a, b) => calculatePrediction(a) - calculatePrediction(b))
      .slice(0, 3);

    const bestAlternatives = allPlayers
      .filter(p => !players.includes(p.id))
      .sort((a, b) => calculatePrediction(b) - calculatePrediction(a))
      .slice(0, 10);

    const transferSuggestions = [];
    for (const playerOut of worstPerformers.slice(0, 2)) {
      for (const playerIn of bestAlternatives.slice(0, 3)) {
        if (playerIn.element_type === playerOut.element_type) {
          const costDiff = (playerIn.now_cost - playerOut.now_cost) / 10;
          if (Math.abs(costDiff) <= 3) {
            const gain = calculatePrediction(playerIn) - calculatePrediction(playerOut);
            if (gain > 0.5) {
              transferSuggestions.push({
                player_out_id: playerOut.id,
                player_out_name: playerOut.web_name,
                player_in_id: playerIn.id,
                player_in_name: playerIn.web_name,
                expected_points_gain: Math.round(gain * 10) / 10,
                expected_points_gain_5gw: Math.round(gain * 5 * 10) / 10,
                transfer_cost: 0,
                net_cost_change: Math.round(costDiff * 10) / 10,
                category: transferSuggestions.length === 0 ? "overall" : "differential",
                risk_level: gain > 2 ? "low" : "medium",
                risk_score: 0.3,
                reasoning: `Upgrade to higher form player with ${gain.toFixed(1)} point advantage`,
                key_factors: [
                  `${playerIn.web_name} form: ${playerIn.form}`,
                  `${playerOut.web_name} form: ${playerOut.form}`,
                  `Cost difference: £${costDiff.toFixed(1)}m`
                ]
              });
              break;
            }
          }
        }
      }
      if (transferSuggestions.length >= 5) break;
    }

    const analysis = {
      team_value: Math.round(teamValue * 10) / 10,
      free_transfers,
      bank,
      players,
      captain_id: captainPlayer.id,
      vice_captain_id: viceCaptain.id,
      predicted_gameweek_points: Math.round(predictedPoints * 10) / 10,
      predicted_bench_points: Math.round(predictedBenchPoints * 10) / 10,
      transfer_suggestions: transferSuggestions.slice(0, 5),
      captain_suggestion: createPlayerPrediction(captainPlayer),
      vice_captain_suggestion: createPlayerPrediction(viceCaptain),
      bench_order: players.slice(11)
    };

    return new Response(
      JSON.stringify(analysis),
      {
        status: 200,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      }
    );

  } catch (error) {
    console.error("Error in analyze-team:", error);
    return new Response(
      JSON.stringify({ error: error.message || "Internal server error" }),
      {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      }
    );
  }
});