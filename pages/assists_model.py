
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

st.title("📊 NBA Player Props Predictor (Assists)")

# Simulated data for player assists
np.random.seed(321)
players = ["LeBron James", "Trae Young", "Luka Doncic", "Tyrese Haliburton"]
df = pd.DataFrame({
    "player": np.random.choice(players, size=500),
    "opponent_ast_rate": np.random.uniform(20, 30, size=500),
    "pace": np.random.uniform(95, 105, size=500),
    "minutes": np.random.uniform(28, 38, size=500),
    "prev_ast": np.random.uniform(4, 13, size=500),
    "usage_rate": np.random.uniform(24, 35, size=500),
    "home": np.random.randint(0, 2, size=500),
    "assists": np.random.uniform(4, 13, size=500)
})

# Train model
features = ["opponent_ast_rate", "pace", "minutes", "prev_ast", "usage_rate", "home"]
X = df[features]
y = df["assists"]
X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42).fit(X_train, y_train)

# UI
player = st.selectbox("Select Player", players)
minutes = st.slider("Projected Minutes", 28, 40, 34)
pace = st.slider("Game Pace", 95, 105, 100)
opp_ast = st.slider("Opponent AST% Allowed", 20.0, 30.0, 25.0)
prev_ast = st.slider("Last Game Assists", 2, 14, 8)
usage = st.slider("Usage Rate (%)", 24, 35, 30)
home = st.radio("Game Location", ["Home", "Away"]) == "Home"
line = st.number_input("Sportsbook Line (Assists)", value=7.5)

# Predict
input_data = pd.DataFrame([{
    "opponent_ast_rate": opp_ast,
    "pace": pace,
    "minutes": minutes,
    "prev_ast": prev_ast,
    "usage_rate": usage,
    "home": 1 if home else 0
}])

pred = model.predict(input_data)[0]
edge = pred - line
prob = 0.5 + min(abs(edge) / 10, 0.4)
kelly = max((0.91 * prob - (1 - prob)) / 0.91, 0)

# Output
st.subheader("📈 Prediction")
st.write(f"**Projected Assists:** {pred:.2f}")
st.write(f"**Line:** {line:.1f}")
st.write(f"**Edge:** {edge:+.2f} assists")
st.write(f"**Kelly % Stake:** {kelly * 100:.2f}%")

if abs(edge) >= 1.5:
    st.success(f"✅ Bet: {'Over' if edge > 0 else 'Under'}")
else:
    st.warning("❌ No Bet — Edge too small")
