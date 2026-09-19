import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="XIGA Trading", page_icon="📈", layout="centered", initial_sidebar_state="collapsed")

# ---------------- SESSION STATE ----------------
def init_state():
    defaults = {
        "history": [], "signals": 0, "wins": 0, "losses": 0,
        "result": {"signal":"READY","strength":0,"description":"Select an asset and start analysis.","success":False},
        "page": "Trade",
    }
    for k,v in defaults.items():
        if k not in st.session_state: st.session_state[k] = v
init_state()

ASSETS = {
    "Forex": {"🇺🇸 🇪🇺 EUR/USD":"EUR/USD","🇬🇧 🇺🇸 GBP/USD":"GBP/USD","🇺🇸 🇯🇵 USD/JPY":"USD/JPY","🇦🇺 🇺🇸 AUD/USD":"AUD/USD","🇺🇸 🇨🇦 USD/CAD":"USD/CAD","🇺🇸 🇨🇭 USD/CHF":"USD/CHF","🇳🇿 🇺🇸 NZD/USD":"NZD/USD","🇪🇺 🇯🇵 EUR/JPY":"EUR/JPY","🇪🇺 🇬🇧 EUR/GBP":"EUR/GBP","🇬🇧 🇯🇵 GBP/JPY":"GBP/JPY"},
    "Stocks": {"🍎 Apple":"AAPL","🪟 Microsoft":"MSFT","🚗 Tesla":"TSLA","🛒 Amazon":"AMZN","💻 NVIDIA":"NVDA","🎬 Netflix":"NFLX","🔵 Meta":"META","💳 Visa":"V","🛩 Boeing":"BA","🤖 Palantir":"PLTR","⚙ AMD":"AMD","🪙 Coinbase":"COIN"},
    "Crypto": {"₿ Bitcoin":"BTC/USD","Ξ Ethereum":"ETH/USD","◎ Solana":"SOL/USD","🐕 Dogecoin":"DOGE/USD","🔷 Cardano":"ADA/USD","🟡 BNB":"BNB/USD","🔗 Chainlink":"LINK/USD","⚡ Litecoin":"LTC/USD","🔵 XRP":"XRP/USD"},
    "Commodities": {"🥇 Gold":"XAU/USD","🥈 Silver":"XAG/USD","🛢 WTI Crude Oil":"WTI/USD","🛢 Brent Oil":"BRENT/USD","🔥 Natural Gas":"NATGAS/USD"},
    "Indices": {"📊 S&P 500":"SPX","💻 NASDAQ 100":"NDX","🏦 Dow Jones":"DJI","🇩🇪 DAX":"DAX","🇬🇧 FTSE 100":"FTSE","🇯🇵 Nikkei 225":"N225"},
    "OTC": {"OTC EUR/USD":None,"OTC GBP/USD":None,"OTC USD/JPY":None,"OTC Gold":None,"OTC Silver":None,"OTC Apple":None,"OTC Microsoft":None,"OTC Tesla":None,"OTC Bitcoin":None,"OTC Ethereum":None},
}
TIMEFRAMES = {"1 MIN":"1min", "5 MIN":"5min"}

# ---------------- API ----------------
def get_api_key():
    try: return str(st.secrets["TWELVE_DATA_API_KEY"]).strip()
    except Exception: return ""

def get_candles(symbol, interval, outputsize=100):
    key = get_api_key()
    if not key: return [], "API KEY NOT FOUND"
    try:
        r = requests.get("https://api.twelvedata.com/time_series", params={"symbol":symbol,"interval":interval,"outputsize":outputsize,"format":"JSON"}, headers={"Authorization":"apikey " + key}, timeout=15)
        data = r.json()
        if r.status_code != 200: return [], f"API ERROR: {data.get('message',r.status_code)}"
        if data.get("status") == "error": return [], data.get("message","TWELVE DATA ERROR")
        vals = data.get("values",[])
        candles=[]
        for x in reversed(vals):
            try: candles.append({"open":float(x["open"]),"high":float(x["high"]),"low":float(x["low"]),"close":float(x["close"]),"datetime":x.get("datetime","")})
            except (KeyError,TypeError,ValueError): pass
        if len(candles)<60: return [], f"NOT ENOUGH DATA ({len(candles)} candles)"
        return candles,"LIVE DATA CONNECTED"
    except requests.exceptions.Timeout: return [],"MARKET DATA TIMEOUT"
    except requests.exceptions.RequestException as e: return [],f"NETWORK ERROR: {e}"
    except ValueError: return [],"INVALID API RESPONSE"
    except Exception as e: return [],f"ERROR: {e}"

