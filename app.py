import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="XIGA Trading",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

APP = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

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
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}

body{
    color:#fff;
}

button,
select{
    font-family:inherit;
}

.app{
    width:100%;
    max-width:470px;
    min-height:100vh;
    margin:auto;
    padding:15px 14px 25px;

    background:
        radial-gradient(
            circle at 50% -15%,
            #173957 0%,
            #0a1c30 27%,
            #030914 65%,
            #020711 100%
        );

    overflow:hidden;
}

/* ==============================
   TOP BAR
   ============================== */

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

    background:
        linear-gradient(
            135deg,
            #3d2d0d,
            #1f1809
        );

    border:1px solid #9b741d;

    color:#ffd76a;
    font-size:10px;
    font-weight:800;
}

/* ==============================
   GLASS
   ============================== */

.glass{
    background:
        linear-gradient(
            145deg,
            rgba(13,34,57,.96),
            rgba(5,16,29,.97)
        );

    border:1px solid rgba(32,91,132,.72);

    border-radius:20px;

    box-shadow:
        0 18px 45px rgba(0,0,0,.32),
        inset 0 1px rgba(255,255,255,.035);
}

/* ==============================
   MARKET BAR
   ============================== */

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

    background:
        linear-gradient(
            145deg,
            rgba(9,39,64,.98),
            rgba(7,25,43,.98)
        );

    border:1px solid #185276;
}

.market-label{
    color:#7d93aa;
    font-size:8px;
    letter-spacing:1.4px;
    text-transform:uppercase;
    margin-bottom:3px;
}

.market-row{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:5px;
}

select{
    width:100%;
    appearance:none;
    -webkit-appearance:none;

    border:0;
    outline:0;

    background:transparent;

    color:white;

    font-size:14px;
    font-weight:800;

    padding:2px 0;
}

select option{
    background:#0b1727;
    color:white;
}

.market-status{
    color:#29f4a5;
    font-size:7px;
    margin-top:2px;
}

/* ==============================
   SIGNAL CARD
   ============================== */

.signal-card{
    position:relative;
    overflow:hidden;

    min-height:545px;

    padding:17px 12px 13px;

    text-align:center;
}

/* ==============================
   CHART
   ============================== */

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

/* ==============================
   SIGNAL HEADER
   ============================== */

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

/* ==============================
   SIGNAL CIRCLE
   ============================== */

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

    background:
        radial-gradient(
            circle,
            rgba(38,246,165,.43) 0%,
            rgba(14,74,61,.70) 35%,
            rgba(3,15,27,.98) 72%
        );

    border:3px solid #29f5a6;

    box-shadow:
        0 0 11px #29f5a6,
        0 0 35px rgba(41,245,166,.65),
        0 0 80px rgba(41,245,166,.22),
        inset 0 0 32px rgba(41,245,166,.27);

    transition:
        .35s ease;
}

.signal-circle.sell{
    background:
        radial-gradient(
            circle,
            rgba(255,53,103,.42) 0%,
            rgba(82,17,41,.72) 35%,
            rgba(3,15,27,.98) 72%
        );

    border-color:#ff3d70;

    box-shadow:
        0 0 11px #ff3d70,
        0 0 35px rgba(255,61,112,.65),
        0 0 80px rgba(255,61,112,.22),
        inset 0 0 32px rgba(255,61,112,.27);
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

    text-shadow:
        0 0 10px #29f5a6,
        0 0 28px rgba(41,245,166,.85);

    transition:.3s ease;
}

.arrow.sell{
    color:#ff688d;

    text-shadow:
        0 0 10px #ff3d70,
        0 0 28px rgba(255,61,112,.85);
}

/* ==============================
   SIGNAL TITLE
   ============================== */

.signal-title{
    position:relative;
    z-index:5;

    font-size:30px;
    font-weight:950;
    letter-spacing:-.4px;
}

.signal-title.buy{
    color:#35f4a9;

    text-shadow:
        0 0 20px rgba(53,244,169,.3);
}

.signal-title.sell{
    color:#ff416f;

    text-shadow:
        0 0 20px rgba(255,65,111,.3);
}

.direction{
    position:relative;
    z-index:5;

    margin-top:4px;

    color:#8597ac;

    font-size:9px;
    letter-spacing:2px;
}

/* ==============================
   STATS
   ============================== */

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

    background:
        linear-gradient(
            145deg,
            rgba(7,29,49,.98),
            rgba(5,17,30,.98)
        );

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

