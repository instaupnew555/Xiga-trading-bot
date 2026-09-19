import streamlit as st
import requests
from datetime import datetime


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="XIGA Trading",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ============================================================
# SESSION DATA
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "stats" not in st.session_state:
    st.session_state.stats = {
        "signals": 0,
        "wins": 0,
        "losses": 0
    }

if "page" not in st.session_state:
    st.session_state.page = "trade"

if "last_result" not in st.session_state:
    st.session_state.last_result = {}


# ============================================================
# ASSETS
# ============================================================

ASSETS = {

    "Forex": {
        "🇺🇸 🇪🇺 EUR/USD": "EUR/USD",
        "🇬🇧 🇺🇸 GBP/USD": "GBP/USD",
        "🇺🇸 🇯🇵 USD/JPY": "USD/JPY",
        "🇦🇺 🇺🇸 AUD/USD": "AUD/USD",
        "🇺🇸 🇨🇦 USD/CAD": "USD/CAD",
        "🇺🇸 🇨🇭 USD/CHF": "USD/CHF",
        "🇳🇿 🇺🇸 NZD/USD": "NZD/USD",
        "🇪🇺 🇯🇵 EUR/JPY": "EUR/JPY",
        "🇪🇺 🇬🇧 EUR/GBP": "EUR/GBP",
        "🇪🇺 🇨🇭 EUR/CHF": "EUR/CHF",
        "🇬🇧 🇯🇵 GBP/JPY": "GBP/JPY",
        "🇦🇺 🇯🇵 AUD/JPY": "AUD/JPY",
        "🇦🇺 🇳🇿 AUD/NZD": "AUD/NZD",
        "🇨🇭 🇯🇵 CHF/JPY": "CHF/JPY",
        "🇳🇿 🇯🇵 NZD/JPY": "NZD/JPY",
        "🇨🇦 🇯🇵 CAD/JPY": "CAD/JPY",
        "🇨🇦 🇨🇭 CAD/CHF": "CAD/CHF",
        "🇦🇺 🇨🇭 AUD/CHF": "AUD/CHF",
    },

    "Stocks": {
        "🍎 Apple": "AAPL",
        "🪟 Microsoft": "MSFT",
        "🚗 Tesla": "TSLA",
        "🛒 Amazon": "AMZN",
        "💻 NVIDIA": "NVDA",
        "🎬 Netflix": "NFLX",
        "🔵 Meta": "META",
        "💳 Visa": "V",
        "🛩 Boeing": "BA",
        "📱 Intel": "INTC",
        "💼 Cisco": "CSCO",
        "🧬 Pfizer": "PFE",
        "💳 American Express": "AXP",
        "📦 FedEx": "FDX",
        "🍔 McDonald's": "MCD",
        "🛢 ExxonMobil": "XOM",
        "💊 Johnson & Johnson": "JNJ",
        "🎮 GameStop": "GME",
        "🪙 Coinbase": "COIN",
        "🤖 Palantir": "PLTR",
        "⚙ AMD": "AMD",
        "🏦 Citigroup": "C",
        "☁ Alibaba": "BABA",
        "⛏ Marathon Digital": "MARA",
    },

    "Crypto": {
        "₿ Bitcoin": "BTC/USD",
        "Ξ Ethereum": "ETH/USD",
        "◎ Solana": "SOL/USD",
        "🐕 Dogecoin": "DOGE/USD",
        "🔷 Cardano": "ADA/USD",
        "🟡 BNB": "BNB/USD",
        "🔗 Chainlink": "LINK/USD",
        "🟣 Polygon": "MATIC/USD",
        "⚡ Litecoin": "LTC/USD",
        "🔺 Avalanche": "AVAX/USD",
        "🔵 XRP": "XRP/USD",
        "🟢 TRON": "TRX/USD",
    },

    "Commodities": {
        "🥇 Gold": "XAU/USD",
        "🥈 Silver": "XAG/USD",
        "🛢 WTI Crude Oil": "WTI/USD",
        "🛢 Brent Oil": "BRENT/USD",
        "🔥 Natural Gas": "NATGAS/USD",
    },

    "Indices": {
        "📊 S&P 500": "SPX",
        "💻 NASDAQ 100": "NDX",
        "🏦 Dow Jones": "DJI",
        "🇩🇪 DAX": "DAX",
        "🇬🇧 FTSE 100": "FTSE",
        "🇯🇵 Nikkei 225": "N225",
    },

    "OTC": {
        "OTC EUR/USD": None,
        "OTC GBP/USD": None,
        "OTC USD/JPY": None,
        "OTC AUD/USD": None,
        "OTC USD/CAD": None,
        "OTC USD/CHF": None,
        "OTC Gold": None,
        "OTC Silver": None,
        "OTC Brent Oil": None,
        "OTC WTI Crude Oil": None,
        "OTC Apple": None,
        "OTC Microsoft": None,
        "OTC Tesla": None,
        "OTC Amazon": None,
        "OTC NVIDIA": None,
        "OTC Netflix": None,
        "OTC Meta": None,
        "OTC Visa": None,
        "OTC Bitcoin": None,
        "OTC Ethereum": None,
        "OTC Solana": None,
        "OTC Dogecoin": None,
        "OTC Litecoin": None,
        "OTC Cardano": None,
        "OTC BNB": None,
        "OTC S&P 500": None,
        "OTC NASDAQ 100": None,
        "OTC Dow Jones": None,
    }
}


