import streamlit as st
import pandas as pd
from odds_api import get_team_odds, get_player_prop
import random

st.title("🧠 Daily Model Picks Dashboard")

# Simulated team matchups
matchups = [
    ("LAL", "BOS"),
    ("GSW", "MIA"),
    ("NYK", "CHI"),
    ("MIL", "PHX")
]

# Simulated players to evaluate
players = [
    "LeBron James", "Kevin Durant", "Steph Curry", "Jayson Tatum",
    "Luka Doncic", "Giannis Antetokounmpo", "Trae Young", "Tyrese Haliburton"
]

# Simulated model prediction (with slight edge)
def simulate_model_prediction(line):
    return line + random.uniform(-3.5, 3.5)

# Evaluate team picks
team_rows = []
for home, away in matchups:
    odds = get_team_odds(home, away)
    pred_spread = simulate_model_prediction(odds['spread'])
    pred_total = simulate_model_prediction(odds['total'])

    spread_edge = pred_spread - odds['spread']
    total_edge = pred_total - odds['total']

    team_rows.append({
        "Type": "Spread",
        "Game": f"{away} @ {home}",
        "Target": odds['spread'],
        "Model": round(pred_spread, 2),
        "Edge": round(spread_edge, 2),
        "Bet": "Over" if spread_edge > 0 else "Under",
        "Kelly %": round(max((0.91 * (0.5 + min(abs(spread_edge) / 10, 0.4)) - 0.5) / 0.91, 0) * 100, 2)
    })

    team_rows.append({
        "Type": "Total",
        "Game": f"{away} @ {home}",
        "Target": odds['total'],
        "Model": round(pred_total, 2),
        "Edge": round(total_edge, 2),
        "Bet": "Over" if total_edge > 0 else "Under",
        "Kelly %": round(max((0.91 * (0.5 + min(abs(total_edge) / 10, 0.4)) - 0.5) / 0.91, 0) * 100, 2)
    })

# Evaluate player props
props = []
for player in players:
    for stat in ["points", "rebounds", "assists"]:
        line = get_player_prop(player, stat)
        model = simulate_model_prediction(line)
        edge = model - line
        kelly = max((0.91 * (0.5 + min(abs(edge) / 10, 0.4)) - 0.5) / 0.91, 0)
        props.append({
            "Type": stat.title(),
            "Game": player,
            "Target": line,
            "Model": round(model, 2),
            "Edge": round(edge, 2),
            "Bet": "Over" if edge > 0 else "Under",
            "Kelly %": round(kelly * 100, 2)
        })

# Combine team and prop picks
df = pd.DataFrame(team_rows + props)
df = df.sort_values(by="Kelly %", ascending=False)

st.subheader("📊 Today's Top Picks")
st.dataframe(df, use_container_width=True)
