import streamlit as st
import requests
from datetime import datetime, timezone
import time

# ============================================================
# XIGA TRADING BOT
# ============================================================

st.set_page_config(
    page_title="XIGA Trading Bot",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# SESSION STATE
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "signals" not in st.session_state:
    st.session_state.signals = 0

if "wins" not in st.session_state:
    st.session_state.wins = 0

if "losses" not in st.session_state:
    st.session_state.losses = 0

if "result" not in st.session_state:
    st.session_state.result = None

if "page" not in st.session_state:
    st.session_state.page = "Trade"


# ============================================================
# MARKET LIST
# ============================================================

ASSETS = {
    "Forex": {
        "EUR/USD": "EUR/USD",
        "GBP/USD": "GBP/USD",
        "USD/JPY": "USD/JPY",
        "USD/CHF": "USD/CHF",
        "AUD/USD": "AUD/USD",
        "USD/CAD": "USD/CAD",
        "NZD/USD": "NZD/USD",
        "EUR/GBP": "EUR/GBP",
        "EUR/JPY": "EUR/JPY",
        "GBP/JPY": "GBP/JPY",
    },

    "Stocks": {
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "Amazon": "AMZN",
        "NVIDIA": "NVDA",
        "Tesla": "TSLA",
        "Meta": "META",
        "Google": "GOOGL",
        "Netflix": "NFLX",
    },

    "Crypto": {
        "Bitcoin / USD": "BTC/USD",
        "Ethereum / USD": "ETH/USD",
        "Solana / USD": "SOL/USD",
        "XRP / USD": "XRP/USD",
        "Dogecoin / USD": "DOGE/USD",
    },

    "Commodities": {
        "Gold / USD": "XAU/USD",
        "Silver / USD": "XAG/USD",
    },
}

# IMPORTANT:
# Only timeframes actually supported by this application.
TIMEFRAMES = {
    "1 MIN": "1min",
    "5 MIN": "5min",
}


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

.stApp {
    background:
        radial-gradient(
            circle at 50% -10%,
            rgba(0,255,153,0.10),
            transparent 35%
        ),
        linear-gradient(
            180deg,
            #07111f 0%,
            #030914 100%
        );
    color: white;
}

.block-container {
    max-width: 470px !important;
    padding-top: 0.7rem !important;
    padding-bottom: 2rem !important;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* HEADER */

.xiga-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    margin-bottom: 18px;
}

.xiga-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}

.xiga-logo {
    width: 44px;
    height: 44px;
    border-radius: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(
        145deg,
        #0c2433,
        #07151f
    );
    border: 1px solid rgba(0,255,153,0.30);
    box-shadow:
        0 0 25px rgba(0,255,153,0.10);
    font-size: 22px;
}

.xiga-name {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 0.5px;
    color: white;
}

.xiga-subtitle {
    font-size: 8px;
    color: #78909c;
    letter-spacing: 2px;
    margin-top: 2px;
}

.pro-badge {
    background: rgba(0,255,153,0.10);
    color: #00ff99;
    border: 1px solid rgba(0,255,153,0.28);
    padding: 6px 11px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 800;
}

/* NAVIGATION */

.nav-container {
    display: flex;
    gap: 7px;
    margin-bottom: 20px;
}

.nav-container .stButton > button {
    min-height: 38px !important;
    padding: 0 8px !important;
    font-size: 10px !important;
    border-radius: 10px !important;
}

/* SECTION */

.section-title {
    color: #78909c;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.7px;
    text-transform: uppercase;
    margin: 8px 0 7px 2px;
}

/* SELECT */

div[data-baseweb="select"] > div {
    background: #091522 !important;
    border: 1px solid #142b3b !important;
    border-radius: 12px !important;
    min-height: 46px !important;
}

div[data-baseweb="select"] span {
    color: white !important;
}

div[data-baseweb="select"] svg {
    fill: #00ff99 !important;
}

/* BUTTON */

.stButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 13px;
    border: 1px solid rgba(0,255,153,0.30);
    background:
        linear-gradient(
            135deg,
            rgba(0,255,153,0.18),
            rgba(0,160,100,0.10)
        );
    color: #00ff99;
    font-weight: 800;
    letter-spacing: 0.5px;
    box-shadow:
        0 0 25px rgba(0,255,153,0.06);
}

.stButton > button:hover {
    border-color: rgba(0,255,153,0.65);
    color: #00ff99;
}

/* SIGNAL CARD */

.signal-card {
    margin-top: 18px;
    padding: 20px 16px 18px 16px;
    border-radius: 22px;
    background:
        radial-gradient(
            circle at 50% 0%,
            rgba(0,255,153,0.08),
            transparent 42%
        ),
        linear-gradient(
            180deg,
            #0a1825 0%,
            #07111b 100%
        );
    border: 1px solid #173243;
    box-shadow:
        0 20px 50px rgba(0,0,0,0.28),
        inset 0 1px 0 rgba(255,255,255,0.025);
    text-align: center;
}

.signal-label {
    font-size: 9px;
    color: #78909c;
    font-weight: 700;
    letter-spacing: 2px;
}

.signal-circle {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    margin: 16px auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.signal-call {
    border: 2px solid #00ff99;
    background:
        radial-gradient(
            circle,
            rgba(0,255,153,0.16),
            transparent 70%
        );
    box-shadow:
        0 0 30px rgba(0,255,153,0.15);
}

.signal-put {
    border: 2px solid #ff466e;
    background:
        radial-gradient(
            circle,
            rgba(255,70,110,0.16),
            transparent 70%
        );
    box-shadow:
        0 0 30px rgba(255,70,110,0.15);
}

.signal-neutral {
    border: 2px solid #667785;
    background:
        radial-gradient(
            circle,
            rgba(100,120,135,0.15),
            transparent 70%
        );
}

.signal-arrow {
    font-size: 34px;
    line-height: 32px;
    font-weight: 800;
}

.signal-call .signal-arrow {
    color: #00ff99;
}

.signal-put .signal-arrow {
    color: #ff466e;
}

.signal-neutral .signal-arrow {
    color: #9aa8b2;
}

.signal-word {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-top: 5px;
}

.signal-call .signal-word {
    color: #00ff99;
}

.signal-put .signal-word {
    color: #ff466e;
}

.signal-neutral .signal-word {
    color: #9aa8b2;
}

.asset-name {
    font-size: 20px;
    font-weight: 800;
}

.direction {
    font-size: 11px;
    color: #8ea0ad;
    margin-top: 4px;
}

.stats-row {
    display: flex;
    gap: 8px;
    margin-top: 18px;
}

.stat-box {
    flex: 1;
    background: #091622;
    border: 1px solid #152d3c;
    border-radius: 12px;
    padding: 12px 5px;
}

.stat-title {
    font-size: 8px;
    color: #657987;
    letter-spacing: 1px;
    font-weight: 700;
}

.stat-value {
    margin-top: 4px;
    font-size: 16px;
    font-weight: 800;
    color: white;
}

.ai-status {
    margin-top: 15px;
    padding: 10px;
    border-radius: 10px;
    background: rgba(0,255,153,0.055);
    border: 1px solid rgba(0,255,153,0.12);
    color: #00ff99;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1.2px;
}

.ai-pending {
    color: #f5c542;
    background: rgba(245,197,66,0.06);
    border-color: rgba(245,197,66,0.15);
}

.ai-loss {
    color: #ff466e;
}

/* INFO */

.info-box {
    background: #08141f;
    border: 1px solid #142c3b;
    border-radius: 14px;
    padding: 15px;
    margin-top: 10px;
    color: #9aabb6;
    font-size: 12px;
    line-height: 1.7;
}

.info-box strong {
    color: white;
}

.small-note {
    color: #5d7180;
    font-size: 9px;
    text-align: center;
    margin-top: 8px;
    line-height: 1.5;
}

/* HISTORY */

.history-card {
    background: #08141f;
    border: 1px solid #142c3b;
    border-radius: 13px;
    padding: 12px;
    margin-top: 8px;
}

.history-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.history-asset {
    font-size: 12px;
    font-weight: 800;
}

.history-time {
    font-size: 8px;
    color: #627582;
    margin-top: 7px;
}

.history-bottom {
    display: flex;
    justify-content: space-between;
    margin-top: 8px;
    font-size: 10px;
}

.win-text {
    color: #00ff99;
    font-weight: 800;
}

.loss-text {
    color: #ff466e;
    font-weight: 800;
}

.pending-text {
    color: #f5c542;
    font-weight: 800;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #41515c;
    font-size: 8px;
    line-height: 1.7;
    margin-top: 25px;
    padding-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# API KEY
# ============================================================

def get_api_key():
    try:
        key = st.secrets["TWELVE_DATA_API_KEY"]

        if not key:
            return None

        return str(key).strip()

    except Exception:
        return None


# ============================================================
# GET MARKET DATA
# ============================================================

def get_candles(symbol, interval, outputsize=100):

    api_key = get_api_key()

    if not api_key:
        return None, "Twelve Data API key is missing."

    if interval not in ["1min", "5min"]:
        return None, "Unsupported timeframe."

    url = "https://api.twelvedata.com/time_series"

    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "format": "JSON",
        "timezone": "UTC"
    }

    headers = {
        "Authorization": "apikey " + api_key
    }

    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=15
        )

        if response.status_code != 200:
            return None, f"API HTTP error: {response.status_code}"

        data = response.json()

        if data.get("status") == "error":
            return None, data.get(
                "message",
                "Twelve Data returned an error."
            )

        values = data.get("values")

        if not values:
            return None, "No market data returned."

        candles = []

        for item in values:

            try:

                candles.append({
                    "datetime": item["datetime"],
                    "open": float(item["open"]),
                    "high": float(item["high"]),
                    "low": float(item["low"]),
                    "close": float(item["close"])
                })

            except Exception:
                continue

        candles.sort(
            key=lambda x: x["datetime"]
        )

        if len(candles) < 60:
            return None, "Not enough market data."

        return candles, None

    except requests.exceptions.Timeout:
        return None, "Market data request timed out."

    except requests.exceptions.RequestException as e:
        return None, f"Network error: {e}"

    except Exception as e:
        return None, f"Unexpected error: {e}"