# ============================================================
# TIMEFRAME MAPPING
# ============================================================

TIMEFRAME_MAP = {
    "1 MIN": "1min",
    "5 MIN": "5min"
}


# ============================================================
# TWELVE DATA
# ============================================================

def get_api_key():

    try:
        key = st.secrets["TWELVE_DATA_API_KEY"]

        if not key:
            return None

        return str(key).strip()

    except Exception:
        return None


def get_candles(symbol, interval="1min", outputsize=100):

    api_key = get_api_key()

    if not api_key:
        return [], "API KEY NOT FOUND"

    url = "https://api.twelvedata.com/time_series"

    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": api_key,
        "format": "JSON"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=(5, 10)
        )

        try:
            data = response.json()

        except ValueError:
            return [], (
                f"INVALID API RESPONSE "
                f"(HTTP {response.status_code})"
            )

        if response.status_code != 200:

            message = data.get(
                "message",
                f"HTTP {response.status_code}"
            )

            return [], (
                f"TWELVE DATA ERROR: {message}"
            )

        if data.get("status") == "error":

            return [], data.get(
                "message",
                "TWELVE DATA ERROR"
            )

        values = data.get("values")

        if not values:

            return [], "NO MARKET DATA RETURNED"

        candles = []

        for item in reversed(values):

            try:

                candles.append({
                    "open": float(item["open"]),
                    "high": float(item["high"]),
                    "low": float(item["low"]),
                    "close": float(item["close"]),
                    "datetime": item.get(
                        "datetime",
                        ""
                    )
                })

            except (
                KeyError,
                TypeError,
                ValueError
            ):
                continue

        if len(candles) < 60:

            return [], (
                f"NOT ENOUGH MARKET DATA "
                f"({len(candles)} candles)"
            )

        return candles, "LIVE DATA CONNECTED"

    except requests.exceptions.Timeout:

        return [], (
            "MARKET DATA TIMEOUT "
            "(Twelve Data did not respond within 10 seconds)"
        )

    except requests.exceptions.ConnectionError:

        return [], (
            "NETWORK CONNECTION ERROR"
        )

    except requests.exceptions.RequestException as e:

        return [], (
            f"REQUEST ERROR: {str(e)}"
        )

    except Exception as e:

        return [], (
            f"CONNECTION ERROR: {str(e)}"
        )


# ============================================================
# INDICATORS
# ============================================================

def ema(values, period):

    if len(values) < period:
        return None

    multiplier = 2 / (period + 1)

    current = sum(
        values[:period]
    ) / period

    for price in values[period:]:

        current = (
            (price - current)
            * multiplier
            + current
        )

    return current


def rsi(values, period=14):

    if len(values) < period + 1:
        return None

    gains = []
    losses = []

    for i in range(1, len(values)):

        change = (
            values[i] -
            values[i - 1]
        )

        if change > 0:

            gains.append(change)
            losses.append(0)

        else:

            gains.append(0)
            losses.append(
                abs(change)
            )

    avg_gain = (
        sum(gains[:period]) /
        period
    )

    avg_loss = (
        sum(losses[:period]) /
        period
    )

    for i in range(
        period,
        len(gains)
    ):

        avg_gain = (
            (
                avg_gain *
                (period - 1)
            )
            + gains[i]
        ) / period

        avg_loss = (
            (
                avg_loss *
                (period - 1)
            )
            + losses[i]
        ) / period

    if avg_loss == 0:

        return 100.0

    rs = avg_gain / avg_loss

    return 100 - (
        100 / (1 + rs)
    )


def macd(values):

    if len(values) < 35:
        return None, None

    fast = ema(values, 12)
    slow = ema(values, 26)

    if fast is None or slow is None:
        return None, None

    current_macd = fast - slow

    previous_values = values[:-1]

    previous_fast = ema(
        previous_values,
        12
    )

    previous_slow = ema(
        previous_values,
        26
    )

    if (
        previous_fast is None
        or previous_slow is None
    ):
        return current_macd, None

    previous_macd = (
        previous_fast -
        previous_slow
    )

    return current_macd, previous_macd


# ============================================================
# MARKET ANALYSIS
# ============================================================

