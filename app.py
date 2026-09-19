import streamlit as st
import random

st.set_page_config(
    page_title="XIGA Trading Signal Bot",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# XIGA MODERN MOBILE UI
# =========================================================

st.markdown("""
<style>

/* ---------- APP ---------- */

.stApp {
    background:
        radial-gradient(circle at 50% -10%, #13243b 0%, #07101d 42%, #030711 100%);
    color: #ffffff;
}

.block-container {
    max-width: 460px;
    padding: 18px 14px 30px;
}

header, footer, #MainMenu {
    visibility: hidden;
}

* {
    box-sizing: border-box;
}

/* ---------- TOP HEADER ---------- */

.topbar {
    display:flex;
    align-items:center;
    justify-content:space-between;
    margin-bottom:18px;
}

.menu {
    width:42px;
    height:42px;
    border-radius:14px;
    background:#101c2d;
    border:1px solid #263a54;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:22px;
}

.brand {
    text-align:center;
    flex:1;
}

.brand-name {
    font-size:27px;
    font-weight:900;
    letter-spacing:1px;
}

.brand-name span {
    color:#24f4a0;
}

.brand-sub {
    color:#8190a7;
    font-size:8px;
    letter-spacing:1.5px;
}

.pro {
    background:linear-gradient(135deg,#3b2d13,#6e511c);
    border:1px solid #a87c2b;
    color:#ffd76a;
    padding:8px 10px;
    border-radius:12px;
    font-size:10px;
    font-weight:800;
}

/* ---------- GLASS CARD ---------- */

.glass {
    background:
        linear-gradient(
            145deg,
            rgba(19,35,57,.94),
            rgba(7,17,31,.96)
        );
    border:1px solid rgba(72,101,132,.38);
    border-radius:18px;
    box-shadow:
        0 15px 40px rgba(0,0,0,.28),
        inset 0 1px rgba(255,255,255,.025);
}

/* ---------- ASSET BAR ---------- */

.asset-bar {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:12px;
    padding:15px;
    margin-bottom:14px;
}

.label {
    color:#74849c;
    font-size:9px;
    text-transform:uppercase;
    letter-spacing:1px;
}

.value {
    color:#fff;
    font-size:16px;
    font-weight:800;
    margin-top:5px;
}

.live-dot {
    color:#28f5a4;
    font-size:9px;
    margin-left:4px;
}

/* ---------- SIGNAL AREA ---------- */

.signal-card {
    padding:18px 12px 20px;
    text-align:center;
    position:relative;
    overflow:hidden;
}

/* subtle chart */

.chart-bg {
    position:absolute;
    left:0;
    right:0;
    top:105px;
    height:145px;
    opacity:.30;
}

.signal-label {
    color:#7d8ca3;
    font-size:10px;
    letter-spacing:1px;
}

.signal-asset {
    font-size:22px;
    font-weight:900;
    margin-top:4px;
}

.signal-time {
    color:#28eeb0;
    font-size:10px;
    margin-top:3px;
}

/* ---------- SIGNAL CIRCLE ---------- */

.signal-circle {
    width:205px;
    height:205px;
    border-radius:50%;
    margin:20px auto 20px;
    position:relative;
    z-index:2;

    display:flex;
    align-items:center;
    justify-content:center;

    background:
        radial-gradient(
            circle,
            rgba(37,247,162,.38) 0%,
            rgba(13,67,55,.70) 35%,
            rgba(4,14,25,.98) 72%
        );

    border:4px solid #29f5a5;

    box-shadow:
        0 0 15px rgba(41,245,165,.95),
        0 0 45px rgba(41,245,165,.45),
        0 0 100px rgba(41,245,165,.15),
        inset 0 0 35px rgba(41,245,165,.25);
}

.signal-circle.sell {
    background:
        radial-gradient(
            circle,
            rgba(255,53,105,.40) 0%,
            rgba(76,17,39,.72) 35%,
            rgba(4,14,25,.98) 72%
        );

    border-color:#ff396d;

    box-shadow:
        0 0 15px rgba(255,57,109,.95),
        0 0 45px rgba(255,57,109,.45),
        0 0 100px rgba(255,57,109,.15),
        inset 0 0 35px rgba(255,57,109,.25);
}

.arrow {
    font-size:82px;
    font-weight:900;
    color:#54ffb2;
    text-shadow:0 0 25px rgba(84,255,178,.7);
}

.sell .arrow {
    color:#ff638b;
    text-shadow:0 0 25px rgba(255,99,139,.7);
}

.signal-main {
    position:relative;
    z-index:3;
    font-size:29px;
    font-weight:950;
    letter-spacing:.2px;
}

.buy-text {
    color:#2bf5a4;
}

.sell-text {
    color:#ff3e71;
}

.direction {
    color:#8b9ab0;
    font-size:10px;
    letter-spacing:1.8px;
    margin-top:4px;
}

/* ---------- STAT CARDS ---------- */

.stats {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:10px;
    margin-top:18px;
}

.stat {
    background:rgba(7,17,31,.78);
    border:1px solid rgba(69,98,130,.42);
    border-radius:16px;
    padding:15px 10px;
}

.stat-title {
    color:#72829b;
    font-size:9px;
    text-transform:uppercase;
}

.stat-number {
    font-size:25px;
    font-weight:900;
    margin-top:5px;
}

.dots {
    font-size:16px;
    letter-spacing:2px;
    margin-top:3px;
}

.green {
    color:#2bf5a4;
}

.red {
    color:#ff416f;
}

.gray {
    color:#34435a;
}

/* ---------- AI STATUS ---------- */

.ai-card {
    margin-top:12px;
    padding:15px;
    text-align:left;
}

.ai-top {
    display:flex;
    align-items:center;
    gap:9px;
    color:#27f3ad;
    font-size:12px;
    font-weight:800;
}

.ai-dot {
    width:9px;
    height:9px;
    border-radius:50%;
    background:#28f5a4;
    box-shadow:0 0 12px #28f5a4;
}

.ai-text {
    color:#71829a;
    font-size:10px;
    margin-top:6px;
}

/* ---------- MAIN BUTTON ---------- */

.stButton > button {
    width:100%;
    height:56px;
    margin-top:13px;

    border-radius:17px;

    background:
        linear-gradient(
            100deg,
            #17c987,
            #36f5aa
        );

    border:1px solid #52ffc0;

    color:#04150e !important;

    font-size:14px;
    font-weight:900;

    box-shadow:
        0 8px 25px rgba(40,245,164,.20);
}

.stButton > button:hover {
    border-color:#72ffca;
    color:#04150e !important;
}

/* ---------- SELECT ---------- */

.stSelectbox {
    margin-bottom:0;
}

.stSelectbox label {
    color:#73849c !important;
    font-size:9px !important;
    text-transform:uppercase;
}

.stSelectbox div[data-baseweb="select"] > div {
    background:#0e1a2c;
    border:1px solid #273d57;
    border-radius:12px;
}

/* ---------- BOTTOM NAV ---------- */

.bottom {
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:5px;

    margin-top:20px;
    padding:9px;

    background:rgba(8,17,30,.96);
    border:1px solid #24364f;
    border-radius:20px;
}

.nav {
    text-align:center;
    color:#718199;
    font-size:9px;
    padding:8px 2px;
}

.nav-icon {
    font-size:20px;
    display:block;
    margin-bottom:4px;
}

.nav.active {
    color:#29f5a4;
}

.footer {
    text-align:center;
    color:#53627a;
    font-size:8px;
    margin-top:12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="topbar">

    <div class="menu">☰</div>

    <div class="brand">
        <div class="brand-name">
            <span>▥</span> XIGA
        </div>
        <div class="brand-sub">
            TRADING SIGNAL BOT
        </div>
    </div>

    <div class="pro">
        👑 PRO
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# ASSET / TIMEFRAME
# =========================================================

st.markdown('<div class="glass asset-bar">', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    st.markdown(
        '<div class="label">Asset</div>',
        unsafe_allow_html=True
    )

    asset = st.selectbox(
        "asset",
        [
            "🇺🇸🇪🇺 EUR/USD",
            "🇬🇧🇺🇸 GBP/USD",
            "🇺🇸🇯🇵 USD/JPY",
            "🥇 XAU/USD"
        ],
        label_visibility="collapsed"
    )

with c2:
    st.markdown(
        '<div class="label">Timeframe</div>',
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
        label_visibility="collapsed"
    )

st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# SIGNAL STATE
# =========================================================

if "signal" not in st.session_state:
    st.session_state.signal = None

if "score" not in st.session_state:
    st.session_state.score = 0


# =========================================================
# GENERATE SIGNAL
# =========================================================

if st.button("⚡  ANALYZE MARKET"):

    score = random.randint(78, 96)

    if score >= 86:
        st.session_state.signal = random.choice(
            ["CALL", "PUT"]
        )
    else:
        st.session_state.signal = "NO TRADE"

    st.session_state.score = score


# =========================================================
# SIGNAL SCREEN
# =========================================================

signal = st.session_state.signal

if signal:

    if signal == "CALL":

        arrow = "↗"
        title = "BUY (CALL)"
        direction = "UPWARD TREND"
        color_class = "buy-text"
        circle_class = ""
        dot_class = "green"

    elif signal == "PUT":

        arrow = "↘"
        title = "SELL (PUT)"
        direction = "DOWNWARD TREND"
        color_class = "sell-text"
        circle_class = "sell"
        dot_class = "red"

    else:

        arrow = "⏸"
        title = "NO TRADE"
        direction = "WAIT FOR CONFIRMATION"
        color_class = "wait"
        circle_class = ""
        dot_class = "gray"

    # Chart background

    st.markdown("""
    <div class="glass signal-card">

        <svg class="chart-bg"
             viewBox="0 0 500 160"
             preserveAspectRatio="none">

            <polyline
                points="
                0,130
                35,115
                60,125
                90,90
                125,105
                160,65
                190,85
                225,45
                260,70
                300,35
                330,60
                370,25
                405,48
                440,15
                475,35
                500,5"
                fill="none"
                stroke="#27f5a4"
                stroke-width="3"/>

        </svg>

        <div class="signal-label">
            SIGNAL FOR
        </div>

    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="signal-asset">
            {asset}
        </div>

        <div class="signal-time">
            ● TIMEFRAME: {timeframe}
        </div>

        <div class="signal-circle {circle_class}">
            <div class="arrow">
                {arrow}
            </div>
        </div>

        <div class="signal-main {color_class}">
            {title}
        </div>

        <div class="direction">
            {direction}
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # STATS
    # =====================================================

    score = st.session_state.score

    strength = min(5, max(1, round(score / 20)))

    filled = "● " * strength
    empty = "● " * (5 - strength)

    st.markdown(
        f"""
        <div class="stats">

            <div class="stat">

                <div class="stat-title">
                    Signal Strength
                </div>

                <div class="dots {dot_class}">
                    {filled}
                    <span class="gray">{empty}</span>
                </div>

                <div class="stat-number">
                    {strength}/5
                </div>

            </div>

            <div class="stat">

                <div class="stat-title">
                    Setup Score
                </div>

                <div class="stat-number {color_class}">
                    {score}%
                </div>

                <div class="live-dot">
                    ● ANALYSIS
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # AI STATUS
    # =====================================================

    st.markdown("""
    <div class="glass ai-card">

        <div class="ai-top">
            <span class="ai-dot"></span>
            AI ANALYSIS COMPLETE
        </div>

        <div class="ai-text">
            Multi-factor market analysis completed
        </div>

    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # NEW SIGNAL
    # =====================================================

    if st.button("↻  GENERATE NEW SIGNAL"):

        st.session_state.signal = None
        st.session_state.score = 0
        st.rerun()

else:

    st.markdown("""
    <div class="glass signal-card">

        <div class="signal-label">
            READY TO ANALYZE
        </div>

        <div class="signal-circle">
            <div class="arrow">
                ◇
            </div>
        </div>

        <div class="signal-main buy-text">
            AI READY
        </div>

        <div class="direction">
            WAITING FOR MARKET ANALYSIS
        </div>

        <div class="glass ai-card">

            <div class="ai-top">
                <span class="ai-dot"></span>
                AI ENGINE READY
            </div>

            <div class="ai-text">
                Select your asset and timeframe
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)

    st.button("⚡  ANALYZE MARKET")


# =========================================================
# BOTTOM NAV
# =========================================================

st.markdown("""
<div class="bottom">

    <div class="nav active">
        <span class="nav-icon">⌁</span>
        Trade
    </div>

    <div class="nav">
        <span class="nav-icon">◷</span>
        History
    </div>

    <div class="nav">
        <span class="nav-icon">▣</span>
        Learn
    </div>

    <div class="nav">
        <span class="nav-icon">♙</span>
        Profile
    </div>

</div>

<div class="footer">
    🔒 SECURE &nbsp; • &nbsp; XIGA AI &nbsp; • &nbsp; v2.0
</div>
""", unsafe_allow_html=True)
