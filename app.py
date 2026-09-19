import streamlit as st
import requests
import time
import textwrap
from datetime import datetime, timezone


# ============================================================
# PAGE CONFIG
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

DEFAULTS = {
    "page": "Trade",
    "history": [],
    "signals": 0,
    "wins": 0,
    "losses": 0,
    "result": None,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# SUPPORTED MARKETS
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


# ONLY SUPPORTED TIMEFRAMES
TIMEFRAMES = {
    "1 MIN": "1min",
    "5 MIN": "5min",
}


# ============================================================
# SAFE HTML RENDERER
# ============================================================
# This is the important fix.
# textwrap.dedent() removes accidental indentation that can
# cause Streamlit Markdown to display HTML as plain code.
# ============================================================

def html(content):
    st.markdown(
        textwrap.dedent(content).strip(),
        unsafe_allow_html=True
    )


# ============================================================
# CSS
# ============================================================

html("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html,
body,
[class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

.stApp {
    background:
        radial-gradient(
            circle at 50% -10%,
            rgba(0,255,153,0.09),
            transparent 35%
        ),
        linear-gradient(
            180deg,
            #07121f 0%,
            #030914 100%
        );
    color: #ffffff;
}

.block-container {
    max-width: 470px !important;
    padding-top: 0.7rem !important;
    padding-bottom: 1rem !important;
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

/* =========================================================
   HEADER
   ========================================================= */

.xiga-header {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
}

.xiga-left {
    display: flex;
    align-items: center;
    gap: 11px;
}

.xiga-logo {
    width: 45px;
    height: 45px;
    border-radius: 14px;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        linear-gradient(
            145deg,
            #0d2938,
            #07141f
        );

    border: 1px solid rgba(0,255,153,0.35);

    box-shadow:
        0 0 25px rgba(0,255,153,0.10);

    font-size: 23px;
}

.xiga-name {
    color: #ffffff;
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 0.5px;
}

.xiga-subtitle {
    color: #78909c;
    font-size: 8px;
    letter-spacing: 2px;
    margin-top: 2px;
}

.pro-badge {
    color: #00ff99;
    background: rgba(0,255,153,0.08);
    border: 1px solid rgba(0,255,153,0.30);
    padding: 7px 11px;
    border-radius: 20px;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 0.5px;
}


/* =========================================================
   SECTION LABEL
   ========================================================= */

.section-title {
    color: #78909c;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 12px 0 7px 3px;
}


/* =========================================================
   SELECT BOX
   ========================================================= */

div[data-baseweb="select"] > div {
    background: #0a1522 !important;
    border: 1px solid #173142 !important;
    border-radius: 13px !important;
    min-height: 48px !important;
    box-shadow: none !important;
}

div[data-baseweb="select"] span {
    color: #ffffff !important;
}

div[data-baseweb="select"] svg {
    fill: #00ff99 !important;
}


/* =========================================================
   ANALYZE BUTTON
   ========================================================= */

.stButton > button {
    width: 100%;
    min-height: 49px;

    border-radius: 13px;

    border: 1px solid rgba(0,255,153,0.34);

    background:
        linear-gradient(
            135deg,
            rgba(0,255,153,0.17),
            rgba(0,150,100,0.08)
        );

    color: #00ff99;

    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.7px;

    box-shadow:
        0 0 25px rgba(0,255,153,0.05);
}

.stButton > button:hover {
    color: #00ff99 !important;

    border-color:
        rgba(0,255,153,0.65);

    background:
        linear-gradient(
            135deg,
            rgba(0,255,153,0.23),
            rgba(0,150,100,0.12)
        );
}


/* =========================================================
   SIGNAL CARD
   ========================================================= */

.signal-card {
    margin-top: 18px;

    padding: 21px 16px 18px 16px;

    border-radius: 22px;

    background:
        radial-gradient(
            circle at 50% 0%,
            rgba(0,255,153,0.075),
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
    color: #78909c;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 2px;
}

.signal-circle {
    width: 120px;
    height: 120px;

    margin: 17px auto;

    border-radius: 50%;

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
        0 0 30px rgba(0,255,153,0.14);
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
        0 0 30px rgba(255,70,110,0.14);
}

.signal-neutral {
    border: 2px solid #657785;

    background:
        radial-gradient(
            circle,
            rgba(100,120,135,0.13),
            transparent 70%
        );
}

.signal-arrow {
    font-size: 35px;
    line-height: 32px;
    font-weight: 800;
}

.signal-call .signal-arrow,
.signal-call .signal-word {
    color: #00ff99;
}

.signal-put .signal-arrow,
.signal-put .signal-word {
    color: #ff466e;
}

.signal-neutral .signal-arrow,
.signal-neutral .signal-word {
    color: #a0adb6;
}

.signal-word {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-top: 5px;
}

.asset-name {
    color: #ffffff;
    font-size: 20px;
    font-weight: 800;
}

.direction {
    color: #8ea0ad;
    font-size: 11px;
    margin-top: 4px;
}


/* =========================================================
   STAT BOXES
   ========================================================= */

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

    padding: 11px 4px;
}

.stat-title {
    color: #657987;
    font-size: 8px;
    font-weight: 700;
    letter-spacing: 1px;
}

.stat-value {
    color: #ffffff;
    font-size: 15px;
    font-weight: 800;
    margin-top: 4px;
}


/* =========================================================
   AI STATUS
   ========================================================= */

.ai-status {
    margin-top: 15px;

    padding: 10px;

    border-radius: 10px;

    color: #00ff99;

    background:
        rgba(0,255,153,0.05);

    border:
        1px solid rgba(0,255,153,0.12);

    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1.2px;
}

.ai-pending {
    color: #f5c542;

    background:
        rgba(245,197,66,0.055);

    border-color:
        rgba(245,197,66,0.15);
}


/* =========================================================
   SMALL MESSAGE
   ========================================================= */

.small-note {
    text-align: center;

    color: #5d7180;

    font-size: 9px;

    line-height: 1.6;

    margin-top: 8px;
}


/* =========================================================
   HISTORY
   ========================================================= */

.history-card {
    background: #08141f;

    border: 1px solid #142c3b;

    border-radius: 13px;

    padding: 12px;

    margin-top: 8px;
}

.history-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.history-asset {
    color: #ffffff;
    font-size: 12px;
    font-weight: 800;
}

.history-bottom {
    display: flex;
    justify-content: space-between;

    color: #8da0ac;

    font-size: 10px;

    margin-top: 8px;
}

.history-time {
    color: #566b78;
    font-size: 8px;
    margin-top: 8px;
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


/* =========================================================
   INFO
   ========================================================= */

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


/* =========================================================
   BOTTOM NAVIGATION
   ========================================================= */

.bottom-nav {
    margin-top: 25px;
    padding-top: 14px;

    border-top: 1px solid rgba(255,255,255,0.04);
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    text-align: center;

    color: #40515c;

    font-size: 8px;

    line-height: 1.7;

    margin-top: 18px;

    padding-bottom: 12px;
}

</style>
""")


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
# MARKET DATA
# ============================================================

def get_candles(symbol, interval, outputsize=100):

    api_key = get_api_key()

    if not api_key:
        return None, "Twelve Data API key is missing."

    if interval not in ("1min", "5min"):
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
            return None, (
                f"Twelve Data HTTP error "
                f"{response.status_code}"
            )

        data = response.json()

        if data.get("status") == "error":
            return None, data.get(
                "message",
                "Twelve Data returned an error."
            )

        values = data.get("values")

        if not values:
            return None, "No market data was returned."

        candles = []

        for item in values:

            try:

                candles.append({
                    "datetime": item["datetime"],
                    "open": float(item["open"]),
                    "high": float(item["high"]),
                    "low": float(item["low"]),
                    "close": float(item["close"]),
                })

            except Exception:
                continue

        candles.sort(
            key=lambda x: x["datetime"]
        )

        if len(candles) < 60:
            return None, "Not enough market candles."

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

def ema(values, period):

    if len(values) < period:
        return None

    multiplier = 2 / (period + 1)

    value = sum(values[:period]) / period

    for price in values[period:]:

        value = (
            (price - value) * multiplier
        ) + value

    return value


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

        avg_gain = (
            (
                avg_gain * (period - 1)
            ) + gains[i]
        ) / period

        avg_loss = (
            (
                avg_loss * (period - 1)
            ) + losses[i]
        ) / period

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))


def macd(values):

    if len(values) < 35:
        return None

    ema12 = ema(values, 12)
    ema26 = ema(values, 26)

    if ema12 is None or ema26 is None:
        return None

    return ema12 - ema26


# ============================================================
# ANALYSIS
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
            "error": "Not enough market data."
        }

    # Last candle can still be forming.
    # Analyze the last completed candle.

    candle = candles[-2]

    closed = candles[:-1]

    closes = [
        x["close"]
        for x in closed
    ]

    price = candle["close"]

    ema9 = ema(closes, 9)
    ema21 = ema(closes, 21)
    ema50 = ema(closes, 50)

    rsi_value = rsi(closes, 14)

    macd_value = macd(closes)

    score = 0

    # EMA 9 / 21

    if ema9 is not None and ema21 is not None:

        if ema9 > ema21:
            score += 1

        elif ema9 < ema21:
            score -= 1

    # EMA 21 / 50

    if ema21 is not None and ema50 is not None:

        if ema21 > ema50:
            score += 1

        elif ema21 < ema50:
            score -= 1

    # Price / EMA21

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

    # Final signal

    if score >= 4:

        signal = "CALL"
        direction = "BUY / UP"

    elif score <= -4:

        signal = "PUT"
        direction = "SELL / DOWN"

    else:

        signal = "NO TRADE"
        direction = "WAIT"

    return {
        "success": True,
        "signal": signal,
        "direction": direction,
        "strength": min(abs(score), 5),
        "score": score,
        "price": price,
        "candle_time": candle["datetime"]
    }


# ============================================================
# FORMAT PRICE
# ============================================================

def format_price(price):

    if price is None:
        return "—"

    try:

        value = float(price)

        if value >= 1000:
            return f"{value:,.2f}"

        if value >= 100:
            return f"{value:.2f}"

        if value >= 1:
            return f"{value:.4f}"

        return f"{value:.5f}"

    except Exception:

        return str(price)


# ============================================================
# WIN RATE
# ============================================================

def get_win_rate():

    total = (
        st.session_state.wins
        + st.session_state.losses
    )

    if total == 0:
        return "—"

    return (
        f"{(
            st.session_state.wins / total
        ) * 100:.1f}%"
    )


# ============================================================
# RESOLVE PENDING SIGNALS
# ============================================================

def resolve_pending_signals():

    pending = [
        x
        for x in st.session_state.history
        if x.get("status") == "PENDING"
    ]

    if not pending:
        return False

    changed = False

    groups = {}

    for item in pending:

        key = (
            item["symbol"],
            item["interval"]
        )

        groups.setdefault(
            key,
            []
        ).append(item)

    for (symbol, interval), signals in groups.items():

        candles, error = get_candles(
            symbol,
            interval,
            20
        )

        if error or not candles:
            continue

        for signal in signals:

            entry_time = signal[
                "entry_candle_time"
            ]

            newer = [
                c
                for c in candles
                if c["datetime"] > entry_time
            ]

            # Need TWO newer candles.
            # This ensures the first newer candle
            # has finished.

            if len(newer) < 2:
                continue

            result_candle = newer[0]

            entry_price = signal[
                "entry_price"
            ]

            result_price = result_candle[
                "close"
            ]

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

            signal[
                "result_candle_time"
            ] = result_candle["datetime"]

            signal["checked_at"] = (
                datetime.now(timezone.utc)
                .strftime(
                    "%Y-%m-%d %H:%M:%S UTC"
                )
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
def automatic_monitor():

    pending_exists = any(
        x.get("status") == "PENDING"
        for x in st.session_state.history
    )

    if not pending_exists:
        return

    changed = resolve_pending_signals()

    if changed:
        st.rerun()


# ============================================================
# HEADER
# ============================================================

html("""
<div class="xiga-header">
    <div class="xiga-left">
        <div class="xiga-logo">⚡</div>

        <div>
            <div class="xiga-name">XIGA</div>
            <div class="xiga-subtitle">
                TRADING INTELLIGENCE
            </div>
        </div>
    </div>

    <div class="pro-badge">PRO</div>
</div>
""")


# ============================================================
# PAGE CONTENT
# ============================================================

if st.session_state.page == "Trade":

    # --------------------------------------------------------
    # MARKET
    # --------------------------------------------------------

    html("""
    <div class="section-title">
        MARKET
    </div>
    """)

    category = st.selectbox(
        "Category",
        list(ASSETS.keys()),
        label_visibility="collapsed",
        key="category"
    )

    asset_name = st.selectbox(
        "Asset",
        list(ASSETS[category].keys()),
        label_visibility="collapsed",
        key="asset"
    )

    symbol = ASSETS[category][asset_name]

    # --------------------------------------------------------
    # TIMEFRAME
    # --------------------------------------------------------

    html("""
    <div class="section-title">
        TIMEFRAME
    </div>
    """)

    timeframe = st.selectbox(
        "Timeframe",
        ["1 MIN", "5 MIN"],
        label_visibility="collapsed",
        key="timeframe"
    )

    # --------------------------------------------------------
    # ANALYZE
    # --------------------------------------------------------

    analyze_clicked = st.button(
        "⚡ ANALYZE MARKET",
        use_container_width=True,
        key="analyze_market"
    )

    if analyze_clicked:

        with st.spinner(
            "Analyzing live market data..."
        ):

            analysis = analyze_market(
                symbol,
                timeframe
            )

        if not analysis["success"]:

            st.error(
                "API ERROR: "
                + analysis["error"]
            )

        else:

            st.session_state.result = analysis

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

                    "interval": TIMEFRAMES[
                        timeframe
                    ],

                    "signal": analysis[
                        "signal"
                    ],

                    "strength": analysis[
                        "strength"
                    ],

                    "score": analysis[
                        "score"
                    ],

                    "entry_price": analysis[
                        "price"
                    ],

                    "entry_candle_time":
                        analysis[
                            "candle_time"
                        ],

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
    # SIGNAL
    # --------------------------------------------------------

    result = st.session_state.result

    if result is None:

        signal = "READY"
        circle_class = "signal-neutral"
        arrow = "•"
        direction = "SELECT MARKET"

    else:

        signal = result["signal"]

        direction = result[
            "direction"
        ]

        if signal == "CALL":

            circle_class = "signal-call"
            arrow = "↑"

        elif signal == "PUT":

            circle_class = "signal-put"
            arrow = "↓"

        else:

            circle_class = "signal-neutral"
            arrow = "•"

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    if result is None:

        status_text = "● AI READY"
        status_class = ""

    elif signal == "NO TRADE":

        status_text = (
            "● NO TRADE — LOW CONFIDENCE"
        )

        status_class = "ai-pending"

    else:

        pending = any(
            x.get("status") == "PENDING"
            and x.get("symbol") == symbol
            and x.get("timeframe") == timeframe
            for x in st.session_state.history
        )

        if pending:

            status_text = "● TRACKING RESULT"
            status_class = "ai-pending"

        else:

            status_text = "● AI ANALYSIS COMPLETE"
            status_class = ""

    # --------------------------------------------------------
    # VALUES
    # --------------------------------------------------------

    if result is None:

        strength_display = "—"
        price_display = "—"

    else:

        strength_display = (
            f'{result["strength"]}/5'
        )

        price_display = format_price(
            result["price"]
        )

    # --------------------------------------------------------
    # SIGNAL CARD
    # --------------------------------------------------------

    html(f"""
    <div class="signal-card">

        <div class="signal-label">
            XIGA AI SIGNAL
        </div>

        <div class="signal-circle {circle_class}">

            <div class="signal-arrow">
                {arrow}
            </div>

            <div class="signal-word">
                {signal}
            </div>

        </div>

        <div class="asset-name">
            {asset_name}
        </div>

        <div class="direction">
            {direction}
        </div>

        <div class="stats-row">

            <div class="stat-box">

                <div class="stat-title">
                    STRENGTH
                </div>

                <div class="stat-value">
                    {strength_display}
                </div>

            </div>

            <div class="stat-box">

                <div class="stat-title">
                    WIN RATE
                </div>

                <div class="stat-value">
                    {get_win_rate()}
                </div>

            </div>

            <div class="stat-box">

                <div class="stat-title">
                    PRICE
                </div>

                <div class="stat-value"
                     style="font-size:13px;">

                    {price_display}

                </div>

            </div>

        </div>

        <div class="ai-status {status_class}">
            {status_text}
        </div>

    </div>
    """)

    # --------------------------------------------------------
    # EXPLANATION
    # --------------------------------------------------------

    if result is not None:

        if signal == "CALL":

            html(f"""
            <div class="small-note">
                Bullish confirmation detected.
                Score: +{result["score"]}.
                Signal is being tracked using completed
                market candles.
            </div>
            """)

        elif signal == "PUT":

            html(f"""
            <div class="small-note">
                Bearish confirmation detected.
                Score: {result["score"]}.
                Signal is being tracked using completed
                market candles.
            </div>
            """)

        else:

            html(f"""
            <div class="small-note">
                Market conditions are mixed.
                Score: {result["score"]}.
                XIGA is avoiding a low-confidence trade.
            </div>
            """)


# ============================================================
# HISTORY PAGE
# ============================================================

elif st.session_state.page == "History":

    html("""
    <div class="section-title">
        TRADING HISTORY
    </div>
    """)

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

    html(f"""
    <div class="info-box"
         style="text-align:center;">

        <strong>
            HISTORICAL WIN RATE
        </strong>

        <br><br>

        <span style="
            color:#00ff99;
            font-size:27px;
            font-weight:800;
        ">
            {get_win_rate()}
        </span>

        <br>

        <span style="font-size:9px;">
            Completed WIN/LOSS signals only.
        </span>

    </div>
    """)

    if not st.session_state.history:

        html("""
        <div class="info-box"
             style="text-align:center;">

            No signals yet.

            <br><br>

            Analyze a market to create
            your first signal.

        </div>
        """)

    else:

        for item in st.session_state.history:

            status = item["status"]

            if status == "WIN":

                status_class = "win-text"

            elif status == "LOSS":

                status_class = "loss-text"

            else:

                status_class = "pending-text"

            result_price = item.get(
                "result_price"
            )

            if result_price is None:

                result_display = "—"

            else:

                result_display = format_price(
                    result_price
                )

            html(f"""
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
                        {format_price(
                            item["entry_price"]
                        )}
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
            """)


# ============================================================
# LEARN PAGE
# ============================================================

elif st.session_state.page == "Learn":

    html("""
    <div class="section-title">
        HOW XIGA WORKS
    </div>

    <div class="info-box">

        <strong>1. Select a market</strong><br>
        Choose a supported market.

        <br><br>

        <strong>2. Select timeframe</strong><br>
        XIGA currently supports 1 MIN and 5 MIN.

        <br><br>

        <strong>3. Analyze</strong><br>
        XIGA evaluates EMA trend, RSI, MACD
        and recent momentum.

        <br><br>

        <strong>4. Signal</strong><br>
        XIGA can produce CALL, PUT or
        NO TRADE.

        <br><br>

        <strong>5. Automatic tracking</strong><br>
        CALL and PUT signals are tracked
        automatically.

        <br><br>

        <strong>6. Result</strong><br>
        The system waits for a completed candle
        before recording WIN or LOSS.

    </div>

    <div class="info-box">

        <strong>Important</strong><br><br>

        XIGA is a market-analysis assistant.
        It does not automatically place trades.

        <br><br>

        Twelve Data market prices can differ
        from Pocket Option prices, especially
        for OTC markets.

        <br><br>

        No signal guarantees profit.

    </div>
    """)


# ============================================================
# PROFILE PAGE
# ============================================================

elif st.session_state.page == "Profile":

    html(f"""
    <div class="section-title">
        XIGA PROFILE
    </div>

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
        {get_win_rate()}

        <br><br>

        <strong>Supported Timeframes</strong><br>
        1 MIN<br>
        5 MIN

    </div>
    """)


# ============================================================
# BOTTOM NAVIGATION
# ============================================================

html("""
<div class="bottom-nav"></div>
""")

nav_options = [
    "Trade",
    "History",
    "Learn",
    "Profile"
]

current_index = nav_options.index(
    st.session_state.page
)

selected_page = st.radio(
    "Navigation",
    nav_options,
    index=current_index,
    horizontal=True,
    label_visibility="collapsed",
    key="bottom_navigation"
)

if selected_page != st.session_state.page:

    st.session_state.page = selected_page

    st.rerun()


# ============================================================
# AUTOMATIC MONITOR
# ============================================================

automatic_monitor()


# ============================================================
# FOOTER
# ============================================================

html("""
<div class="footer">
    XIGA Trading Intelligence<br>
    Market analysis assistant — not an automatic trading system.<br>
    All rights reserved designed by Khawaja.
</div>
""")
