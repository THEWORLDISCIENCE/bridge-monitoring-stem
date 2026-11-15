
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
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {
    margin:0!important;
    padding:0!important;
    background:#071522!important;
}
header, footer, #MainMenu,
[data-testid="stHeader"],
[data-testid="stToolbar"] {
    display:none!important;
}
.block-container {
    padding:0!important;
    max-width:100%!important;
}
iframe {
    border:0!important;
    display:block;
}
</style>
""", unsafe_allow_html=True)

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
* { box-sizing:border-box; }
html,body {
    margin:0;
    width:100%;
    height:100%;
    overflow:hidden;
    font-family:Inter,Arial,sans-serif;
    background:#071522;
    color:#eaf7ff;
}
#scene {
    position:fixed;
    inset:0;
    z-index:0;
}
canvas { display:block; }

.glass {
    position:absolute;
    z-index:5;
    color:#eaf7ff;
    background:linear-gradient(
        135deg,
        rgba(7,26,43,.88),
        rgba(8,38,57,.69)
    );
    border:1px solid rgba(119,213,255,.28);
    border-radius:12px;
    backdrop-filter:blur(18px);
    -webkit-backdrop-filter:blur(18px);
    box-shadow:0 12px 45px rgba(0,0,0,.32),
               inset 0 1px 0 rgba(255,255,255,.08);
    padding:13px;
    font-size:11px;
}
#header {
    top:12px;
    left:14px;
    right:14px;
    height:66px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:10px 19px;
}
.logo {
    font-size:17px;
    font-weight:800;
    letter-spacing:1.2px;
}
.kicker {
    color:#8fb6cb;
    font-size:9px;
    letter-spacing:1.7px;
    margin-top:5px;
}
.header-right {
    display:flex;
    align-items:center;
    gap:24px;
}
.online {
    color:#62f2bd;
    font-weight:800;
    letter-spacing:1px;
}
.mode {
    color:#83dfff;
    font-size:10px;
    margin-top:5px;
}
#left {
    top:91px;
    left:14px;
    width:244px;
    bottom:143px;
    overflow-y:auto;
}
#right {
    top:91px;
    right:14px;
    width:260px;
    bottom:143px;
    overflow-y:auto;
}
#bottom {
    left:14px;
    right:14px;
    bottom:12px;
    min-height:116px;
    display:grid;
    grid-template-columns:1fr 1fr 1fr 1.25fr;
    gap:12px;
}
h3 {
    margin:0 0 10px;
    color:#a8dff5;
    font-size:10px;
    letter-spacing:1.5px;
}
.section {
    border-bottom:1px solid rgba(143,207,235,.16);
    padding-bottom:12px;
    margin-bottom:13px;
}
.section:last-child {
    border:0;
    margin-bottom:0;
}
label {
    display:flex;
    justify-content:space-between;
    color:#aac6d7;
    font-size:10px;
    margin:8px 0 4px;
}
input[type=range] {
    width:100%;
    accent-color:#48cfff;
    cursor:pointer;
}
select {
    width:100%;
    color:#eaf7ff;
    background:#15364c;
    border:1px solid #35657c;
    border-radius:5px;
    padding:7px;
    margin:4px 0;
}
button {
    background:linear-gradient(135deg,#087fa8,#19b7d4);
    border:1px solid rgba(126,225,255,.35);
    border-radius:6px;
    color:white;
    font-weight:700;
    font-size:10px;
    padding:8px 10px;
    cursor:pointer;
    margin:3px 2px 3px 0;
}
button.secondary {
    background:rgba(93,137,160,.22);
}
button:hover { filter:brightness(1.2); }
.value {
    color:#f2fbff;
    font-size:17px;
    font-weight:800;
}
.small {
    color:#8eafc2;
    font-size:9px;
}
.row {
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:7px 0;
    border-bottom:1px solid rgba(255,255,255,.07);
}
.green { color:#59edb0; }
.cyan { color:#64dfff; }
.red { color:#ff777d; }
.amber { color:#ffca71; }
.pill {
    display:inline-block;
    padding:4px 7px;
    border-radius:20px;
    background:rgba(65,203,255,.12);
    color:#80dcff;
    border:1px solid rgba(92,211,255,.2);
    font-size:9px;
}
.metric {
    background:rgba(110,185,220,.08);
    border:1px solid rgba(127,210,245,.12);
    border-radius:8px;
    padding:9px;
}
.metric .value { font-size:20px; }
#historyChart {
    width:100%;
    height:48px;
}
#loading {
    position:absolute;
    inset:0;
    z-index:20;
    display:flex;
    align-items:center;
    justify-content:center;
    flex-direction:column;
    background:#102e43;
    color:#dff6ff;
    letter-spacing:2px;
    font-size:14px;
}
#loadError {
    color:#ffb1a9;
    max-width:520px;
    line-height:1.6;
    text-align:center;
    padding:20px;
}
#toast {
    position:absolute;
    z-index:10;
    bottom:145px;
    left:50%;
    transform:translateX(-50%);
    background:rgba(5,24,38,.85);
    border:1px solid rgba(110,220,255,.3);
    padding:8px 15px;
    border-radius:8px;
    font-size:10px;
    color:#bfeeff;
    display:none;
}
@media(max-width:900px) {
    #left { width:205px; }
    #right { width:215px; }
    #bottom { grid-template-columns:1fr 1fr; }
    .header-right .small { display:none; }
}
</style>
</head>

<body>
<div id="scene"></div>
<div id="loading">
    <div>INTELLIGENT BRIDGE MONITORING</div>
    <div class="small" style="margin-top:12px">
        INITIALIZING 3D DIGITAL TWIN
    </div>
    <div id="loadError"></div>
</div>

<div class="glass" id="header">
    <div>
        <div class="logo">◈ INTELLIGENT BRIDGE MONITORING</div>
        <div class="kicker">STRUCTURAL DIGITAL TWIN · LIVE SIMULATION</div>
    </div>
    <div class="header-right">
        <div>
            <div class="online" id="systemStatus">● SYSTEM ONLINE</div>
            <div class="mode" id="mode">CONTINUOUS MONITORING</div>
        </div>
        <div>
            <div class="pill">SIMULATION ENVIRONMENT</div>
            <div class="small" style="margin-top:5px;text-align:right">
                MODEL-BASED VISUALIZATION
            </div>
        </div>
    </div>
</div>

<!-- LEFT CONTROL PANEL -->
<div class="glass" id="left">

    <div class="section">
        <h3>01 / VEHICLE SIMULATION</h3>

        <label>Vehicle weight <b id="weightVal">25 tons</b></label>
        <input id="weight" type="range" min="5" max="80" value="25">

        <label>Number of axles <b id="axlesVal">3</b></label>
        <input id="axles" type="range" min="2" max="8" value="3">

        <label>Axle spacing <b id="spacingVal">3.0 m</b></label>
        <input id="spacing" type="range" min="1" max="8" step=".5" value="3">

        <label>Vehicle speed <b id="speedVal">60 km/h</b></label>
        <input id="speed" type="range" min="10" max="120" value="60">

        <label>Traffic volume</label>
        <select id="traffic">
            <option value="normal">Normal traffic</option>
            <option value="busy">Busy traffic</option>
            <option value="heavy">Heavy traffic</option>
        </select>

        <div style="margin-top:8px">
            <button id="start">▶ START</button>
            <button class="secondary" id="pause">Ⅱ PAUSE</button>
            <button class="secondary" id="resetVehicle">RESET</button>
        </div>
    </div>

    <div class="section">
        <h3>02 / STRUCTURAL CHANGE INPUT</h3>

        <label>Global stiffness reduction <b id="stiffVal">0%</b></label>
        <input id="stiffness" type="range" min="0" max="30" value="0">

        <label>Local change signal <b id="localVal">0%</b></label>
        <input id="localChange" type="range" min="0" max="30" value="0">

        <label>Simulated change location <b id="locationVal">50%</b></label>
        <input id="location" type="range" min="5" max="95" value="50">

        <label>Deflection attention trigger <b id="triggerVal">2.0 mm</b></label>
        <input id="trigger" type="range" min=".5" max="5" step=".1" value="2">

        <div style="margin-top:7px">
            <button class="secondary" id="clearChange">CLEAR CHANGE INPUT</button>
        </div>
    </div>

    <div class="section">
        <h3>03 / SIMULATION CONTROLS</h3>
        <label>Simulation time step</label>
        <select id="timeStep">
            <option value="1">1× Real-time</option>
            <option value="2">2× Accelerated</option>
            <option value="4">4× Accelerated</option>
        </select>
        <label>Monitoring mode</label>
        <select id="monitoring">
            <option value="adaptive">Adaptive attention</option>
            <option value="normal">Always-on only</option>
        </select>
        <button class="secondary" id="resetAll">RESET ALL SETTINGS</button>
    </div>
</div>

<!-- RIGHT SENSOR PANEL -->
<div class="glass" id="right">
    <div class="section">
        <h3>04 / SENSOR NETWORK</h3>
        <div class="row">
            <span>Always-on sensors</span>
            <b class="green">55 ACTIVE</b>
        </div>
        <div class="row">
            <span>Additional sensors</span>
            <b id="extraCount" class="amber">66 STANDBY</b>
        </div>
        <div class="row">
            <span>Sensor stations</span><b>11</b>
        </div>
        <div class="row">
            <span>Always-on channels</span><b>5</b>
        </div>
        <div class="row">
            <span>Additional channels</span><b>6</b>
        </div>
    </div>

    <div class="section">
        <h3>05 / LIVE MEASUREMENTS</h3>
        <div class="row"><span>Deflection</span><b id="deflection" class="cyan">0.00 mm</b></div>
        <div class="row"><span>Strain proxy</span><b id="strain">0.000</b></div>
        <div class="row"><span>Vibration index</span><b id="vibration">0.000</b></div>
        <div class="row"><span>Temperature</span><b id="temperature">24.5 °C</b></div>
        <div class="row"><span>Traffic/load index</span><b id="loadIndex">0%</b></div>
    </div>

    <div class="section">
        <h3>06 / SPECIAL-ATTENTION SENSORS</h3>
        <div class="row"><span>Tilt proxy</span><b id="tilt">STANDBY</b></div>
        <div class="row"><span>Humidity</span><b id="humidity">STANDBY</b></div>
        <div class="row"><span>Corrosion indicator</span><b id="corrosion">STANDBY</b></div>
        <div class="row"><span>Crack-width proxy</span><b id="crack">STANDBY</b></div>
        <div class="row"><span>Acoustic activity</span><b id="acoustic">STANDBY</b></div>
        <div class="row"><span>Joint displacement</span><b id="joint">STANDBY</b></div>
    </div>

    <div class="section">
        <h3>07 / EVENT ANALYSIS</h3>
        <div id="alert" class="green">● NO EVENT DETECTED</div>
        <div class="small" id="alertDetail" style="margin-top:8px">
            Baseline response within simulated limits.
        </div>
        <div class="row">
            <span>Baseline comparison</span>
            <b id="baselineStatus" class="green">MATCH</b>
        </div>
        <div class="row">
            <span>Change persistence</span>
            <b id="persistence">NOT DETECTED</b>
        </div>
        <div class="row">
            <span>Attention mode</span>
            <b id="attentionMode" class="green">NORMAL</b>
        </div>
    </div>
</div>

<!-- BOTTOM DASHBOARD -->
<div class="glass" id="bottom">
    <div>
        <h3>08 / TRAFFIC STATUS</h3>
        <div class="value" id="trafficPercent">100%</div>
        <div class="small" id="trafficText">Normal traffic volume</div>
    </div>

    <div>
        <h3>09 / STRUCTURAL RESPONSE</h3>
        <div class="value" id="responseValue">0.0%</div>
        <div class="small">Response difference from baseline</div>
    </div>

    <div>
        <h3>10 / SENSOR HISTORY</h3>
        <div class="value" id="historyCount">0</div>
        <div class="small">Recorded data snapshots</div>
        <canvas id="historyChart"></canvas>
    </div>

    <div>
        <h3>11 / DIGITAL TWIN CONTROLS</h3>
        <div class="small">Drag to rotate · Scroll to zoom · Right-click to pan</div>
        <button class="secondary" id="cameraReset">RESET CAMERA</button>
        <button class="secondary" id="exportCsv">EXPORT CSV</button>
        <button class="secondary" id="sensorToggle">SENSOR VISIBILITY</button>
    </div>
</div>

<div id="toast"></div>

<script type="importmap">
{
 "imports": {
  "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
  "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
 }
}
</script>

<script type="module">
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { Sky } from "three/addons/objects/Sky.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

const MODEL_URL =
"https://raw.githubusercontent.com/experimentscience/bridge-monitoring-stem/main/assets/cable-stayed-bridge.glb";

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x91c8e4);
scene.fog = new THREE.Fog(0x91c8e4, 350, 1100);

const camera = new THREE.PerspectiveCamera(
    42, innerWidth/innerHeight, 0.1, 3000
);
camera.position.set(130,90,170);

const renderer = new THREE.WebGLRenderer({
    antialias:true,
    powerPreference:"high-performance"
});
renderer.setSize(innerWidth,innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
document.getElementById("scene").appendChild(renderer.domElement);

const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(
    new RoomEnvironment(renderer), .04
).texture;

const controls = new OrbitControls(camera,renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = .06;
controls.target.set(0,20,0);
controls.minDistance = 35;
controls.maxDistance = 550;
controls.maxPolarAngle = Math.PI*.48;

scene.add(new THREE.HemisphereLight(0xd9f2ff,0x526c61,1.7));

const sunlight = new THREE.DirectionalLight(0xfff2df,3.2);
sunlight.position.set(-120,220,100);
sunlight.castShadow = true;
sunlight.shadow.mapSize.set(2048,2048);
sunlight.shadow.camera.left = -300;
sunlight.shadow.camera.right = 300;
sunlight.shadow.camera.top = 300;
sunlight.shadow.camera.bottom = -300;
sunlight.shadow.bias = -.00015;
scene.add(sunlight);

const sky = new Sky();
sky.scale.setScalar(10000);
sky.material.uniforms.turbidity.value = 6;
sky.material.uniforms.rayleigh.value = 2;
sky.material.uniforms.mieCoefficient.value = .004;
sky.material.uniforms.mieDirectionalG.value = .8;
scene.add(sky);

const waterMaterial = new THREE.MeshPhysicalMaterial({
    color:0x287fa5,
    roughness:.22,
    metalness:.22,
    clearcoat:.9,
    clearcoatRoughness:.12
});
const water = new THREE.Mesh(
    new THREE.PlaneGeometry(3000,3000),
    waterMaterial
);
water.rotation.x=-Math.PI/2;
water.position.y=-3;
water.receiveShadow=true;
scene.add(water);

const shore = new THREE.Mesh(
    new THREE.PlaneGeometry(3000,400),
    new THREE.MeshStandardMaterial({
        color:0x527d54,
        roughness:1
    })
);
shore.rotation.x=-Math.PI/2;
shore.position.set(0,-2.7,-430);
scene.add(shore);

// Distant horizon haze and restrained landscape silhouettes
const horizon = new THREE.Mesh(
    new THREE.PlaneGeometry(3000,500),
    new THREE.MeshBasicMaterial({
        color:0x83b6c9,
        transparent:true,
        opacity:.22
    })
);
horizon.position.set(0,100,-650);
scene.add(horizon);

const bridgeGroup = new THREE.Group();
scene.add(bridgeGroup);

const alwaysGroup = new THREE.Group();
const extraGroup = new THREE.Group();
scene.add(alwaysGroup,extraGroup);

let modelLength = 200;
let deckY = 12;
let modelLoaded = false;
let vehiclePosition = -115;
let running = false;
let history = [];
let rows = [[
    "timestamp","vehicle_weight_tons","axles","axle_spacing_m",
    "speed_kmh","traffic","deflection_mm","strain_proxy",
    "vibration_index","stiffness_reduction_percent",
    "local_change_percent","special_attention"
]];

const $ = id => document.getElementById(id);

function toast(message) {
    $("toast").textContent=message;
    $("toast").style.display="block";
    setTimeout(()=> $("toast").style.display="none",2200);
}

function marker(color,radius=.65) {
    const m = new THREE.Mesh(
        new THREE.SphereGeometry(radius,20,20),
        new THREE.MeshStandardMaterial({
            color,
            emissive:color,
            emissiveIntensity:1.3,
            roughness:.2,
            metalness:.1
        })
    );
    m.castShadow=true;
    return m;
}

function buildSensors() {
    alwaysGroup.clear();
    extraGroup.clear();

    for(let i=0;i<11;i++) {
        const x=-modelLength*.43+i*modelLength*.086;
        const a=marker(0x35f4b1,.7);
        a.position.set(x,deckY+1,0);
        alwaysGroup.add(a);

        const b=marker(0xff4d5e,.58);
        b.position.set(x,deckY+2.5,1.5);
        extraGroup.add(b);
    }

    [-.25,.25].forEach(z=>{
        [-.25,.25].forEach(x=>{
            const m=marker(0x35f4b1,.8);
            m.position.set(x*modelLength,deckY+5,z*modelLength*.1);
            alwaysGroup.add(m);
        });
    });
    extraGroup.visible=false;
}

function addVehicle() {
    const g=new THREE.Group();

    const bodyMat=new THREE.MeshStandardMaterial({
        color:0x263d4b,
        metalness:.8,
        roughness:.24
    });
    const glassMat=new THREE.MeshPhysicalMaterial({
        color:0x83b9ce,
        metalness:.5,
        roughness:.12,
        transparent:true,
        opacity:.8
    });
    const body=new THREE.Mesh(
        new THREE.BoxGeometry(8,2.1,3.5),bodyMat
    );
    body.position.y=1.6;
    body.castShadow=true;
    g.add(body);

    const cabin=new THREE.Mesh(
        new THREE.BoxGeometry(3.8,1.6,3.15),glassMat
    );
    cabin.position.set(-.5,3.3,0);
    cabin.castShadow=true;
    g.add(cabin);

    const wheelMat=new THREE.MeshStandardMaterial({
        color:0x111820,roughness:.85
    });
    for(const x of [-2.7,2.7]) {
        for(const z of [-1.8,1.8]) {
            const w=new THREE.Mesh(
                new THREE.CylinderGeometry(.8,.8,.45,20),
                wheelMat
            );
            w.rotation.x=Math.PI/2;
            w.position.set(x,.8,z);
            g.add(w);
        }
    }
    scene.add(g);
    return g;
}
const vehicle=addVehicle();

const loader=new GLTFLoader();
loader.load(
    MODEL_URL,
    gltf=>{
        const model=gltf.scene;
        let box=new THREE.Box3().setFromObject(model);
        let size=box.getSize(new THREE.Vector3());

        // Rotate so the bridge's longest horizontal dimension runs along X.
        if(size.z>size.x) {
            model.rotation.y=Math.PI/2;
        }

        box=new THREE.Box3().setFromObject(model);
        let center=box.getCenter(new THREE.Vector3());
        let longest=Math.max(size.x,size.z);
        const scale=220/longest;
        model.scale.setScalar(scale);
        model.position.sub(center.multiplyScalar(scale));

        box=new THREE.Box3().setFromObject(model);
        model.position.y-=box.min.y;

        model.traverse(o=>{
            if(o.isMesh) {
                o.castShadow=true;
                o.receiveShadow=true;
                if(o.material) {
                    o.material.envMapIntensity=1.1;
                    o.material.needsUpdate=true;
                }
            }
        });

        bridgeGroup.add(model);
        box=new THREE.Box3().setFromObject(model);
        const finalSize=box.getSize(new THREE.Vector3());

        modelLength=Math.max(finalSize.x,finalSize.z);
        deckY=finalSize.y*.28;
        buildSensors();

        controls.target.set(0,finalSize.y*.38,0);
        camera.position.set(
            modelLength*.55,
            finalSize.y*1.45,
            modelLength*.72
        );
        controls.update();

        modelLoaded=true;
        $("loading").style.display="none";
        toast("3D bridge model loaded");
    },
    xhr=>{
        if(xhr.total) {
            $("loadError").textContent=
                "Loading bridge model: "+
                Math.round(xhr.loaded/xhr.total*100)+"%";
        }
    },
    error=>{
        $("loadError").textContent=
            "Bridge model could not be loaded. Check that the file is committed to the main branch at assets/cable-stayed-bridge.glb, and that the repository is public.";
        console.error(error);
    }
);

// INPUTS
const inputs=[
    ["weight","weightVal",v=>v+" tons"],
    ["axles","axlesVal",v=>v],
    ["spacing","spacingVal",v=>Number(v).toFixed(1)+" m"],
    ["speed","speedVal",v=>v+" km/h"],
    ["stiffness","stiffVal",v=>v+"%"],
    ["localChange","localVal",v=>v+"%"],
    ["location","locationVal",v=>v+"%"],
    ["trigger","triggerVal",v=>Number(v).toFixed(1)+" mm"]
];

inputs.forEach(([id,label,format])=>{
    $(id).addEventListener("input",()=>{
        $(label).textContent=format($(id).value);
    });
});

$("start").onclick=()=>{running=true;toast("Vehicle simulation started");};
$("pause").onclick=()=>{running=false;toast("Simulation paused");};
$("resetVehicle").onclick=()=>{
    running=false;
    vehiclePosition=-modelLength*.5;
    toast("Vehicle position reset");
};

$("clearChange").onclick=()=>{
    $("stiffness").value=0;
    $("localChange").value=0;
    $("stiffVal").textContent="0%";
    $("localVal").textContent="0%";
    toast("Structural change inputs cleared");
};

$("resetAll").onclick=()=>{
    const defaults={
        weight:25,axles:3,spacing:3,speed:60,
        stiffness:0,localChange:0,location:50,trigger:2
    };
    Object.entries(defaults).forEach(([id,v])=>{
        $(id).value=v;
        $(id).dispatchEvent(new Event("input"));
    });
    $("traffic").value="normal";
    $("monitoring").value="adaptive";
    $("timeStep").value="1";
    running=false;
    vehiclePosition=-modelLength*.5;
    toast("All simulation settings reset");
};

$("cameraReset").onclick=()=>{
    camera.position.set(modelLength*.55,90,modelLength*.72);
    controls.target.set(0,deckY+8,0);
    controls.update();
};

$("sensorToggle").onclick=()=>{
    alwaysGroup.visible=!alwaysGroup.visible;
    extraGroup.visible=extraGroup.visible && alwaysGroup.visible;
    toast(alwaysGroup.visible?"Sensors visible":"Sensors hidden");
};

$("exportCsv").onclick=()=>{
    const csv=rows.map(r=>r.join(",")).join("\n");
    const blob=new Blob([csv],{type:"text/csv"});
    const url=URL.createObjectURL(blob);
    const a=document.createElement("a");
    a.href=url;
    a.download="bridge-monitoring-data.csv";
    a.click();
    URL.revokeObjectURL(url);
};

function drawHistory() {
    const c=$("historyChart");
    const ctx=c.getContext("2d");
    const w=c.width=c.clientWidth*2;
    const h=c.height=c.clientHeight*2;
    ctx.clearRect(0,0,w,h);
    if(history.length<2)return;

    const max=Math.max(...history,1);
    ctx.beginPath();
    history.forEach((v,i)=>{
        const x=i/(history.length-1)*w;
        const y=h-(v/max)*(h*.85)-h*.05;
        if(i===0)ctx.moveTo(x,y);
        else ctx.lineTo(x,y);
    });
    ctx.strokeStyle="#53d9ff";
    ctx.lineWidth=3;
    ctx.stroke();
}

let lastSnapshot=0;
let previous=performance.now();

function updateSimulation(dt) {
    const weight=Number($("weight").value);
    const axles=Number($("axles").value);
    const spacing=Number($("spacing").value);
    const speed=Number($("speed").value);
    const stiffness=Number($("stiffness").value);
    const local=Number($("localChange").value);
    const location=Number($("location").value);
    const trigger=Number($("trigger").value);
    const traffic=$("traffic").value;
    const adaptive=$("monitoring").value==="adaptive";

    const trafficFactor={
        normal:1,busy:1.45,heavy:2
    }[traffic];

    if(running) {
        vehiclePosition+=dt*speed/18*Number($("timeStep").value);
        if(vehiclePosition>modelLength*.52)
            vehiclePosition=-modelLength*.52;
    }

    const vehicleX=vehiclePosition;
    vehicle.position.set(vehicleX,deckY,0);

    const normalizedDistance=Math.abs(vehicleX)/(modelLength*.52);
    const proximity=Math.max(0,1-normalizedDistance);

    const baselineDeflection=
        (weight/25)*(axles/3)*(1+spacing*.025)*
        proximity*1.6*trafficFactor;

    const stiffnessFactor=1+stiffness/100;
    const localFactor=1+local/100;
    const deflection=baselineDeflection*stiffnessFactor*localFactor;
    const strain=deflection*.72;
    const vibration=proximity*(speed/60)*.9*trafficFactor;
    const responseDifference=
        baselineDeflection>0
        ? ((deflection-baselineDeflection)/baselineDeflection)*100
        : stiffness+local;

    const persistent=stiffness>=5 || local>=5;
    const temporary=deflection>=trigger;
    const special=adaptive && (temporary || persistent);

    $("deflection").textContent=deflection.toFixed(2)+" mm";
    $("strain").textContent=strain.toFixed(3);
    $("vibration").textContent=vibration.toFixed(3);
    $("temperature").textContent=(24.5+proximity*.6).toFixed(1)+" °C";
    $("loadIndex").textContent=Math.round(proximity*weight/80*100)+"%";
    $("responseValue").textContent=responseDifference.toFixed(1)+"%";

    const trafficPercent={
        normal:100,busy:145,heavy:200
    }[traffic];
    $("trafficPercent").textContent=trafficPercent+"%";
    $("trafficText").textContent=traffic+" traffic volume";

    $("mode").textContent=special
        ?"EVENT-TRIGGERED SPECIAL ATTENTION"
        :"CONTINUOUS MONITORING";

    $("extraCount").textContent=special?"66 ACTIVE":"66 STANDBY";
    $("extraCount").className=special?"red":"amber";
    extraGroup.visible=special;

    $("tilt").textContent=special?(local*.03+stiffness*.02).toFixed(3)+"°":"STANDBY";
    $("humidity").textContent=special?"58%":"STANDBY";
    $("corrosion").textContent=special?(stiffness*.8+local*.4).toFixed(1)+"%":"STANDBY";
    $("crack").textContent=special?(local*.012).toFixed(3)+" mm":"STANDBY";
    $("acoustic").textContent=special?(vibration*12).toFixed(2)+" idx":"STANDBY";
    $("joint").textContent=special?(deflection*.08).toFixed(3)+" mm":"STANDBY";

    $("alert").textContent=persistent
        ?"● PERSISTENT CHANGE SIGNAL"
        :temporary
        ?"● TEMPORARY LOAD EVENT"
        :"● NO EVENT DETECTED";

    $("alert").className=persistent?"red":temporary?"amber":"green";
    $("alertDetail").textContent=persistent
        ?"Simulated response differs from the baseline. Additional sensors are active."
        :temporary
        ?"Vehicle-load response exceeded the selected attention threshold."
        :"Baseline response is within the selected simulation threshold.";

    $("baselineStatus").textContent=persistent?"DIFFERENCE":"MATCH";
    $("baselineStatus").className=persistent?"red":"green";
    $("persistence").textContent=persistent?"SIGNAL PRESENT":"NOT DETECTED";
    $("attentionMode").textContent=special?"SPECIAL":"NORMAL";
    $("attentionMode").className=special?"red":"green";

    const targetX=-modelLength*.43+location/100*modelLength*.86;
    extraGroup.children.forEach((m,i)=>{
        const x=-modelLength*.43+i*modelLength*.086;
        const selected=Math.abs(x-targetX)<modelLength*.055;
        m.material.color.set(selected?0xffc35c:0xff4d5e);
        m.material.emissive.set(selected?0xff9e35:0xff253d);
    });

    const now=performance.now();
    if(now-lastSnapshot>1000) {
        lastSnapshot=now;
        history.push(deflection);
        if(history.length>80)history.shift();
        $("historyCount").textContent=history.length;
        drawHistory();

        rows.push([
            new Date().toISOString(),
            weight,axles,spacing,speed,traffic,
            deflection.toFixed(4),strain.toFixed(4),
            vibration.toFixed(4),stiffness,local,
            special?"YES":"NO"
        ]);
    }
}

function animate() {
    requestAnimationFrame(animate);
    const now=performance.now();
    const dt=Math.min((now-previous)/1000,.05);
    previous=now;
    updateSimulation(dt);
    controls.update();
    renderer.render(scene,camera);
}
animate();

window.addEventListener("resize",()=>{
    camera.aspect=innerWidth/innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth,innerHeight);
});
</script>
</body>
</html>
"""

components.html(html, height=1050, scrolling=False)
