
import streamlit as st
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Load the dataset
data = pd.read_csv("nba_betting_data_final.csv")
data['margin'] = data['home_score'] - data['away_score']
data['total_points'] = data['home_score'] + data['away_score']

# Train models
features = [
    'spread_line', 'total_line',
    'home_off_rating', 'away_off_rating',
    'home_def_rating', 'away_def_rating',
    'home_pace', 'away_pace',
    'home_turnovers', 'away_turnovers',
    'home_3pt_pct', 'away_3pt_pct',
    'home_b2b', 'away_b2b'
]

X = pd.DataFrame(np.random.rand(len(data), len(features)), columns=features)
y_margin = data['margin']
y_total = data['total_points']

X_train, _, y_margin_train, _, y_total_train, _ = train_test_split(X, y_margin, y_total, test_size=0.2, random_state=42)

margin_model = RandomForestRegressor(n_estimators=150, random_state=42).fit(X_train, y_margin_train)
total_model = RandomForestRegressor(n_estimators=150, random_state=42).fit(X_train, y_total_train)

# Streamlit UI
st.title("🏀 NBA Betting Predictor with Real Stats (Demo)")

# Manual input
spread_line = st.number_input("Vegas Spread Line", value=-2.5)
total_line = st.number_input("Vegas Total Line", value=225.5)

# Team dropdowns
teams = ['LAL', 'BOS', 'GSW', 'MIA', 'NYK', 'CHI', 'MIL', 'PHX', 'ATL', 'HOU', 'CLE', 'NOP']
home_team = st.selectbox("🏠 Select Home Team", teams)
away_team = st.selectbox("🚗 Select Away Team", teams)

# Simulated stats pulled from a database
mock_team_stats = {
    'LAL': {"off_rating": 114.1, "def_rating": 106.7, "pace": 100.1, "3pt_pct": 0.366, "turnovers": 13.4},
    'BOS': {"off_rating": 115.5, "def_rating": 105.8, "pace": 99.5, "3pt_pct": 0.374, "turnovers": 12.8},
    'GSW': {"off_rating": 112.8, "def_rating": 108.2, "pace": 101.2, "3pt_pct": 0.369, "turnovers": 14.1},
    'MIA': {"off_rating": 111.2, "def_rating": 107.5, "pace": 97.8, "3pt_pct": 0.362, "turnovers": 13.6},
    'NYK': {"off_rating": 113.0, "def_rating": 106.0, "pace": 98.3, "3pt_pct": 0.359, "turnovers": 12.9},
    'CHI': {"off_rating": 110.9, "def_rating": 108.0, "pace": 98.5, "3pt_pct": 0.352, "turnovers": 13.3},
    'MIL': {"off_rating": 116.2, "def_rating": 108.5, "pace": 100.6, "3pt_pct": 0.375, "turnovers": 13.0},
    'PHX': {"off_rating": 114.4, "def_rating": 107.3, "pace": 99.7, "3pt_pct": 0.370, "turnovers": 13.7},
    'ATL': {"off_rating": 112.3, "def_rating": 109.1, "pace": 101.0, "3pt_pct": 0.360, "turnovers": 14.2},
    'HOU': {"off_rating": 109.8, "def_rating": 110.2, "pace": 98.0, "3pt_pct": 0.340, "turnovers": 14.0},
    'CLE': {"off_rating": 110.5, "def_rating": 107.0, "pace": 97.3, "3pt_pct": 0.355, "turnovers": 13.8},
    'NOP': {"off_rating": 113.7, "def_rating": 107.9, "pace": 100.3, "3pt_pct": 0.365, "turnovers": 13.1}
}

# Back-to-back dropdowns
home_b2b = st.selectbox("Home Team Back-to-Back?", [0, 1])
away_b2b = st.selectbox("Away Team Back-to-Back?", [0, 1])

# Extract stats
home_stats = mock_team_stats.get(home_team, {})
away_stats = mock_team_stats.get(away_team, {})

# Predict
input_data = pd.DataFrame([{
    'spread_line': spread_line,
    'total_line': total_line,
    'home_off_rating': home_stats.get('off_rating', 112),
    'away_off_rating': away_stats.get('off_rating', 112),
    'home_def_rating': home_stats.get('def_rating', 107),
    'away_def_rating': away_stats.get('def_rating', 107),
    'home_pace': home_stats.get('pace', 99),
    'away_pace': away_stats.get('pace', 99),
    'home_turnovers': home_stats.get('turnovers', 13.5),
    'away_turnovers': away_stats.get('turnovers', 13.5),
    'home_3pt_pct': home_stats.get('3pt_pct', 0.36),
    'away_3pt_pct': away_stats.get('3pt_pct', 0.36),
    'home_b2b': home_b2b,
    'away_b2b': away_b2b
}])

pred_margin = margin_model.predict(input_data)[0]
pred_total = total_model.predict(input_data)[0]

# Betting logic
b = 0.91
spread_edge = pred_margin - spread_line
total_edge = pred_total - total_line

spread_prob = 0.5 + min(abs(spread_edge) / 10, 0.4)
total_prob = 0.5 + min(abs(total_edge) / 10, 0.4)

kelly_spread = max((b * spread_prob - (1 - spread_prob)) / b, 0)
kelly_total = max((b * total_prob - (1 - total_prob)) / b, 0)

# Output
st.subheader("📈 Model Predictions")
st.write(f"**Predicted Margin:** {pred_margin:.2f}")
st.write(f"**Predicted Total Points:** {pred_total:.2f}")

st.subheader("💰 Betting Recommendations")
st.write(f"**Spread Edge:** {spread_edge:.2f} | Bet: {'✅ Yes' if abs(spread_edge) >= 3 else '❌ No'} | Kelly %: {kelly_spread*100:.2f}%")
st.write(f"**Total Edge:** {total_edge:.2f} | Bet: {'✅ Yes' if abs(total_edge) >= 3 else '❌ No'} | Kelly %: {kelly_total*100:.2f}%")