def analyze_market(
    symbol,
    timeframe="1 MIN"
):

    # --------------------------------------------------------
    # Validate timeframe
    # --------------------------------------------------------

    if timeframe not in TIMEFRAME_MAP:

        return {
            "success": False,
            "signal": "NO TRADE",
            "strength": 0,
            "status": (
                "SECOND-BASED DATA NOT AVAILABLE. "
                "Twelve Data currently provides "
                "1 MIN and larger standard intervals "
                "for this analysis."
            ),
            "description": (
                "10 SEC, 15 SEC and 30 SEC signals "
                "are disabled to avoid using fake "
                "second-level market data."
            )
        }

    interval = TIMEFRAME_MAP[timeframe]

    # --------------------------------------------------------
    # Fetch market data
    # --------------------------------------------------------

    candles, status = get_candles(
        symbol,
        interval,
        100
    )

    if not candles:

        return {
            "success": False,
            "signal": "NO TRADE",
            "strength": 0,
            "status": status,
            "description": status
        }

    # --------------------------------------------------------
    # Closing prices
    # --------------------------------------------------------

    closes = [
        candle["close"]
        for candle in candles
    ]

    if len(closes) < 60:

        return {
            "success": False,
            "signal": "NO TRADE",
            "strength": 0,
            "status": "NOT ENOUGH DATA",
            "description": (
                "The data provider returned "
                "too few candles."
            )
        }

    current = closes[-1]

    # --------------------------------------------------------
    # Indicators
    # --------------------------------------------------------

    ema9 = ema(closes, 9)
    ema21 = ema(closes, 21)
    ema50 = ema(closes, 50)

    rsi_value = rsi(
        closes,
        14
    )

    macd_value, previous_macd = macd(
        closes
    )

    score = 0

    reasons = []

    # --------------------------------------------------------
    # EMA 9 / EMA 21
    # --------------------------------------------------------

    if (
        ema9 is not None
        and ema21 is not None
    ):

        if ema9 > ema21:

            score += 1

            reasons.append(
                "Short-term trend is bullish"
            )

        elif ema9 < ema21:

            score -= 1

            reasons.append(
                "Short-term trend is bearish"
            )

    # --------------------------------------------------------
    # EMA 21 / EMA 50
    # --------------------------------------------------------

    if (
        ema21 is not None
        and ema50 is not None
    ):

        if ema21 > ema50:

            score += 1

            reasons.append(
                "Medium-term trend is bullish"
            )

        elif ema21 < ema50:

            score -= 1

            reasons.append(
                "Medium-term trend is bearish"
            )

    # --------------------------------------------------------
    # Current price vs EMA 21
    # --------------------------------------------------------

    if ema21 is not None:

        if current > ema21:

            score += 1

            reasons.append(
                "Price is above EMA 21"
            )

        elif current < ema21:

            score -= 1

            reasons.append(
                "Price is below EMA 21"
            )

    # --------------------------------------------------------
    # RSI
    # --------------------------------------------------------

    if rsi_value is not None:

        if rsi_value >= 55:

            score += 1

            reasons.append(
                f"RSI bullish ({rsi_value:.1f})"
            )

        elif rsi_value <= 45:

            score -= 1

            reasons.append(
                f"RSI bearish ({rsi_value:.1f})"
            )

        else:

            reasons.append(
                f"RSI neutral ({rsi_value:.1f})"
            )

    # --------------------------------------------------------
    # MACD
    # --------------------------------------------------------

    if macd_value is not None:

        if macd_value > 0:

            score += 1

            reasons.append(
                "MACD is positive"
            )

        elif macd_value < 0:

            score -= 1

            reasons.append(
                "MACD is negative"
            )

        if previous_macd is not None:

            if (
                macd_value >
                previous_macd
            ):

                reasons.append(
                    "MACD momentum is rising"
                )

            elif (
                macd_value <
                previous_macd
            ):

                reasons.append(
                    "MACD momentum is falling"
                )

    # --------------------------------------------------------
    # Recent momentum
    # --------------------------------------------------------

    if len(closes) >= 6:

        momentum = (
            closes[-1] -
            closes[-6]
        )

        if momentum > 0:

            score += 1

            reasons.append(
                "Recent price momentum is bullish"
            )

        elif momentum < 0:

            score -= 1

            reasons.append(
                "Recent price momentum is bearish"
            )

    # --------------------------------------------------------
    # Strength
    # --------------------------------------------------------

    absolute_score = abs(score)

    if absolute_score >= 5:

        strength = 5

    elif absolute_score >= 4:

        strength = 4

    elif absolute_score >= 3:

        strength = 3

    elif absolute_score >= 2:

        strength = 2

    else:

        strength = 1

    # --------------------------------------------------------
    # Signal
    # --------------------------------------------------------

    if score >= 4:

        signal = "CALL"

    elif score <= -4:

        signal = "PUT"

    else:

        signal = "NO TRADE"

    # --------------------------------------------------------
    # Description
    # --------------------------------------------------------

    if signal == "CALL":

        description = (
            f"Bullish confirmation from "
            f"{len(reasons)} technical conditions. "
            f"Score: {score:+d}/6."
        )

    elif signal == "PUT":

        description = (
            f"Bearish confirmation from "
            f"{len(reasons)} technical conditions. "
            f"Score: {score:+d}/6."
        )

    else:

        description = (
            f"Market conditions are mixed. "
            f"Score: {score:+d}/6. "
            f"XIGA recommends waiting for stronger "
            f"confirmation."
        )

    return {

        "success": True,

        "signal": signal,

        "strength": strength,

        "score": score,

        "price": current,

        "ema9": ema9,

        "ema21": ema21,

        "ema50": ema50,

        "rsi": rsi_value,

        "macd": macd_value,

        "reasons": reasons,

        "status": status,

        "description": description,

        "data_interval": interval,

        "timeframe": timeframe

    }


