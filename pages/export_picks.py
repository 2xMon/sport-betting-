
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from odds_api import get_team_odds, get_player_prop

st.title("📤 Export Picks — CSV Download")

# Matchups and players to simulate
matchups = [("LAL", "BOS"), ("GSW", "MIA"), ("NYK", "CHI"), ("MIL", "PHX")]
players = ["LeBron James", "Kevin Durant", "Jayson Tatum", "Steph Curry", "Luka Doncic", "Tyrese Haliburton"]

def model_margin(home, away):
    return round(np.random.uniform(-10, 10), 2)

def model_total(home, away):
    return round(np.random.uniform(210, 240), 2)

def model_stat(player, stat):
    return round(get_player_prop(player, stat) + np.random.uniform(-2.5, 2.5), 2)

def get_bet_row(type_, name, model, line):
    edge = round(model - line, 2)
    prob = 0.5 + min(abs(edge) / 10, 0.4)
    kelly = max((0.91 * prob - (1 - prob)) / 0.91, 0)
    bet = "✅ Over" if edge > 1.5 else "❌ No Bet"
    if type_ in ["Spread", "Total"] and abs(edge) > 2:
        bet = "✅ Bet"
    return {
        "Bet Type": type_,
        "Target": name,
        "Model": model,
        "Line": line,
        "Edge": edge,
        "Bet": bet,
        "Kelly %": kelly * 100
    }

bets = []

for home, away in matchups:
    odds = get_team_odds(home, away)
    margin_pred = model_margin(home, away)
    total_pred = model_total(home, away)
    bets.append(get_bet_row("Spread", f"{home} vs {away}", margin_pred, odds["spread"]))
    bets.append(get_bet_row("Total", f"{home} vs {away}", total_pred, odds["total"]))

for p in players:
    for stat in ["points", "rebounds", "assists"]:
        line = get_player_prop(p, stat)
        pred = model_stat(p, stat)
        bets.append(get_bet_row(stat.title(), p, pred, line))

df = pd.DataFrame(bets)
st.subheader("📋 All Picks for Today")
st.dataframe(df, use_container_width=True)

# Download
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download CSV", csv, file_name="daily_picks.csv", mime='text/csv')