# ============================================================
# INDICATORS
# ============================================================

def calculate_ema(values, period):

    if len(values) < period:
        return None

    multiplier = 2 / (period + 1)

    value = sum(values[:period]) / period

    for price in values[period:]:
        value = (
            (price - value) * multiplier
        ) + value

    return value


def calculate_rsi(values, period=14):

    if len(values) < period + 1:
        return None

    gains = []
    losses = []

    for i in range(1, len(values)):

        change = values[i] - values[i - 1]

        if change > 0:
            gains.append(change)
            losses.append(0)

        else:
            gains.append(0)
            losses.append(abs(change))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(gains)):

        avg_gain = (
            ((avg_gain * (period - 1)) + gains[i])
            / period
        )

        avg_loss = (
            ((avg_loss * (period - 1)) + losses[i])
            / period
        )

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))


def calculate_macd(values):

    if len(values) < 35:
        return None

    ema12 = calculate_ema(values, 12)
    ema26 = calculate_ema(values, 26)

    if ema12 is None or ema26 is None:
        return None

    return ema12 - ema26


# ============================================================
# ANALYZE MARKET
# ============================================================

def analyze_market(symbol, timeframe):

    interval = TIMEFRAMES[timeframe]

    candles, error = get_candles(
        symbol,
        interval,
        120
    )

    if error:
        return {
            "success": False,
            "error": error
        }

    if len(candles) < 60:
        return {
            "success": False,
            "error": "Not enough candles."
        }

    # The latest candle may still be forming.
    # We analyze the previous completed candle.

    signal_candle = candles[-2]

    closed_candles = candles[:-1]

    closes = [
        candle["close"]
        for candle in closed_candles
    ]

    price = signal_candle["close"]

    ema9 = calculate_ema(closes, 9)
    ema21 = calculate_ema(closes, 21)
    ema50 = calculate_ema(closes, 50)

    rsi = calculate_rsi(closes, 14)
    macd = calculate_macd(closes)

    score = 0

    # EMA 9 / EMA 21
    if ema9 and ema21:

        if ema9 > ema21:
            score += 1

        elif ema9 < ema21:
            score -= 1

    # EMA 21 / EMA 50
    if ema21 and ema50:

        if ema21 > ema50:
            score += 1

        elif ema21 < ema50:
            score -= 1

    # Price / EMA21
    if ema21:

        if price > ema21:
            score += 1

        elif price < ema21:
            score -= 1

    # RSI
    if rsi is not None:

        if rsi >= 55:
            score += 1

        elif rsi <= 45:
            score -= 1

    # MACD
    if macd is not None:

        if macd > 0:
            score += 1

        elif macd < 0:
            score -= 1

    # Momentum
    if len(closes) >= 6:

        momentum = closes[-1] - closes[-6]

        if momentum > 0:
            score += 1

        elif momentum < 0:
            score -= 1

    # Signal
    if score >= 4:

        signal = "CALL"
        direction = "BUY / UP"

    elif score <= -4:

        signal = "PUT"
        direction = "SELL / DOWN"

    else:

        signal = "NO TRADE"
        direction = "WAIT"

    strength = min(abs(score), 5)

    return {
        "success": True,
        "signal": signal,
        "direction": direction,
        "strength": strength,
        "score": score,
        "price": price,
        "candle_time": signal_candle["datetime"]
    }


