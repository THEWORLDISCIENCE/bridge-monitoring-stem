import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(
    page_title="Intelligent Bridge Monitoring",
    page_icon="🌉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
#MainMenu,
header,
footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"]{
    display:none!important;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main,
.block-container{
    padding:0!important;
    margin:0!important;
    max-width:100%!important;
    background:#8ecae6!important;
}
</style>
""", unsafe_allow_html=True)

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html>
<head>

<meta charset="utf-8">

<meta
name="viewport"
content="width=device-width, initial-scale=1.0">

<title>
Intelligent Bridge Monitoring
</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<style>

:root{

 --hud:#55e7ff;
 --hud-soft:#9cefff;
 --panel:#071d32;
 --panel2:#0b3555;
 --bg:#8fcfe8;
}

*{
 box-sizing:border-box;
 margin:0;
 padding:0;
}

html,
body{

 width:100%;
 height:100%;

 overflow:hidden;

 background:var(--bg);

 font-family:
 Inter,
 Segoe UI,
 sans-serif;
}

#app{

 position:fixed;
 inset:0;
}

#renderCanvas{

 position:absolute;
 inset:0;

 width:100%;
 height:100%;

 display:block;
}

.panel{

 position:absolute;

 background:
 linear-gradient(
 180deg,
 rgba(4,20,34,.88),
 rgba(6,40,65,.65)
 );

 border:
 1px solid rgba(110,235,255,.22);

 backdrop-filter:blur(22px);

 border-radius:18px;

 color:white;

 box-shadow:
 0 0 35px rgba(0,200,255,.18),
 inset 0 0 20px rgba(255,255,255,.04);
}

#topBar{

 left:12px;
 right:12px;
 top:12px;

 height:72px;

 display:flex;
 justify-content:space-between;
 align-items:center;

 padding:16px;
}

.title{

 font-size:24px;
 font-weight:900;
 letter-spacing:2px;
}

.subtitle{

 color:#8dddfa;

 font-size:10px;

 letter-spacing:3px;
}

.statusContainer{

 display:flex;
 gap:10px;
}

.badge{

 padding:8px 14px;

 border-radius:30px;

 background:
 rgba(0,150,200,.18);

 border:
 1px solid rgba(0,230,255,.25);
}

#leftPanel{

 top:100px;
 bottom:140px;
 left:12px;

 width:280px;

 overflow:auto;
}

#rightPanel{

 top:100px;
 bottom:140px;
 right:12px;

 width:320px;

 overflow:auto;
}

.panelBody{
 padding:18px;
}

.sectionTitle{

 color:#7fe8ff;

 font-size:11px;

 letter-spacing:2px;

 margin-bottom:12px;

 font-weight:800;
}

.metricGrid{

 display:grid;

 grid-template-columns:1fr 1fr;

 gap:8px;
}

.metric{

 background:
 rgba(255,255,255,.05);

 border:
 1px solid rgba(255,255,255,.06);

 border-radius:10px;

 padding:10px;
}

.metricLabel{

 font-size:10px;

 color:#9bc6d8;
}

.metricValue{

 font-size:24px;

 font-weight:900;

 color:var(--hud);
}

#bottomPanel{

 left:12px;
 right:12px;
 bottom:12px;

 height:112px;

 display:grid;

 grid-template-columns:
 1fr
 1fr
 2fr
 1fr;

 gap:10px;

 padding:12px;
}

.card{

 background:
 rgba(255,255,255,.04);

 border-radius:12px;

 padding:10px;
}

.small{

 font-size:10px;
 color:#a8d3e5;
}

.big{

 font-size:26px;

 font-weight:900;
}

button{

 width:100%;

 background:
 linear-gradient(
 135deg,
 #18b8d5,
 #4876ff
 );

 color:white;

 border:none;

 border-radius:8px;

 padding:10px;

 margin-top:8px;

 cursor:pointer;
}

input[type=range]{

 width:100%;
 margin-top:6px;
 margin-bottom:8px;
}

</style>

</head>

<body>

<div id="app">

<canvas id="renderCanvas"></canvas>

<div id="topBar" class="panel">

<div>
<div class="title">
INTELLIGENT BRIDGE MONITORING
</div>

<div class="subtitle">
DIGITAL TWIN • STRUCTURAL HEALTH • AI ANALYTICS
</div>
</div>

<div class="statusContainer">

<div class="badge">
🟢 SYSTEM ONLINE
</div>

<div class="badge">
55 SENSORS ACTIVE
</div>

<div class="badge" id="clock">
00:00:00
</div>

</div>

</div>

<div id="leftPanel" class="panel">

<div class="panelBody">

<div class="sectionTitle">
SIMULATION CONTROL
</div>

<label>Vehicle Weight</label>
<input id="weight" type="range" min="5" max="50" value="18">

<label>Vehicle Speed</label>
<input id="speed" type="range" min="10" max="120" value="55">

<label>Traffic Volume</label>
<input id="traffic" type="range" min="0" max="100" value="65">

<button>
START ANALYSIS
</button>

<button>
RESET MODEL
</button>

</div>

</div>

<div id="rightPanel" class="panel">

<div class="panelBody">

<div class="sectionTitle">
LIVE TELEMETRY
</div>

<div class="metricGrid">

<div class="metric">
<div class="metricLabel">
DEFLECTION
</div>
<div class="metricValue" id="deflection">
2.4
</div>
</div>

<div class="metric">
<div class="metricLabel">
STRAIN
</div>
<div class="metricValue" id="strain">
118
</div>
</div>

<div class="metric">
<div class="metricLabel">
VIBRATION
</div>
<div class="metricValue" id="vibration">
0.12
</div>
</div>

<div class="metric">
<div class="metricLabel">
TEMP
</div>
<div class="metricValue" id="temp">
27
</div>
</div>

</div>

</div>

</div>

<div id="bottomPanel" class="panel">

<div class="card">
<div class="small">TRAFFIC</div>
<div class="big">65%</div>
</div>

<div class="card">
<div class="small">HEALTH</div>
<div class="big">97%</div>
</div>

<div class="card">
<div class="small">AI ANALYSIS</div>
Bridge operating within
expected structural limits.
</div>

<div class="card">
<div class="small">STATUS</div>
<div class="big">NORMAL</div>
</div>

</div>

</div>

<script>

setInterval(()=>{

const now=new Date();

document.getElementById("clock")
.innerText=
now.toLocaleTimeString();

},1000);

</script>

</body>
</html>
"""

components.html(
    HTML_TEMPLATE,
    height=1080,
    scrolling=False
)
<script>

const canvas =
document.getElementById("renderCanvas");

const ctx =
canvas.getContext("2d");

function resize(){

 canvas.width = window.innerWidth;
 canvas.height = window.innerHeight;

}

resize();

window.addEventListener(
"resize",
resize
);

const sensors = [];

for(let i=0;i<50;i++){

 sensors.push({

  x:100 + i*15,
  y:250 + Math.sin(i)*25,

  pulse:
  Math.random()*100

 });

}

const vehicles=[];

for(let i=0;i<4;i++){

 vehicles.push({

  x:-200 - i*120,
  speed:2 + Math.random()*2

 });

}

let t=0;

function drawSky(){

 const grad =
 ctx.createLinearGradient(
  0,
  0,
  0,
  canvas.height
 );

 grad.addColorStop(
<script>

const hud =
document.createElement("div");

hud.style.position = "absolute";
hud.style.top = "100px";
hud.style.left = "50%";
hud.style.transform =
"translateX(-50%)";

hud.style.width = "380px";
hud.style.height = "180px";

hud.style.background =
"rgba(5,25,40,.55)";

hud.style.border =
"1px solid rgba(100,255,255,.2)";

hud.style.backdropFilter =
"blur(16px)";

hud.style.borderRadius =
"16px";

hud.style.color =
"white";

hud.style.padding =
"18px";

hud.style.zIndex="50";

hud.innerHTML = `

<div style="
font-size:12px;
letter-spacing:2px;
color:#79eaff;
margin-bottom:8px;
">
AI ANOMALY DETE
<script>

//
// DIGITAL TWIN MINIMAP
//

const minimap =
document.createElement("canvas");

minimap.width = 220;
minimap.height = 140;

minimap.style.position = "absolute";
minimap.style.right = "340px";
minimap.style.top = "100px";

minimap.style.zIndex = "55";

minimap.style.background =
"rgba(5,25,40,.55)";

minimap.style.border =
"1px solid rgba(0,255,255,.2)";

minimap.style.borderRadius =
"12px";

document.body.appendChild(
minimap
);

const mctx =
minimap.getContext("2d");

//
// HEATMAP PANEL
//

const heatPanel =
document.createElement("div");

heatPanel.style.position =
"absolute";

heatPanel.style.right = "340px";

heatPanel.style.top = "260px";

heatPanel.style.width = "220px";

heatPanel.style.height = "180px";

heatPanel.style.zIndex = "55";

heatPanel.style.background =
"rgba(5,25,40,.55)";

heatPanel.style.backdropFilter =
"blur(14px)";

heatPanel.style.border =
"1px solid rgba(0,255,255,.2)";

heatPanel.style.borderRadius =
"12px";

heatPanel.style.padding =
"12px";

heatPanel.innerHTML = `

<div style="
color:#78ecff;
font-size:11px;
letter-spacing
<script>

//
// SCANNING GRID OVERLAY
//

const scanGrid =
document.createElement("canvas");

scanGrid.width =
window.innerWidth;

scanGrid.height =
window.innerHeight;

scanGrid.style.position =
"absolute";

scanGrid.style.inset =
"0";

scanGrid.style.pointerEvents =
"none";

scanGrid.style.opacity =
".25";

scanGrid.style.zIndex =
"2";

document.body.appendChild(
scanGrid
);

const gctx =
scanGrid.getContext("2d");

function drawGrid(){

 gctx.clearRect(
 0,
 0,
 scanGrid.width,
 scanGrid.height
 );

 gctx.strokeStyle =
 "rgba(0,255,255,.12)";

 for(
 let x=0;
 x<scanGrid.width;
 x+=40
 ){

  gctx.beginPath();

  gctx.moveTo(x,0);

  gctx.lineTo(
   x,
   scanGrid.height
  );

  gctx.stroke();

 }

 for(
 let y=0;
 y<scanGrid.height;
 y+=40
 ){

  gctx.beginPath();

  gctx.moveTo(0,y);

  gctx.lineTo(
   scanGrid.
      <script>

//
// MISSION CONTROL PANEL
//

const mission =
document.createElement("div");

mission.style.position =
"absolute";

mission.style.left =
"850px";

mission.style.top =
"100px";

mission.style.width =
"280px";

mission.style.height =
"290px";

mission.style.background =
"rgba(5,20,35,.70)";

mission.style.border =
"1px solid rgba(0,255,255,.18)";

mission.style.borderRadius =
"16px";

mission.style.padding =
"15px";

mission.style.zIndex =
"80";

mission.style.color =
"white";

mission.innerHTML = `

<div style="
color:#69f1ff;
font-size:11px;
font-weight:800;
letter-spacing:2px;
margin-bottom:12px;
">
MISSION CONTROL
</div>

<div style="
display:flex;
justify-content:center;
margin-bottom:12px;
">
<canvas
id="healthGauge"
width="180"
height="100">
</canvas>
</div>

<div id="healthLabel"
style="
text-align:center;
font-size:28px;
font-weight:900;
color:#57ffd0;
">
98%
</div>

<div style="
text-align:center;
font-size:10px;
color:#9ed9eb;
">
OVERALL STRUCTURAL HEALTH
</div>

<div style="
margin-top:14px;
font-size:10px;
color:#99d6e9;">
SATELLITE LINK:
<span id="linkStatus"
style="color:#5cffae">
ONLINE
</span>
</div>

<div style="
margin-top:8px;
font-size:10px;
color:#99d6e9;">
AI CONFIDENCE:
<span id="aiConfidence"
style="color:#6deeff">
99.2%
</span>
</div>

`;

document.body.appendChild(
mission
);

//
// MAINTENANCE FORECAST BOX
//

const maintenance =
document.createElement("div");

maintenance.style.position =
"absolute";

maintenance.style.left =
"850px";

maintenance.style.top =
"410px";

maintenance.style.width =
"280px";

maintenance.style.background =
"rgba(5,20,35,.70)";

maintenance.style.border =
"1px solid rgba(0,255,255,.18)";

maintenance.style.borderRadius =
"16px";
<script>

//
// COMMAND CENTER
//

const commandCenter =
document.createElement("div");

commandCenter.style.position =
"absolute";

commandCenter.style.left =
"50%";

commandCenter.style.top =
"82px";

commandCenter.style.transform =
"translateX(-50%)";

commandCenter.style.width =
"620px";

commandCenter.style.height =
"95px";

commandCenter.style.background =
"rgba(3,20,35,.72)";

commandCenter.style.border =
"1px solid rgba(0,255,255,.22)";

commandCenter.style.borderRadius =
"18px";

commandCenter.style.backdropFilter =
"blur(18px)";

commandCenter.style.zIndex =
"100";

commandCenter.style.display =
"grid";

commandCenter.style.gridTemplateColumns =
"1fr 1fr 1fr 1fr";

commandCenter.style.gap =
"10px";

commandCenter.style.padding =
"12px";

commandCenter.innerHTML = `

<div>
<div style="font-size:10px;color:#8ce8ff">
NETWORK HEALTH
</div>
<div id="networkHealth"
style="
font-size:28px;
font-weight:900;
color:#54ffd0;">
99%
</div>
</div>

<div>
<div style="font-size:10px;color:#8ce8ff">
ACTIVE VEHICLES
</div>
<div id="vehicleCount"
style="
font-size:28px;
font-weight:900;
color:#7aecff;">
12
</div>
</div>

<div>
<div style="font-size:10px;color:#8ce8ff">
AI STATUS
</div>
<div id="aiState"
style="
font-size:18px;
font-weight:900;
color:#6fff9e;">
ONLINE
</div>
</div>

<div>
<div style="font-size:10px;color:#8ce8ff">
DIGITAL TWIN
</div>
<div id="twinSync"
style="
font-size:18px;
font-weight:900;
color:#7eeeef;">
SYNCED
</div>
</div>

`;

document.body.appendChild(
commandCenter
);

//
// STRUCTURAL STRESS MAP
//

const stressMap =
document.createElement(
"canvas"
);

stressMap.width = 300;
stressMap.height = 160;

stressMap.style.position =
"absolute";

stressMap.style.left =
"560px";

stressMap.style.bottom =
"140px";

stressMap.style.background =
"rgba(5,20,35,.75)";

stressMap.style.border =
"1px solid rgba(0,255,255,.18)";

stressMap.style.borderRadius =
"12px";

stressMap.style.zIndex =
"90";

document.body.appendChild(
stressMap
);
<script>

//
// AI CORE
//

const aiCore =
document.createElement("div");

aiCore.style.position =
"absolute";

aiCore.style.left =
"50%";

aiCore.style.top =
"220px";

aiCore.style.transform =
"translateX(-50%)";

aiCore.style.width =
"260px";

aiCore.style.height =
"260px";

aiCore.style.pointerEvents =
"none";

aiCore.style.zIndex =
"110";

document.body.appendChild(
aiCore
);

const coreCanvas =
document.createElement(
"canvas"
);

coreCanvas.width = 260;
coreCanvas.height = 260;

aiCore.appendChild(
coreCanvas
);

const cc =
coreCanvas.getContext("2d");

let coreRotation = 0;

function drawAICore(){

 coreRotation += 0.01;

 cc.clearRect(
 0,
 0,
 260,
 260
 );

 const cx = 130;
 const cy = 130;

 cc.strokeStyle =
 "#33f4ff";

 cc.lineWidth = 2;

 for
