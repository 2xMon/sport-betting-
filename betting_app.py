
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

st.title("🏀 NBA Spread/Total Betting Predictor")

# Input lines
spread_line = st.number_input("Vegas Spread", value=-2.5)
total_line = st.number_input("Vegas Total", value=225.5)

# Home team stats
st.subheader("🏠 Home Team")
home_off_rating = st.number_input("Home Offensive Rating", value=113.5)
home_def_rating = st.number_input("Home Defensive Rating", value=106.2)
home_pace = st.number_input("Home Pace", value=99.5)
home_turnovers = st.number_input("Home Turnovers", value=13.2)
home_3pt_pct = st.number_input("Home 3PT%", value=0.365)
home_b2b = st.selectbox("Home Back-to-Back?", [0, 1])

# Away team stats
st.subheader("🚗 Away Team")
away_off_rating = st.number_input("Away Offensive Rating", value=111.2)
away_def_rating = st.number_input("Away Defensive Rating", value=107.9)
away_pace = st.number_input("Away Pace", value=98.0)
away_turnovers = st.number_input("Away Turnovers", value=14.1)
away_3pt_pct = st.number_input("Away 3PT%", value=0.348)
away_b2b = st.selectbox("Away Back-to-Back?", [0, 1])

# Load data and train models
data = pd.read_csv("nba_betting_data_final.csv")
data['margin'] = data['home_score'] - data['away_score']
data['total_points'] = data['home_score'] + data['away_score']

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

X_train, _, y_margin_train, _, y_total_train, _ = train_test_split(
    X, y_margin, y_total, test_size=0.2, random_state=42
)

margin_model = RandomForestRegressor(n_estimators=150, random_state=42).fit(X_train, y_margin_train)
total_model = RandomForestRegressor(n_estimators=150, random_state=42).fit(X_train, y_total_train)

# Predict
input_data = pd.DataFrame([{
    'spread_line': spread_line,
    'total_line': total_line,
    'home_off_rating': home_off_rating,
    'away_off_rating': away_off_rating,
    'home_def_rating': home_def_rating,
    'away_def_rating': away_def_rating,
    'home_pace': home_pace,
    'away_pace': away_pace,
    'home_turnovers': home_turnovers,
    'away_turnovers': away_turnovers,
    'home_3pt_pct': home_3pt_pct,
    'away_3pt_pct': away_3pt_pct,
    'home_b2b': home_b2b,
    'away_b2b': away_b2b
}])

pred_margin = margin_model.predict(input_data)[0]
pred_total = total_model.predict(input_data)[0]

# Betting logic
b = 0.91
spread_edge = pred_margin - spread_line
spread_prob = 0.5 + min(abs(spread_edge) / 10, 0.4)
kelly_spread = max((b * spread_prob - (1 - spread_prob)) / b, 0)

total_edge = pred_total - total_line
total_prob = 0.5 + min(abs(total_edge) / 10, 0.4)
kelly_total = max((b * total_prob - (1 - total_prob)) / b, 0)

# Output
st.subheader("📈 Model Predictions")
st.write(f"**Predicted Margin:** {pred_margin:.2f}")
st.write(f"**Predicted Total Points:** {pred_total:.2f}")

st.subheader("💰 Betting Recommendations")
st.write(f"**Spread Edge:** {spread_edge:.2f} | Bet: {'✅ Yes' if abs(spread_edge) >= 3 else '❌ No'} | Kelly %: {kelly_spread*100:.2f}%")
st.write(f"**Total Edge:** {total_edge:.2f} | Bet: {'✅ Yes' if abs(total_edge) >= 3 else '❌ No'} | Kelly %: {kelly_total*100:.2f}%")