# ============================================================
# PRICE FORMAT
# ============================================================

def format_price(price):

    if price is None:
        return "—"

    try:

        price = float(price)

        if price >= 1000:
            return f"{price:,.2f}"

        if price >= 100:
            return f"{price:.2f}"

        if price >= 1:
            return f"{price:.4f}"

        return f"{price:.5f}"

    except Exception:
        return str(price)


# ============================================================
# WIN RATE
# ============================================================

def win_rate():

    total = (
        st.session_state.wins
        + st.session_state.losses
    )

    if total == 0:
        return "—"

    return (
        f"{(st.session_state.wins / total) * 100:.1f}%"
    )


# ============================================================
# RESOLVE SIGNALS
# ============================================================

def resolve_pending():

    pending = [
        item
        for item in st.session_state.history
        if item["status"] == "PENDING"
    ]

    if not pending:
        return False

    changed = False

    # Group by market/timeframe to reduce API calls.
    groups = {}

    for item in pending:

        key = (
            item["symbol"],
            item["interval"]
        )

        if key not in groups:
            groups[key] = []

        groups[key].append(item)

    for (symbol, interval), signals in groups.items():

        candles, error = get_candles(
            symbol,
            interval,
            20
        )

        if error or not candles:
            continue

        for signal in signals:

            entry_time = signal["entry_candle_time"]

            newer = [
                candle
                for candle in candles
                if candle["datetime"] > entry_time
            ]

            # We need TWO newer timestamps.
            #
            # Example:
            # Signal candle = 10:00
            # 10:01 = may be forming
            # 10:02 exists = 10:01 is now completed
            #
            # Therefore we use 10:01 as the result candle.

            if len(newer) < 2:
                continue

            result_candle = newer[0]

            entry_price = signal["entry_price"]
            result_price = result_candle["close"]

            if signal["signal"] == "CALL":

                if result_price > entry_price:
                    outcome = "WIN"

                elif result_price < entry_price:
                    outcome = "LOSS"

                else:
                    continue

            elif signal["signal"] == "PUT":

                if result_price < entry_price:
                    outcome = "WIN"

                elif result_price > entry_price:
                    outcome = "LOSS"

                else:
                    continue

            else:
                continue

            signal["status"] = outcome
            signal["result_price"] = result_price
            signal["result_candle_time"] = (
                result_candle["datetime"]
            )

            signal["checked_at"] = (
                datetime.now(timezone.utc)
                .strftime("%Y-%m-%d %H:%M:%S UTC")
            )

            if outcome == "WIN":
                st.session_state.wins += 1
            else:
                st.session_state.losses += 1

            changed = True

    return changed