def ema(values, period):
    if len(values)<period: return None
    m=2/(period+1); cur=sum(values[:period])/period
    for v in values[period:]: cur=(v-cur)*m+cur
    return cur

def rsi(values, period=14):
    if len(values)<period+1: return None
    gains=[]; losses=[]
    for i in range(1,len(values)):
        d=values[i]-values[i-1]; gains.append(max(d,0)); losses.append(max(-d,0))
    ag=sum(gains[:period])/period; al=sum(losses[:period])/period
    for i in range(period,len(gains)):
        ag=((ag*(period-1))+gains[i])/period; al=((al*(period-1))+losses[i])/period
    if al==0: return 100.0
    rs=ag/al
    return 100-(100/(1+rs))

def macd(values):
    if len(values)<35: return None,None
    fast,slow=ema(values,12),ema(values,26)
    if fast is None or slow is None: return None,None
    cur=fast-slow; prev=values[:-1]
    pf,ps=ema(prev,12),ema(prev,26)
    return cur,(pf-ps if pf is not None and ps is not None else None)

def analyze_market(symbol,timeframe):
    interval=TIMEFRAMES.get(timeframe)
    candles,status=get_candles(symbol,interval)
    if not candles:
        return {"success":False,"signal":"NO TRADE","strength":0,"description":status,"status":status}
    closes=[c["close"] for c in candles]; current=closes[-1]
    e9,e21,e50=ema(closes,9),ema(closes,21),ema(closes,50); rv=rsi(closes); mv,pm=macd(closes)
    score=0; reasons=[]
    if e9 is not None and e21 is not None:
        if e9>e21: score+=1; reasons.append("EMA 9 is above EMA 21")
        elif e9<e21: score-=1; reasons.append("EMA 9 is below EMA 21")
    if e21 is not None and e50 is not None:
        if e21>e50: score+=1; reasons.append("Medium-term trend is bullish")
        elif e21<e50: score-=1; reasons.append("Medium-term trend is bearish")
    if e21 is not None:
        if current>e21: score+=1; reasons.append("Price is above EMA 21")
        elif current<e21: score-=1; reasons.append("Price is below EMA 21")
    if rv is not None:
        if rv>=55: score+=1; reasons.append(f"RSI bullish ({rv:.1f})")
        elif rv<=45: score-=1; reasons.append(f"RSI bearish ({rv:.1f})")
        else: reasons.append(f"RSI neutral ({rv:.1f})")
    if mv is not None:
        if mv>0: score+=1; reasons.append("MACD is positive")
        elif mv<0: score-=1; reasons.append("MACD is negative")
        if pm is not None:
            if mv>pm: reasons.append("MACD momentum is rising")
            elif mv<pm: reasons.append("MACD momentum is falling")
    if len(closes)>=6:
        mom=closes[-1]-closes[-6]
        if mom>0: score+=1; reasons.append("Recent momentum is bullish")
        elif mom<0: score-=1; reasons.append("Recent momentum is bearish")
    strength=min(5,max(1,abs(score)))
    if score>=4:
        signal="CALL"; desc=f"Bullish confirmation. Score {score:+d}. This is an analysis signal, not a guarantee."
    elif score<=-4:
        signal="PUT"; desc=f"Bearish confirmation. Score {score:+d}. This is an analysis signal, not a guarantee."
    else:
        signal="NO TRADE"; desc=f"Mixed conditions. Score {score:+d}. Waiting for stronger confirmation."
    return {"success":True,"signal":signal,"strength":strength,"score":score,"price":current,"entry_candle_time":candles[-1]["datetime"],"rsi":rv,"macd":mv,"description":desc,"status":status,"reasons":reasons}

# ---------------- AUTOMATIC RESULT TRACKING ----------------
def candle_time_value(value):
    """Convert a Twelve Data candle timestamp to a comparable datetime."""
    if not value:
        return None
    text = str(value).strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
            try:
                return datetime.strptime(str(value).strip(), fmt)
            except ValueError:
                pass
    return None


