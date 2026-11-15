
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
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] {
    display:none !important;
}
.stApp, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main, .block-container {
    background:#071b2b !important;
    padding:0 !important;
    margin:0 !important;
    max-width:100% !important;
}
iframe { border:0 !important; }
</style>
""", unsafe_allow_html=True)

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
  }
}
</script>
<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;font-family:Inter,Arial,sans-serif;background:#9bc9e3;color:#eaf7ff}
#scene{position:fixed;inset:0;width:100%;height:100%;z-index:0}
#scene canvas{display:block}
#loading{position:absolute;inset:0;z-index:20;display:flex;align-items:center;justify-content:center;background:linear-gradient(#8cc9eb,#c7e6ed);color:#12334b;font-size:18px;font-weight:700}
#loading small{display:block;margin-top:12px;font-size:12px;font-weight:500}
.hud{position:absolute;z-index:5;background:rgba(5,23,39,.77);border:1px solid rgba(143,218,255,.42);border-radius:13px;box-shadow:0 8px 32px rgba(0,20,40,.23);backdrop-filter:blur(15px);-webkit-backdrop-filter:blur(15px);padding:13px;color:#eaf7ff}
#top{left:15px;right:15px;top:12px;height:66px;display:flex;align-items:center;justify-content:space-between;padding:10px 18px}
.brand{font-size:18px;font-weight:800;letter-spacing:.5px}
.sub{font-size:10px;color:#a8c9dd;margin-top:4px;letter-spacing:1.5px}
.topright{display:flex;gap:9px;align-items:center}
.pill{font-size:10px;padding:8px 11px;border:1px solid #4b829d;border-radius:20px;background:rgba(22,62,82,.65);white-space:nowrap}
.dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#3ce5a0;margin-right:6px;box-shadow:0 0 9px #3ce5a0}
#left{top:92px;left:15px;width:248px;max-height:calc(100vh - 240px);overflow:auto}
#right{top:92px;right:15px;width:270px;max-height:calc(100vh - 240px);overflow:auto}
#bottom{left:15px;right:15px;bottom:12px;min-height:112px;display:grid;grid-template-columns:1.1fr 1.1fr 1.7fr 1fr;gap:12px;align-items:stretch}
.paneltitle{font-size:11px;font-weight:800;letter-spacing:1.4px;text-transform:uppercase;color:#9edfff;margin-bottom:12px}
.section{border-top:1px solid rgba(155,213,241,.18);margin-top:12px;padding-top:11px}
label{display:flex;justify-content:space-between;gap:8px;font-size:11px;color:#b9d4e3;margin:9px 0 5px}
output{color:#fff;font-weight:700}
input[type=range]{width:100%;accent-color:#47d5ed}
select,button{font:inherit}
select{width:100%;background:#102f43;color:white;border:1px solid #47738a;border-radius:7px;padding:8px;font-size:11px}
button{background:linear-gradient(135deg,#147d9e,#1dabc0);border:1px solid #58d4e8;color:white;border-radius:7px;padding:9px 11px;font-size:10px;font-weight:700;cursor:pointer}
button:hover{filter:brightness(1.18)}
button.secondary{background:rgba(29,65,86,.9);border-color:#4c829b}
button.active{background:linear-gradient(135deg,#b64b42,#e4775e)}
.btnrow{display:flex;gap:7px;margin-top:9px}
.btnrow button{flex:1}
.metricgrid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.metric{background:rgba(32,76,99,.52);border:1px solid rgba(129,194,222,.18);border-radius:8px;padding:9px}
.metric .name{font-size:9px;color:#a9c8d9;letter-spacing:.5px}
.metric .value{font-size:19px;font-weight:800;margin-top:5px}
.metric .unit{font-size:9px;color:#a9c8d9}
.status{font-size:10px;color:#a9c8d9;line-height:1.5}
.alert{padding:9px;border-radius:8px;background:rgba(30,89,104,.4);border:1px solid rgba(84,201,216,.25);font-size:10px;line-height:1.5;margin-top:7px}
.alert.warn{background:rgba(143,83,42,.3);border-color:rgba(255,177,95,.45)}
.alert.good{background:rgba(32,117,88,.25);border-color:rgba(77,222,162,.35)}
.sensorrow{display:flex;justify-content:space-between;font-size:10px;padding:6px 0;border-bottom:1px solid rgba(155,213,241,.12);color:#c3dce9}
.sensorstate{color:#51e5ae;font-weight:700}
.sensorstate.off{color:#f0b17b}
.bottomtitle{font-size:9px;color:#a6d7eb;letter-spacing:1px;margin-bottom:8px}
.big{font-size:20px;font-weight:800}
.small{font-size:9px;color:#a8c8d9;margin-top:4px}
#history{width:100%;height:52px}
#history polyline{fill:none;stroke:#58dff0;stroke-width:2}
#history .fill{fill:rgba(65,200,230,.12);stroke:none}
#footerNote{position:absolute;bottom:132px;left:50%;transform:translateX(-50%);font-size:9px;color:#15394b;background:rgba(234,249,255,.72);padding:5px 10px;border-radius:20px;white-space:nowrap;z-index:4}
#cameraHint{position:absolute;right:300px;bottom:145px;color:#12374c;background:rgba(240,250,255,.65);padding:7px 10px;border-radius:8px;font-size:9px;z-index:4}
#toast{position:absolute;top:88px;left:50%;transform:translateX(-50%);z-index:10;background:#10374d;color:#eafaff;padding:9px 15px;border-radius:8px;font-size:11px;display:none}
input[type=checkbox]{accent-color:#47d5ed}
.checkline{display:flex;align-items:center;gap:7px;font-size:10px;color:#c5deeb;margin-top:8px}
@media(max-width:900px){
 #left{width:210px;left:8px}
 #right{width:220px;right:8px}
 #top{left:8px;right:8px}
 #bottom{left:8px;right:8px;grid-template-columns:1fr 1fr}
 #footerNote{display:none}
}
@media(max-width:650px){
 #left{top:85px;width:47%;max-height:55vh}
 #right{top:85px;width:47%;max-height:55vh}
 #bottom{grid-template-columns:1fr 1fr;max-height:22vh;overflow:auto}
 .brand{font-size:13px}
 .pill{font-size:8px;padding:6px}
}
</style>
</head>
<body>
<div id="scene"></div>
<div id="loading">INITIALIZING BRIDGE ENVIRONMENT
  <small>Loading 3D bridge model and monitoring systems…</small>
</div>
<div id="toast"></div>

<div class="hud" id="top">
  <div>
    <div class="brand">INTELLIGENT BRIDGE MONITORING</div>
    <div class="sub">STRUCTURAL HEALTH • LIVE DIGITAL TWIN</div>
  </div>
  <div class="topright">
    <div class="pill"><span class="dot"></span>SYSTEM ONLINE</div>
    <div class="pill" id="modePill">CONTINUOUS MONITORING</div>
    <div class="pill" id="clock">00:00:00</div>
  </div>
</div>

<div class="hud" id="left">
  <div class="paneltitle">01 / Simulation controls</div>

  <label>Vehicle weight <output id="weightOut">18 t</output></label>
  <input id="weight" type="range" min="5" max="45" value="18">

  <label>Vehicle speed <output id="speedOut">55 km/h</output></label>
  <input id="speed" type="range" min="10" max="110" value="55">

  <label>Number of axles <output id="axleOut">3</output></label>
  <input id="axles" type="range" min="2" max="6" value="3">

  <label>Traffic volume <output id="trafficOut">65%</output></label>
  <input id="traffic" type="range" min="0" max="100" value="65">

  <div class="section">
    <div class="paneltitle">Structural change scenario</div>
    <label>Stiffness change <output id="stiffOut">0%</output></label>
    <input id="stiff" type="range" min="0" max="30" value="0">

    <label>Local change signal <output id="localOut">0%</output></label>
    <input id="local" type="range" min="0" max="100" value="0">

    <label>Test location</label>
    <select id="location">
      <option value="Midspan">Midspan</option>
      <option value="North tower">North tower</option>
      <option value="South tower">South tower</option>
      <option value="Deck joint">Deck joint</option>
      <option value="Cable zone">Cable zone</option>
    </select>

    <label>Event trigger sensitivity <output id="triggerOut">65%</output></label>
    <input id="trigger" type="range" min="10" max="100" value="65">
  </div>

  <div class="section">
    <div class="paneltitle">Monitoring mode</div>
    <select id="monitorMode">
      <option value="adaptive">Adaptive attention</option>
      <option value="primary">Primary sensors only</option>
      <option value="always">All sensors always active</option>
    </select>

    <label>Simulation time step <output id="stepOut">1.0 s</output></label>
    <input id="step" type="range" min="1" max="10" value="1">

    <div class="btnrow">
      <button id="runBtn">▶ RUN</button>
      <button id="resetBtn" class="secondary">↺ RESET</button>
    </div>
    <div class="btnrow">
      <button id="vehicleBtn" class="secondary">ADD VEHICLE</button>
      <button id="cameraBtn" class="secondary">RESET CAMERA</button>
    </div>
  </div>
</div>

<div class="hud" id="right">
  <div class="paneltitle">02 / Live sensor network</div>
  <div class="metricgrid">
    <div class="metric">
      <div class="name">DECK DEFLECTION</div>
      <div class="value" id="deflection">2.4</div>
      <div class="unit">mm · simulated</div>
    </div>
    <div class="metric">
      <div class="name">STRAIN PROXY</div>
      <div class="value" id="strain">118</div>
      <div class="unit">με · simulated</div>
    </div>
    <div class="metric">
      <div class="name">VIBRATION</div>
      <div class="value" id="vibration">0.12</div>
      <div class="unit">g · simulated</div>
    </div>
    <div class="metric">
      <div class="name">TEMPERATURE</div>
      <div class="value" id="temperature">27.0</div>
      <div class="unit">°C · simulated</div>
    </div>
  </div>

  <div class="section">
    <div class="paneltitle">Sensor inventory</div>
    <div class="sensorrow"><span>Primary sensors</span><b>55 ONLINE</b></div>
    <div class="sensorrow"><span>Additional sensors</span><b id="extraState" class="sensorstate off">66 STANDBY</b></div>
    <div class="sensorrow"><span>Strain gauges</span><b class="sensorstate">ACTIVE</b></div>
    <div class="sensorrow"><span>Accelerometers</span><b class="sensorstate">ACTIVE</b></div>
    <div class="sensorrow"><span>Temperature sensors</span><b class="sensorstate">ACTIVE</b></div>
    <div class="sensorrow"><span>Tilt sensors</span><b id="tiltState" class="sensorstate off">STANDBY</b></div>
    <div class="sensorrow"><span>Acoustic sensors</span><b id="acousticState" class="sensorstate off">STANDBY</b></div>
    <div class="sensorrow"><span>Joint displacement</span><b id="jointState" class="sensorstate off">STANDBY</b></div>
  </div>

  <div class="section">
    <div class="paneltitle">03 / Event analysis</div>
    <div class="metricgrid">
      <div class="metric">
        <div class="name">BASELINE DEVIATION</div>
        <div class="value" id="deviation">0.0%</div>
      </div>
      <div class="metric">
        <div class="name">PERSISTENCE</div>
        <div class="value" id="persistence">LOW</div>
      </div>
    </div>
    <div id="alertBox" class="alert good">Normal operating pattern. Primary monitoring is active.</div>
    <div class="status" style="margin-top:9px">
      Adaptive attention activates additional sensor groups when an event exceeds the selected trigger threshold.
    </div>
  </div>

  <div class="section">
    <div class="paneltitle">Additional sensor readings</div>
    <div class="sensorrow"><span>Tilt estimate</span><b id="tiltValue">0.02°</b></div>
    <div class="sensorrow"><span>Humidity</span><b id="humidity">68%</b></div>
    <div class="sensorrow"><span>Corrosion proxy</span><b id="corrosion">Low</b></div>
    <div class="sensorrow"><span>Crack-width proxy</span><b id="crack">0.00 mm</b></div>
    <div class="sensorrow"><span>Acoustic activity</span><b id="acousticValue">Low</b></div>
    <div class="sensorrow"><span>Joint displacement</span><b id="jointValue">0.3 mm</b></div>
  </div>
</div>

<div id="footerNote">EDUCATIONAL DIGITAL-TWIN SIMULATION · NOT A REAL BRIDGE SAFETY SYSTEM</div>
<div id="cameraHint">DRAG TO ROTATE · SCROLL TO ZOOM</div>

<div class="hud" id="bottom">
  <div>
    <div class="bottomtitle">TRAFFIC / LOAD</div>
    <div class="big" id="trafficBig">65%</div>
    <div class="small">Relative traffic volume</div>
    <div class="small" id="vehicleCount">Vehicles in simulation: 1</div>
  </div>
  <div>
    <div class="bottomtitle">STRUCTURAL RESPONSE</div>
    <div class="big" id="responseBig">NORMAL</div>
    <div class="small" id="responseSmall">Within simulated baseline</div>
  </div>
  <div>
    <div class="bottomtitle">SENSOR HISTORY / RESPONSE TREND</div>
    <svg id="history" viewBox="0 0 400 55" preserveAspectRatio="none">
      <polygon id="historyFill" class="fill" points="0,52 400,52"/>
      <polyline id="historyLine" points="0,35 400,35"/>
    </svg>
    <div class="small">Live simulated response · recent samples</div>
  </div>
  <div>
    <div class="bottomtitle">SYSTEM ACTIONS</div>
    <div class="btnrow">
      <button id="exportBtn">EXPORT CSV</button>
      <button id="sensorsBtn" class="secondary">HIDE SENSORS</button>
    </div>
    <div class="small" id="exportStatus">Data updates while simulation runs</div>
  </div>
</div>

<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { Sky } from 'three/addons/objects/Sky.js';

const MODEL_URL = 'https://raw.githubusercontent.com/experimentscience/bridge-monitoring-stem/main/assets/cable-stayed-bridge.glb';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x9bcbe7);
scene.fog = new THREE.Fog(0x9bcbe7, 500, 1800);

const camera = new THREE.PerspectiveCamera(48, innerWidth/innerHeight, 0.1, 5000);
camera.position.set(0, 90, 300);

const renderer = new THREE.WebGLRenderer({antialias:true, alpha:false});
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(innerWidth, innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.12;
renderer.outputColorSpace = THREE.SRGBColorSpace;
document.getElementById('scene').appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.06;
controls.maxPolarAngle = Math.PI * 0.49;
controls.minDistance = 30;
controls.maxDistance = 850;
controls.target.set(0, 35, 0);

scene.add(new THREE.HemisphereLight(0xd9f3ff, 0x52745e, 2.0));
const sun = new THREE.DirectionalLight(0xfff4dc, 3.0);
sun.position.set(-180, 260, 120);
sun.castShadow = true;
sun.shadow.mapSize.set(2048,2048);
sun.shadow.camera.left = -400;
sun.shadow.camera.right = 400;
sun.shadow.camera.top = 400;
sun.shadow.camera.bottom = -400;
scene.add(sun);

const sky = new Sky();
sky.scale.setScalar(4500);
sky.material.uniforms.turbidity.value = 7;
sky.material.uniforms.rayleigh.value = 2.2;
sky.material.uniforms.mieCoefficient.value = 0.004;
sky.material.uniforms.mieDirectionalG.value = 0.78;
sky.material.uniforms.sunPosition.value.copy(sun.position).normalize();
scene.add(sky);

const water = new THREE.Mesh(
  new THREE.PlaneGeometry(5000,5000),
  new THREE.MeshStandardMaterial({
    color:0x287e9c, roughness:0.24, metalness:0.25,
    transparent:true, opacity:0.94
  })
);
water.rotation.x = -Math.PI/2;
water.position.y = -7;
water.receiveShadow = true;
scene.add(water);

const shoreMat = new THREE.MeshStandardMaterial({color:0x527b54, roughness:1});
for(let i=0;i<9;i++){
  const hill = new THREE.Mesh(
    new THREE.SphereGeometry(1,32,20),
    shoreMat
  );
  hill.scale.set(90+i*18, 16+i*2, 40);
  hill.position.set(-300+i*78, -1, -240-(i%3)*32);
  scene.add(hill);
}
for(let i=0;i<7;i++){
  const hill = new THREE.Mesh(new THREE.SphereGeometry(1,32,20),shoreMat);
  hill.scale.set(100,20,48);
  hill.position.set(-270+i*90,-2,280+(i%2)*30);
  scene.add(hill);
}

let bridge = null;
let bridgeAxis = 'x';
let bridgeLength = 300;
let deckY = 35;
let sensorGroup = new THREE.Group();
scene.add(sensorGroup);
let vehicleGroup = new THREE.Group();
scene.add(vehicleGroup);
let sensorVisible = true;
let vehicles = [];
let extraActive = false;
let running = true;
let elapsed = 0;
let history = [];
let rows = [];
let lastValues = {};
let vehicleCounter = 0;

function toast(msg){
  const el=document.getElementById('toast');
  el.textContent=msg;
  el.style.display='block';
  setTimeout(()=>el.style.display='none',2200);
}

function normalizeBridge(model){
  const box = new THREE.Box3().setFromObject(model);
  const size = new THREE.Vector3();
  const center = new THREE.Vector3();
  box.getSize(size);
  box.getCenter(center);
  bridgeAxis = size.x >= size.z ? 'x' : 'z';
  bridgeLength = Math.max(size.x,size.z);
  const scale = 300 / Math.max(bridgeLength,1);
  model.scale.setScalar(scale);
  model.position.sub(center.multiplyScalar(scale));
  model.position.y += 15;
  model.traverse(obj=>{
    if(obj.isMesh){
      obj.castShadow=true;
      obj.receiveShadow=true;
      if(obj.material){
        obj.material.side=THREE.DoubleSide;
      }
    }
  });
  const newBox = new THREE.Box3().setFromObject(model);
  const newSize = new THREE.Vector3();
  newBox.getSize(newSize);
  deckY = newBox.min.y + newSize.y*0.31;
  controls.target.set(0,deckY+12,0);
  camera.position.set(
    bridgeAxis==='x' ? 0 : 225,
    deckY+100,
    bridgeAxis==='x' ? 225 : 0
  );
  controls.update();
}

function addSensor(position, color, size=1.3){
  const mesh = new THREE.Mesh(
    new THREE.SphereGeometry(size,14,14),
    new THREE.MeshStandardMaterial({
      color, emissive:color, emissiveIntensity:1.8,
      roughness:0.3, metalness:0.1
    })
  );
  mesh.position.copy(position);
  sensorGroup.add(mesh);
  const halo = new THREE.Mesh(
    new THREE.SphereGeometry(size*2.2,12,12),
    new THREE.MeshBasicMaterial({color,transparent:true,opacity:0.12})
  );
  halo.position.copy(position);
  sensorGroup.add(halo);
}

function buildSensors(){
  sensorGroup.clear();
  for(let i=0;i<27;i++){
    const t=(i/26-0.5)*bridgeLength*0.86;
    const pos=bridgeAxis==='x'
      ? new THREE.Vector3(t,deckY+1.5,0)
      : new THREE.Vector3(0,deckY+1.5,t);
    addSensor(pos,0x43e6a1,1.05);
  }
  for(let i=0;i<12;i++){
    const t=(i/11-0.5)*bridgeLength*0.7;
    const pos=bridgeAxis==='x'
      ? new THREE.Vector3(t,deckY+4,8)
      : new THREE.Vector3(8,deckY+4,t);
    addSensor(pos,0x5ac8ff,0.85);
  }
  for(let i=0;i<14;i++){
    const t=(i/13-0.5)*bridgeLength*0.72;
    const pos=bridgeAxis==='x'
      ? new THREE.Vector3(t,deckY+7,-7)
      : new THREE.Vector3(-7,deckY+7,t);
    addSensor(pos,0x43e6a1,0.8);
  }
  for(let i=0;i<18;i++){
    const t=(i/17-0.5)*bridgeLength*0.8;
    const pos=bridgeAxis==='x'
      ? new THREE.Vector3(t,deckY+3,12)
      : new THREE.Vector3(-12,deckY+3,t);
    addSensor(pos,0xff655c,0.9);
  }
  sensorGroup.visible=sensorVisible;
}

function createVehicle(){
  const group=new THREE.Group();
  const bodyMat=new THREE.MeshStandardMaterial({
    color:0xf3f5f6,metalness:0.48,roughness:0.32
  });
  const body=new THREE.Mesh(new THREE.BoxGeometry(10,3.2,4.3),bodyMat);
  body.position.y=2.8;
  body.castShadow=true;
  group.add(body);
  const cabin=new THREE.Mesh(
    new THREE.BoxGeometry(4.2,2.6,4.0),
    new THREE.MeshStandardMaterial({color:0x8ab7c8,metalness:0.4,roughness:0.2})
  );
  cabin.position.set(-1.8,5.3,0);
  group.add(cabin);
  const wheelMat=new THREE.MeshStandardMaterial({color:0x18232b,roughness:0.9});
  for(const x of [-3.4,3.3]){
    for(const z of [-2.1,2.1]){
      const wheel=new THREE.Mesh(new THREE.CylinderGeometry(0.9,0.9,0.5,18),wheelMat);
      wheel.rotation.x=Math.PI/2;
      wheel.position.set(x,1.2,z);
      group.add(wheel);
    }
  }
  vehicleGroup.add(group);
  vehicles.push({mesh:group, progress:Math.random()*0.3});
  vehicleCounter++;
  document.getElementById('vehicleCount').textContent='Vehicles in simulation: '+vehicles.length;
}
createVehicle();

function getVal(id){return Number(document.getElementById(id).value)}
function setText(id,value){document.getElementById(id).textContent=value}

function syncLabels(){
  setText('weightOut',getVal('weight')+' t');
  setText('speedOut',getVal('speed')+' km/h');
  setText('axleOut',getVal('axles'));
  setText('trafficOut',getVal('traffic')+'%');
  setText('stiffOut',getVal('stiff')+'%');
  setText('localOut',getVal('local')+'%');
  setText('triggerOut',getVal('trigger')+'%');
  setText('stepOut',(getVal('step')/10).toFixed(1)+' s');
  setText('trafficBig',getVal('traffic')+'%');
}
['weight','speed','axles','traffic','stiff','local','trigger','step'].forEach(id=>{
  document.getElementById(id).addEventListener('input',syncLabels);
});
syncLabels();

function updateHistory(value){
  history.push(value);
  if(history.length>60)history.shift();
  const pts=history.map((v,i)=>{
    const x=i/(Math.max(history.length-1,1))*400;
    const y=49-Math.min(v/40,1)*43;
    return x.toFixed(1)+','+y.toFixed(1);
  }).join(' ');
  document.getElementById('historyLine').setAttribute('points',pts);
  document.getElementById('historyFill').setAttribute('points','0,52 '+pts+' 400,52');
}

function updateSimulation(dt){
  const weight=getVal('weight');
  const speed=getVal('speed');
  const traffic=getVal('traffic');
  const stiffness=getVal('stiff');
  const local=getVal('local');
  const trigger=getVal('trigger');
  const mode=document.getElementById('monitorMode').value;

  const load=weight/45;
  const temporary=load*(traffic/100)*(speed/110);
  const changeSignal=(stiffness/30)*0.75+(local/100)*0.55;
  const response=temporary*12+changeSignal*14;
  const deviation=changeSignal*100+temporary*3;
  const eventScore=Math.min(100,Math.max(0,deviation*1.4));
  extraActive=mode==='always'||(mode==='adaptive'&&eventScore>=trigger);

  const deflection=0.7+temporary*4.4+changeSignal*5.2;
  const strain=72+temporary*110+changeSignal*180;
  const vibration=0.03+temporary*0.34+changeSignal*0.2;
  const temperature=27+Math.sin(elapsed/25)*1.5;

  setText('deflection',deflection.toFixed(2));
  setText('strain',strain.toFixed(0));
  setText('vibration',vibration.toFixed(2));
  setText('temperature',temperature.toFixed(1));
  setText('deviation',deviation.toFixed(1)+'%');
  setText('persistence',changeSignal>0.3?'ELEVATED':changeSignal>0.08?'MODERATE':'LOW');
  setText('extraState',extraActive?'66 ACTIVE':'66 STANDBY');
  document.getElementById('extraState').className='sensorstate'+(extraActive?'':' off');
  ['tiltState','acousticState','jointState'].forEach(id=>{
    setText(id,extraActive?'ACTIVE':'STANDBY');
    document.getElementById(id).className='sensorstate'+(extraActive?'':' off');
  });
  setText('tiltValue',(0.02+changeSignal*0.6).toFixed(2)+'°');
  setText('humidity','68%');
  setText('corrosion',changeSignal>0.6?'Elevated proxy':'Low');
  setText('crack',(changeSignal*0.28).toFixed(2)+' mm');
  setText('acousticValue',extraActive?'Elevated':'Low');
  setText('jointValue',(0.3+changeSignal*1.4).toFixed(2)+' mm');
  setText('modePill',extraActive?'ADAPTIVE ATTENTION ACTIVE':mode==='always'?'ALL SENSORS ACTIVE':'CONTINUOUS MONITORING');

  const alert=document.getElementById('alertBox');
  const responseBig=document.getElementById('responseBig');
  if(changeSignal>0.3){
    alert.className='alert warn';
    alert.textContent='Persistent-change scenario detected in the simulation. Additional sensor attention is '+(extraActive?'ACTIVE':'not active')+'.';
    responseBig.textContent='CHANGE';
    setText('responseSmall','Simulated response differs from baseline');
  }else if(temporary>0.4){
    alert.className='alert';
    alert.textContent='Elevated temporary traffic-load response. Continue comparing with baseline.';
    responseBig.textContent='LOAD';
    setText('responseSmall','Temporary load response in simulation');
  }else{
    alert.className='alert good';
    alert.textContent='Normal operating pattern. Primary monitoring is active.';
    responseBig.textContent='NORMAL';
    setText('responseSmall','Within simulated baseline');
  }
  updateHistory(response);
  lastValues={elapsed,weight,speed,traffic,deflection,strain,vibration,temperature,deviation,extraActive,stiffness,local};
  rows.push({...lastValues});
  if(rows.length>2000)rows.shift();
}

document.getElementById('runBtn').onclick=()=>{
  running=!running;
  setText('runBtn',running?'Ⅱ PAUSE':'▶ RUN');
  toast(running?'Simulation running':'Simulation paused');
};
document.getElementById('resetBtn').onclick=()=>{
  elapsed=0;history=[];rows=[];
  ['stiff','local'].forEach(id=>document.getElementById(id).value=0);
  syncLabels();
  updateSimulation(0);
  toast('Simulation reset');
};
document.getElementById('vehicleBtn').onclick=()=>{
  createVehicle();
  toast('Vehicle added to simulation');
};
document.getElementById('cameraBtn').onclick=()=>{
  if(bridge){
    camera.position.set(bridgeAxis==='x'?0:225,deckY+100,bridgeAxis==='x'?225:0);
    controls.target.set(0,deckY+12,0);
    controls.update();
  }
};
document.getElementById('sensorsBtn').onclick=()=>{
  sensorVisible=!sensorVisible;
  sensorGroup.visible=sensorVisible;
  setText('sensorsBtn',sensorVisible?'HIDE SENSORS':'SHOW SENSORS');
};
document.getElementById('exportBtn').onclick=()=>{
  if(!rows.length){toast('Run the simulation to collect data');return;}
  const keys=Object.keys(rows[0]);
  const csv=[keys.join(','),...rows.map(r=>keys.map(k=>r[k]).join(','))].join('\\n');
  const blob=new Blob([csv],{type:'text/csv'});
  const url=URL.createObjectURL(blob);
  const a=document.createElement('a');
  a.href=url;a.download='bridge-monitoring-simulation.csv';a.click();
  URL.revokeObjectURL(url);
  setText('exportStatus','CSV file exported');
};

const loader=new GLTFLoader();
loader.load(
  MODEL_URL,
  gltf=>{
    bridge=gltf.scene;
    normalizeBridge(bridge);
    scene.add(bridge);
    buildSensors();
    document.getElementById('loading').style.display='none';
    toast('3D bridge model loaded');
  },
  xhr=>{
    if(xhr.total){
      document.querySelector('#loading').innerHTML=
        'LOADING 3D BRIDGE MODEL<br><small>'+Math.round(xhr.loaded/xhr.total*100)+'%</small>';
    }
  },
  error=>{
    document.getElementById('loading').innerHTML=
      'BRIDGE MODEL COULD NOT LOAD<br><small>Check that the GLB file is uploaded to the repository assets folder and the repository is public.</small>';
    console.error(error);
  }
);

function animate(){
  requestAnimationFrame(animate);
  const dt=Math.min(clock.getDelta(),0.05);
  if(running){
    elapsed+=dt;
    vehicles.forEach(v=>{
      v.progress+=dt*(getVal('speed')/110)*0.08;
      if(v.progress>1.1)v.progress=-0.1;
      const p=(v.progress-0.5)*bridgeLength*0.82;
      if(bridgeAxis==='x'){
        v.mesh.position.set(p,deckY+0.5,0);
      }else{
        v.mesh.position.set(0,deckY+0.5,p);
        v.mesh.rotation.y=Math.PI/2;
      }
    });
    if(Math.floor(elapsed*2)!==Math.floor((elapsed-dt)*2)){
      updateSimulation(dt);
    }
  }
  controls.update();
  renderer.render(scene,camera);
  const seconds=Math.floor(elapsed);
  setText('clock',new Date(seconds*1000).toISOString().substring(11,19));
}
const clock=new THREE.Clock();
updateSimulation(0);
animate();

addEventListener('resize',()=>{
  camera.aspect=innerWidth/innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth,innerHeight);
});
</script>
</body>
</html>
"""

components.html(html, height=1050, scrolling=False)