# ============================================================
# AUTOMATIC MONITOR
# ============================================================

@st.fragment(run_every="15s")
def monitor():

    has_pending = any(
        item["status"] == "PENDING"
        for item in st.session_state.history
    )

    if not has_pending:
        return

    changed = resolve_pending()

    if changed:
        st.rerun()


# ============================================================
# HEADER
# ============================================================

# IMPORTANT:
# This is deliberately written as one clean HTML block
# with unsafe_allow_html=True so it cannot become a code block.

st.markdown(
    """
<div class="xiga-header">
    <div class="xiga-brand">
        <div class="xiga-logo">⚡</div>
        <div>
            <div class="xiga-name">XIGA</div>
            <div class="xiga-subtitle">
                TRADING INTELLIGENCE
            </div>
        </div>
    </div>

    <div class="pro-badge">
        PRO
    </div>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# NAVIGATION
# ============================================================

n1, n2, n3, n4 = st.columns(4)

with n1:
    if st.button("Trade", key="trade_nav"):
        st.session_state.page = "Trade"

with n2:
    if st.button("History", key="history_nav"):
        st.session_state.page = "History"

with n3:
    if st.button("Learn", key="learn_nav"):
        st.session_state.page = "Learn"

with n4:
    if st.button("Profile", key="profile_nav"):
        st.session_state.page = "Profile"


# ============================================================
# TRADE
# ============================================================

if st.session_state.page == "Trade":

    st.markdown(
        '<div class="section-title">MARKET</div>',
        unsafe_allow_html=True
    )

    category = st.selectbox(
        "Category",
        list(ASSETS.keys()),
        label_visibility="collapsed",
        key="market_category"
    )

    asset_name = st.selectbox(
        "Asset",
        list(ASSETS[category].keys()),
        label_visibility="collapsed",
        key="market_asset"
    )

    symbol = ASSETS[category][asset_name]

    st.markdown(
        '<div class="section-title">TIMEFRAME</div>',
        unsafe_allow_html=True
    )

    timeframe = st.selectbox(
        "Timeframe",
        list(TIMEFRAMES.keys()),
        label_visibility="collapsed",
        key="market_timeframe"
    )

    # --------------------------------------------------------
    # ANALYZE
    # --------------------------------------------------------

    analyze = st.button(
        "⚡ ANALYZE MARKET",
        use_container_width=True,
        key="analyze"
    )

    if analyze:

        with st.spinner("Analyzing live market data..."):

            analysis = analyze_market(
                symbol,
                timeframe
            )

        if not analysis["success"]:

            st.error(
                "API ERROR: " + analysis["error"]
            )

        else:

            st.session_state.result = analysis

            # Only CALL and PUT are saved.
            # NO TRADE does not become a fake result.

            if analysis["signal"] in [
                "CALL",
                "PUT"
            ]:

                record = {
                    "id": time.time_ns(),

                    "time": datetime.now(
                        timezone.utc
                    ).strftime(
                        "%Y-%m-%d %H:%M:%S UTC"
                    ),

                    "asset": asset_name,
                    "symbol": symbol,

                    "timeframe": timeframe,
                    "interval": TIMEFRAMES[timeframe],

                    "signal": analysis["signal"],
                    "strength": analysis["strength"],
                    "score": analysis["score"],

                    "entry_price": analysis["price"],

                    "entry_candle_time":
                        analysis["candle_time"],

                    "status": "PENDING",

                    "result_price": None,

                    "result_candle_time": None,

                    "checked_at": None
                }

                st.session_state.history.insert(
                    0,
                    record
                )

                st.session_state.signals += 1


    # --------------------------------------------------------
    # DISPLAY SIGNAL
    # --------------------------------------------------------

    result = st.session_state.result

    if result:

        signal = result["signal"]

        if signal == "CALL":

            circle = "signal-call"
            arrow = "↑"
            word = "CALL"

        elif signal == "PUT":

            circle = "signal-put"
            arrow = "↓"
            word = "PUT"

        else:

            circle = "signal-neutral"
            arrow = "•"
            word = "NO TRADE"

        current_pending = False

        if signal in ["CALL", "PUT"]:

            for item in st.session_state.history:

                if (
                    item["symbol"] == symbol
                    and item["timeframe"] == timeframe
                    and item["status"] == "PENDING"
                ):
                    current_pending = True
                    break

        if current_pending:

            ai_text = "● TRACKING RESULT"
            ai_class = "ai-pending"

        elif signal in ["CALL", "PUT"]:

            ai_text = "● RESULT COMPLETED"
            ai_class = ""

        else:

            ai_text = "● NO TRADE"
            ai_class = "ai-pending"

        st.markdown(
            f"""
<div class="signal-card">

    <div class="signal-label">
        XIGA AI SIGNAL
    </div>

    <div class="signal-circle {circle}">
        <div class="signal-arrow">
            {arrow}
        </div>

        <div class="signal-word">
            {word}
        </div>
    </div>

    <div class="asset-name">
        {asset_name}
    </div>

    <div class="direction">
        {result["direction"]}
    </div>

    <div class="stats-row">

        <div class="stat-box">
            <div class="stat-title">
                STRENGTH
            </div>

            <div class="stat-value">
                {result["strength"]}/5
            </div>
        </div>

        <div class="stat-box">
            <div class="stat-title">
                WIN RATE
            </div>

            <div class="stat-value">
                {win_rate()}
            </div>
        </div>

        <div class="stat-box">
            <div class="stat-title">
                PRICE
            </div>

            <div class="stat-value"
                 style="font-size:13px;">
                {format_price(result["price"])}
            </div>
        </div>

    </div>

    <div class="ai-status {ai_class}">
        {ai_text}
    </div>

</div>
""",
            unsafe_allow_html=True
        )

        if signal == "CALL":

            st.markdown(
                f"""
<div class="small-note">
Bullish confirmation detected.
Score: +{result["score"]}.
The signal is being tracked using completed candles.
</div>
""",
                unsafe_allow_html=True
            )

        elif signal == "PUT":

            st.markdown(
                f"""
<div class="small-note">
Bearish confirmation detected.
Score: {result["score"]}.
The signal is being tracked using completed candles.
</div>
""",
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
<div class="small-note">
Market conditions are mixed.
Score: {result["score"]}.
XIGA is avoiding a low-confidence signal.
</div>
""",
                unsafe_allow_html=True
            )

    else:

        st.markdown(
            f"""
<div class="signal-card">

    <div class="signal-label">
        XIGA AI SIGNAL
    </div>

    <div class="signal-circle signal-neutral">
        <div class="signal-arrow">•</div>

        <div class="signal-word">
            READY
        </div>
    </div>

    <div class="asset-name">
        {asset_name}
    </div>

    <div class="direction">
        Press ANALYZE MARKET
    </div>

    <div class="stats-row">

        <div class="stat-box">
            <div class="stat-title">
                STRENGTH
            </div>

            <div class="stat-value">
                —
            </div>
        </div>

        <div class="stat-box">
            <div class="stat-title">
                WIN RATE
            </div>

            <div class="stat-value">
                {win_rate()}
            </div>
        </div>

        <div class="stat-box">
            <div class="stat-title">
                PRICE
            </div>

            <div class="stat-value">
                —
            </div>
        </div>

    </div>

    <div class="ai-status">
        ● AI READY
    </div>

</div>
""",
            unsafe_allow_html=True
        )