# ============================================================
# COMPONENT HTML
# ============================================================

HTML = r"""
<div class="app">

<div class="topbar">

    <div class="menu">☰</div>

    <div class="brand">

        <div class="brand-title">
            <span>▰</span> XIGA
        </div>

        <div class="brand-subtitle">
            TRADING SIGNAL BOT
        </div>

    </div>

    <div class="pro">👑 PRO</div>

</div>


<div class="glass market">

    <div class="market-box">

        <div class="market-label">
            Asset
        </div>

        <select id="category"></select>

        <select id="asset"></select>

        <div class="market-status" id="marketStatus">
            ● MARKET READY
        </div>

    </div>


    <div class="market-box">

        <div class="market-label">
            Timeframe
        </div>

        <select id="timeframe">

            <option>10 SEC</option>
            <option>15 SEC</option>
            <option>30 SEC</option>
            <option selected>1 MIN</option>
            <option>5 MIN</option>

        </select>

        <div class="market-status">
            ● ANALYSIS READY
        </div>

    </div>

</div>


<div class="glass signal-card">


<svg
    class="chart"
    viewBox="0 0 500 220"
    preserveAspectRatio="none"
>

<line class="grid" x1="0" y1="35" x2="500" y2="35"/>
<line class="grid" x1="0" y1="85" x2="500" y2="85"/>
<line class="grid" x1="0" y1="135" x2="500" y2="135"/>
<line class="grid" x1="0" y1="185" x2="500" y2="185"/>

<polyline
class="green-line"
points="
0,175
35,155
65,165
100,130
135,145
170,105
205,120
240,80
275,100
310,65
345,75
380,42
420,60
460,28
500,12"
/>

<polyline
class="red-line"
points="
0,183
55,172
90,180
125,148
160,160
205,125
250,138
290,102
330,110
375,75
420,90
455,55
500,43"
/>

<line class="candle-green" x1="35" y1="180" x2="35" y2="135"/>
<rect class="candle-green" x="29" y="145" width="12" height="25" rx="2"/>

<line class="candle-red" x1="72" y1="170" x2="72" y2="125"/>
<rect class="candle-red" x="66" y="135" width="12" height="25" rx="2"/>

<line class="candle-green" x1="110" y1="150" x2="110" y2="105"/>
<rect class="candle-green" x="104" y="115" width="12" height="25" rx="2"/>

<line class="candle-green" x1="148" y1="135" x2="148" y2="88"/>
<rect class="candle-green" x="142" y="98" width="12" height="25" rx="2"/>

<line class="candle-red" x1="186" y1="145" x2="186" y2="95"/>
<rect class="candle-red" x="180" y="105" width="12" height="28" rx="2"/>

<line class="candle-green" x1="224" y1="115" x2="224" y2="65"/>
<rect class="candle-green" x="218" y="75" width="12" height="28" rx="2"/>

<line class="candle-green" x1="262" y1="105" x2="262" y2="50"/>
<rect class="candle-green" x="256" y="58" width="12" height="30" rx="2"/>

<line class="candle-red" x1="300" y1="115" x2="300" y2="62"/>
<rect class="candle-red" x="294" y="72" width="12" height="28" rx="2"/>

<line class="candle-green" x1="338" y1="85" x2="338" y2="38"/>
<rect class="candle-green" x="332" y="45" width="12" height="27" rx="2"/>

<line class="candle-green" x1="376" y1="70" x2="376" y2="25"/>
<rect class="candle-green" x="370" y="31" width="12" height="27" rx="2"/>

<line class="candle-red" x1="414" y1="82" x2="414" y2="35"/>
<rect class="candle-red" x="408" y="43" width="12" height="26" rx="2"/>

<line class="candle-green" x1="452" y1="52" x2="452" y2="10"/>
<rect class="candle-green" x="446" y="17" width="12" height="25" rx="2"/>

</svg>


<div class="signal-label">
    SIGNAL FOR
</div>

<div class="asset-name" id="signalAsset">
    EUR/USD
</div>

<div class="time-label" id="signalTime">
    ● TIMEFRAME: 1 MIN
</div>


<div class="signal-circle" id="signalCircle">

    <div class="inner-ring"></div>

    <div class="arrow" id="arrow">
        ◇
    </div>

</div>


<div class="signal-title buy" id="signalTitle">
    AI READY
</div>

<div class="direction" id="direction">
    WAITING FOR ANALYSIS
</div>


<div class="stats">

<div class="stat">

    <div class="stat-label">
        Signal Strength
    </div>

    <div class="dots green" id="strengthDots">
        ● ● ● ●
        <span class="empty">●</span>
    </div>

    <div class="stat-number" id="strengthText">
        —
    </div>

</div>


<div class="stat">

    <div class="stat-label">
        Win Rate
    </div>

    <div class="win" id="winRate">
        —
    </div>

    <div class="no-data" id="winStatus">
        ● WAITING FOR RESULTS
    </div>

</div>

</div>


<div class="ai">

    <div class="ai-icon">
        ✓
    </div>

    <div>

        <div class="ai-title" id="aiTitle">
            AI ENGINE READY
        </div>

        <div class="ai-description" id="aiDescription">
            Select an asset and start analysis
        </div>

    </div>

</div>


</div>


<button class="generate" id="generate">
    ⚡ ANALYZE MARKET
</button>


<div class="countdown" id="countdown">
    Analysis complete • Data source:
    <span id="dataSource">
        Twelve Data
    </span>
</div>


<div class="bottom">

    <div class="nav active" data-page="trade">
        <span class="nav-icon">⌁</span>
        Trade
    </div>

    <div class="nav" data-page="history">
        <span class="nav-icon">◷</span>
        History
    </div>

    <div class="nav" data-page="learn">
        <span class="nav-icon">▣</span>
        Learn
    </div>

    <div class="nav" data-page="profile">
        <span class="nav-icon">♙</span>
        Profile
    </div>

</div>


<div class="footer">
    🔒 SECURE • XIGA AI • V5.1 • LIVE ANALYSIS
</div>

</div>
"""


