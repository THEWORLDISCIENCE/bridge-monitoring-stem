
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Intelligent Bridge Monitoring",
    page_icon="🌉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
#MainMenu,footer,header,[data-testid="stToolbar"],
[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none!important}
.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"],
.main,.block-container{padding:0!important;margin:0!important;
max-width:100%!important;background:#91c9e5!important}
iframe{border:0!important}
</style>
""", unsafe_allow_html=True)

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<script type="importmap">
{"imports":{
"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
"three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
}}
</script>
<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;
font-family:Inter,Arial,sans-serif;background:#9acde9;color:#effaff}
#world{position:fixed;inset:0}
#world canvas{width:100%;height:100%;display:block}
.glass{
 position:absolute;z-index:4;color:#edfaff;
 background:linear-gradient(145deg,rgba(7,28,45,.84),rgba(9,42,62,.69));
 border:1px solid rgba(150,220,255,.38);
 border-radius:13px;
 box-shadow:0 12px 35px rgba(0,25,45,.24),inset 0 1px rgba(255,255,255,.09);
 backdrop-filter:blur(17px);-webkit-backdrop-filter:blur(17px);
 padding:13px
}
#header{top:13px;left:15px;right:15px;height:66px;
display:flex;align-items:center;justify-content:space-between;padding:10px 19px}
.logo{font-size:17px;font-weight:850;letter-spacing:1px}
.kicker{font-size:9px;color:#a5d8ec;letter-spacing:2px;margin-top:4px}
.headright{display:flex;gap:8px;align-items:center}
.tag{padding:8px 11px;border-radius:20px;background:rgba(30,83,108,.55);
border:1px solid rgba(151,221,249,.3);font-size:9px;white-space:nowrap}
.green{color:#5df0b2}
#left{left:15px;top:94px;width:248px;max-height:calc(100vh - 245px);overflow:auto}
#right{right:15px;top:94px;width:270px;max-height:calc(100vh - 245px);overflow:auto}
.heading{font-size:10px;letter-spacing:1.6px;color:#9cdef6;font-weight:800;margin-bottom:12px}
.subheading{font-size:9px;letter-spacing:1.2px;color:#85c9e6;
margin:13px 0 8px;padding-top:10px;border-top:1px solid #ffffff22}
label{display:flex;justify-content:space-between;gap:5px;
font-size:10px;color:#c4deeb;margin:9px 0 5px}
output{color:white;font-weight:700}
input[type=range]{width:100%;accent-color:#42d8ee;height:13px}
select{width:100%;padding:8px;background:#12354a;color:white;
border:1px solid #4c829d;border-radius:7px;font-size:10px}
button{background:linear-gradient(120deg,#147f9e,#20b4c7);
border:1px solid #60d9e9;color:white;border-radius:7px;
padding:9px;font-size:9px;font-weight:800;cursor:pointer}
button.secondary{background:#183f56;border-color:#47788e}
button:hover{filter:brightness(1.2)}
.buttons{display:flex;gap:7px;margin-top:9px}
.buttons button{flex:1}
.metricgrid{display:grid;grid-template-columns:1fr 1fr;gap:7px}
.metric{padding:9px;border:1px solid #a6ddf022;border-radius:8px;
background:rgba(53,111,137,.2)}
.metricname{font-size:8px;color:#a9d1e3;letter-spacing:.6px}
.metricvalue{font-size:19px;font-weight:850;margin-top:5px}
.unit{font-size:8px;color:#9bc4d8}
.sensor{display:flex;justify-content:space-between;
padding:7px 0;border-bottom:1px solid #ffffff16;font-size:9px;color:#c5deeb}
.on{color:#5de9ae;font-weight:800}.off{color:#f2bd82;font-weight:800}
.alert{padding:9px;border-radius:8px;font-size:9px;line-height:1.6;
background:#185c594f;border:1px solid #52d7ae55;margin-top:8px}
.warning{background:#9b63344c;border-color:#ffbd7655}
#bottom{bottom:13px;left:15px;right:15px;min-height:105px;
display:grid;grid-template-columns:1fr 1fr 1.6fr 1fr;gap:12px}
.bottomlabel{font-size:8px;color:#9dd6ed;letter-spacing:1.5px;margin-bottom:8px}
.big{font-size:20px;font-weight:850}
.muted{font-size:9px;color:#a9cbdc;margin-top:5px}
#chart{width:100%;height:53px}
#chart polyline{fill:none;stroke:#59e0ef;stroke-width:2}
#chart polygon{fill:#49cde522}
#hint{position:absolute;z-index:3;bottom:132px;right:300px;
font-size:9px;color:#153c50;background:#e8f7f8aa;padding:7px 10px;border-radius:7px}
#disclaimer{position:absolute;z-index:3;bottom:132px;left:50%;
transform:translateX(-50%);font-size:8px;color:#163c50;
background:#eaf8f5aa;padding:6px 10px;border-radius:20px;white-space:nowrap}
#loading{position:absolute;inset:0;z-index:10;display:grid;place-content:center;
text-align:center;color:#153a50;background:linear-gradient(#94cce9,#d5e9df);
font-size:17px;font-weight:800}
#loading small{font-size:10px;font-weight:500;margin-top:10px}
#toast{display:none;position:absolute;z-index:12;top:90px;left:50%;
transform:translateX(-50%);background:#123b51;padding:9px 15px;
border-radius:8px;font-size:10px}
@media(max-width:850px){
 #left{width:215px;left:8px}
 #right{width:225px;right:8px}
 #bottom{left:8px;right:8px;grid-template-columns:1fr 1fr}
 #header{left:8px;right:8px}
}
@media(max-width:600px){
 #left{top:85px;width:47%;max-height:48vh}
 #right{top:85px;width:47%;max-height:48vh}
 #bottom{max-height:25vh;overflow:auto}
 .logo{font-size:11px}.tag{font-size:7px;padding:6px}
 #disclaimer,#hint{display:none}
}
</style>
</head>
<body>
<div id="world"></div>
<div id="loading">INITIALIZING DIGITAL BRIDGE ENVIRONMENT
<small>Loading bridge geometry and sensor network</small></div>
<div id="toast"></div>

<div id="header" class="glass">
 <div>
  <div class="logo">INTELLIGENT BRIDGE MONITORING</div>
  <div class="kicker">STRUCTURAL INTELLIGENCE · DIGITAL TWIN</div>
 </div>
 <div class="headright">
  <div class="tag"><span class="green">●</span> SYSTEM ONLINE</div>
  <div class="tag" id="mode">CONTINUOUS MONITORING</div>
  <div class="tag" id="clock">00:00:00</div>
 </div>
</div>

<div id="left" class="glass">
 <div class="heading">01 / SIMULATION CONTROL</div>
 <label>Vehicle weight <output id="weightV">18 t</output></label>
 <input id="weight" type="range" min="5" max="45" value="18">
 <label>Vehicle speed <output id="speedV">55 km/h</output></label>
 <input id="speed" type="range" min="10" max="110" value="55">
 <label>Number of axles <output id="axleV">3</output></label>
 <input id="axles" type="range" min="2" max="6" value="3">
 <label>Traffic volume <output id="trafficV">65%</output></label>
 <input id="traffic" type="range" min="0" max="100" value="65">

 <div class="subheading">STRUCTURAL CHANGE SCENARIO</div>
 <label>Stiffness change <output id="stiffV">0%</output></label>
 <input id="stiff" type="range" min="0" max="30" value="0">
 <label>Local change signal <output id="localV">0%</output></label>
 <input id="local" type="range" min="0" max="100" value="0">
 <label>Test location</label>
 <select id="location">
  <option>Midspan</option><option>North tower</option>
  <option>South tower</option><option>Deck joint</option><option>Cable zone</option>
 </select>
 <label>Event trigger sensitivity <output id="triggerV">65%</output></label>
 <input id="trigger" type="range" min="10" max="100" value="65">

 <div class="subheading">MONITORING CONFIGURATION</div>
 <select id="monitor">
  <option value="adaptive">Adaptive attention</option>
  <option value="primary">Primary sensors only</option>
  <option value="all">All sensors always active</option>
 </select>
 <label>Time step <output id="stepV">1.0 s</output></label>
 <input id="step" type="range" min="1" max="10" value="1">
 <div class="buttons">
  <button id="run">Ⅱ PAUSE</button>
  <button id="reset" class="secondary">↺ RESET</button>
 </div>
 <div class="buttons">
  <button id="addVehicle">＋ VEHICLE</button>
  <button id="camera" class="secondary">CAMERA RESET</button>
 </div>
</div>

<div id="right" class="glass">
 <div class="heading">02 / LIVE STRUCTURAL TELEMETRY</div>
 <div class="metricgrid">
  <div class="metric"><div class="metricname">DECK DEFLECTION</div>
   <div class="metricvalue" id="deflection">2.40</div><div class="unit">mm · simulated</div></div>
  <div class="metric"><div class="metricname">STRAIN PROXY</div>
   <div class="metricvalue" id="strain">118</div><div class="unit">με · simulated</div></div>
  <div class="metric"><div class="metricname">VIBRATION</div>
   <div class="metricvalue" id="vibration">0.12</div><div class="unit">g · simulated</div></div>
  <div class="metric"><div class="metricname">TEMPERATURE</div>
   <div class="metricvalue" id="temperature">27.0</div><div class="unit">°C · simulated</div></div>
 </div>

 <div class="subheading">SENSOR NETWORK</div>
 <div class="sensor"><span>Primary sensors</span><b class="on">55 ONLINE</b></div>
 <div class="sensor"><span>Additional sensors</span><b id="extra" class="off">66 STANDBY</b></div>
 <div class="sensor"><span>Strain gauges</span><b class="on">ACTIVE</b></div>
 <div class="sensor"><span>Accelerometers</span><b class="on">ACTIVE</b></div>
 <div class="sensor"><span>Temperature sensors</span><b class="on">ACTIVE</b></div>
 <div class="sensor"><span>Tilt sensors</span><b id="tilt" class="off">STANDBY</b></div>
 <div class="sensor"><span>Acoustic sensors</span><b id="acoustic" class="off">STANDBY</b></div>
 <div class="sensor"><span>Joint displacement</span><b id="joint" class="off">STANDBY</b></div>

 <div class="subheading">03 / EVENT ANALYSIS</div>
 <div class="metricgrid">
  <div class="metric"><div class="metricname">BASELINE DEVIATION</div>
   <div class="metricvalue" id="deviation">0.0%</div></div>
  <div class="metric"><div class="metricname">PERSISTENCE</div>
   <div class="metricvalue" id="persistence">LOW</div></div>
 </div>
 <div id="alert" class="alert">Normal simulated operating pattern. Primary monitoring active.</div>

 <div class="subheading">ADDITIONAL SENSOR READINGS</div>
 <div class="sensor"><span>Tilt estimate</span><b id="tiltValue">0.02°</b></div>
 <div class="sensor"><span>Humidity</span><b>68%</b></div>
 <div class="sensor"><span>Corrosion proxy</span><b id="corrosion">Low</b></div>
 <div class="sensor"><span>Crack-width proxy</span><b id="crack">0.00 mm</b></div>
 <div class="sensor"><span>Acoustic activity</span><b id="acousticValue">Low</b></div>
 <div class="sensor"><span>Joint displacement</span><b id="jointValue">0.30 mm</b></div>
</div>

<div id="hint">DRAG TO ORBIT · SCROLL TO ZOOM</div>
<div id="disclaimer">EDUCATIONAL SIMULATION · NOT A REAL BRIDGE SAFETY SYSTEM</div>

<div id="bottom" class="glass">
 <div><div class="bottomlabel">TRAFFIC / LOAD</div>
  <div class="big" id="trafficBig">65%</div>
  <div class="muted">Relative traffic volume</div>
  <div class="muted" id="count">Vehicles: 1</div></div>
 <div><div class="bottomlabel">STRUCTURAL RESPONSE</div>
  <div class="big" id="response">NORMAL</div>
  <div class="muted" id="responseNote">Within simulated baseline</div></div>
 <div><div class="bottomlabel">SENSOR HISTORY / RESPONSE TREND</div>
  <svg id="chart" viewBox="0 0 400 55" preserveAspectRatio="none">
   <polygon id="fill" points="0,52 400,52"/>
   <polyline id="line" points="0,35 400,35"/>
  </svg><div class="muted">Recent simulated measurements</div></div>
 <div><div class="bottomlabel">SYSTEM ACTIONS</div>
  <div class="buttons"><button id="export">EXPORT CSV</button>
  <button id="sensorToggle" class="secondary">HIDE SENSORS</button></div>
  <div class="muted" id="exportStatus">Live data collection</div></div>
</div>

<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {Sky} from 'three/addons/objects/Sky.js';

const root=document.getElementById('world');
const scene=new THREE.Scene();
scene.background=new THREE.Color(0x9acde9);
scene.fog=new THREE.Fog(0x9acde9,650,1900);
const camera=new THREE.PerspectiveCamera(43,innerWidth/innerHeight,.1,5000);
camera.position.set(0,100,360);

const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.setSize(innerWidth,innerHeight);
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.15;
root.appendChild(renderer.domElement);

const controls=new OrbitControls(camera,renderer.domElement);
controls.enableDamping=true;
controls.dampingFactor=.055;
controls.maxPolarAngle=Math.PI*.49;
controls.minDistance=35;
controls.maxDistance=850;
controls.target.set(0,40,0);

scene.add(new THREE.HemisphereLight(0xdaf5ff,0x54725a,2.1));
const sun=new THREE.DirectionalLight(0xfff1d8,3.2);
sun.position.set(-200,300,140);
sun.castShadow=true;
sun.shadow.mapSize.set(2048,2048);
sun.shadow.camera.left=-400;sun.shadow.camera.right=400;
sun.shadow.camera.top=400;sun.shadow.camera.bottom=-400;
scene.add(sun);

const sky=new Sky();
sky.scale.setScalar(4500);
sky.material.uniforms.turbidity.value=6;
sky.material.uniforms.rayleigh.value=2.4;
sky.material.uniforms.mieCoefficient.value=.004;
sky.material.uniforms.mieDirectionalG.value=.8;
sky.material.uniforms.sunPosition.value.copy(sun.position).normalize();
scene.add(sky);

const water=new THREE.Mesh(
 new THREE.PlaneGeometry(5000,5000),
 new THREE.MeshStandardMaterial({color:0x287d9d,roughness:.22,metalness:.22})
);
water.rotation.x=-Math.PI/2;water.position.y=-8;water.receiveShadow=true;
scene.add(water);

const landMat=new THREE.MeshStandardMaterial({color:0x64865a,roughness:1});
for(let i=0;i<18;i++){
 const hill=new THREE.Mesh(new THREE.SphereGeometry(1,32,20),landMat);
 hill.scale.set(75+(i%4)*22,13+(i%3)*5,42);
 hill.position.set(-500+i*60,-4,i%2===0?-250:280);
 scene.add(hill);
}

const bridgeGroup=new THREE.Group();scene.add(bridgeGroup);
const sensors=new THREE.Group();scene.add(sensors);
const vehicles=new THREE.Group();scene.add(vehicles);
let bridgeAxis='x',deckY=35,bridgeLength=300,modelLoaded=false;
let vehicleObjects=[],showSensors=true,active=true,elapsed=0,history=[],data=[];

function makeMat(color,roughness=.6,metalness=.2){
 return new THREE.MeshStandardMaterial({color,roughness,metalness});
}
const concrete=makeMat(0xc4cbd0,.78,.1);
const steel=makeMat(0x9caeb9,.34,.65);
const cableMat=makeMat(0xe3edf0,.35,.5);
const roadMat=makeMat(0x313a42,.9,.05);
const white=makeMat(0xf4f4e8,.65,.05);

function box(parent,x,y,z,sx,sy,sz,mat){
 const m=new THREE.Mesh(new THREE.BoxGeometry(sx,sy,sz),mat);
 m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;
 parent.add(m);return m;
}
function cylinder(parent,a,b,r1,r2,mat,segments=12){
 const d=new THREE.Vector3().subVectors(b,a);
 const m=new THREE.Mesh(new THREE.CylinderGeometry(r1,r2,d.length(),segments),mat);
 m.position.copy(a).add(b).multiplyScalar(.5);
 m.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),d.normalize());
 m.castShadow=true;parent.add(m);return m;
}
function line(parent,a,b,mat,r=.18){
 cylinder(parent,a,b,r,r,mat,8);
}
function buildFallbackBridge(){
 bridgeGroup.clear();
 const L=300,W=28,Y=35;
 box(bridgeGroup,0,Y,0,L,2.4,W,roadMat);
 box(bridgeGroup,0,Y-1.5,0,L,1,W+2,steel);
 for(let z of [-W/2-1,W/2+1]){
  box(bridgeGroup,0,Y+2,z,L,.45,.65,white);
  box(bridgeGroup,0,Y+4,z,L,.22,.25,steel);
  for(let x=-L/2;x<=L/2;x+=12){
   box(bridgeGroup,x,Y+3,z,.25,1.4,.25,steel);
  }
 }
 for(let x=-L/2;x<=L/2;x+=18){
  box(bridgeGroup,x,Y+1.25,0,.3,.05,W-2,white);
 }
 for(const x of [-65,65]){
  for(const z of [-7,7]){
   box(bridgeGroup,x,Y-12,z,5,24,5,concrete);
  }
  const top=Y+100;
  const base=new THREE.Vector3(x,Y+2,0);
  const apex=new THREE.Vector3(x,Y+100,0);
  const left=new THREE.Vector3(x-7,Y+2,0);
  const right=new THREE.Vector3(x+7,Y+2,0);
  line(bridgeGroup,left,apex,concrete,2.7);
  line(bridgeGroup,right,apex,concrete,2.7);
  line(bridgeGroup,apex,new THREE.Vector3(x,Y+2,0),concrete,2.4);
  for(let i=0;i<11;i++){
   const t=(i+1)/12;
   const px=x+(t-.5)*100;
   const deckPoint=new THREE.Vector3(px,Y+2,0);
   const towerPoint=new THREE.Vector3(x,Y+98-t*12,0);
   line(bridgeGroup,deckPoint,towerPoint,cableMat,.16);
   const deckPoint2=new THREE.Vector3(px,Y+2,0);
   const towerPoint2=new THREE.Vector3(x,Y+98-t*12,0);
   line(bridgeGroup,deckPoint2,towerPoint2,cableMat,.16);
  }
 }
 for(let i=0;i<14;i++){
  const x=-145+i*22;
  box(bridgeGroup,x,Y-3,0,1.2,5,W,steel);
 }
 deckY=Y;
 bridgeLength=L;
}
function centerModel(model){
 const box3=new THREE.Box3().setFromObject(model);
 const size=new THREE.Vector3(),center=new THREE.Vector3();
 box3.getSize(size);box3.getCenter(center);
 bridgeAxis=size.x>=size.z?'x':'z';
 bridgeLength=Math.max(size.x,size.z);
 const scale=300/Math.max(bridgeLength,1);
 model.scale.setScalar(scale);
 model.position.sub(center.multiplyScalar(scale));
 model.position.y+=20;
 model.traverse(o=>{
  if(o.isMesh){o.castShadow=true;o.receiveShadow=true;
   if(o.material)o.material.side=THREE.DoubleSide;}
 });
 const b=new THREE.Box3().setFromObject(model);
 const s=new THREE.Vector3();b.getSize(s);
 deckY=b.min.y+s.y*.28;
 bridgeGroup.add(model);
 controls.target.set(0,deckY+12,0);
 camera.position.set(0,deckY+100,340);
 controls.update();
}
function addSensor(x,y,z,color=0x48e9aa,size=.9){
 const m=new THREE.Mesh(new THREE.SphereGeometry(size,14,14),
 new THREE.MeshStandardMaterial({color,emissive:color,emissiveIntensity:1.8}));
 m.position.set(x,y,z);sensors.add(m);
 const halo=new THREE.Mesh(new THREE.SphereGeometry(size*2.3,12,12),
 new THREE.MeshBasicMaterial({color,transparent:true,opacity:.13}));
 halo.position.copy(m.position);sensors.add(halo);
}
function buildSensors(){
 sensors.clear();
 for(let i=0;i<34;i++){
  const p=(i/33-.5)*bridgeLength*.85;
  if(bridgeAxis==='x'){addSensor(p,deckY+2,0);addSensor(p,deckY+2,9,0x62caff);}
  else{addSensor(0,deckY+2,p);addSensor(9,deckY+2,p,0x62caff);}
 }
 for(let i=0;i<18;i++){
  const p=(i/17-.5)*bridgeLength*.8;
  if(bridgeAxis==='x')addSensor(p,deckY+3,-10,0xff665e);
  else addSensor(-10,deckY+3,p,0xff665e);
 }
 sensors.visible=showSensors;
}
function vehicle(){
 const g=new THREE.Group();
 const body=new THREE.Mesh(new THREE.BoxGeometry(10,3.4,4.5),makeMat(0xe6ecef,.32,.45));
 body.position.y=3;body.castShadow=true;g.add(body);
 const cabin=new THREE.Mesh(new THREE.BoxGeometry(4,2.6,4.2),makeMat(0x8db7c8,.2,.45));
 cabin.position.set(-2,5.8,0);g.add(cabin);
 const wheelMat=makeMat(0x1a252c,.9,0);
 for(const x of [-3.5,3.5])for(const z of [-2.15,2.15]){
  const w=new THREE.Mesh(new THREE.CylinderGeometry(1,1,.55,20),wheelMat);
  w.rotation.x=Math.PI/2;w.position.set(x,1.2,z);g.add(w);
 }
 vehicles.add(g);vehicleObjects.push({mesh:g,p:Math.random()*.3});
 document.getElementById('count').textContent='Vehicles: '+vehicleObjects.length;
}
vehicle();

function toast(t){
 const e=document.getElementById('toast');e.textContent=t;e.style.display='block';
 setTimeout(()=>e.style.display='none',2000);
}
function val(id){return +document.getElementById(id).value}
function put(id,v){document.getElementById(id).textContent=v}
function labels(){
 put('weightV',val('weight')+' t');put('speedV',val('speed')+' km/h');
 put('axleV',val('axles'));put('trafficV',val('traffic')+'%');
 put('stiffV',val('stiff')+'%');put('localV',val('local')+'%');
 put('triggerV',val('trigger')+'%');put('stepV',(val('step')/10).toFixed(1)+' s');
 put('trafficBig',val('traffic')+'%');
}
['weight','speed','axles','traffic','stiff','local','trigger','step'].forEach(id=>{
 document.getElementById(id).addEventListener('input',labels);
});
labels();

function drawHistory(v){
 history.push(v);if(history.length>60)history.shift();
 const pts=history.map((n,i)=>(i/(Math.max(1,history.length-1))*400)+','+
 (49-Math.min(n/40,1)*43)).join(' ');
 document.getElementById('line').setAttribute('points',pts);
 document.getElementById('fill').setAttribute('points','0,52 '+pts+' 400,52');
}
function simulate(){
 const w=val('weight')/45,s=val('speed')/110,t=val('traffic')/100;
 const change=val('stiff')/30*.75+val('local')/100*.55;
 const temporary=w*s*t;
 const deviation=change*100+temporary*3;
 const score=Math.min(100,deviation*1.4);
 const mode=document.getElementById('monitor').value;
 const extra=mode==='all'||(mode==='adaptive'&&score>=val('trigger'));
 const def=.7+temporary*4.4+change*5.2;
 const strain=72+temporary*110+change*180;
 const vib=.03+temporary*.34+change*.2;
 put('deflection',def.toFixed(2));put('strain',strain.toFixed(0));
 put('vibration',vib.toFixed(2));put('temperature',(27+Math.sin(elapsed/25)*1.5).toFixed(1));
 put('deviation',deviation.toFixed(1)+'%');
 put('persistence',change>.3?'ELEVATED':change>.08?'MODERATE':'LOW');
 put('extra',extra?'66 ACTIVE':'66 STANDBY');
 put('mode',extra?'ADAPTIVE ATTENTION ACTIVE':mode==='all'?'ALL SENSORS ACTIVE':'CONTINUOUS MONITORING');
 ['tilt','acoustic','joint'].forEach(id=>{
  put(id,extra?'ACTIVE':'STANDBY');
  document.getElementById(id).className=extra?'on':'off';
 });
 document.getElementById('extra').className=extra?'on':'off';
 put('tiltValue',(0.02+change*.6).toFixed(2)+'°');
 put('corrosion',change>.6?'Elevated proxy':'Low');
 put('crack',(change*.28).toFixed(2)+' mm');
 put('acousticValue',extra?'Elevated':'Low');
 put('jointValue',(0.3+change*1.4).toFixed(2)+' mm');
 const alert=document.getElementById('alert');
 if(change>.3){
  alert.className='alert warning';
  alert.textContent='Persistent-change scenario detected. Additional sensor attention: '+(extra?'ACTIVE':'INACTIVE')+'.';
  put('response','CHANGE');put('responseNote','Simulated response differs from baseline');
 }else if(temporary>.4){
  alert.className='alert';
  alert.textContent='Elevated temporary traffic-load response. Comparing against baseline.';
  put('response','LOAD');put('responseNote','Temporary load response in simulation');
 }else{
  alert.className='alert';
  alert.textContent='Normal simulated operating pattern. Primary monitoring active.';
  put('response','NORMAL');put('responseNote','Within simulated baseline');
 }
 drawHistory(def);
 data.push({time:elapsed,weight:val('weight'),speed:val('speed'),traffic:val('traffic'),
 deflection:def,strain,vibration:vib,temperature:27+Math.sin(elapsed/25)*1.5,
 deviation,additionalSensors:extra,stiffness:val('stiff'),localChange:val('local')});
 if(data.length>2000)data.shift();
}
document.getElementById('run').onclick=()=>{
 active=!active;put('run',active?'Ⅱ PAUSE':'▶ RUN');
 toast(active?'Simulation resumed':'Simulation paused');
};
document.getElementById('reset').onclick=()=>{
 elapsed=0;history=[];data=[];
 document.getElementById('stiff').value=0;document.getElementById('local').value=0;
 labels();simulate();toast('Simulation reset');
};
document.getElementById('addVehicle').onclick=()=>{vehicle();toast('Vehicle added')};
document.getElementById('camera').onclick=()=>{
 camera.position.set(0,deckY+100,340);
 controls.target.set(0,deckY+12,0);controls.update();
};
document.getElementById('sensorToggle').onclick=()=>{
 showSensors=!showSensors;sensors.visible=showSensors;
 put('sensorToggle',showSensors?'HIDE SENSORS':'SHOW SENSORS');
};
document.getElementById('export').onclick=()=>{
 if(!data.length){toast('Run simulation first');return;}
 const keys=Object.keys(data[0]);
 const csv=[keys.join(','),...data.map(r=>keys.map(k=>r[k]).join(','))].join('\n');
 const a=document.createElement('a');
 a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));
 a.download='bridge-monitoring-data.csv';a.click();
 put('exportStatus','CSV exported');
};

const MODEL='https://raw.githubusercontent.com/experimentscience/bridge-monitoring-stem/main/assets/cable-stayed-bridge.glb';
new GLTFLoader().load(MODEL,gltf=>{
 centerModel(gltf.scene);modelLoaded=true;buildSensors();
 document.getElementById('loading').style.display='none';
 toast('Bridge model loaded');
},xhr=>{
 if(xhr.total)document.querySelector('#loading').innerHTML=
 'LOADING 3D BRIDGE · '+Math.round(xhr.loaded/xhr.total*100)+'%';
},err=>{
 console.error(err);
 buildFallbackBridge();buildSensors();
 document.getElementById('loading').style.display='none';
 toast('Using generated bridge scene: external model unavailable');
});

const clock=new THREE.Clock();
function animate(){
 requestAnimationFrame(animate);
 const dt=Math.min(clock.getDelta(),.05);
 if(active){
  elapsed+=dt;
  vehicleObjects.forEach(v=>{
   v.p+=dt*(val('speed')/110)*.08;
   if(v.p>1.1)v.p=-.1;
   const p=(v.p-.5)*bridgeLength*.82;
   if(bridgeAxis==='x'){v.mesh.position.set(p,deckY+.5,0);v.mesh.rotation.y=0}
   else{v.mesh.position.set(0,deckY+.5,p);v.mesh.rotation.y=Math.PI/2}
  });
  if(Math.floor(elapsed*2)!==Math.floor((elapsed-dt)*2))simulate();
 }
 put('clock',new Date(Math.floor(elapsed)*1000).toISOString().slice(11,19));
 controls.update();renderer.render(scene,camera);
}
simulate();animate();
addEventListener('resize',()=>{
 camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();
 renderer.setSize(innerWidth,innerHeight);
});
</script>
</body>
</html>
"""

components.html(html, height=1050, scrolling=False)
