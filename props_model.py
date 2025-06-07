
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

st.title("📊 NBA Player Props Predictor (Points)")

# Simulated player game logs for training
np.random.seed(42)
players = ["LeBron James", "Kevin Durant", "Jayson Tatum", "Steph Curry"]
df = pd.DataFrame({
    "player": np.random.choice(players, size=500),
    "opponent_def_rating": np.random.uniform(105, 115, size=500),
    "pace": np.random.uniform(95, 105, size=500),
    "minutes": np.random.uniform(28, 38, size=500),
    "usage_rate": np.random.uniform(24, 35, size=500),
    "prev_points": np.random.uniform(15, 40, size=500),
    "home": np.random.randint(0, 2, size=500),
    "points": np.random.uniform(15, 40, size=500)
})

# Train model
features = ["opponent_def_rating", "pace", "minutes", "usage_rate", "prev_points", "home"]
X = df[features]
y = df["points"]
X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42).fit(X_train, y_train)

# UI
player = st.selectbox("Select Player", players)
minutes = st.slider("Projected Minutes", 28, 40, 35)
usage = st.slider("Usage Rate (%)", 20, 40, 30)
pace = st.slider("Game Pace", 95, 105, 100)
opp_def = st.slider("Opponent Defensive Rating", 105, 115, 108)
prev_pts = st.slider("Last Game Points", 10, 45, 26)
home = st.radio("Game Location", ["Home", "Away"]) == "Home"
line = st.number_input("Sportsbook Line (Points)", value=25.5)

# Predict
input_data = pd.DataFrame([{
    "opponent_def_rating": opp_def,
    "pace": pace,
    "minutes": minutes,
    "usage_rate": usage,
    "prev_points": prev_pts,
    "home": 1 if home else 0
}])

pred = model.predict(input_data)[0]
edge = pred - line
prob = 0.5 + min(abs(edge) / 10, 0.4)
kelly = max((0.91 * prob - (1 - prob)) / 0.91, 0)

# Output
st.subheader("📈 Prediction")
st.write(f"**Projected Points:** {pred:.2f}")
st.write(f"**Line:** {line:.1f}")
st.write(f"**Edge:** {edge:+.2f} points")
st.write(f"**Kelly % Stake:** {kelly * 100:.2f}%")

if abs(edge) >= 2:
    st.success(f"✅ Bet: {'Over' if edge > 0 else 'Under'}")
else:
    st.warning("❌ No Bet — Edge too small")