def update_pending_results():
    changed = False

    pending = [
        x for x in st.session_state.history
        if x.get("status") == "PENDING"
        and x.get("signal") in ("CALL", "PUT")
        and x.get("symbol")
        and x.get("timeframe") in TIMEFRAMES
    ]

    groups = {}
    for item in pending:
        key = (item["symbol"], TIMEFRAMES[item["timeframe"]])
        groups.setdefault(key, []).append(item)

    for (symbol, interval), items in groups.items():

        candles, _ = get_candles(
            symbol,
            interval,
            outputsize=10
        )

        if len(candles) < 3:
            continue

        candle_times = [
            candle_time_value(c.get("datetime"))
            for c in candles
        ]

        for item in items:

            entry_time = candle_time_value(
                item.get("entry_candle_time")
            )

            if entry_time is None:
                continue

            # Find the first candle strictly after the signal candle.
            # We then require ONE candle after that result candle as
            # proof that the result candle has finished.
            newer_indexes = [
                i for i, candle_time in enumerate(candle_times)
                if candle_time is not None and candle_time > entry_time
            ]

            if not newer_indexes:
                continue

            result_index = newer_indexes[0]

            # The result candle must itself be completed.
            # If another candle has started after it, its close is final.
            if result_index + 1 >= len(candles):
                continue

            result_candle = candles[result_index]
            result_price = result_candle["close"]
            entry_price = float(item["price"])

            if item["signal"] == "CALL":
                if result_price > entry_price:
                    outcome = "WIN"
                elif result_price < entry_price:
                    outcome = "LOSS"
                else:
                    outcome = "DRAW"
            else:
                if result_price < entry_price:
                    outcome = "WIN"
                elif result_price > entry_price:
                    outcome = "LOSS"
                else:
                    outcome = "DRAW"

            item["status"] = outcome
            item["result_price"] = result_price
            item["result_candle_time"] = result_candle["datetime"]
            item["checked_at"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            if outcome == "WIN":
                st.session_state.wins += 1
            elif outcome == "LOSS":
                st.session_state.losses += 1

            changed = True

    return changed


try:
    fragment = st.fragment
except AttributeError:
    fragment = None


def tracker():
    changed = update_pending_results()

    if changed:
        # Force the complete Streamlit app to rerun so the
        # WIN/LOSS and historical win rate are immediately visible.
        try:
            st.rerun(scope="app")
        except TypeError:
            st.rerun()


# ---------------- CSS: ORIGINAL DESIGN ----------------
st.markdown("""
<style>
html,body,[data-testid="stAppViewContainer"]{background:radial-gradient(circle at 50% -10%,#173957 0%,#0a1c30 25%,#030914 62%,#020711 100%) !important}
[data-testid="stHeader"]{background:transparent !important}
[data-testid="stMainBlockContainer"]{max-width:500px !important;padding-top:12px !important;padding-left:12px !important;padding-right:12px !important}
.block-container{padding-bottom:25px !important}
.xiga-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}.xiga-menu{width:42px;height:42px;border-radius:13px;display:flex;align-items:center;justify-content:center;background:rgba(11,30,49,.88);border:1px solid #214967;color:#dceeff;font-size:21px}.xiga-brand{text-align:center;flex:1}.xiga-title{color:#fff;font-size:25px;font-weight:900;letter-spacing:1px}.xiga-title span{color:#28f3a5}.xiga-subtitle{margin-top:4px;color:#71859d;font-size:8px;letter-spacing:2px}.xiga-pro{min-width:66px;padding:9px 8px;text-align:center;border-radius:12px;background:linear-gradient(135deg,#3d2d0d,#1f1809);border:1px solid #9b741d;color:#ffd76a;font-size:10px;font-weight:800}
.xiga-card{background:linear-gradient(145deg,rgba(13,34,57,.96),rgba(5,16,29,.97));border:1px solid rgba(32,91,132,.72);border-radius:20px;box-shadow:0 18px 45px rgba(0,0,0,.32),inset 0 1px rgba(255,255,255,.035);padding:12px;margin-bottom:12px}
div[data-testid="stSelectbox"] label{color:#7d93aa !important;font-size:8px !important;letter-spacing:1.4px !important;text-transform:uppercase !important}div[data-baseweb="select"]>div{background:linear-gradient(145deg,rgba(9,39,64,.98),rgba(7,25,43,.98)) !important;border:1px solid #185276 !important;color:white !important;border-radius:12px !important}div[data-baseweb="select"] span{color:white !important}.xiga-market-status{color:#29f4a5;font-size:7px;margin-top:3px}
.xiga-signal{text-align:center;position:relative;overflow:hidden;min-height:560px}.xiga-signal:before{content:"";position:absolute;left:-10%;right:-10%;top:105px;height:190px;opacity:.22;background:repeating-linear-gradient(0deg,transparent 0px,transparent 45px,#226082 46px)}.xiga-signal-label{color:#8ca1b7;font-size:9px;letter-spacing:1.5px;text-transform:uppercase;position:relative}.xiga-asset{color:white;font-size:22px;font-weight:900;position:relative;margin-top:4px}.xiga-time{color:#28f3a5;font-size:9px;letter-spacing:1px;margin-top:4px;position:relative}
.xiga-circle{width:205px;height:205px;border-radius:50%;margin:25px auto 18px;display:flex;align-items:center;justify-content:center;position:relative}.xiga-circle.call{background:radial-gradient(circle,rgba(38,246,165,.43) 0%,rgba(14,74,61,.70) 35%,rgba(3,15,27,.98) 72%);border:3px solid #29f5a6;box-shadow:0 0 11px #29f5a6,0 0 35px rgba(41,245,166,.65),0 0 80px rgba(41,245,166,.22),inset 0 0 32px rgba(41,245,166,.27)}.xiga-circle.put{background:radial-gradient(circle,rgba(255,53,103,.42) 0%,rgba(82,17,41,.72) 35%,rgba(3,15,27,.98) 72%);border:3px solid #ff3d70;box-shadow:0 0 11px #ff3d70,0 0 35px rgba(255,61,112,.65),0 0 80px rgba(255,61,112,.22)}.xiga-circle.neutral{background:radial-gradient(circle,rgba(80,140,180,.28) 0%,rgba(17,46,68,.72) 35%,rgba(3,15,27,.98) 72%);border:3px solid #5e91b5;box-shadow:0 0 11px #5e91b5,0 0 35px rgba(94,145,181,.35)}.xiga-arrow{font-size:76px;font-weight:900;line-height:1}.call-text{color:#35f4a9;text-shadow:0 0 20px rgba(53,244,169,.3)}.put-text{color:#ff416f;text-shadow:0 0 20px rgba(255,65,111,.3)}.neutral-text{color:#8fb4cf}.xiga-signal-title{font-size:29px;font-weight:950;position:relative}.xiga-direction{color:#8597ac;font-size:9px;letter-spacing:2px;margin-top:4px}.xiga-stat{background:linear-gradient(145deg,rgba(7,29,49,.98),rgba(5,17,30,.98));border:1px solid #17557d;border-radius:15px;padding:13px 8px;text-align:center;min-height:100px}.xiga-stat-label{color:#8296ad;font-size:9px;text-transform:uppercase}.xiga-strength{color:#29f5a6;font-size:18px;margin-top:8px;letter-spacing:2px}.xiga-number{color:white;font-size:12px;font-weight:800;margin-top:3px}.xiga-win{color:#29f5a6;font-size:25px;font-weight:900;margin-top:6px}.xiga-ai{display:flex;gap:11px;align-items:center;margin-top:11px;padding:12px;text-align:left;border-radius:15px;background:linear-gradient(145deg,rgba(7,37,47,.97),rgba(5,19,31,.97));border:1px solid rgba(31,181,150,.55)}.xiga-ai-icon{width:35px;height:35px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#2af5a5;border:1px solid rgba(42,245,165,.48);flex-shrink:0}.xiga-ai-title{color:#2af5a5;font-size:11px;font-weight:900}.xiga-ai-desc{color:#7f92a7;font-size:8px;margin-top:3px}
.stButton>button{width:100%;height:55px;border-radius:16px;border:1px solid #5affaf;background:linear-gradient(100deg,#13ca87,#38f5ad);color:#03130d;font-size:14px;font-weight:900;box-shadow:0 8px 28px rgba(37,245,166,.20)}.stButton>button:hover{border-color:#5affaf;color:#03130d}.xiga-footer{text-align:center;margin-top:9px;color:#4f647a;font-size:7px;letter-spacing:.5px}
/* Keep Streamlit navigation compact and horizontal like the original design. */
div[role="radiogroup"]{display:flex !important;justify-content:center !important;gap:4px !important;flex-wrap:nowrap !important;margin:0 0 12px !important}div[role="radiogroup"] label{color:#8ca1b7 !important;font-size:10px !important;padding:5px 7px !important;white-space:nowrap !important}div[role="radiogroup"] label:has(input:checked){color:#29f5a6 !important}
</style>
""",unsafe_allow_html=True)

# tracker runs every 15 seconds without changing the page design
if fragment: 
    @st.fragment(run_every="15s")
    def auto_tracker(): tracker()
    auto_tracker()
else:
    tracker()

# ---------------- TOP BAR ----------------
st.markdown('''<div class="xiga-top"><div class="xiga-menu">☰</div><div class="xiga-brand"><div class="xiga-title"><span>▰</span> XIGA</div><div class="xiga-subtitle">TRADING SIGNAL BOT</div></div><div class="xiga-pro">👑 PRO</div></div>''',unsafe_allow_html=True)

nav_options=["Trade","History","Learn","Profile"]
selected_page=st.radio("Navigation",nav_options,index=nav_options.index(st.session_state.page),horizontal=True,label_visibility="collapsed",key="navigation")
st.session_state.page=selected_page

# ---------------- TRADE ----------------
if selected_page=="Trade":
    st.markdown('<div class="xiga-card">',unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1: category=st.selectbox("Asset",list(ASSETS.keys()),key="category")
    asset_names=list(ASSETS[category].keys())
    with col2: display_asset=st.selectbox("Market",asset_names,key="asset")
    timeframe=st.selectbox("Timeframe",list(TIMEFRAMES.keys()),index=0,key="timeframe")
    market_status="OTC DATA FEED REQUIRED" if category=="OTC" else "LIVE MARKET READY"
    st.markdown(f'<div class="xiga-market-status">● {market_status}</div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    result=st.session_state.result; signal=result.get("signal","READY")
    if signal=="CALL": circle_class="call";arrow="↗";title="BUY (CALL)";direction="UPWARD SIGNAL";title_class="call-text"
    elif signal=="PUT": circle_class="put";arrow="↘";title="SELL (PUT)";direction="DOWNWARD SIGNAL";title_class="put-text"
    elif signal=="NO TRADE": circle_class="neutral";arrow="—";title="NO TRADE";direction="WAIT FOR STRONGER CONFIRMATION";title_class="neutral-text"
    else: circle_class="neutral";arrow="◇";title="AI READY";direction="WAITING FOR ANALYSIS";title_class="neutral-text"
    clean_asset=display_asset
    for flag in ["🇺🇸","🇪🇺","🇬🇧","🇯🇵","🇦🇺","🇨🇦","🇨🇭","🇳🇿","🇩🇪"]: clean_asset=clean_asset.replace(flag,"")
    clean_asset=clean_asset.strip(); strength=int(result.get("strength",0)); filled="● "*strength; empty="● "*(5-strength)
    strength_html=(f'<span style="color:#29f5a6">{filled}</span><span style="color:#26394c">{empty}</span>' if strength else '<span style="color:#26394c">● ● ● ● ●</span>')
    total=st.session_state.wins+st.session_state.losses
    if total: win_display=f'{round(st.session_state.wins/total*100,1)}%'; win_status=f'● {st.session_state.wins} WINS • {st.session_state.losses} LOSSES'
    else: win_display="—";win_status="● WAITING FOR RESULTS"
    ai_title="AI ANALYSIS COMPLETE" if result.get("success") else "AI ENGINE READY"
    st.markdown(f'''<div class="xiga-card xiga-signal"><div class="xiga-signal-label">SIGNAL FOR</div><div class="xiga-asset">{clean_asset}</div><div class="xiga-time">● TIMEFRAME: {timeframe}</div><div class="xiga-circle {circle_class}"><div class="xiga-arrow">{arrow}</div></div><div class="xiga-signal-title {title_class}">{title}</div><div class="xiga-direction">{direction}</div><br><div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;"><div class="xiga-stat"><div class="xiga-stat-label">SIGNAL STRENGTH</div><div class="xiga-strength">{strength_html}</div><div class="xiga-number">{strength}/5</div></div><div class="xiga-stat"><div class="xiga-stat-label">WIN RATE</div><div class="xiga-win">{win_display}</div><div style="color:#29f5a6;font-size:8px;margin-top:3px;">{win_status}</div></div></div><div class="xiga-ai"><div class="xiga-ai-icon">✓</div><div><div class="xiga-ai-title">{ai_title}</div><div class="xiga-ai-desc">{result.get("description","Select an asset and start analysis.")}</div></div></div></div>''',unsafe_allow_html=True)

    analyze_clicked=st.button("⚡ ANALYZE MARKET",key="analyze_button",use_container_width=True)
    if analyze_clicked:
        if category=="OTC":
            st.session_state.result={"success":False,"signal":"NO TRADE","strength":0,"description":"Pocket Option OTC prices use a separate feed. XIGA will not invent an OTC signal.","status":"OTC DATA FEED REQUIRED"};st.rerun()
        symbol=ASSETS[category][display_asset]
        with st.spinner("Connecting to live market data..."): analysis=analyze_market(symbol,timeframe)
        if analysis.get("success") and analysis.get("signal") in ("CALL","PUT"):
            st.session_state.signals+=1
            st.session_state.history.insert(0,{"time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"asset":clean_asset,"symbol":symbol,"timeframe":timeframe,"signal":analysis["signal"],"strength":analysis["strength"],"price":analysis.get("price","—"),"entry_candle_time":analysis.get("entry_candle_time",""),"status":"PENDING"})
            st.session_state.history=st.session_state.history[:100]
        st.session_state.result=analysis;st.rerun()
    st.markdown('<div class="xiga-footer">🔒 SECURE • XIGA AI • V5.1 • LIVE ANALYSIS</div>',unsafe_allow_html=True)

# ---------------- HISTORY ----------------
elif selected_page=="History":
    st.markdown('<div class="xiga-card">',unsafe_allow_html=True);st.markdown("### 📊 XIGA Trade History")
    if not st.session_state.history: st.info("No signals have been generated yet.")
    else:
        for item in st.session_state.history[:30]:
            result_price=item.get("result_price","—"); result_time=item.get("result_candle_time","—")
            status=item.get("status","PENDING")
            st.markdown(f'''**{item["asset"]}**  
Signal: **{item["signal"]}**  
Strength: **{item["strength"]}/5**  
Entry Price: `{item["price"]}`  
Result Price: `{result_price}`  
Timeframe: `{item["timeframe"]}`  
Signal Time: `{item["time"]}`  
Result Candle: `{result_time}`  
Status: **{status}**  
---''')
    st.markdown('</div>',unsafe_allow_html=True)

# ---------------- LEARN ----------------
elif selected_page=="Learn":
    st.markdown('<div class="xiga-card">',unsafe_allow_html=True);st.markdown("### 📚 XIGA Learn");st.markdown("""### 📈 EMA
Moving averages help identify the direction of a market trend.

### 📊 RSI
RSI measures recent price momentum.

### 📉 MACD
MACD compares moving averages to help identify momentum.

### 🟢 CALL
A CALL means the configured indicators currently show stronger bullish conditions.

### 🔴 PUT
A PUT means the configured indicators currently show stronger bearish conditions.

### ⚪ NO TRADE
When the indicators are mixed, XIGA does not force a directional signal.

### ⚠️ Important
Signals are analysis only. Markets can move unexpectedly and no signal guarantees a winning trade.
""");st.markdown('</div>',unsafe_allow_html=True)

# ---------------- PROFILE ----------------
elif selected_page=="Profile":
    st.markdown('<div class="xiga-card">',unsafe_allow_html=True);st.markdown("### 👤 XIGA Profile")
    st.metric("Total Signals",st.session_state.signals);completed=st.session_state.wins+st.session_state.losses;st.metric("Completed Results",completed)
    st.metric("Historical Win Rate",f'{round(st.session_state.wins/completed*100,1)}%' if completed else "—")
    st.caption("Win rate is calculated only from actual completed results recorded by XIGA.");st.markdown('</div>',unsafe_allow_html=True)

st.caption("XIGA is a market-analysis assistant. It does not automatically place trades.")
