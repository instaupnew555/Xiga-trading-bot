import streamlit as st
import random
from datetime import datetime

# ============================================================
# XIGA TRADING SIGNAL BOT
# PREMIUM MOBILE UI - VERSION 3
# ============================================================

st.set_page_config(
    page_title="XIGA Trading Signal Bot",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# SESSION STATE
# ============================================================

if "signal" not in st.session_state:
    st.session_state.signal = None

if "strength" not in st.session_state:
    st.session_state.strength = 4

if "signal_time" not in st.session_state:
    st.session_state.signal_time = None

if "page" not in st.session_state:
    st.session_state.page = "Trade"

# ============================================================
# PREMIUM CSS
# ============================================================

st.markdown("""
<style>

/* =========================================================
   GLOBAL
   ========================================================= */

html, body {
    margin: 0;
    padding: 0;
    background: #030914;
}

.stApp {
    background:
        radial-gradient(
            circle at 50% -10%,
            #173452 0%,
            #091728 32%,
            #030914 70%
        );
    color: #ffffff;
}

.block-container {
    max-width: 500px !important;
    padding: 16px 14px 25px !important;
}

header {
    visibility: hidden;
    height: 0;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

/* =========================================================
   REMOVE DEFAULT STREAMLIT ELEMENT SPACING
   ========================================================= */

div[data-testid="stVerticalBlock"] {
    gap: 0.45rem;
}

/* =========================================================
   TOP HEADER
   ========================================================= */

.xiga-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 58px;
    margin-bottom: 12px;
}

.xiga-menu {
    width: 42px;
    height: 42px;
    border-radius: 13px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: rgba(10, 31, 52, 0.85);
    border: 1px solid #16466b;

    color: #d9edff;
    font-size: 23px;
}

.xiga-brand {
    flex: 1;
    text-align: center;
    line-height: 1;
}

.xiga-logo {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;

    font-size: 25px;
    font-weight: 900;
    letter-spacing: 1px;
}

.xiga-logo-icon {
    color: #24f4b0;
    font-size: 27px;
}

.xiga-brand-sub {
    margin-top: 5px;
    color: #8295ad;
    font-size: 8px;
    letter-spacing: 1.6px;
}

.xiga-pro {
    min-width: 66px;
    padding: 9px 8px;
    border-radius: 12px;

    text-align: center;

    color: #ffd96a;
    font-size: 10px;
    font-weight: 800;

    background:
        linear-gradient(
            135deg,
            rgba(91, 66, 16, .8),
            rgba(41, 31, 9, .8)
        );

    border: 1px solid #a87b19;

    box-shadow:
        0 0 15px rgba(220, 166, 40, .12);
}

/* =========================================================
   GLASS
   ========================================================= */

.glass {
    background:
        linear-gradient(
            145deg,
            rgba(12, 32, 54, .94),
            rgba(5, 17, 31, .97)
        );

    border: 1px solid rgba(31, 96, 143, .65);

    border-radius: 19px;

    box-shadow:
        0 14px 40px rgba(0,0,0,.30),
        inset 0 1px rgba(255,255,255,.035);
}

/* =========================================================
   MARKET SELECTOR
   ========================================================= */

.market-card {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;

    padding: 10px;

    margin-bottom: 12px;
}

.market-box {
    min-height: 63px;

    padding: 10px 12px;

    border-radius: 13px;

    background:
        linear-gradient(
            145deg,
            rgba(10, 39, 65, .95),
            rgba(7, 25, 44, .95)
        );

    border: 1px solid #16517d;
}

.market-label {
    color: #8ca6bf;
    font-size: 9px;
    margin-bottom: 5px;
}

.market-value {
    color: #ffffff;
    font-size: 15px;
    font-weight: 800;
}

.market-live {
    color: #27f5a6;
    font-size: 8px;
    margin-left: 4px;
}

/* =========================================================
   STREAMLIT SELECTBOX
   ========================================================= */

.stSelectbox {
    margin: 0 !important;
}

.stSelectbox label {
    display: none !important;
}

.stSelectbox div[data-baseweb="select"] {
    margin: 0 !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    min-height: 38px !important;

    background: transparent !important;

    border: none !important;

    padding: 0 2px !important;

    box-shadow: none !important;
}

.stSelectbox div[data-baseweb="select"] span {
    color: #ffffff !important;
    font-size: 14px !important;
    font-weight: 700 !important;
}

/* =========================================================
   SIGNAL CARD
   ========================================================= */

.signal-card {
    position: relative;

    overflow: hidden;

    padding: 17px 12px 13px;

    text-align: center;

    min-height: 535px;
}

/* =========================================================
   BACKGROUND CHART
   ========================================================= */

.chart-background {
    position: absolute;

    left: 0;
    right: 0;

    top: 118px;

    width: 100%;
    height: 210px;

    opacity: .35;

    pointer-events: none;
}

.chart-grid {
    stroke: #1c587d;
    stroke-width: 1;
    opacity: .25;
}

.chart-line-green {
    fill: none;
    stroke: #1cf2a3;
    stroke-width: 2;
}

.chart-line-red {
    fill: none;
    stroke: #ff3d70;
    stroke-width: 2;
}

.candle-green {
    stroke: #1cf2a3;
    fill: #1cf2a3;
}

.candle-red {
    stroke: #ff3d70;
    fill: #ff3d70;
}

/* =========================================================
   WORLD MAP EFFECT
   ========================================================= */

.map-dots {
    position: absolute;

    left: 15px;
    right: 15px;

    top: 125px;

    height: 130px;

    opacity: .12;

    background-image:
        radial-gradient(
            circle,
            #24f4b0 1px,
            transparent 1px
        );

    background-size: 9px 9px;

    mask-image:
        linear-gradient(
            90deg,
            transparent,
            black 15%,
            black 85%,
            transparent
        );

    pointer-events: none;
}

/* =========================================================
   SIGNAL TEXT
   ========================================================= */

.signal-label {
    position: relative;
    z-index: 4;

    color: #91a5ba;

    font-size: 9px;

    text-transform: uppercase;

    letter-spacing: 1.5px;
}

.signal-asset {
    position: relative;
    z-index: 4;

    margin-top: 4px;

    font-size: 22px;

    font-weight: 900;
}

.signal-time {
    position: relative;
    z-index: 4;

    margin-top: 4px;

    color: #26efa4;

    font-size: 9px;

    letter-spacing: 1px;
}

/* =========================================================
   SIGNAL CIRCLE
   ========================================================= */

.signal-circle {
    position: relative;
    z-index: 5;

    width: 218px;
    height: 218px;

    margin: 23px auto 18px;

    border-radius: 50%;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        radial-gradient(
            circle,
            rgba(34, 245, 164, .40) 0%,
            rgba(15, 77, 65, .70) 34%,
            rgba(4, 16, 28, .98) 72%
        );

    border: 3px solid #23f3a4;

    box-shadow:
        0 0 10px #23f3a4,
        0 0 32px rgba(35,243,164,.65),
        0 0 80px rgba(35,243,164,.23),
        inset 0 0 30px rgba(35,243,164,.28);
}

.signal-circle.sell {
    background:
        radial-gradient(
            circle,
            rgba(255, 47, 101, .40) 0%,
            rgba(82, 17, 42, .70) 34%,
            rgba(4, 16, 28, .98) 72%
        );

    border-color: #ff376c;

    box-shadow:
        0 0 10px #ff376c,
        0 0 32px rgba(255,55,108,.65),
        0 0 80px rgba(255,55,108,.23),
        inset 0 0 30px rgba(255,55,108,.28);
}

.signal-ring {
    position: absolute;

    width: 187px;
    height: 187px;

    border-radius: 50%;

    border: 1px solid rgba(255,255,255,.16);
}

.signal-arrow {
    position: relative;

    font-size: 82px;

    font-weight: 900;

    line-height: 1;

    color: #5cffba;

    text-shadow:
        0 0 10px #2df5a8,
        0 0 25px rgba(45,245,168,.85);
}

.signal-arrow.sell-arrow {
    color: #ff668b;

    text-shadow:
        0 0 10px #ff3f72,
        0 0 25px rgba(255,63,114,.85);
}

/* =========================================================
   SIGNAL TITLE
   ========================================================= */

.signal-title {
    position: relative;
    z-index: 5;

    font-size: 31px;

    font-weight: 950;

    letter-spacing: -.5px;
}

.signal-title.buy {
    color: #36f5aa;

    text-shadow:
        0 0 20px rgba(54,245,170,.25);
}

.signal-title.sell {
    color: #ff416f;

    text-shadow:
        0 0 20px rgba(255,65,111,.25);
}

.signal-direction {
    position: relative;
    z-index: 5;

    margin-top: 4px;

    color: #8a9bb0;

    font-size: 9px;

    letter-spacing: 2px;

    text-transform: uppercase;
}

/* =========================================================
   STATISTICS
   ========================================================= */

.stats-row {
    position: relative;
    z-index: 5;

    display: grid;

    grid-template-columns: 1fr 1fr;

    gap: 10px;

    margin-top: 17px;
}

.stat-card {
    min-height: 101px;

    padding: 14px 8px;

    border-radius: 15px;

    background:
        linear-gradient(
            145deg,
            rgba(8, 29, 49, .96),
            rgba(5, 18, 32, .96)
        );

    border: 1px solid #15517a;
}

.stat-label {
    color: #91a4b9;

    font-size: 10px;
}

.stat-dots {
    margin-top: 8px;

    font-size: 17px;

    letter-spacing: 2px;
}

.dot-green {
    color: #24f5a4;

    text-shadow:
        0 0 10px rgba(36,245,164,.7);
}

.dot-red {
    color: #ff3b6d;

    text-shadow:
        0 0 10px rgba(255,59,109,.7);
}

.dot-empty {
    color: #24384c;
}

.stat-bottom {
    margin-top: 4px;

    color: #ffffff;

    font-size: 13px;

    font-weight: 800;
}

.win-number {
    margin-top: 8px;

    color: #28f5a5;

    font-size: 26px;

    font-weight: 900;
}

.live-text {
    margin-top: 2px;

    color: #27f5a4;

    font-size: 9px;
}

/* =========================================================
   AI CARD
   ========================================================= */

.ai-card {
    position: relative;
    z-index: 5;

    display: flex;

    align-items: center;

    gap: 12px;

    padding: 14px;

    margin-top: 11px;

    text-align: left;

    border-radius: 15px;

    background:
        linear-gradient(
            145deg,
            rgba(7, 34, 45, .96),
            rgba(5, 20, 32, .96)
        );

    border: 1px solid rgba(31, 183, 153, .55);
}

.ai-icon {
    width: 35px;
    height: 35px;

    flex-shrink: 0;

    border-radius: 50%;

    display: flex;
    align-items: center;
    justify-content: center;

    background: rgba(35,245,164,.15);

    border: 1px solid rgba(35,245,164,.5);

    color: #2af5a5;

    font-size: 17px;

    box-shadow:
        0 0 15px rgba(35,245,164,.2);
}

.ai-title {
    color: #2af5a5;

    font-size: 12px;

    font-weight: 900;
}

.ai-description {
    margin-top: 3px;

    color: #8497ac;

    font-size: 9px;
}

/* =========================================================
   ACTION BUTTON
   ========================================================= */

.action-button {
    position: relative;
    z-index: 8;

    margin-top: 11px;
}

/* =========================================================
   STREAMLIT BUTTON
   ========================================================= */

.stButton > button {
    width: 100%;

    min-height: 53px;

    border-radius: 15px !important;

    border: 1px solid #4affbd !important;

    background:
        linear-gradient(
            100deg,
            #15cf8c,
            #37f5ad
        ) !important;

    color: #03130d !important;

    font-size: 14px !important;

    font-weight: 900 !important;

    letter-spacing: .2px;

    box-shadow:
        0 8px 30px rgba(32,245,165,.18);
}

.stButton > button:hover {
    border-color: #73ffca !important;

    color: #03130d !important;

    box-shadow:
        0 8px 35px rgba(32,245,165,.28);
}

.stButton > button:active {
    transform: scale(.985);
}

/* =========================================================
   NAVIGATION
   ========================================================= */

.nav-wrap {
    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 5px;

    margin-top: 14px;

    padding: 7px;

    border-radius: 18px;

    background:
        rgba(5, 16, 29, .96);

    border: 1px solid #16405e;
}

.nav-item {
    text-align: center;

    padding: 9px 3px;

    border-radius: 12px;

    color: #72859d;

    font-size: 9px;
}

.nav-item.active {
    color: #27f5a4;

    background:
        radial-gradient(
            circle at 50% 50%,
            rgba(34,245,164,.14),
            transparent 70%
        );

    text-shadow:
        0 0 12px rgba(34,245,164,.35);
}

.nav-icon {
    display: block;

    font-size: 20px;

    line-height: 20px;

    margin-bottom: 4px;
}

/* =========================================================
   FOOTER
   ========================================================= */

.footer-text {
    text-align: center;

    color: #53667c;

    font-size: 8px;

    margin-top: 10px;

    letter-spacing: .4px;
}

/* =========================================================
   HISTORY / PROFILE / LEARN
   ========================================================= */

.page-card {
    padding: 18px;

    margin-bottom: 11px;
}

.page-title {
    font-size: 25px;

    font-weight: 900;

    margin-bottom: 3px;
}

.page-subtitle {
    color: #778ba2;

    font-size: 11px;

    margin-bottom: 15px;
}

.history-item {
    display: flex;

    justify-content: space-between;

    align-items: center;

    padding: 13px 3px;

    border-bottom: 1px solid rgba(64,94,120,.25);
}

.history-left strong {
    display: block;

    font-size: 13px;
}

.history-left span {
    color: #73879d;

    font-size: 9px;
}

.history-win {
    color: #29f5a5;

    font-size: 10px;

    font-weight: 900;
}

.history-loss {
    color: #ff416f;

    font-size: 10px;

    font-weight: 900;
}

.info-icon {
    font-size: 27px;

    margin-bottom: 6px;
}

.profile-row {
    padding: 15px 3px;

    border-bottom: 1px solid rgba(64,94,120,.25);

    font-size: 13px;

    font-weight: 700;
}

.profile-row span {
    float: right;

    color: #647990;
}

/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 420px) {

    .block-container {
        padding-left: 10px !important;
        padding-right: 10px !important;
    }

    .signal-circle {
        width: 198px;
        height: 198px;
    }

    .signal-ring {
        width: 170px;
        height: 170px;
    }

    .signal-arrow {
        font-size: 72px;
    }

    .signal-title {
        font-size: 28px;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TOP HEADER
# ============================================================

st.markdown("""
<div class="xiga-header">

    <div class="xiga-menu">☰</div>

    <div class="xiga-brand">
        <div class="xiga-logo">
            <span class="xiga-logo-icon">▰</span>
            <span>XIGA</span>
        </div>

        <div class="xiga-brand-sub">
            TRADING SIGNAL BOT
        </div>
    </div>

    <div class="xiga-pro">
        👑 PRO
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# NAVIGATION BUTTONS
# Unique keys prevent duplicate-element errors.
# ============================================================

n1, n2, n3, n4 = st.columns(4)

with n1:
    if st.button("📈 Trade", key="nav_trade", use_container_width=True):
        st.session_state.page = "Trade"

with n2:
    if st.button("◷ History", key="nav_history", use_container_width=True):
        st.session_state.page = "History"

with n3:
    if st.button("▣ Learn", key="nav_learn", use_container_width=True):
        st.session_state.page = "Learn"

with n4:
    if st.button("♙ Profile", key="nav_profile", use_container_width=True):
        st.session_state.page = "Profile"


# ============================================================
# TRADE PAGE
# ============================================================

if st.session_state.page == "Trade":

    # --------------------------------------------------------
    # MARKET CARD
    # --------------------------------------------------------

    st.markdown(
        '<div class="glass market-card">',
        unsafe_allow_html=True
    )

    m1, m2 = st.columns(2)

    with m1:

        st.markdown(
            """
            <div class="market-box">
                <div class="market-label">ASSET</div>
            """,
            unsafe_allow_html=True
        )

        asset = st.selectbox(
            "asset",
            [
                "🇺🇸 🇪🇺  EUR/USD",
                "🇬🇧 🇺🇸  GBP/USD",
                "🇺🇸 🇯🇵  USD/JPY",
                "🇦🇺 🇺🇸  AUD/USD",
                "🇺🇸 🇨🇦  USD/CAD",
                "🥇  XAU/USD"
            ],
            key="asset_select",
            label_visibility="collapsed"
        )

        st.markdown(
            '<span class="market-live">● MARKET</span></div>',
            unsafe_allow_html=True
        )

    with m2:

        st.markdown(
            """
            <div class="market-box">
                <div class="market-label">TIMEFRAME</div>
            """,
            unsafe_allow_html=True
        )

        timeframe = st.selectbox(
            "timeframe",
            [
                "10 SEC",
                "15 SEC",
                "30 SEC",
                "1 MIN",
                "5 MIN"
            ],
            key="timeframe_select",
            label_visibility="collapsed"
        )

        st.markdown(
            '<span class="market-live">● READY</span></div>',
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # SIGNAL
    # --------------------------------------------------------

    signal = st.session_state.signal

    if signal is None:

        signal = "READY"

    # --------------------------------------------------------
    # GENERATE SIGNAL
    #
    # This is only a visual demo.
    # It does NOT use market data.
    # --------------------------------------------------------

    if st.button(
        "⚡  GENERATE NEW SIGNAL",
        key="generate_signal",
        use_container_width=True
    ):

        st.session_state.signal = random.choice(
            ["CALL", "PUT"]
        )

        st.session_state.strength = random.choice(
            [3, 4, 4, 5]
        )

        st.session_state.signal_time = datetime.now()

        st.rerun()

    signal = st.session_state.signal

    # --------------------------------------------------------
    # SIGNAL CARD
    # --------------------------------------------------------

    if signal == "CALL":

        circle_class = ""
        arrow_class = ""
        arrow = "↗"
        title = "BUY (CALL)"
        title_class = "buy"
        direction = "UPWARD TREND"

        filled_color = "dot-green"

    elif signal == "PUT":

        circle_class = "sell"
        arrow_class = "sell-arrow"
        arrow = "↘"
        title = "SELL (PUT)"
        title_class = "sell"
        direction = "DOWNWARD TREND"

        filled_color = "dot-red"

    else:

        circle_class = ""
        arrow_class = ""
        arrow = "⌁"
        title = "AI READY"
        title_class = "buy"
        direction = "WAITING FOR ANALYSIS"

        filled_color = "dot-green"

    strength = st.session_state.strength

    filled = "● " * strength
    empty = "● " * (5 - strength)

    # --------------------------------------------------------
    # CHART + SIGNAL
    # --------------------------------------------------------

    st.markdown(
        f"""
<div class="glass signal-card">

<svg class="chart-background"
     viewBox="0 0 500 210"
     preserveAspectRatio="none">

    <line class="chart-grid"
          x1="0" y1="40"
          x2="500" y2="40"/>

    <line class="chart-grid"
          x1="0" y1="90"
          x2="500" y2="90"/>

    <line class="chart-grid"
          x1="0" y1="140"
          x2="500" y2="140"/>

    <line class="chart-grid"
          x1="0" y1="190"
          x2="500" y2="190"/>

    <!-- candles -->

    <line class="candle-green"
          x1="35" y1="135"
          x2="35" y2="80"/>

    <rect class="candle-green"
          x="29" y="95"
          width="12"
          height="30"
          rx="2"/>

    <line class="candle-red"
          x1="72" y1="120"
          x2="72" y2="70"/>

    <rect class="candle-red"
          x="66" y="82"
          width="12"
          height="25"
          rx="2"/>

    <line class="candle-green"
          x1="108" y1="105"
          x2="108" y2="50"/>

    <rect class="candle-green"
          x="102" y="65"
          width="12"
          height="30"
          rx="2"/>

    <line class="candle-green"
          x1="145" y1="90"
          x2="145" y2="35"/>

    <rect class="candle-green"
          x="139" y="45"
          width="12"
          height="30"
          rx="2"/>

    <line class="candle-red"
          x1="182" y1="100"
          x2="182" y2="45"/>

    <rect class="candle-red"
          x="176" y="55"
          width="12"
          height="28"
          rx="2"/>

    <line class="candle-green"
          x1="220" y1="82"
          x2="220" y2="25"/>

    <rect class="candle-green"
          x="214" y="34"
          width="12"
          height="33"
          rx="2"/>

    <line class="candle-green"
          x1="258" y1="72"
          x2="258" y2="15"/>

    <rect class="candle-green"
          x="252" y="25"
          width="12"
          height="30"
          rx="2"/>

    <line class="candle-red"
          x1="295" y1="85"
          x2="295" y2="30"/>

    <rect class="candle-red"
          x="289" y="42"
          width="12"
          height="28"
          rx="2"/>

    <line class="candle-green"
          x1="333" y1="65"
          x2="333" y2="10"/>

    <rect class="candle-green"
          x="327" y="20"
          width="12"
          height="30"
          rx="2"/>

    <line class="candle-green"
          x1="370" y1="55"
          x2="370" y2="5"/>

    <rect class="candle-green"
          x="364" y="12"
          width="12"
          height="29"
          rx="2"/>

    <line class="candle-red"
          x1="408" y1="68"
          x2="408" y2="15"/>

    <rect class="candle-red"
          x="402" y="25"
          width="12"
          height="29"
          rx="2"/>

    <line class="candle-green"
          x1="446" y1="45"
          x2="446" y2="0"/>

    <rect class="candle-green"
          x="440" y="8"
          width="12"
          height="25"
          rx="2"/>

    <polyline
        class="chart-line-green"
        points="
        0,155
        35,132
        72,143
        108,106
        145,92
        182,106
        220,78
        258,68
        295,82
        333,54
        370,42
        408,57
        446,25
        500,10"/>

</svg>

<div class="map-dots"></div>

<div class="signal-label">
    SIGNAL FOR
</div>

<div class="signal-asset">
    {asset}
</div>

<div class="signal-time">
    ● TIMEFRAME: {timeframe}
</div>

<div class="signal-circle {circle_class}">
    <div class="signal-ring"></div>
    <div class="signal-arrow {arrow_class}">
        {arrow}
    </div>
</div>

<div class="signal-title {title_class}">
    {title}
</div>

<div class="signal-direction">
    {direction}
</div>

<div class="stats-row">

    <div class="stat-card">

        <div class="stat-label">
            Signal Strength
        </div>

        <div class="stat-dots {filled_color}">
            {filled}<span class="dot-empty">{empty}</span>
        </div>

        <div class="stat-bottom">
            {strength}/5
        </div>

    </div>

    <div class="stat-card">

        <div class="stat-label">
            Win Rate
        </div>

        <div class="win-number">
            —
        </div>

        <div class="live-text">
            ● NO DATA YET
        </div>

    </div>

</div>

<div class="ai-card">

    <div class="ai-icon">
        ✓
    </div>

    <div>

        <div class="ai-title">
            AI ANALYSIS COMPLETE
        </div>

        <div class="ai-description">
            {("Demo signal — live market engine will be connected next."
             if signal != "READY"
             else "Select your market and start analysis.")}
        </div>

    </div>

</div>

</div>
""",
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # SECOND ACTION BUTTON
    # --------------------------------------------------------

    if signal is not None:

        if st.button(
            "↻  GENERATE NEW SIGNAL",
            key="new_signal",
            use_container_width=True
        ):

            st.session_state.signal = random.choice(
                ["CALL", "PUT"]
            )

            st.session_state.strength = random.choice(
                [3, 4, 4, 5]
            )

            st.session_state.signal_time = datetime.now()

            st.rerun()

    # --------------------------------------------------------
    # DISCLAIMER
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="footer-text">
            ⚠ DEMO MODE • SIGNALS ARE SIMULATED •
            NO LIVE MARKET DATA
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HISTORY PAGE
# ============================================================

elif st.session_state.page == "History":

    st.markdown("""
    <div class="glass page-card">

        <div class="page-title">
            Signal History
        </div>

        <div class="page-subtitle">
            Track your generated signals
        </div>

        <div class="history-item">

            <div class="history-left">
                <strong>EUR/USD</strong>
                <span>BUY • 30 SEC</span>
            </div>

            <div class="history-win">
                DEMO
            </div>

        </div>

        <div class="history-item">

            <div class="history-left">
                <strong>GBP/USD</strong>
                <span>SELL • 1 MIN</span>
            </div>

            <div class="history-loss">
                DEMO
            </div>

        </div>

        <div class="history-item">

            <div class="history-left">
                <strong>XAU/USD</strong>
                <span>BUY • 1 MIN</span>
            </div>

            <div class="history-win">
                DEMO
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# LEARN PAGE
# ============================================================

elif st.session_state.page == "Learn":

    st.markdown("""
    <div class="glass page-card">

        <div class="page-title">
            Learn
        </div>

        <div class="page-subtitle">
            How the XIGA analysis engine will work
        </div>

        <div class="profile-row">
            📊 Market Trend
            <span>›</span>
        </div>

        <div class="profile-row">
            📈 Technical Indicators
            <span>›</span>
        </div>

        <div class="profile-row">
            🎯 Signal Filtering
            <span>›</span>
        </div>

        <div class="profile-row">
            📚 Performance Tracking
            <span>›</span>
        </div>

        <div class="profile-row">
            🧠 AI Confirmation
            <span>›</span>
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# PROFILE PAGE
# ============================================================

elif st.session_state.page == "Profile":

    st.markdown("""
    <div class="glass page-card">

        <div style="
            display:flex;
            align-items:center;
            gap:15px;
            padding:5px 0 18px;
        ">

            <div style="
                width:60px;
                height:60px;
                border-radius:50%;
                display:flex;
                align-items:center;
                justify-content:center;
                background:#102b45;
                border:1px solid #24658e;
                font-size:28px;
            ">
                👤
            </div>

            <div>

                <div style="
                    font-size:18px;
                    font-weight:900;
                ">
                    XIGA Trader
                </div>

                <div style="
                    color:#29f5a4;
                    font-size:10px;
                    margin-top:4px;
                ">
                    👑 FREE PLAN
                </div>

            </div>

        </div>

        <div class="profile-row">
            👑 Upgrade to Pro
            <span>›</span>
        </div>

        <div class="profile-row">
            ⚙ Settings
            <span>›</span>
        </div>

        <div class="profile-row">
            🔔 Notifications
            <span>›</span>
        </div>

        <div class="profile-row">
            🔒 Security
            <span>›</span>
        </div>

        <div class="profile-row">
            ❓ Help & Support
            <span>›</span>
        </div>

        <div class="profile-row">
            ℹ About XIGA
            <span>›</span>
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer-text">
    🔒 SECURE &nbsp; • &nbsp;
    XIGA AI &nbsp; • &nbsp;
    v3.0
</div>
""", unsafe_allow_html=True)
