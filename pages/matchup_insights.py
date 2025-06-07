import streamlit as st
import pandas as pd
import numpy as np

st.title("🧠 Player Matchup Intelligence")

players = ["LeBron James", "Kevin Durant", "Jayson Tatum", "Giannis Antetokounmpo", "Luka Doncic"]
opponents = ["BOS", "MIA", "PHX", "CHI", "MIL", "GSW"]

# Simulated matchup data
def get_defense_rank(opponent):
    return np.random.randint(1, 30)

def get_last_5_vs_opponent(player, opponent):
    return pd.DataFrame({
        "Date": pd.date_range(end=pd.Timestamp.today(), periods=5).date,
        "Points": np.random.randint(18, 35, size=5),
        "Rebounds": np.random.randint(4, 12, size=5),
        "Assists": np.random.randint(3, 10, size=5)
    })

# Inputs
player = st.selectbox("Select Player", players)
opponent = st.selectbox("Opponent", opponents)

# Output
st.subheader(f"🛡️ Defense Rank vs {opponent}")
rank = get_defense_rank(opponent)
st.write(f"{opponent} is ranked **#{rank}** defensively against this position.")

st.subheader(f"📈 Last 5 Games vs {opponent}")
df = get_last_5_vs_opponent(player, opponent)
st.dataframe(df, use_container_width=True)

# Simulated insight
st.subheader("🧠 Insight")
avg_pts = df["Points"].mean()
avg_reb = df["Rebounds"].mean()
avg_ast = df["Assists"].mean()
st.write(f"**{player}** averages:")
st.markdown(f"- 🟢 **{avg_pts:.1f} PTS**, 🔵 **{avg_reb:.1f} REB**, 🟡 **{avg_ast:.1f} AST** vs {opponent}")
st.success("✅ Favorable matchup!" if rank >= 20 else "⚠️ Tough defense. Consider caution.")
