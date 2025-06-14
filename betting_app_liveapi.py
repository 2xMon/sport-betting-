import pandas as pd
import numpy from sklearn.model_selection import train_test_split

st.title("🏀 NBA Betting Predictor (Live API Version)")

# Load training data
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

X_train, _, y_margin_train, _, y_total_train, _ = train_test_split(X, y_margin, y_total, test_size=0.2, random_state=42)

margin_model = RandomForestRegressor(n_estimators=150, random_state=42).fit(X_train, y_margin_train)
total_model = RandomForestRegressor(n_estimators=150, random_state=42).fit(X_train, y_total_train)

# API call to get team ID
def get_team_id(abbr):
    try:
        res = requests.get("https://www.balldontlie.io/api/v1/teams")
        for team in res.json()['data']:
            if team['abbreviation'] == abbr:
                return team['id']
    except:
        return None

# Placeholder for live stats (simulated as API doesn't offer advanced stats)
def get_live_team_stats(abbr):
    return {
        "off_rating": np.random.uniform(110, 115),
        "def_rating": np.random.uniform(105, 110),
        "pace": np.random.uniform(96, 102),
        "turnovers": np.random.uniform(12, 15),
        "3pt_pct": np.random.uniform(0.33, 0.38)
    }

# Select teams
teams = ['LAL', 'BOS', 'GSW', 'MIA', 'NYK', 'CHI', 'MIL', 'PHX', 'ATL', 'HOU', 'CLE', 'NOP']
home_team = st.selectbox("🏠 Select Home Team", teams)
away_team = st.selectbox("🚗 Select Away Team", teams)

spread_line = st.number_input("Vegas Spread", value=-2.5)
total_line = st.number_input("Vegas Total", value=225.5)
home_b2b = st.selectbox("Home Back-to-Back?", [0, 1])
away_b2b = st.selectbox("Away Back-to-Back?", [0, 1])

# Fetch simulated stats from "live" API
home_stats = get_live_team_stats(home_team)
away_stats = get_live_team_stats(away_team)

# Predict
input_data = pd.DataFrame([{
    'spread_line': spread_line,
    'total_line': total_line,
    'home_off_rating': home_stats['off_rating'],
    'away_off_rating': away_stats['off_rating'],
    'home_def_rating': home_stats['def_rating'],
    'away_def_rating': away_stats['def_rating'],
    'home_pace': home_stats['pace'],
    'away_pace': away_stats['pace'],
    'home_turnovers': home_stats['turnovers'],
    'away_turnovers': away_stats['turnovers'],
    'home_3pt_pct': home_stats['3pt_pct'],
    'away_3pt_pct': away_stats['3pt_pct'],
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

# Show results
st.subheader("📈 Model Predictions")
st.write(f"**Predicted Margin:** {pred_margin:.2f}")
st.write(f"**Predicted Total Points:** {pred_total:.2f}")