# ============================================================
# HISTORY
# ============================================================

elif st.session_state.page == "History":

    st.markdown(
        '<div class="section-title">TRADING HISTORY</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Signals",
            st.session_state.signals
        )

    with c2:
        st.metric(
            "Wins",
            st.session_state.wins
        )

    with c3:
        st.metric(
            "Losses",
            st.session_state.losses
        )

    st.markdown(
        f"""
<div class="info-box"
     style="text-align:center;">

    <strong>Historical Win Rate</strong>

    <br>

    <span style="
        font-size:25px;
        color:#00ff99;
        font-weight:800;
    ">
        {win_rate()}
    </span>

    <br>

    <span style="font-size:9px;">
        Based only on completed WIN/LOSS signals.
    </span>

</div>
""",
        unsafe_allow_html=True
    )

    if not st.session_state.history:

        st.markdown(
            """
<div class="info-box"
     style="text-align:center;">

    No signals yet.

    <br>

    Analyze a market to create your first signal.

</div>
""",
            unsafe_allow_html=True
        )

    else:

        for item in st.session_state.history:

            status = item["status"]

            if status == "WIN":

                status_class = "win-text"

            elif status == "LOSS":

                status_class = "loss-text"

            else:

                status_class = "pending-text"

            result_price = item["result_price"]

            if result_price is None:
                result_display = "—"
            else:
                result_display = format_price(
                    result_price
                )

            st.markdown(
                f"""
<div class="history-card">

    <div class="history-top">

        <div class="history-asset">
            {item["asset"]}
        </div>

        <div class="{status_class}">
            {status}
        </div>

    </div>

    <div class="history-bottom">

        <span>
            {item["signal"]}
            •
            {item["timeframe"]}
        </span>

        <span>
            {item["strength"]}/5
        </span>

    </div>

    <div class="history-bottom">

        <span>
            Entry:
            {format_price(item["entry_price"])}
        </span>

        <span>
            Result:
            {result_display}
        </span>

    </div>

    <div class="history-time">
        {item["time"]}
    </div>

</div>
""",
                unsafe_allow_html=True
            )


