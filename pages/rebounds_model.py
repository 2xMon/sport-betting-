
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

st.title("📊 NBA Player Props Predictor (Rebounds)")

# Simulated data for player rebounds
np.random.seed(123)
players = ["LeBron James", "Kevin Durant", "Jayson Tatum", "Giannis Antetokounmpo"]
df = pd.DataFrame({
    "player": np.random.choice(players, size=500),
    "opponent_reb_rate": np.random.uniform(45, 55, size=500),
    "pace": np.random.uniform(95, 105, size=500),
    "minutes": np.random.uniform(28, 38, size=500),
    "prev_reb": np.random.uniform(4, 14, size=500),
    "home": np.random.randint(0, 2, size=500),
    "rebounds": np.random.uniform(4, 14, size=500)
})

# Train the model
features = ["opponent_reb_rate", "pace", "minutes", "prev_reb", "home"]
X = df[features]
y = df["rebounds"]
X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42).fit(X_train, y_train)

# User interface
player = st.selectbox("Select Player", players)
minutes = st.slider("Projected Minutes", 28, 40, 34)
pace = st.slider("Game Pace", 95, 105, 100)
opp_reb = st.slider("Opponent Rebound % Allowed", 45.0, 55.0, 50.0)
prev_reb = st.slider("Last Game Rebounds", 2, 16, 8)
home = st.radio("Game Location", ["Home", "Away"]) == "Home"
line = st.number_input("Sportsbook Line (Rebounds)", value=7.5)

# Predict
input_data = pd.DataFrame([{
    "opponent_reb_rate": opp_reb,
    "pace": pace,
    "minutes": minutes,
    "prev_reb": prev_reb,
    "home": 1 if home else 0
}])

pred = model.predict(input_data)[0]
edge = pred - line
prob = 0.5 + min(abs(edge) / 10, 0.4)
kelly = max((0.91 * prob - (1 - prob)) / 0.91, 0)

# Output
st.subheader("📈 Prediction")
st.write(f"**Projected Rebounds:** {pred:.2f}")
st.write(f"**Line:** {line:.1f}")
st.write(f"**Edge:** {edge:+.2f} rebounds")
st.write(f"**Kelly % Stake:** {kelly * 100:.2f}%")

if abs(edge) >= 1.5:
    st.success(f"✅ Bet: {'Over' if edge > 0 else 'Under'}")
else:
    st.warning("❌ No Bet — Edge too small")
