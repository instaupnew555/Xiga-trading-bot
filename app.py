import streamlit as st
import random
from datetime import datetime

st.set_page_config(
    page_title="XIGA Trading Signal Bot",
    page_icon="📊",
    layout="centered"
)

st.title("📊 XIGA Trading Signal Bot")
st.caption("Short-term market signal analysis")

st.divider()

asset = st.selectbox(
    "Select Asset",
    [
        "EUR/USD",
        "GBP/USD",
        "USD/JPY",
        "AUD/USD",
        "USD/CAD",
        "XAU/USD"
    ]
)

timeframe = st.selectbox(
    "Analysis Timeframe",
    ["15 Seconds", "1 Minute", "5 Minutes"]
)

expiry = st.selectbox(
    "Trade Expiry",
    ["15 Seconds", "1 Minute", "2 Minutes", "5 Minutes"]
)

st.divider()

if st.button("🚀 START ANALYSIS", use_container_width=True):

    with st.spinner("Analyzing market conditions..."):

        score = random.randint(45, 95)

        if score >= 75:
            signal = random.choice(["CALL", "PUT"])
        else:
            signal = "NO TRADE"

    st.subheader("Analysis Result")

    if signal == "CALL":
        st.success("🟢 CALL")

    elif signal == "PUT":
        st.error("🔴 PUT")

    else:
        st.warning("⚪ NO TRADE")

    st.metric("Setup Score", f"{score}/100")

    st.write(f"**Asset:** {asset}")
    st.write(f"**Analysis Timeframe:** {timeframe}")
    st.write(f"**Expiry:** {expiry}")

    st.write(
        f"**Signal Time:** "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    st.info(
        "⚠️ DEMO VERSION — This signal is randomly generated "
        "and does NOT use live market data."
    )