# ============================================================
# LEARN
# ============================================================

elif st.session_state.page == "Learn":

    st.markdown(
        '<div class="section-title">HOW XIGA WORKS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="info-box">

<strong>1. Select a market</strong><br>
Choose a supported market such as EUR/USD,
GBP/USD, Bitcoin or Gold.

<br><br>

<strong>2. Select a timeframe</strong><br>
XIGA currently supports only 1 MIN and 5 MIN.

<br><br>

<strong>3. Analyze</strong><br>
XIGA evaluates EMA trend, RSI, MACD and
recent price momentum.

<br><br>

<strong>4. Signal</strong><br>
The result can be CALL, PUT or NO TRADE.

<br><br>

<strong>5. Automatic tracking</strong><br>
CALL and PUT signals are stored as PENDING.
XIGA checks the market automatically.

<br><br>

<strong>6. WIN / LOSS</strong><br>
After the required completed candle is available,
the signal becomes WIN or LOSS.

<br><br>

<strong>7. Win rate</strong><br>
Only completed signals are included in the
historical win rate.

</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="info-box">

<strong>Important</strong><br><br>

XIGA is a market-analysis assistant.

It does not automatically place trades.

Twelve Data market prices can differ from
Pocket Option prices, especially OTC prices.

No signal is a guarantee of profit.

</div>
""",
        unsafe_allow_html=True
    )


# ============================================================
# PROFILE
# ============================================================

elif st.session_state.page == "Profile":

    st.markdown(
        '<div class="section-title">XIGA PROFILE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
<div class="info-box">

<strong>XIGA Trading Bot</strong><br>
AI-assisted market analysis.

<br><br>

<strong>Total Signals</strong><br>
{st.session_state.signals}

<br><br>

<strong>Wins</strong><br>
{st.session_state.wins}

<br><br>

<strong>Losses</strong><br>
{st.session_state.losses}

<br><br>

<strong>Historical Win Rate</strong><br>
{win_rate()}

<br><br>

<strong>Supported Timeframes</strong><br>
1 MIN<br>
5 MIN

</div>
""",
        unsafe_allow_html=True
    )


# ============================================================
# AUTOMATIC MONITOR
# ============================================================

monitor()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">
XIGA Trading Intelligence<br>
Market analysis assistant — not an automatic trading system.<br>
All rights reserved designed by Khawaja.
</div>
""",
    unsafe_allow_html=True
)