# ============================================================
# COMPONENT CSS
# ============================================================

CSS = r"""
*{
    box-sizing:border-box;
    margin:0;
    padding:0;
    -webkit-tap-highlight-color:transparent;
}

html,body{
    width:100%;
    min-height:100%;
    background:#020812;
    font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}

body{
    color:#fff;
}

button,select{
    font-family:inherit;
}

.app{
    width:100%;
    max-width:470px;
    min-height:100vh;
    margin:auto;
    padding:15px 14px 25px;
    background:radial-gradient(circle at 50% -15%,#173957 0%,#0a1c30 27%,#030914 65%,#020711 100%);
    overflow:hidden;
}

.topbar{
    height:58px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    margin-bottom:14px;
}

.menu{
    width:42px;
    height:42px;
    border-radius:13px;
    display:flex;
    align-items:center;
    justify-content:center;
    background:rgba(11,30,49,.88);
    border:1px solid #214967;
    color:#dceeff;
    font-size:21px;
}

.brand{
    text-align:center;
    flex:1;
}

.brand-title{
    font-size:25px;
    line-height:25px;
    font-weight:900;
    letter-spacing:1px;
}

.brand-title span{
    color:#28f3a5;
}

.brand-subtitle{
    margin-top:5px;
    color:#71859d;
    font-size:8px;
    letter-spacing:2px;
}

.pro{
    min-width:66px;
    padding:9px 8px;
    text-align:center;
    border-radius:12px;
    background:linear-gradient(135deg,#3d2d0d,#1f1809);
    border:1px solid #9b741d;
    color:#ffd76a;
    font-size:10px;
    font-weight:800;
}

.glass{
    background:linear-gradient(145deg,rgba(13,34,57,.96),rgba(5,16,29,.97));
    border:1px solid rgba(32,91,132,.72);
    border-radius:20px;
    box-shadow:0 18px 45px rgba(0,0,0,.32),inset 0 1px rgba(255,255,255,.035);
}

.market{
    padding:9px;
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:9px;
    margin-bottom:12px;
}

.market-box{
    min-height:62px;
    padding:9px 11px;
    border-radius:14px;
    background:linear-gradient(145deg,rgba(9,39,64,.98),rgba(7,25,43,.98));
    border:1px solid #185276;
}

.market-label{
    color:#7d93aa;
    font-size:8px;
    letter-spacing:1.4px;
    text-transform:uppercase;
    margin-bottom:3px;
}

select{
    width:100%;
    appearance:none;
    -webkit-appearance:none;
    border:0;
    outline:0;
    background:transparent;
    color:white;
    font-size:12px;
    font-weight:800;
    padding:2px 0;
    margin-bottom:2px;
}

select option{
    background:#0b1727;
    color:white;
}

.market-status{
    color:#29f4a5;
    font-size:7px;
    margin-top:2px;
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
}

.signal-card{
    position:relative;
    overflow:hidden;
    min-height:545px;
    padding:17px 12px 13px;
    text-align:center;
}

.chart{
    position:absolute;
    top:115px;
    left:0;
    width:100%;
    height:220px;
    opacity:.42;
    pointer-events:none;
}

.grid{
    stroke:#226082;
    stroke-width:1;
    opacity:.22;
}

.green-line{
    fill:none;
    stroke:#22ef9e;
    stroke-width:2;
}

.red-line{
    fill:none;
    stroke:#ff416e;
    stroke-width:2;
}

.candle-green{
    stroke:#22ef9e;
    fill:#22ef9e;
}

.candle-red{
    stroke:#ff416e;
    fill:#ff416e;
}

.signal-label{
    position:relative;
    z-index:5;
    color:#8ca1b7;
    font-size:9px;
    letter-spacing:1.5px;
    text-transform:uppercase;
}

.asset-name{
    position:relative;
    z-index:5;
    margin-top:4px;
    font-size:22px;
    font-weight:900;
}

.time-label{
    position:relative;
    z-index:5;
    margin-top:4px;
    color:#28f3a5;
    font-size:9px;
    letter-spacing:1px;
}

.signal-circle{
    position:relative;
    z-index:5;
    width:214px;
    height:214px;
    margin:23px auto 18px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    background:radial-gradient(circle,rgba(38,246,165,.43) 0%,rgba(14,74,61,.70) 35%,rgba(3,15,27,.98) 72%);
    border:3px solid #29f5a6;
    box-shadow:0 0 11px #29f5a6,0 0 35px rgba(41,245,166,.65),0 0 80px rgba(41,245,166,.22),inset 0 0 32px rgba(41,245,166,.27);
    transition:.35s ease;
}

.signal-circle.sell{
    background:radial-gradient(circle,rgba(255,53,103,.42) 0%,rgba(82,17,41,.72) 35%,rgba(3,15,27,.98) 72%);
    border-color:#ff3d70;
    box-shadow:0 0 11px #ff3d70,0 0 35px rgba(255,61,112,.65),0 0 80px rgba(255,61,112,.22),inset 0 0 32px rgba(255,61,112,.27);
}

.signal-circle.neutral{
    background:radial-gradient(circle,rgba(80,140,180,.28) 0%,rgba(17,46,68,.72) 35%,rgba(3,15,27,.98) 72%);
    border-color:#5e91b5;
    box-shadow:0 0 11px #5e91b5,0 0 35px rgba(94,145,181,.35),inset 0 0 32px rgba(94,145,181,.20);
}

.inner-ring{
    position:absolute;
    width:183px;
    height:183px;
    border-radius:50%;
    border:1px solid rgba(255,255,255,.14);
}

.arrow{
    position:relative;
    z-index:2;
    font-size:83px;
    line-height:1;
    color:#5cffb8;
    text-shadow:0 0 10px #29f5a6,0 0 28px rgba(41,245,166,.85);
}

.arrow.sell{
    color:#ff688d;
    text-shadow:0 0 10px #ff3d70,0 0 28px rgba(255,61,112,.85);
}

.arrow.neutral{
    color:#91b9d5;
    text-shadow:0 0 10px #5e91b5;
}

.signal-title{
    position:relative;
    z-index:5;
    font-size:30px;
    font-weight:950;
    letter-spacing:-.4px;
}

.signal-title.buy{
    color:#35f4a9;
    text-shadow:0 0 20px rgba(53,244,169,.3);
}

.signal-title.sell{
    color:#ff416f;
    text-shadow:0 0 20px rgba(255,65,111,.3);
}

.signal-title.neutral{
    color:#8fb4cf;
}

.direction{
    position:relative;
    z-index:5;
    margin-top:4px;
    color:#8597ac;
    font-size:9px;
    letter-spacing:2px;
}

.stats{
    position:relative;
    z-index:5;
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:10px;
    margin-top:17px;
}

.stat{
    min-height:99px;
    padding:13px 9px;
    border-radius:15px;
    background:linear-gradient(145deg,rgba(7,29,49,.98),rgba(5,17,30,.98));
    border:1px solid #17557d;
}

.stat-label{
    color:#8296ad;
    font-size:9px;
    text-transform:uppercase;
    letter-spacing:.4px;
}

.dots{
    margin-top:8px;
    font-size:17px;
    letter-spacing:1px;
}

.green{
    color:#29f5a6;
    text-shadow:0 0 9px rgba(41,245,166,.7);
}

.empty{
    color:#26394c;
}

.stat-number{
    margin-top:3px;
    color:white;
    font-size:13px;
    font-weight:800;
}

.win{
    margin-top:7px;
    color:#29f5a6;
    font-size:25px;
    font-weight:900;
}

.no-data{
    margin-top:3px;
    color:#29f5a6;
    font-size:8px;
}

.ai{
    position:relative;
    z-index:5;
    display:flex;
    align-items:center;
    gap:11px;
    margin-top:11px;
    padding:13px;
    text-align:left;
    border-radius:15px;
    background:linear-gradient(145deg,rgba(7,37,47,.97),rgba(5,19,31,.97));
    border:1px solid rgba(31,181,150,.55);
}

.ai-icon{
    width:35px;
    height:35px;
    flex-shrink:0;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    color:#2af5a5;
    background:rgba(42,245,165,.13);
    border:1px solid rgba(42,245,165,.48);
    box-shadow:0 0 15px rgba(42,245,165,.17);
}

.ai-title{
    color:#2af5a5;
    font-size:11px;
    font-weight:900;
}

.ai-description{
    color:#7f92a7;
    font-size:8px;
    margin-top:3px;
}

.generate{
    width:100%;
    height:55px;
    margin-top:11px;
    border-radius:16px;
    border:1px solid #5affaF;
    background:linear-gradient(100deg,#13ca87,#38f5ad);
    color:#03130d;
    font-size:14px;
    font-weight:900;
    cursor:pointer;
    box-shadow:0 8px 28px rgba(37,245,166,.20);
}

.generate:disabled{
    opacity:.65;
    cursor:wait;
}

.countdown{
    position:relative;
    z-index:5;
    margin-top:8px;
    color:#a6b6c9;
    font-size:9px;
    text-align:center;
}

.countdown span{
    color:#29f5a6;
    font-weight:900;
}

.bottom{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:4px;
    margin-top:13px;
    padding:7px;
    border-radius:18px;
    background:rgba(4,15,27,.97);
    border:1px solid #173f5b;
}

.nav{
    text-align:center;
    padding:8px 2px;
    border-radius:12px;
    color:#71869d;
    font-size:8px;
    cursor:pointer;
}

.nav.active{
    color:#29f5a6;
    background:radial-gradient(circle,rgba(41,245,166,.12),transparent 75%);
    text-shadow:0 0 12px rgba(41,245,166,.35);
}

.nav-icon{
    display:block;
    font-size:19px;
    line-height:20px;
    margin-bottom:3px;
}

.footer{
    text-align:center;
    margin-top:9px;
    color:#4f647a;
    font-size:7px;
    letter-spacing:.5px;
}

@media(max-width:370px){

    .app{
        padding-left:9px;
        padding-right:9px;
    }

    .signal-circle{
        width:190px;
        height:190px;
    }

    .inner-ring{
        width:163px;
        height:163px;
    }

    .arrow{
        font-size:70px;
    }

    .signal-title{
        font-size:27px;
    }

}
"""


