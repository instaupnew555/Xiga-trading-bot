import streamlit as st
import requests
from datetime import datetime, timezone
import time

# ============================================================
# XIGA TRADING BOT
# Live market analysis + automatic WIN/LOSS tracking
# Data source: Twelve Data
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

defaults = {
    "history": [],
    "signals": 0,
    "wins": 0,
    "losses": 0,
    "result": None,
    "page": "Trade",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# MARKET LIST
# Only intervals supported by Twelve Data are displayed.
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

TIMEFRAMES = {
    "1 MIN": "1min",
    "5 MIN": "5min",
}


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 50% -10%, rgba(0, 255, 153, 0.10), transparent 35%),
        linear-gradient(180deg, #07111f 0%, #030914 100%);
    color: #ffffff;
}

.block-container {
    max-width: 470px;
    padding-top: 0.8rem;
    padding-bottom: 2rem;
}

/* Hide default Streamlit decoration */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* Main header */
.xiga-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 2px 20px 2px;
}

.xiga-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}

.xiga-logo {
    width: 42px;
    height: 42px;
    border-radius: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(145deg, #0c2433, #07151f);
    border: 1px solid rgba(0,255,153,0.30);
    box-shadow: 0 0 25px rgba(0,255,153,0.10);
    color: #00ff99;
    font-size: 21px;
    font-weight: 800;
}

.xiga-name {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 0.5px;
}

.xiga-subtitle {
    font-size: 9px;
    color: #78909c;
    letter-spacing: 2px;
    margin-top: 1px;
}

.pro-badge {
    background: rgba(0,255,153,0.10);
    color: #00ff99;
    border: 1px solid rgba(0,255,153,0.28);
    padding: 6px 10px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 800;
}

/* Section titles */
.section-title {
    color: #78909c;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.7px;
    text-transform: uppercase;
    margin: 5px 0 7px 2px;
}

/* Select boxes */
div[data-baseweb="select"] > div {
    background: #091522 !important;
    border: 1px solid #142b3b !important;
    border-radius: 12px !important;
    min-height: 46px;
}

div[data-baseweb="select"] span {
    color: #ffffff !important;
}

div[data-baseweb="select"] svg {
    fill: #00ff99 !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 13px;
    min-height: 48px;
    border: 1px solid rgba(0,255,153,0.30);
    background: linear-gradient(
        135deg,
        rgba(0,255,153,0.18),
        rgba(0,160,100,0.10)
    );
    color: #00ff99;
    font-weight: 800;
    letter-spacing: 0.5px;
    box-shadow: 0 0 25px rgba(0,255,153,0.06);
    transition: 0.2s ease;
}

.stButton > button:hover {
    border-color: rgba(0,255,153,0.60);
    background: linear-gradient(
        135deg,
        rgba(0,255,153,0.24),
        rgba(0,160,100,0.15)
    );
}

/* Signal card */
.signal-card {
    margin-top: 18px;
    padding: 20px 16px 18px 16px;
    border-radius: 22px;
    background:
        radial-gradient(circle at 50% 0%, rgba(0,255,153,0.08), transparent 42%),
        linear-gradient(180deg, #0a1825 0%, #07111b 100%);
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
    align-items: center;
    justify-content: center;
    flex-direction: column;
    position: relative;
}

.signal-call {
    border: 2px solid #00ff99;
    background: radial-gradient(
        circle,
        rgba(0,255,153,0.16),
        rgba(0,255,153,0.02) 65%,
        transparent 70%
    );
    box-shadow:
        0 0 30px rgba(0,255,153,0.15),
        inset 0 0 30px rgba(0,255,153,0.08);
}

.signal-put {
    border: 2px solid #ff466e;
    background: radial-gradient(
        circle,
        rgba(255,70,110,0.16),
        rgba(255,70,110,0.02) 65%,
        transparent 70%
    );
    box-shadow:
        0 0 30px rgba(255,70,110,0.15),
        inset 0 0 30px rgba(255,70,110,0.08);
}

.signal-neutral {
    border: 2px solid #6f8190;
    background: radial-gradient(
        circle,
        rgba(111,129,144,0.15),
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
    margin-top: 3px;
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
    color: #ffffff;
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

.pending-status {
    color: #f5c542;
    background: rgba(245,197,66,0.06);
    border-color: rgba(245,197,66,0.15);
}

.loss-status {
    color: #ff466e;
    background: rgba(255,70,110,0.06);
    border-color: rgba(255,70,110,0.15);
}

/* Result cards */
.result-win {
    color: #00ff99;
}

.result-loss {
    color: #ff466e;
}

.result-pending {
    color: #f5c542;
}

/* History */
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

/* Information boxes */
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
    color: #ffffff;
}

/* Bottom nav */
.nav-spacer {
    height: 15px;
}

.footer {
    text-align: center;
    color: #41515c;
    font-size: 8px;
    line-height: 1.7;
    margin-top: 25px;
    padding-bottom: 10px;
}

.small-note {
    color: #5d7180;
    font-size: 9px;
    text-align: center;
    margin-top: 8px;
    line-height: 1.5;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.65rem;
}

</style>
""",
    unsafe_allow_html=True
)


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
# TWELVE DATA
# ============================================================

def get_candles(symbol, interval="1min", outputsize=100):
    """
    Returns candles sorted oldest -> newest.

    Twelve Data returns newest -> oldest.
    """

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
        "timezone": "UTC",
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
            message = data.get("message", "Unknown Twelve Data error.")
            return None, message

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
                    "close": float(item["close"]),
                    "volume": float(item.get("volume", 0) or 0),
                })
            except Exception:
                continue

        candles.sort(key=lambda x: x["datetime"])

        if len(candles) < 60:
            return None, "Not enough market candles returned."

        return candles, None

    except requests.exceptions.Timeout:
        return None, "Market data request timed out."

    except requests.exceptions.RequestException as e:
        return None, f"Network error: {str(e)}"

    except Exception as e:
        return None, f"Unexpected API error: {str(e)}"


# ============================================================
# INDICATORS
# ============================================================

def ema(values, period):
    if len(values) < period:
        return None

    multiplier = 2 / (period + 1)

    ema_value = sum(values[:period]) / period

    for price in values[period:]:
        ema_value = (
            (price - ema_value) * multiplier
        ) + ema_value

    return ema_value


def rsi(values, period=14):
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
        avg_gain = ((avg_gain * (period - 1)) + gains[i]) / period
        avg_loss = ((avg_loss * (period - 1)) + losses[i]) / period

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))


def macd(values):
    if len(values) < 35:
        return None, None

    ema12 = ema(values, 12)
    ema26 = ema(values, 26)

    if ema12 is None or ema26 is None:
        return None, None

    return ema12 - ema26, ema26


# ============================================================
# MARKET ANALYSIS
# ============================================================

def analyze_market(symbol, timeframe):
    interval = TIMEFRAMES.get(timeframe)

    if interval not in ["1min", "5min"]:
        return {
            "success": False,
            "error": "This timeframe is not supported."
        }

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

    if not candles or len(candles) < 60:
        return {
            "success": False,
            "error": "Not enough market data."
        }

    # --------------------------------------------------------
    # IMPORTANT:
    # The newest candle may still be forming.
    # Use the previous candle as the signal candle.
    # --------------------------------------------------------

    signal_candle = candles[-2]

    closes = [
        c["close"]
        for c in candles[:-1]
    ]

    price = signal_candle["close"]

    ema9 = ema(closes, 9)
    ema21 = ema(closes, 21)
    ema50 = ema(closes, 50)
    rsi_value = rsi(closes, 14)
    macd_value, _ = macd(closes)

    score = 0

    # EMA 9 vs EMA 21
    if ema9 is not None and ema21 is not None:
        if ema9 > ema21:
            score += 1
        elif ema9 < ema21:
            score -= 1

    # EMA 21 vs EMA 50
    if ema21 is not None and ema50 is not None:
        if ema21 > ema50:
            score += 1
        elif ema21 < ema50:
            score -= 1

    # Price vs EMA21
    if ema21 is not None:
        if price > ema21:
            score += 1
        elif price < ema21:
            score -= 1

    # RSI
    if rsi_value is not None:
        if rsi_value >= 55:
            score += 1
        elif rsi_value <= 45:
            score -= 1

    # MACD
    if macd_value is not None:
        if macd_value > 0:
            score += 1
        elif macd_value < 0:
            score -= 1

    # Momentum
    if len(closes) >= 6:
        momentum = closes[-1] - closes[-6]

        if momentum > 0:
            score += 1
        elif momentum < 0:
            score -= 1

    # --------------------------------------------------------
    # SIGNAL DECISION
    # --------------------------------------------------------

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
        "candle_time": signal_candle["datetime"],
        "rsi": rsi_value,
        "ema9": ema9,
        "ema21": ema21,
        "ema50": ema50,
        "macd": macd_value,
    }


# ============================================================
# PRICE FORMATTING
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

def get_win_rate():
    wins = st.session_state.wins
    losses = st.session_state.losses

    total = wins + losses

    if total == 0:
        return "—"

    return f"{(wins / total) * 100:.1f}%"


# ============================================================
# OUTCOME RESOLUTION
# ============================================================

def resolve_pending_signals():
    """
    Resolve pending signals using completed candles only.

    For a signal created on candle T:
      - T+1 may still be forming
      - once T+2 exists, T+1 is completed
      - compare entry price against T+1 close

    This prevents using an unfinished candle as the result.
    """

    pending = [
        item
        for item in st.session_state.history
        if item.get("status") == "PENDING"
    ]

    if not pending:
        return False

    changed = False

    # Group requests by symbol/timeframe
    grouped = {}

    for item in pending:
        key = (
            item.get("symbol"),
            item.get("interval")
        )

        if key not in grouped:
            grouped[key] = []

        grouped[key].append(item)

    for (symbol, interval), signals in grouped.items():

        candles, error = get_candles(
            symbol,
            interval,
            20
        )

        if error or not candles:
            continue

        for signal_item in signals:

            entry_time = signal_item.get("entry_candle_time")

            if not entry_time:
                continue

            newer = [
                candle
                for candle in candles
                if candle["datetime"] > entry_time
            ]

            # We need at least TWO newer candles.
            # The first newer candle is then completed.
            if len(newer) < 2:
                continue

            result_candle = newer[0]

            result_price = result_candle["close"]
            entry_price = signal_item["entry_price"]

            direction = signal_item["signal"]

            if direction == "CALL":

                if result_price > entry_price:
                    result = "WIN"
                elif result_price < entry_price:
                    result = "LOSS"
                else:
                    continue

            elif direction == "PUT":

                if result_price < entry_price:
                    result = "WIN"
                elif result_price > entry_price:
                    result = "LOSS"
                else:
                    continue

            else:
                continue

            signal_item["status"] = result
            signal_item["result_price"] = result_price
            signal_item["result_candle_time"] = result_candle["datetime"]
            signal_item["checked_at"] = datetime.now(
                timezone.utc
            ).strftime("%Y-%m-%d %H:%M:%S UTC")

            if result == "WIN":
                st.session_state.wins += 1
            else:
                st.session_state.losses += 1

            changed = True

    return changed


# ============================================================
# AUTOMATIC MONITOR
# ============================================================

@st.fragment(run_every="15s")
def automatic_monitor():

    # Only perform API work when there are pending signals.
    has_pending = any(
        item.get("status") == "PENDING"
        for item in st.session_state.history
    )

    if not has_pending:
        return

    changed = resolve_pending_signals()

    # Refresh the entire UI only when an actual result changes.
    if changed:
        st.rerun()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="xiga-header">

    <div class="xiga-brand">
        <div class="xiga-logo">⚡</div>

        <div>
            <div class="xiga-name">XIGA</div>
            <div class="xiga-subtitle">TRADING INTELLIGENCE</div>
        </div>
    </div>

    <div class="pro-badge">PRO</div>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# NAVIGATION
# ============================================================

nav1, nav2, nav3, nav4 = st.columns(4)

with nav1:
    if st.button("Trade", key="nav_trade"):
        st.session_state.page = "Trade"

with nav2:
    if st.button("History", key="nav_history"):
        st.session_state.page = "History"

with nav3:
    if st.button("Learn", key="nav_learn"):
        st.session_state.page = "Learn"

with nav4:
    if st.button("Profile", key="nav_profile"):
        st.session_state.page = "Profile"


# ============================================================
# TRADE PAGE
# ============================================================

if st.session_state.page == "Trade":

    st.markdown(
        '<div class="section-title">MARKET</div>',
        unsafe_allow_html=True
    )

    category = st.selectbox(
        "Category",
        list(ASSETS.keys()),
        key="category",
        label_visibility="collapsed"
    )

    display_asset = st.selectbox(
        "Asset",
        list(ASSETS[category].keys()),
        key="asset",
        label_visibility="collapsed"
    )

    symbol = ASSETS[category][display_asset]

    st.markdown(
        '<div class="section-title" style="margin-top:8px;">TIMEFRAME</div>',
        unsafe_allow_html=True
    )

    timeframe = st.selectbox(
        "Timeframe",
        list(TIMEFRAMES.keys()),
        index=0,
        key="timeframe",
        label_visibility="collapsed"
    )

    # --------------------------------------------------------
    # ANALYZE BUTTON
    # --------------------------------------------------------

    analyze_clicked = st.button(
        "⚡ ANALYZE MARKET",
        key="analyze_button",
        use_container_width=True
    )

    if analyze_clicked:

        with st.spinner("Analyzing live market data..."):

            analysis = analyze_market(
                symbol,
                timeframe
            )

        if not analysis["success"]:

            st.error(
                f"API ERROR: {analysis['error']}"
            )

        else:

            st.session_state.result = analysis

            # ------------------------------------------------
            # Store only real CALL/PUT signals.
            # NO TRADE is not counted.
            # ------------------------------------------------

            if analysis["signal"] in ["CALL", "PUT"]:

                signal_record = {
                    "id": time.time_ns(),
                    "time": datetime.now(
                        timezone.utc
                    ).strftime("%Y-%m-%d %H:%M:%S UTC"),

                    "asset": display_asset,
                    "symbol": symbol,

                    "timeframe": timeframe,
                    "interval": TIMEFRAMES[timeframe],

                    "signal": analysis["signal"],
                    "strength": analysis["strength"],
                    "score": analysis["score"],

                    "entry_price": analysis["price"],
                    "price": analysis["price"],

                    "entry_candle_time": analysis["candle_time"],

                    "status": "PENDING",

                    "result_price": None,
                    "result_candle_time": None,
                    "checked_at": None,
                }

                st.session_state.history.insert(
                    0,
                    signal_record
                )

                st.session_state.signals += 1

            else:
                # NO TRADE is displayed but not added
                # to the WIN/LOSS history.
                pass


    # --------------------------------------------------------
    # SIGNAL DISPLAY
    # --------------------------------------------------------

    result = st.session_state.result

    if result:

        signal = result.get("signal", "NO TRADE")
        strength = result.get("strength", 0)
        score = result.get("score", 0)
        price = result.get("price")

        if signal == "CALL":
            card_class = "signal-call"
            arrow = "↑"
            title = "CALL"

        elif signal == "PUT":
            card_class = "signal-put"
            arrow = "↓"
            title = "PUT"

        else:
            card_class = "signal-neutral"
            arrow = "•"
            title = "NO TRADE"

        # Find latest pending signal belonging to this analysis.
        pending_for_current = None

        for item in st.session_state.history:
            if (
                item.get("symbol") == symbol
                and item.get("timeframe") == timeframe
                and item.get("status") == "PENDING"
            ):
                pending_for_current = item
                break

        if signal in ["CALL", "PUT"] and pending_for_current:
            status_text = "● TRACKING RESULT"
            status_class = "pending-status"
        elif signal in ["CALL", "PUT"]:
            status_text = "● SIGNAL COMPLETED"
            status_class = ""
        else:
            status_text = "● WAITING FOR CONFIRMATION"
            status_class = "pending-status"

        st.markdown(
            f"""
<div class="signal-card">

    <div class="signal-label">XIGA AI SIGNAL</div>

    <div class="signal-circle {card_class}">
        <div class="signal-arrow">{arrow}</div>
        <div class="signal-word">{title}</div>
    </div>

    <div class="asset-name">{display_asset}</div>

    <div class="direction">
        {result.get("direction", "WAIT")}
    </div>

    <div class="stats-row">

        <div class="stat-box">
            <div class="stat-title">STRENGTH</div>
            <div class="stat-value">
                {strength}/5
            </div>
        </div>

        <div class="stat-box">
            <div class="stat-title">WIN RATE</div>
            <div class="stat-value">
                {get_win_rate()}
            </div>
        </div>

        <div class="stat-box">
            <div class="stat-title">PRICE</div>
            <div class="stat-value" style="font-size:13px;">
                {format_price(price)}
            </div>
        </div>

    </div>

    <div class="ai-status {status_class}">
        {status_text}
    </div>

</div>
""",
            unsafe_allow_html=True
        )

        if signal == "CALL":

            st.markdown(
                f"""
<div class="small-note">
    Bullish confirmation detected. Score: +{score}.
    Signal is being tracked using completed market candles.
</div>
""",
                unsafe_allow_html=True
            )

        elif signal == "PUT":

            st.markdown(
                f"""
<div class="small-note">
    Bearish confirmation detected. Score: {score}.
    Signal is being tracked using completed market candles.
</div>
""",
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
<div class="small-note">
    Market conditions are mixed. Score: {score}.
    XIGA is avoiding a low-confidence trade.
</div>
""",
                unsafe_allow_html=True
            )

    else:

        st.markdown(
            """
<div class="signal-card">

    <div class="signal-label">XIGA AI SIGNAL</div>

    <div class="signal-circle signal-neutral">
        <div class="signal-arrow">•</div>
        <div class="signal-word">READY</div>
    </div>

    <div class="asset-name">Select a Market</div>

    <div class="direction">
        Press ANALYZE MARKET to generate a signal
    </div>

    <div class="stats-row">

        <div class="stat-box">
            <div class="stat-title">STRENGTH</div>
            <div class="stat-value">—</div>
        </div>

        <div class="stat-box">
            <div class="stat-title">WIN RATE</div>
            <div class="stat-value">
                {get_win_rate()}
            </div>
        </div>

        <div class="stat-box">
            <div class="stat-title">PRICE</div>
            <div class="stat-value">—</div>
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
# HISTORY PAGE
# ============================================================

elif st.session_state.page == "History":

    st.markdown(
        '<div class="section-title">TRADING HISTORY</div>',
        unsafe_allow_html=True
    )

    total = st.session_state.wins + st.session_state.losses

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Signals",
            st.session_state.signals
        )

    with col2:
        st.metric(
            "Wins",
            st.session_state.wins
        )

    with col3:
        st.metric(
            "Losses",
            st.session_state.losses
        )

    st.markdown(
        f"""
<div class="info-box" style="text-align:center;">
    <strong>Historical Win Rate</strong><br>
    <span style="font-size:25px;color:#00ff99;font-weight:800;">
        {get_win_rate()}
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
<div class="info-box" style="text-align:center;">
    No signals yet.<br>
    Analyze a market to create your first signal.
</div>
""",
            unsafe_allow_html=True
        )

    else:

        for item in st.session_state.history:

            status = item.get("status", "PENDING")

            if status == "WIN":
                status_class = "win-text"
                status_text = "WIN"

            elif status == "LOSS":
                status_class = "loss-text"
                status_text = "LOSS"

            else:
                status_class = "pending-text"
                status_text = "PENDING"

            entry_price = format_price(
                item.get("entry_price")
            )

            result_price = item.get("result_price")

            if result_price is not None:
                result_price_text = format_price(
                    result_price
                )
            else:
                result_price_text = "—"

            st.markdown(
                f"""
<div class="history-card">

    <div class="history-top">

        <div class="history-asset">
            {item.get("asset", "Unknown")}
        </div>

        <div class="{status_class}">
            {status_text}
        </div>

    </div>

    <div class="history-bottom">

        <span>
            {item.get("signal", "—")}
            &nbsp;•&nbsp;
            {item.get("timeframe", "—")}
        </span>

        <span>
            Strength {item.get("strength", "—")}/5
        </span>

    </div>

    <div class="history-bottom">

        <span>
            Entry: {entry_price}
        </span>

        <span>
            Result: {result_price_text}
        </span>

    </div>

    <div class="history-time" style="margin-top:8px;">
        {item.get("time", "")}
    </div>

</div>
""",
                unsafe_allow_html=True
            )


# ============================================================
# LEARN PAGE
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
Choose a supported asset such as EUR/USD, GBP/USD,
Bitcoin, Gold or a supported stock.

<br><br>

<strong>2. Select a timeframe</strong><br>
XIGA currently supports 1 MIN and 5 MIN.
Unsupported second-based timeframes have been removed.

<br><br>

<strong>3. Analyze the market</strong><br>
XIGA evaluates several technical conditions including
EMA trend, RSI, MACD and recent momentum.

<br><br>

<strong>4. Receive a signal</strong><br>
The result can be CALL, PUT or NO TRADE.

<br><br>

<strong>5. Automatic result tracking</strong><br>
After a CALL or PUT signal is created, XIGA waits for
the appropriate completed candle and then records the
result as WIN or LOSS.

<br><br>

<strong>6. Win rate</strong><br>
The displayed win rate uses only actual completed
signals. Pending signals are not included.

</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="info-box">

<strong>Important</strong><br><br>

XIGA is a market-analysis assistant. It does not
automatically place trades in Pocket Option.

Market data is supplied by Twelve Data and may differ
from Pocket Option pricing, particularly for OTC assets.

Never treat a signal as a guarantee of profit.

</div>
""",
        unsafe_allow_html=True
    )


# ============================================================
# PROFILE PAGE
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
AI-assisted market analysis interface.

<br><br>

<strong>Total Signals</strong><br>
{st.session_state.signals}

<br><br>

<strong>Completed Wins</strong><br>
{st.session_state.wins}

<br><br>

<strong>Completed Losses</strong><br>
{st.session_state.losses}

<br><br>

<strong>Historical Win Rate</strong><br>
{get_win_rate()}

<br><br>

<strong>Supported Timeframes</strong><br>
1 MIN<br>
5 MIN

</div>
""",
        unsafe_allow_html=True
    )


# ============================================================
# AUTOMATIC RESULT MONITOR
# Must be called during every full app execution.
# ============================================================

automatic_monitor()


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
