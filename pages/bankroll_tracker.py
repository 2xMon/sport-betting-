import streamlit as st
import pandas as pd

st.title("💰 Bankroll Tracker & ROI Calculator")

st.markdown("Log bets manually to track profit, loss, ROI and units.")

# In-memory store (or swap with database later)
if "bets" not in st.session_state:
    st.session_state.bets = []

with st.form("log_bet"):
    col1, col2 = st.columns(2)
    with col1:
        player = st.selectbox("Player or Team", [
            "LeBron James", "Jayson Tatum", "Steph Curry", "Luka Doncic",
            "LAL vs BOS", "NYK vs CHI", "GSW vs MIA"
        ])
        bet_type = st.selectbox("Bet Type", ["Points", "Rebounds", "Assists", "Spread", "Total"])
        line = st.number_input("Line", value=25.5)
        stake = st.number_input("Stake ($)", min_value=1.0, step=1.0)
    with col2:
        model_proj = st.number_input("Model Prediction", value=27.5)
        result = st.selectbox("Outcome", ["Won", "Lost", "Push"])
        odds = st.number_input("Odds (+/-)", value=-110)

    submitted = st.form_submit_button("Add Bet")

    if submitted:
        payout = stake if result == "Push" else (
            stake * (abs(odds)/100) if odds > 0 else stake / (abs(odds)/100)
        )
        profit = 0
        if result == "Won":
            profit = payout
        elif result == "Lost":
            profit = -stake

        st.session_state.bets.append({
            "Target": player,
            "Type": bet_type,
            "Line": line,
            "Model": model_proj,
            "Result": result,
            "Stake": stake,
            "Odds": odds,
            "Profit": profit
        })
        st.success("Bet logged.")

# Display table
df = pd.DataFrame(st.session_state.bets)
if not df.empty:
    st.subheader("📋 Bet History")
    st.dataframe(df, use_container_width=True)

    st.subheader("📊 Summary Stats")
    total_bets = len(df)
    wins = (df["Result"] == "Won").sum()
    losses = (df["Result"] == "Lost").sum()
    pushes = (df["Result"] == "Push").sum()
    roi = (df["Profit"].sum() / df["Stake"].sum()) * 100

    st.markdown(f"""
    - Total Bets: **{total_bets}**
    - Wins: **{wins}**
    - Losses: **{losses}**
    - Pushes: **{pushes}**
    - ROI: **{roi:.2f}%**
    - Total Profit: **${df["Profit"].sum():.2f}**
    """)
else:
    st.info("No bets logged yet.")