.red{
    color:#ff416f;
    text-shadow:0 0 9px rgba(255,65,111,.7);
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

/* ==============================
   AI STATUS
   ============================== */

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

    background:
        linear-gradient(
            145deg,
            rgba(7,37,47,.97),
            rgba(5,19,31,.97)
        );

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

/* ==============================
   MAIN BUTTON
   ============================== */

.generate{
    width:100%;

    height:55px;

    margin-top:11px;

    border-radius:16px;

    border:1px solid #5affaF;

    background:
        linear-gradient(
            100deg,
            #13ca87,
            #38f5ad
        );

    color:#03130d;

    font-size:14px;

    font-weight:900;

    cursor:pointer;

    box-shadow:
        0 8px 28px rgba(37,245,166,.20);

    transition:.18s ease;
}

.generate:active{
    transform:scale(.98);
}

.generate:hover{
    filter:brightness(1.06);
}

/* ==============================
   COUNTDOWN
   ============================== */

.countdown{
    position:relative;
    z-index:5;

    display:none;

    margin-top:8px;

    color:#a6b6c9;

    font-size:9px;
}

.countdown span{
    color:#29f5a6;

    font-weight:900;
}

/* ==============================
   BOTTOM NAV
   ============================== */

.bottom{
    display:grid;

    grid-template-columns:
        repeat(4,1fr);

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

    background:
        radial-gradient(
            circle,
            rgba(41,245,166,.12),
            transparent 75%
        );
}

.nav-icon{
    display:block;

    font-size:19px;

    line-height:20px;

    margin-bottom:3px;
}

/* ==============================
   FOOTER
   ============================== */

.footer{
    text-align:center;

    margin-top:9px;

    color:#4f647a;

    font-size:7px;

    letter-spacing:.5px;
}

/* ==============================
   SMALL PHONES
   ============================== */

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

</style>
</head>

<body>

<div class="app">

    <!-- ================= HEADER ================= -->

    <div class="topbar">

        <div class="menu">
            ☰
        </div>

        <div class="brand">

            <div class="brand-title">
                <span>▰</span> XIGA
            </div>

            <div class="brand-subtitle">
                TRADING SIGNAL BOT
            </div>

        </div>

        <div class="pro">
            👑 PRO
        </div>

    </div>


    <!-- ================= MARKET ================= -->

    <div class="glass market">

        <div class="market-box">

            <div class="market-label">
                Asset
            </div>

            <select id="asset">

                <option>🇺🇸 🇪🇺  EUR/USD</option>
                <option>🇬🇧 🇺🇸  GBP/USD</option>
                <option>🇺🇸 🇯🇵  USD/JPY</option>
                <option>🇦🇺 🇺🇸  AUD/USD</option>
                <option>🇺🇸 🇨🇦  USD/CAD</option>
                <option>🥇  XAU/USD</option>

            </select>

            <div class="market-status">
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
                <option>1 MIN</option>
                <option>5 MIN</option>

            </select>

            <div class="market-status">
                ● ANALYSIS READY
            </div>

        </div>

    </div>


    <!-- ================= SIGNAL ================= -->

    <div class="glass signal-card">


        <!-- CHART -->

        <svg
            class="chart"
            viewBox="0 0 500 220"
            preserveAspectRatio="none"
        >

            <line class="grid"
                x1="0" y1="35"
                x2="500" y2="35"/>

            <line class="grid"
                x1="0" y1="85"
                x2="500" y2="85"/>

            <line class="grid"
                x1="0" y1="135"
                x2="500" y2="135"/>

            <line class="grid"
                x1="0" y1="185"
                x2="500" y2="185"/>


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


            <!-- candles -->

            <line class="candle-green"
                x1="35" y1="180"
                x2="35" y2="135"/>

            <rect class="candle-green"
                x="29" y="145"
                width="12"
                height="25"
                rx="2"/>


            <line class="candle-red"
                x1="72" y1="170"
                x2="72" y2="125"/>

            <rect class="candle-red"
                x="66" y="135"
                width="12"
                height="25"
                rx="2"/>


            <line class="candle-green"
                x1="110" y1="150"
                x2="110" y2="105"/>

            <rect class="candle-green"
                x="104" y="115"
                width="12"
                height="25"
                rx="2"/>


            <line class="candle-green"
                x1="148" y1="135"
                x2="148" y2="88"/>

            <rect class="candle-green"
                x="142" y="98"
                width="12"
                height="25"
                rx="2"/>


            <line class="candle-red"
                x1="186" y1="145"
                x2="186" y2="95"/>

            <rect class="candle-red"
                x="180" y="105"
                width="12"
                height="28"
                rx="2"/>


            <line class="candle-green"
                x1="224" y1="115"
                x2="224" y2="65"/>

            <rect class="candle-green"
                x="218" y="75"
                width="12"
                height="28"
                rx="2"/>


            <line class="candle-green"
                x1="262" y1="105"
                x2="262" y2="50"/>

            <rect class="candle-green"
                x="256" y="58"
                width="12"
                height="30"
                rx="2"/>


            <line class="candle-red"
                x1="300" y1="115"
                x2="300" y2="62"/>

            <rect class="candle-red"
                x="294" y="72"
                width="12"
                height="28"
                rx="2"/>


            <line class="candle-green"
                x1="338" y1="85"
                x2="338" y2="38"/>

            <rect class="candle-green"
                x="332" y="45"
                width="12"
                height="27"
                rx="2"/>


            <line class="candle-green"
                x1="376" y1="70"
                x2="376" y2="25"/>

            <rect class="candle-green"
                x="370" y="31"
                width="12"
                height="27"
                rx="2"/>


            <line class="candle-red"
                x1="414" y1="82"
                x2="414" y2="35"/>

            <rect class="candle-red"
                x="408" y="43"
                width="12"
                height="26"
                rx="2"/>


            <line class="candle-green"
                x1="452" y1="52"
                x2="452" y2="10"/>

            <rect class="candle-green"
                x="446" y="17"
                width="12"
                height="25"
                rx="2"/>

        </svg>


        <!-- SIGNAL HEADER -->

        <div class="signal-label">
            SIGNAL FOR
        </div>

        <div
            class="asset-name"
            id="signalAsset"
        >
            EUR/USD
        </div>

        <div
            class="time-label"
            id="signalTime"
        >
            ● TIMEFRAME: 10 SEC
        </div>


        <!-- SIGNAL CIRCLE -->

        <div
            class="signal-circle"
            id="signalCircle"
        >

            <div class="inner-ring"></div>

            <div
                class="arrow"
                id="arrow"
            >
                ◇
            </div>

        </div>


        <!-- TITLE -->

        <div
            class="signal-title buy"
            id="signalTitle"
        >
            AI READY
        </div>

        <div
            class="direction"
            id="direction"
        >
            WAITING FOR ANALYSIS
        </div>


        <!-- STATS -->

        <div class="stats">


            <div class="stat">

                <div class="stat-label">
                    Signal Strength
                </div>

                <div
                    class="dots green"
                    id="strengthDots"
                >
                    ● ● ● ●
                    <span class="empty">●</span>
                </div>

                <div
                    class="stat-number"
                    id="strengthText"
                >
                    4/5
                </div>

            </div>


            <div class="stat">

                <div class="stat-label">
                    Win Rate
                </div>

                <div
                    class="win"
                    id="winRate"
                >
                    —
                </div>

                <div class="no-data">
                    ● NO REAL DATA YET
                </div>

            </div>

        </div>


        <!-- AI -->

        <div class="ai">

            <div class="ai-icon">
                ✓
            </div>

            <div>

                <div
                    class="ai-title"
                    id="aiTitle"
                >
                    AI ENGINE READY
                </div>

                <div
                    class="ai-description"
                    id="aiDescription"
                >
                    Select an asset and start analysis
                </div>

            </div>

        </div>


    </div>


    <!-- ================= ACTION ================= -->

    <button
        class="generate"
        id="generate"
    >
        ⚡ ANALYZE MARKET
    </button>


    <div
        class="countdown"
        id="countdown"
    >
        Signal generated • Expires in
        <span id="seconds">15</span>s
    </div>


    <!-- ================= NAV ================= -->

    <div class="bottom">

        <div
            class="nav active"
            onclick="setNav(this)"
        >
            <span class="nav-icon">⌁</span>
            Trade
        </div>

        <div
            class="nav"
            onclick="setNav(this)"
        >
            <span class="nav-icon">◷</span>
            History
        </div>

        <div
            class="nav"
            onclick="setNav(this)"
        >
            <span class="nav-icon">▣</span>
            Learn
        </div>

        <div
            class="nav"
            onclick="setNav(this)"
        >
            <span class="nav-icon">♙</span>
            Profile
        </div>

    </div>


    <div class="footer">
        🔒 SECURE • XIGA AI • V4.0 • DEMO MODE
    </div>

</div>


<script>

/* ==========================================
   ELEMENTS
   ========================================== */

const asset = document.getElementById("asset");
const timeframe = document.getElementById("timeframe");

const signalAsset = document.getElementById("signalAsset");
const signalTime = document.getElementById("signalTime");

const signalCircle = document.getElementById("signalCircle");
const arrow = document.getElementById("arrow");

const signalTitle = document.getElementById("signalTitle");
const direction = document.getElementById("direction");

const strengthDots = document.getElementById("strengthDots");
const strengthText = document.getElementById("strengthText");

const aiTitle = document.getElementById("aiTitle");
const aiDescription = document.getElementById("aiDescription");

const generate = document.getElementById("generate");

const countdown = document.getElementById("countdown");
const seconds = document.getElementById("seconds");


/* ==========================================
   UPDATE MARKET DISPLAY
   ========================================== */

function updateMarket(){

    let cleanAsset = asset.value
        .replace("🇺🇸 🇪🇺  ","")
        .replace("🇬🇧 🇺🇸  ","")
        .replace("🇺🇸 🇯🇵  ","")
        .replace("🇦🇺 🇺🇸  ","")
        .replace("🇺🇸 🇨🇦  ","")
        .replace("🥇  ","");

    signalAsset.innerText = cleanAsset;

    signalTime.innerText =
        "● TIMEFRAME: " + timeframe.value;
}

asset.addEventListener("change", updateMarket);
timeframe.addEventListener("change", updateMarket);


/* ==========================================
   SIGNAL GENERATOR
   ========================================== */

let timer = null;

generate.addEventListener("click", function(){

    updateMarket();

    /* visual processing */

    generate.innerText = "◌ ANALYZING MARKET...";
    generate.disabled = true;

    aiTitle.innerText = "AI ANALYZING...";
    aiDescription.innerText =
        "Processing market conditions...";

    signalTitle.innerText = "ANALYZING";
    signalTitle.className =
        "signal-title buy";

    direction.innerText =
        "PROCESSING MARKET DATA";

    arrow.innerText = "◌";

    setTimeout(function(){

        const signal =
            Math.random() < 0.5
            ? "CALL"
            : "PUT";

        const strength =
            Math.floor(Math.random()*3)+3;

        showSignal(signal,strength);

        generate.disabled = false;
        generate.innerText =
            "↻ GENERATE NEW SIGNAL";

    },1200);

});


/* ==========================================
   SHOW SIGNAL
   ========================================== */

function showSignal(signal,strength){

    signalCircle.classList.remove("sell");
    arrow.classList.remove("sell");
    signalTitle.classList.remove("sell");
    signalTitle.classList.remove("buy");

    if(signal === "CALL"){

        arrow.innerText = "↗";

        signalTitle.innerText =
            "BUY (CALL)";

        signalTitle.classList.add("buy");

        direction.innerText =
            "UPWARD SIGNAL";

        aiTitle.innerText =
            "AI ANALYSIS COMPLETE";

        aiDescription.innerText =
            "Demo signal generated successfully";

    }else{

        signalCircle.classList.add("sell");
        arrow.classList.add("sell");

        arrow.innerText = "↘";

        signalTitle.innerText =
            "SELL (PUT)";

        signalTitle.classList.add("sell");

        direction.innerText =
            "DOWNWARD SIGNAL";

        aiTitle.innerText =
            "AI ANALYSIS COMPLETE";

        aiDescription.innerText =
            "Demo signal generated successfully";

    }


    /* strength */

    let filled = "";

    for(let i=0;i<strength;i++){
        filled += "● ";
    }

    let empty = "";

    for(let i=strength;i<5;i++){
        empty += "● ";
    }

    strengthDots.innerHTML =
        filled +
        '<span class="empty">' +
        empty +
        '</span>';

    strengthText.innerText =
        strength + "/5";


    /* countdown */

    let count = 15;

    seconds.innerText = count;

    countdown.style.display = "block";

    if(timer){
        clearInterval(timer);
    }

    timer = setInterval(function(){

        count--;

        seconds.innerText = count;

        if(count <= 0){

            clearInterval(timer);

            countdown.style.display =
                "none";

        }

    },1000);

}


/* ==========================================
   NAVIGATION VISUAL
   ========================================== */

function setNav(element){

    document
        .querySelectorAll(".nav")
        .forEach(function(item){

            item.classList.remove("active");

        });

    element.classList.add("active");

}

</script>

</body>
</html>
"""

components.html(
    APP,
    height=900,
    scrolling=False
)
