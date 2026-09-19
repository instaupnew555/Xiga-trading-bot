import streamlit as st
import random
from datetime import datetime

# =========================================================
# XIGA TRADING SIGNAL BOT
# UI VERSION
# =========================================================

st.set_page_config(
    page_title="XIGA Trading Signal",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "Trade"

if "signal" not in st.session_state:
    st.session_state.signal = None

if "score" not in st.session_state:
    st.session_state.score = 0

if "signal_time" not in st.session_state:
    st.session_state.signal_time = None

if "history" not in st.session_state:
    st.session_state.history = []


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

* {
    box-sizing: border-box;
}

.stApp {
    background:
        radial-gradient(circle at 50% 0%, #14233d 0%, #07101e 42%, #030711 100%);
    color: #ffffff;
}

.block-container {
    max-width: 520px;
    padding: 20px 15px 35px;
}

header {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* HEADER */

.logo {
    text-align: center;
    font-size: 30px;
    font-weight: 900;
    letter-spacing: 1px;
    margin-top: 5px;
}

.logo-icon {
    color: #25f5a3;
}

.tagline {
    text-align: center;
    color: #71819b;
    font-size: 10px;
    letter-spacing: 2px;
    margin-top: -5px;
    margin-bottom: 22px;
}

/* CARDS */

.card {
    background: linear-gradient(
        145deg,
        rgba(20, 34, 56, .92),
        rgba(8, 17, 31, .94)
    );
    border: 1px solid rgba(81, 111, 145, .35);
    border-radius: 20px;
    padding: 18px;
    margin-bottom: 14px;
    box-shadow: 0 12px 35px rgba(0,0,0,.25);
}

/* ASSET CARD */

.asset-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
}

.small-label {
    color: #73839c;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.asset-value {
    font-size: 19px;
    font-weight: 800;
    margin-top: 5px;
}

.live {
    color: #26f5a4;
    font-size: 11px;
}

/* SIGNAL */

.signal-area {
    text-align: center;
    padding: 5px 0 12px;
}

.signal-circle {
    width: 205px;
    height: 205px;
    margin: 10px auto 20px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 75px;

    background:
        radial-gradient(
            circle,
            rgba(42,255,169,.32) 0%,
            rgba(15,57,54,.75) 42%,
            rgba(4,13,23,.95) 72%
        );

    border: 4px solid #29f5a4;

    box-shadow:
        0 0 18px rgba(41,245,164,.8),
        0 0 55px rgba(41,245,164,.35),
        inset 0 0 35px rgba(41,245,164,.18);
}

.signal-circle.put {
    background:
        radial-gradient(
            circle,
            rgba(255,54,105,.32) 0%,
            rgba(69,18,40,.75) 42%,
            rgba(4,13,23,.95) 72%
        );

    border-color: #ff396d;

    box-shadow:
        0 0 18px rgba(255,57,109,.8),
        0 0 55px rgba(255,57,109,.35),
        inset 0 0 35px rgba(255,57,109,.18);
}

.signal-circle.wait {
    background:
        radial-gradient(
            circle,
            rgba(255,196,76,.25) 0%,
            rgba(55,42,17,.75) 42%,
            rgba(4,13,23,.95) 72%
        );

    border-color: #ffc44d;
}

.buy {
    color: #29f5a4;
}

.sell {
    color: #ff396d;
}

.wait {
    color: #ffc44d;
}

.signal-text {
    font-size: 31px;
    font-weight: 900;
    margin-bottom: 3px;
}

.direction {
    color: #7e8da4;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* STATS */

.stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 18px;
}

.stat {
    background: rgba(7,16,29,.75);
    border: 1px solid rgba(74,103,135,.35);
    border-radius: 15px;
    padding: 15px;
    text-align: center;
}

.stat-title {
    color: #71819b;
    font-size: 10px;
    text-transform: uppercase;
}

.stat-value {
    font-size: 25px;
    font-weight: 900;
    margin-top: 6px;
}

/* AI STATUS */

.ai-status {
    text-align: center;
    background: rgba(15,32,43,.85);
    border: 1px solid rgba(41,245,164,.25);
    border-radius: 14px;
    padding: 14px;
    color: #29f5a4;
    font-size: 12px;
    margin: 15px 0;
}

/* BUTTON */

.stButton > button {
    width: 100%;
    height: 55px;
    border-radius: 16px;
    border: 1px solid #29f5a4;
    background: linear-gradient(100deg,#18b979,#29f5a4);
    color: #03120d;
    font-weight: 900;
    font-size: 15px;
    letter-spacing: .3px;
}

.stButton > button:hover {
    border-color: #55ffba;
    color: #03120d;
}

/* SELECT */

.stSelectbox label {
    color: #8797ad !important;
    font-size: 11px !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: #101c2f;
    border: 1px solid #263c57;
    border-radius: 13px;
}

/* PAGE TITLE */

.page-title {
    font-size: 25px;
    font-weight: 900;
    margin-bottom: 3px;
}

.page-subtitle {
    color: #75849b;
    font-size: 12px;
    margin-bottom: 18px;
}

/* HISTORY */

.history-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 13px 5px;
    border-bottom: 1px solid rgba(80,100,125,.18);
}

.history-asset {
    font-weight: 700;
    font-size: 14px;
}

.history-meta {
    color: #71819b;
    font-size: 10px;
}

.win {
    color: #29f5a4;
    font-weight: 800;
}

.loss {
    color: #ff396d;
    font-weight: 800;
}

/* NAVIGATION */

.nav-title {
    text-align: center;
    color: #71819b;
    font-size: 9px;
    margin-top: 22px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="logo">
    <span class="logo-icon">▥</span> XIGA
</div>
<div class="tagline">TRADING SIGNAL BOT</div>
""", unsafe_allow_html=True)


# =========================================================
# NAVIGATION
# =========================================================

nav1, nav2, nav3, nav4 = st.columns(4)

with nav1:
    if st.button("📈\nTrade", use_container_width=True):
        st.session_state.page = "Trade"

with nav2:
    if st.button("◷\nHistory", use_container_width=True):
        st.session_state.page = "History"

with nav3:
    if st.button("▣\nLearn", use_container_width=True):
        st.session_state.page = "Learn"

with nav4:
    if st.button("♙\nProfile", use_container_width=True):
        st.session_state.page = "Profile"


st.divider()


# =========================================================
# TRADE PAGE
# =========================================================

if st.session_state.page == "Trade":

    st.markdown("""
    <div class="page-title">Trading Setup</div>
    <div class="page-subtitle">
        Configure your market analysis
    </div>
    """, unsafe_allow_html=True)

    # Asset

    asset = st.selectbox(
        "ASSET",
        [
            "🇺🇸🇪🇺 EUR/USD",
            "🇬🇧🇺🇸 GBP/USD",
            "🇺🇸🇯🇵 USD/JPY",
            "🇦🇺🇺🇸 AUD/USD",
            "🇺🇸🇨🇦 USD/CAD",
            "🥇 XAU/USD"
        ]
    )

    timeframe = st.selectbox(
        "TIMEFRAME",
        [
            "10 Seconds",
            "15 Seconds",
            "30 Seconds",
            "1 Minute",
            "5 Minutes"
        ]
    )

    expiry = st.selectbox(
        "TRADE EXPIRY",
        [
            "15 Seconds",
            "30 Seconds",
            "1 Minute",
            "2 Minutes",
            "5 Minutes"
        ]
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # GENERATE
    # =====================================================

    if st.button("⚡ ANALYZE MARKET", use_container_width=True):

        with st.spinner("Analyzing market conditions..."):

            score = random.randint(72, 96)

            if score >= 82:
                signal = random.choice(["CALL", "PUT"])
            else:
                signal = "NO TRADE"

            st.session_state.signal = signal
            st.session_state.score = score
            st.session_state.signal_time = datetime.now()

    # =====================================================
    # SIGNAL
    # =====================================================

    if st.session_state.signal:

        signal = st.session_state.signal
        score = st.session_state.score

        st.markdown("""
        <div class="card">
        """, unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="small-label">SIGNAL FOR</div>
            <div class="asset-value">{asset}</div>
            <div class="live">● MARKET ANALYSIS</div>
            """,
            unsafe_allow_html=True
        )

        if signal == "CALL":

            st.markdown("""
            <div class="signal-area">
                <div class="signal-circle">↗</div>
                <div class="signal-text buy">BUY (CALL)</div>
                <div class="direction">UPWARD SIGNAL</div>
            </div>
            """, unsafe_allow_html=True)

        elif signal == "PUT":

            st.markdown("""
            <div class="signal-area">
                <div class="signal-circle put">↘</div>
                <div class="signal-text sell">SELL (PUT)</div>
                <div class="direction">DOWNWARD SIGNAL</div>
            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown("""
            <div class="signal-area">
                <div class="signal-circle wait">⏸</div>
                <div class="signal-text wait">NO TRADE</div>
                <div class="direction">WAIT FOR CONFIRMATION</div>
            </div>
            """, unsafe_allow_html=True)

        # Stats

        st.markdown(
            f"""
            <div class="stats">

                <div class="stat">
                    <div class="stat-title">
                        Signal Strength
                    </div>

                    <div class="stat-value">
                        {min(5, max(1, round(score / 20)))}/5
                    </div>
                </div>

                <div class="stat">
                    <div class="stat-title">
                        Setup Score
                    </div>

                    <div class="stat-value">
                        {score}/100
                    </div>
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class="ai-status">
            ● AI ANALYSIS COMPLETE<br>
            <span style="color:#71819b;font-size:10px;">
            Live market engine will be connected next
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="card">

                <div class="history-row">
                    <span class="history-meta">TIMEFRAME</span>
                    <span>{timeframe}</span>
                </div>

                <div class="history-row">
                    <span class="history-meta">EXPIRY</span>
                    <span>{expiry}</span>
                </div>

                <div class="history-row">
                    <span class="history-meta">SIGNAL TIME</span>
                    <span>
                    {st.session_state.signal_time.strftime("%H:%M:%S")}
                    </span>
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("🔄 GENERATE NEW SIGNAL", use_container_width=True):
            st.session_state.signal = None
            st.rerun()

    else:

        st.markdown("""
        <div class="card">
            <div class="signal-area">
                <div class="signal-circle wait">◎</div>
                <div class="signal-text wait">
                    READY
                </div>
                <div class="direction">
                    START MARKET ANALYSIS
                </div>
            </div>

            <div class="ai-status">
                ● AI ENGINE READY
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.caption(
        "⚠️ Demo interface. No live trading signal is generated yet."
    )


# =========================================================
# HISTORY
# =========================================================

elif st.session_state.page == "History":

    st.markdown("""
    <div class="page-title">Signal History</div>
    <div class="page-subtitle">
        Track your signals and results
    </div>
    """, unsafe_allow_html=True)

    if len(st.session_state.history) == 0:

        st.markdown("""
        <div class="card" style="text-align:center;padding:45px 20px;">
            <div style="font-size:45px;">◷</div>
            <div style="font-size:18px;font-weight:800;">
                No Signal History
            </div>
            <div style="color:#71819b;font-size:12px;margin-top:8px;">
                Your completed signals will appear here.
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:

        for item in st.session_state.history:

            result_class = "win" if item["result"] == "WIN" else "loss"

            st.markdown(
                f"""
                <div class="card">
                    <div class="history-row">

                        <div>
                            <div class="history-asset">
                                {item["asset"]}
                            </div>

                            <div class="history-meta">
                                {item["direction"]} · {item["expiry"]}
                            </div>
                        </div>

                        <div class="{result_class}">
                            {item["result"]}
                        </div>

                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# LEARN
# =========================================================

elif st.session_state.page == "Learn":

    st.markdown("""
    <div class="page-title">Learn</div>
    <div class="page-subtitle">
        Understand how XIGA analyzes markets
    </div>
    """, unsafe_allow_html=True)

    sections = [
        (
            "📊 Trend Analysis",
            "The future engine will analyze multiple timeframes "
            "to identify the dominant market direction."
        ),
        (
            "📈 Technical Indicators",
            "EMA, RSI, MACD, Bollinger Bands, ADX and volatility "
            "will be combined rather than relying on one indicator."
        ),
        (
            "🎯 Signal Filtering",
            "When market evidence conflicts, XIGA can return "
            "NO TRADE instead of forcing a signal."
        ),
        (
            "📚 Performance",
            "Every completed signal can be recorded so actual "
            "historical performance can be calculated."
        )
    ]

    for title, description in sections:

        st.markdown(
            f"""
            <div class="card">
                <div style="font-size:17px;font-weight:800;">
                    {title}
                </div>

                <div style="
                    color:#7d8ca4;
                    font-size:12px;
                    line-height:1.6;
                    margin-top:8px;
                ">
                    {description}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# PROFILE
# =========================================================

elif st.session_state.page == "Profile":

    st.markdown("""
    <div class="page-title">Profile</div>
    <div class="page-subtitle">
        XIGA account and application settings
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">

        <div style="
            font-size:19px;
            font-weight:800;
        ">
            👤 XIGA Trader
        </div>

        <div style="
            color:#29f5a4;
            font-size:11px;
            margin-top:5px;
        ">
            ● FREE PLAN
        </div>

    </div>
    """, unsafe_allow_html=True)

    options = [
        ("⚙️", "Settings"),
        ("🔔", "Notifications"),
        ("🔒", "Security"),
        ("❓", "Help & Support"),
        ("ℹ️", "About XIGA")
    ]

    for icon, title in options:

        st.markdown(
            f"""
            <div class="card"
                 style="
                    padding:16px;
                    margin-bottom:8px;
                 ">

                <span style="font-size:18px;">
                    {icon}
                </span>

                <span style="
                    margin-left:12px;
                    font-size:14px;
                    font-weight:700;
                ">
                    {title}
                </span>

                <span style="
                    float:right;
                    color:#71819b;
                ">
                    ›
                </span>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="nav-title">
    🔒 SECURE &nbsp; • &nbsp; XIGA AI &nbsp; • &nbsp; v1.0
</div>
""", unsafe_allow_html=True)
