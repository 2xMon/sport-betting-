
import streamlit as st
import pandas as pd
import numpy as np
from real_odds import get_game_odds

st.set_page_config(page_title="🏀 Sports Betting Model", layout="wide")
st.sidebar.title("🏀 Sports Betting Model")
st.title("🏠 Home — Team Spread & Total Predictor")

st.markdown("---")

matchups = [("LAL", "BOS"), ("GSW", "MIA"), ("NYK", "CHI"), ("MIL", "PHX")]

home_team = st.selectbox("Select Home Team", sorted(set([h for h, _ in matchups])))
away_team = st.selectbox("Select Away Team", sorted(set([a for _, a in matchups])))

if home_team == away_team:
    st.warning("⚠️ Please select two different teams.")
else:
    col1, col2 = st.columns(2)

    with col1:
        model_spread = np.random.uniform(-8, 8)
        vegas_odds = get_game_odds(home_team, away_team)
        vegas_spread = vegas_odds['spread']

        st.metric("📊 Model Spread", f"{model_spread:.1f}", f"{model_spread - vegas_spread:+.1f} edge")
        st.metric("🎯 Vegas Spread", f"{vegas_spread:.1f}")

    with col2:
        model_total = np.random.uniform(215, 235)
        vegas_total = vegas_odds['total']

        st.metric("📊 Model Total", f"{model_total:.1f}", f"{model_total - vegas_total:+.1f} edge")
        st.metric("🎯 Vegas Total", f"{vegas_total:.1f}")

    st.markdown("---")

    edge_spread = model_spread - vegas_spread
    edge_total = model_total - vegas_total

    kelly_spread = max((0.91 * (0.5 + min(abs(edge_spread) / 10, 0.4)) - (1 - (0.5 + min(abs(edge_spread) / 10, 0.4)))) / 0.91, 0)
    kelly_total = max((0.91 * (0.5 + min(abs(edge_total) / 10, 0.4)) - (1 - (0.5 + min(abs(edge_total) / 10, 0.4)))) / 0.91, 0)

    st.subheader("💰 Bet Recommendations")

    if abs(edge_spread) >= 2:
        st.success(f"✅ Bet: {'Home' if edge_spread < 0 else 'Away'} ({edge_spread:+.1f} edge)")
        st.write(f"Recommended Kelly Stake: {kelly_spread * 100:.2f}%")
    else:
        st.warning("❌ No Bet: Spread edge too small.")

    if abs(edge_total) >= 2:
        st.success(f"✅ Bet: {'Over' if edge_total > 0 else 'Under'} ({edge_total:+.1f} edge)")
        st.write(f"Recommended Kelly Stake: {kelly_total * 100:.2f}%")
    else:
        st.warning("❌ No Bet: Total edge too small.")