# ============================================================
# COMPONENT JAVASCRIPT
# ============================================================

JS = r"""
export default function(component){

    const {
        parentElement,
        setStateValue,
        setTriggerValue,
        data
    } = component;


    const category =
        parentElement.querySelector("#category");

    const asset =
        parentElement.querySelector("#asset");

    const timeframe =
        parentElement.querySelector("#timeframe");

    const generate =
        parentElement.querySelector("#generate");

    const signalAsset =
        parentElement.querySelector("#signalAsset");

    const signalTime =
        parentElement.querySelector("#signalTime");

    const signalCircle =
        parentElement.querySelector("#signalCircle");

    const arrow =
        parentElement.querySelector("#arrow");

    const signalTitle =
        parentElement.querySelector("#signalTitle");

    const direction =
        parentElement.querySelector("#direction");

    const strengthDots =
        parentElement.querySelector("#strengthDots");

    const strengthText =
        parentElement.querySelector("#strengthText");

    const winRate =
        parentElement.querySelector("#winRate");

    const winStatus =
        parentElement.querySelector("#winStatus");

    const aiTitle =
        parentElement.querySelector("#aiTitle");

    const aiDescription =
        parentElement.querySelector("#aiDescription");

    const marketStatus =
        parentElement.querySelector("#marketStatus");

    const dataSource =
        parentElement.querySelector("#dataSource");


    const assets =
        data?.assets || {};

    const result =
        data?.result || {};

    const stats =
        data?.stats || {};


    /* ==========================================
       CATEGORY
       ========================================== */

    category.innerHTML = "";

    Object.keys(assets).forEach(
        function(name){

            const option =
                document.createElement(
                    "option"
                );

            option.value = name;
            option.textContent = name;

            category.appendChild(
                option
            );

        }
    );


    /* ==========================================
       ASSETS
       ========================================== */

    function populateAssets(){

        const selected =
            category.value;

        asset.innerHTML = "";

        const list =
            assets[selected] || {};

        Object.keys(list).forEach(
            function(name){

                const option =
                    document.createElement(
                        "option"
                    );

                option.value = name;
                option.textContent = name;

                asset.appendChild(
                    option
                );

            }
        );

        updateAsset();

    }


    function cleanAssetName(name){

        return name
            .replace(/🇺🇸|🇪🇺|🇬🇧|🇯🇵|🇦🇺|🇨🇦|🇨🇭|🇳🇿/g,"")
            .replace(/^\s+/,"")
            .trim();

    }


    function updateAsset(){

        const selected =
            category.value;

        const list =
            assets[selected] || {};

        const display =
            asset.value ||
            Object.keys(list)[0] ||
            "🇺🇸 🇪🇺 EUR/USD";

        signalAsset.textContent =
            cleanAssetName(display);

        signalTime.textContent =
            "● TIMEFRAME: " +
            timeframe.value;


        if(selected === "OTC"){

            marketStatus.textContent =
                "● OTC DATA FEED REQUIRED";

        }
        else if(
            timeframe.value === "10 SEC" ||
            timeframe.value === "15 SEC" ||
            timeframe.value === "30 SEC"
        ){

            marketStatus.textContent =
                "● SECOND DATA UNAVAILABLE";

        }
        else{

            marketStatus.textContent =
                "● MARKET READY";

        }

    }


    category.onchange =
        populateAssets;

    asset.onchange =
        updateAsset;

    timeframe.onchange =
        updateAsset;


    populateAssets();


    /* ==========================================
       RESET UI
       ========================================== */

    function resetSignalUI(){

        signalCircle.classList.remove(
            "sell",
            "neutral"
        );

        arrow.classList.remove(
            "sell",
            "neutral"
        );

        signalTitle.className =
            "signal-title buy";

        arrow.textContent =
            "◇";

        signalTitle.textContent =
            "AI READY";

        direction.textContent =
            "WAITING FOR ANALYSIS";

    }


    /* ==========================================
       ANALYZE
       ========================================== */

    generate.onclick = function(){

        const categoryName =
            category.value;

        const selectedAsset =
            asset.value;

        const selectedTimeframe =
            timeframe.value;


        generate.disabled =
            true;

        generate.textContent =
            "◌ ANALYZING MARKET...";


        aiTitle.textContent =
            "AI ANALYZING...";

        aiDescription.textContent =
            "Connecting to live market data...";


        signalTitle.className =
            "signal-title buy";

        signalTitle.textContent =
            "ANALYZING";

        direction.textContent =
            "READING MARKET DATA";

        arrow.textContent =
            "◌";


        setTriggerValue(
            "analyze",
            {
                category:
                    categoryName,

                asset:
                    selectedAsset,

                timeframe:
                    selectedTimeframe,

                timestamp:
                    Date.now()
            }
        );

    };


    /* ==========================================
       NAVIGATION
       ========================================== */

    parentElement
        .querySelectorAll(".nav")
        .forEach(
            function(nav){

                nav.onclick =
                    function(){

                        const page =
                            nav.dataset.page;


                        parentElement
                            .querySelectorAll(
                                ".nav"
                            )
                            .forEach(
                                function(item){

                                    item.classList
                                        .remove(
                                            "active"
                                        );

                                }
                            );


                        nav.classList.add(
                            "active"
                        );


                        setStateValue(
                            "page",
                            page
                        );


                        setTriggerValue(
                            "navigation",
                            page
                        );

                    };

            }
        );


    /* ==========================================
       RESULT
       ========================================== */

    if(result && result.signal){

        const signal =
            result.signal;

        const strength =
            Number(
                result.strength || 0
            );


        signalCircle.classList.remove(
            "sell",
            "neutral"
        );

        arrow.classList.remove(
            "sell",
            "neutral"
        );

        signalTitle.classList.remove(
            "buy",
            "sell",
            "neutral"
        );


        if(signal === "CALL"){

            signalCircle.classList.remove(
                "neutral"
            );

            arrow.classList.remove(
                "sell",
                "neutral"
            );

            signalCircle.classList.add(
                "buy"
            );

            arrow.textContent =
                "↗";

            signalTitle.textContent =
                "BUY (CALL)";

            signalTitle.classList.add(
                "buy"
            );

            direction.textContent =
                "UPWARD SIGNAL";

        }


        else if(signal === "PUT"){

            signalCircle.classList.add(
                "sell"
            );

            arrow.classList.add(
                "sell"
            );

            arrow.textContent =
                "↘";

            signalTitle.textContent =
                "SELL (PUT)";

            signalTitle.classList.add(
                "sell"
            );

            direction.textContent =
                "DOWNWARD SIGNAL";

        }


        else{

            signalCircle.classList.add(
                "neutral"
            );

            arrow.classList.add(
                "neutral"
            );

            arrow.textContent =
                "—";

            signalTitle.textContent =
                "NO TRADE";

            signalTitle.classList.add(
                "neutral"
            );

            direction.textContent =
                "WAIT FOR STRONGER CONFIRMATION";

        }


        let filled = "";
        let empty = "";


        for(
            let
