import streamlit as st
import random
from datetime import datetime

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="XIGA Trading",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 50% 15%, #17243b 0%, #080d18 45%, #050912 100%);
    color: white;
}

.block-container {
    max-width: 520px;
    padding: 25px 18px 35px 18px;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Main title */

.xiga-title {
    text-align: center;
    font-size: 32px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-top: 5px;
    margin-bottom: 4px;
}

.xiga-subtitle {
    text-align: center;
    color: #8d9bb5;
    font-size: 14px;
    margin-bottom: 25px;
}

/* Cards */

.panel {
    background: rgba(20, 29, 47, 0.92);
    border: 1px solid #263650;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 14px;
}

/* Asset */

.asset-label {
    color: #8d9bb5;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.asset-name {
    font-size: 24px;
    font-weight: 800;
    margin-top: 5px;
}

.timeframe {
    color: #00e5ff;
    font-size: 13px;
    margin-top: 5px;
}

/* Signal */

.signal-card {
    text-align: center;
    padding: 22px 10px;
    margin: 12px 0;
}

.signal-circle {
    width: 220px;
    height: 220px;
    border-radius: 50%;
    margin: 5px auto 20px auto;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 62px;

    border: 4px solid #42ff9b;
    background: radial-gradient(circle, #42ff9b 0%, #183d35 45%, #071016 75%);
    box-shadow:
        0 0 25px rgba(66,255,155,.65),
        0 0 70px rgba(66,255,155,.25);
}

.signal-down {
    border-color: #ff416c;
    background: radial-gradient(circle, #ff416c 0%, #42182b 45%, #071016 75%);
    box-shadow:
        0 0 25px rgba(255,65,108,.65),
        0 0 70px rgba(255,65,108,.25);
}

.signal-title {
    font-size: 32px;
    font-weight: 900;
    margin-bottom: 4px;
}

.call {
    color: #55ff9d;
}

.put {
    color: #ff416c;
}

.no-trade {
    color: #ffc857;
}

.direction {
    color: #a9b5c9;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* Stats */

.stats {
    display: flex;
    gap: 12px;
    margin-top: 20px;
}

.stat {
    flex: 1;
    background: #111a2b;
    border: 1px solid #273752;
    border-radius: 15px;
    padding: 16px 8px;
    text-align: center;
}

.stat-label {
    color: #7787a1;
    font-size: 11px;
    text-transform: uppercase;
}

.stat-value {
    color: white;
    font-size: 25px;
    font-weight: 800;
    margin-top: 7px;
}

/* Processing */

.processing {
    background: #101a2b;
    border: 1px solid #273752;
    border-radius: 14px;
    padding: 15px;
    text-align: center;
    color: #00e5ff;
    margin-top: 15px;
}

/* Details */

.detail-row {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #202c42;
}

.detail-label {
    color: #8290a8;
}

.detail-value {
    color: white;
    font-weight: 700;
}

/* Bottom navigation */

.bottom-nav {
    display: flex;
    justify-content: space-around;
    background: #0d1525;
    border: 1px solid #273752;
    border-radius: 18px;
    padding: 13px 5px;
    margin-top: 25px;
}

.nav-item {
    text-align: center;
    color: #7787a1;
    font-size: 12px;
}

.nav-active {
    color: #42ff9b;
}

.nav-icon {
    font-size: 21px;
    display: block;
    margin-bottom: 4px;
}

/* Buttons */

.stButton > button {
    width: 100%;
    height: 55px;
    border-radius: 15px;
    border: 1px solid #42ff9b;
    background: linear-gradient(90deg, #183d35, #1d624c);
    color: #ffffff;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: .5px;
}

.stButton > button:hover {
    border-color: #55ff9d;
    color: white;
}

/* Select boxes */

.stSelectbox label {
    color: #8d9bb5 !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background-color: #151d2d;
    border-color: #2a3b57;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="xiga-title">📊 XIGA Trading</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="xiga-subtitle">AI Short-Term Signal Analyzer</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

asset = st.selectbox(
    "Asset",
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
    "Timeframe",
    [
        "15 Seconds",
        "30 Seconds",
        "1 Minute",
        "5 Minutes"
    ]
)

expiry = st.selectbox(
    "Trade Expiry",
    [
        "15 Seconds",
        "30 Seconds",
        "1 Minute",
        "2 Minutes",
        "5 Minutes"
    ]
)


# --------------------------------------------------
# DEFAULT SIGNAL
# --------------------------------------------------

if "signal" not in st.session_state:
    st.session_state.signal = None

if "score" not in st.session_state:
    st.session_state.score = 0

if "time" not in st.session_state:
    st.session_state.time = None


# --------------------------------------------------
# GENERATE SIGNAL
# --------------------------------------------------

if st.button("🚀  GENERATE NEW SIGNAL"):

    with st.spinner("AI PROCESSING..."):

        score = random.randint(70, 95)

        if score >= 80:
            signal = random.choice(["CALL", "PUT"])
        else:
            signal = "NO TRADE"

        st.session_state.signal = signal
        st.session_state.score = score
        st.session_state.time = datetime.now()


# --------------------------------------------------
# SIGNAL DISPLAY
# --------------------------------------------------

if st.session_state.signal:

    signal = st.session_state.signal
    score = st.session_state.score

    st.markdown(
        f"""
        <div class="panel signal-card">

            <div class="asset-label">SIGNAL FOR</div>

            <div class="asset-name">
                {asset}
            </div>

            <div class="timeframe">
                TIMEFRAME: {timeframe}
            </div>

        """,
        unsafe_allow_html=True
    )

    if signal == "CALL":

        st.markdown(
            """
            <div class="signal-circle">
                ↗
            </div>

            <div class="signal-title call">
                BUY (CALL)
            </div>

            <div class="direction">
                UPWARD
            </div>
            """,
            unsafe_allow_html=True
        )

    elif signal == "PUT":

        st.markdown(
            """
            <div class="signal-circle signal-down">
                ↘
            </div>

            <div class="signal-title put">
                SELL (PUT)
            </div>

            <div class="direction">
                DOWNWARD
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="signal-circle">
                ⏸
            </div>

            <div class="signal-title no-trade">
                NO TRADE
            </div>

            <div class="direction">
                WAIT FOR CONFIRMATION
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class="stats">

            <div class="stat">
                <div class="stat-label">
                    Signal Strength
                </div>

                <div class="stat-value">
                    {min(5, max(1, round(score / 20)))} / 5
                </div>
            </div>

            <div class="stat">
                <div class="stat-label">
                    Setup Score
                </div>

                <div class="stat-value">
                    {score}%
                </div>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="processing">
            🟢 &nbsp; AI ANALYSIS COMPLETE
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="panel">

            <div class="detail-row">
                <span class="detail-label">Asset</span>
                <span class="detail-value">{asset}</span>
            </div>

            <div class="detail-row">
                <span class="detail-label">Timeframe</span>
                <span class="detail-value">{timeframe}</span>
            </div>

            <div class="detail-row">
                <span class="detail-label">Expiry</span>
                <span class="detail-value">{expiry}</span>
            </div>

            <div class="detail-row">
                <span class="detail-label">Signal Time</span>
                <span class="detail-value">
                    {st.session_state.time.strftime("%H:%M:%S")}
                </span>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        """
        <div class="processing">
            🔵 &nbsp; READY FOR MARKET ANALYSIS
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# DISCLAIMER
# --------------------------------------------------

st.caption(
    "⚠️ DEMO UI — Signals are currently simulated. "
    "Live market data and real analysis will be added next."
)


# --------------------------------------------------
# BOTTOM NAVIGATION
# --------------------------------------------------

st.markdown(
    """
    <div class="bottom-nav">

        <div class="nav-item nav-active">
            <span class="nav-icon">📈</span>
            TRADE
        </div>

        <div class="nav-item">
            <span class="nav-icon">☆</span>
            REVIEWS
        </div>

        <div class="nav-item">
            <span class="nav-icon">👤</span>
            PROFILE
        </div>

    </div>

    <div style="
        text-align:center;
        color:#64738c;
        font-size:10px;
        margin-top:12px;
    ">
        🔒 SECURE &nbsp; | &nbsp; XIGA AI &nbsp; | &nbsp; v1.0
    </div>
    """,
    unsafe_allow_html=True
)
