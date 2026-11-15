
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
[data-testid="stMain"], .block-container {
    margin: 0 !important;
    padding: 0 !important;
    max-width: 100% !important;
    overflow: hidden !important;
}
header, footer, #MainMenu {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing:border-box; }
html,body {
    margin:0;
    width:100%;
    height:100%;
    overflow:hidden;
    font-family:Arial,sans-serif;
    background:#86c9ed;
}
#scene {
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
}
.panel {
    position:absolute;
    z-index:5;
    color:white;
    background:rgba(8,42,70,.76);
    border:1px solid rgba(255,255,255,.32);
    border-radius:13px;
    padding:13px;
    backdrop-filter:blur(12px);
    box-shadow:0 6px 25px rgba(0,25,55,.22);
}
#top {
    top:12px; left:1%; right:1%;
    min-height:65px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:12px;
}
#left {
    left:1%; top:92px;
    width:245px;
    max-height:70vh;
    overflow:auto;
}
#right {
    right:1%; top:92px;
    width:250px;
    max-height:70vh;
    overflow:auto;
}
#bottom {
    left:1%; right:1%; bottom:10px;
    min-height:83px;
    display:flex;
    justify-content:space-around;
    align-items:center;
    gap:12px;
    flex-wrap:wrap;
}
h2 {margin:0;font-size:19px;letter-spacing:1px;}
h3 {margin:5px 0 12px;font-size:15px;}
small {opacity:.8;}
.metric {
    background:rgba(255,255,255,.12);
    border-radius:8px;
    padding:9px;
    margin:7px 0;
    font-size:12px;
}
.metric b {float:right;font-size:14px;}
label {
    display:block;
    font-size:12px;
    margin-top:12px;
}
input[type=range] {
    width:100%;
    accent-color:#25d8ff;
}
button {
    border:1px solid #8beaff;
    border-radius:7px;
    background:#087fb5;
    color:white;
    padding:8px 12px;
    cursor:pointer;
}
.green {color:#4dff85;}
.red {color:#ff6262;}
#hint {
    position:absolute;
    bottom:110px;
    left:50%;
    transform:translateX(-50%);
    z-index:4;
    color:white;
    background:rgba(0,30,55,.55);
    padding:7px 13px;
    border-radius:20px;
    font-size:11px;
}
@media(max-width:700px) {
    #left {width:190px;top:90px;}
    #right {width:185px;top:90px;}
    #bottom {font-size:10px;}
    h2 {font-size:14px;}
}
</style>
</head>
<body>

<div id="scene"></div>

<div class="panel" id="top">
    <div>
        <h2>🌉 INTELLIGENT BRIDGE MONITOR</h2>
        <small>STRUCTURAL HEALTH MONITORING SYSTEM</small>
    </div>
    <div><span class="green">● SYSTEM ONLINE</span><br>
    <small>Continuous monitoring</small></div>
    <div><b>LIVE MONITORING</b><br>
    <small>3D structural simulation</small></div>
</div>

<div class="panel" id="left">
    <h3>🚙 VEHICLE CONTROLS</h3>
    <label>Vehicle position: <span id="positionText">50%</span></label>
    <input id="position" type="range" min="0" max="100" value="50">

    <label>Vehicle load: <span id="loadText">20,000 N</span></label>
    <input id="load" type="range" min="5000" max="50000" step="1000" value="20000">

    <label>Traffic volume</label>
    <select id="traffic" style="width:100%;padding:7px">
      <option>Low</option>
      <option selected>Medium</option>
      <option>High</option>
      <option>Very High</option>
    </select>

    <label>Structural stiffness reduction: <span id="stiffText">0%</span></label>
    <input id="stiff" type="range" min="0" max="30" value="0">

    <label>Simulated local change: <span id="changeText">0%</span></label>
    <input id="change" type="range" min="0" max="40" value="0">

    <label>Attention threshold: <span id="thresholdText">5 mm</span></label>
    <input id="threshold" type="range" min="1" max="20" value="5">

    <hr style="opacity:.25">
    <button id="play">▶ Move vehicle</button>
    <button id="reset">Reset</button>
</div>

<div class="panel" id="right">
    <h3>📡 SENSOR READINGS</h3>
    <div class="metric">🟢 Normal sensors <b>55</b></div>
    <div class="metric">🔴 Additional sensors <b id="extraCount">0 / 66</b></div>
    <div class="metric">Maximum deflection <b id="deflection">0.00 mm</b></div>
    <div class="metric">Average strain <b id="strain">0 με</b></div>
    <div class="metric">Vibration index <b id="vibration">0.00</b></div>
    <hr style="opacity:.25">
    <h3>🚨 CHANGE DETECTION</h3>
    <div id="status" class="green">● Normal monitoring</div>
    <p id="message" style="font-size:12px;line-height:1.5">
    No simulated persistent change configured.
    </p>
    <hr style="opacity:.25">
    <h3>📍 SENSOR LEGEND</h3>
    <div class="metric"><span class="green">●</span> Always-on sensors</div>
    <div class="metric"><span class="red">●</span> Special-attention sensors</div>
</div>

<div id="hint">Drag to rotate · Scroll to zoom · Right-click to pan</div>

<div class="panel" id="bottom">
    <div>🚗 <b>TRAFFIC</b><br><span id="trafficValue">Medium</span></div>
    <div>📍 <b>VEHICLE LOCATION</b><br><span id="locationValue">20 m</span></div>
    <div>📊 <b>SENSOR NETWORK</b><br>55 primary · 66 additional</div>
    <div>📈 <b>MONITORING HISTORY</b><br><span id="historyValue">0 snapshots</span></div>
    <div><button id="export">Export data CSV</button></div>
</div>

<script type="module">
import * as THREE from
'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';
import { OrbitControls } from
'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/controls/OrbitControls.js';

const container = document.getElementById('scene');

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x91d4f5);
scene.fog = new THREE.Fog(0x91d4f5, 65, 150);

const camera = new THREE.PerspectiveCamera(
    43, innerWidth/innerHeight, .1, 300
);
camera.position.set(31, 23, 39);

const renderer = new THREE.WebGLRenderer({
    antialias:true,
    powerPreference:"high-performance"
});
renderer.setSize(innerWidth,innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
container.appendChild(renderer.domElement);

const controls = new OrbitControls(camera,renderer.domElement);
controls.target.set(0,5,0);
controls.enableDamping = true;
controls.dampingFactor = .06;
controls.minDistance = 15;
controls.maxDistance = 95;
controls.maxPolarAngle = Math.PI*.48;

// LIGHTING
scene.add(new THREE.HemisphereLight(0xdaf4ff,0x547348,2.0));

const sun = new THREE.DirectionalLight(0xfff4dc,3.0);
sun.position.set(-25,45,25);
sun.castShadow = true;
sun.shadow.mapSize.set(2048,2048);
scene.add(sun);

// MATERIALS
const concrete = new THREE.MeshStandardMaterial({
    color:0xc9d1d5, roughness:.72
});
const roadMaterial = new THREE.MeshStandardMaterial({
    color:0x343c43, roughness:.92
});
const cableMaterial = new THREE.MeshStandardMaterial({
    color:0xeaf3f6, metalness:.35, roughness:.3
});
const greenMaterial = new THREE.MeshStandardMaterial({
    color:0x438c43, roughness:1
});

// WATER
const water = new THREE.Mesh(
    new THREE.PlaneGeometry(250,180,1,1),
    new THREE.MeshStandardMaterial({
        color:0x168fc3,
        roughness:.25,
        metalness:.18
    })
);
water.rotation.x=-Math.PI/2;
water.position.y=-.6;
water.receiveShadow=true;
scene.add(water);

// DISTANT HILLS
function hill(x,z,sx,sy,sz,color) {
    const mesh=new THREE.Mesh(
        new THREE.SphereGeometry(1,32,24),
        new THREE.MeshStandardMaterial({
            color,roughness:1
        })
    );
    mesh.position.set(x,sy*.35,z);
    mesh.scale.set(sx,sy,sz);
    mesh.castShadow=true;
    scene.add(mesh);
}
for(let i=0;i<22;i++){
    hill(
        -65+i*6,
        30+Math.sin(i*.8)*7,
        10+Math.random()*6,
        7+Math.random()*8,
        12+Math.random()*6,
        [0x488d43,0x5c9b4c,0x367d40][i%3]
    );
    hill(
        -65+i*6,
        -48+Math.sin(i*.8)*5,
        10+Math.random()*6,
        7+Math.random()*8,
        12+Math.random()*6,
        [0x488d43,0x5c9b4c,0x367d40][i%3]
    );
}

// BRIDGE DECK
const deck = new THREE.Mesh(
    new THREE.BoxGeometry(62,1.0,9),
    concrete
);
deck.position.set(0,8,0);
deck.castShadow=true;
deck.receiveShadow=true;
scene.add(deck);

// ROAD SURFACE
const road = new THREE.Mesh(
    new THREE.BoxGeometry(61.5,.12,7.4),
    roadMaterial
);
road.position.set(0,8.57,0);
road.receiveShadow=true;
scene.add(road);

// LANE MARKINGS
for(let z of [-2.4,0,2.4]){
    const line=new THREE.Mesh(
        new THREE.BoxGeometry(60,.025,.07),
        new THREE.MeshBasicMaterial({color:0xf4e9b9})
    );
    line.position.set(0,8.65,z);
    scene.add(line);
}

// BRIDGE EDGE RAILS
for(let z of [-4.3,4.3]){
    const rail=new THREE.Mesh(
        new THREE.BoxGeometry(62,.18,.18),
        cableMaterial
    );
    rail.position.set(0,9.05,z);
    scene.add(rail);
}

// PIERS
function cylinderBetween(a,b,r,material){
    const direction=new THREE.Vector3().subVectors(b,a);
    const mesh=new THREE.Mesh(
        new THREE.CylinderGeometry(r,r,direction.length(),12),
        material
    );
    mesh.position.copy(a).add(b).multiplyScalar(.5);
    mesh.quaternion.setFromUnitVectors(
        new THREE.Vector3(0,1,0),
        direction.normalize()
    );
    mesh.castShadow=true;
    scene.add(mesh);
    return mesh;
}

for(let x of [-22,-11,0,11,22]){
    cylinderBetween(
        new THREE.Vector3(x,0,0),
        new THREE.Vector3(x,7.7,0),
        .7,concrete
    );
}

// TWO CABLE-STAYED TOWERS
const towerPositions=[-12,12];

for(const tx of towerPositions){
    for(const z of [-.65,.65]){
        const tower=new THREE.Mesh(
            new THREE.BoxGeometry(.8,24,.8),
            concrete
        );
        tower.position.set(tx,19.5,z);
        tower.castShadow=true;
        scene.add(tower);
    }

    const cross=new THREE.Mesh(
        new THREE.BoxGeometry(1.1,.8,2),
        concrete
    );
    cross.position.set(tx,29.5,0);
    scene.add(cross);

    // Cable stays
    for(let side of [-1,1]){
        for(let i=1;i<=13;i++){
            const anchor=tx+side*i*2.0;
            if(Math.abs(anchor)>30) continue;

            const start=new THREE.Vector3(tx,29.2,0);
            const end=new THREE.Vector3(anchor,8.8,0);

            const cable=new THREE.Mesh(
                new THREE.CylinderGeometry(.025,.025,
                start.distanceTo(end),6),
                cableMaterial
            );
            cable.position.copy(start).add(end).multiplyScalar(.5);
            cable.quaternion.setFromUnitVectors(
                new THREE.Vector3(0,1,0),
                new THREE.Vector3().subVectors(end,start).normalize()
            );
            scene.add(cable);
        }
    }
}

// SIDE CROSS BRACING
for(let x of [-20,-8,8,20]){
    for(let z of [-4.3,4.3]){
        cylinderBetween(
            new THREE.Vector3(x,8.9,z),
            new THREE.Vector3(x+2,8.9,z),
            .035,cableMaterial
        );
    }
}

// SENSOR MATERIALS
const greenSensorMaterial=new THREE.MeshStandardMaterial({
    color:0x00ff54,
    emissive:0x00a52f,
    emissiveIntensity:1.4
});
const redSensorMaterial=new THREE.MeshStandardMaterial({
    color:0xff2727,
    emissive:0xaa0000,
    emissiveIntensity:1.5
});

const normalSensors=[];
const specialSensors=[];

function makeSensor(x,z,material,radius=.17){
    const dot=new THREE.Mesh(
        new THREE.SphereGeometry(radius,12,12),
        material
    );
    dot.position.set(x,9.15,z);
    scene.add(dot);
    return dot;
}

// 55 PRIMARY SENSORS
for(let i=0;i<11;i++){
    for(let j=0;j<5;j++){
        const x=-27+i*5.4;
        const z=-3.3+j*1.65;
        normalSensors.push(makeSensor(
            x,z,greenSensorMaterial,.17
        ));
    }
}

// 66 ADDITIONAL SENSORS
for(let i=0;i<11;i++){
    for(let j=0;j<6;j++){
        const x=-27+i*5.4;
        const z=-3.6+j*1.44;
        specialSensors.push(makeSensor(
            x,z,redSensorMaterial,.19
        ));
    }
}
specialSensors.forEach(s=>s.visible=false);

// VEHICLE
const vehicle=new THREE.Group();

const body=new THREE.Mesh(
    new THREE.BoxGeometry(2.5,1.0,1.35),
    new THREE.MeshStandardMaterial({
        color:0xeeeeee,roughness:.4
    })
);
body.position.y=.85;
body.castShadow=true;
vehicle.add(body);

const cabin=new THREE.Mesh(
    new THREE.BoxGeometry(1.1,.8,1.2),
    new THREE.MeshStandardMaterial({
        color:0x278ac0,metalness:.25,roughness:.2
    })
);
cabin.position.set(-.35,1.65,0);
vehicle.add(cabin);

for(let x of [-.8,.8]){
    for(let z of [-.68,.68]){
        const wheel=new THREE.Mesh(
            new THREE.CylinderGeometry(.32,.32,.18,20),
            new THREE.MeshStandardMaterial({color:0x17191b})
        );
        wheel.rotation.x=Math.PI/2;
        wheel.position.set(x,.4,z);
        vehicle.add(wheel);
    }
}
vehicle.position.set(0,8.65,0);
scene.add(vehicle);

// SIMULATION
const $=id=>document.getElementById(id);
let moving=false;
let history=[];
let lastPosition=50;

function updateSimulation(){
    const pos=Number($("position").value);
    const load=Number($("load").value);
    const stiffness=Number($("stiff").value);
    const change=Number($("change").value);
    const threshold=Number($("threshold").value);

    $("positionText").textContent=pos+"%";
    $("loadText").textContent=load.toLocaleString()+" N";
    $("stiffText").textContent=stiffness+"%";
    $("changeText").textContent=change+"%";
    $("thresholdText").textContent=threshold+" mm";

    vehicle.position.x=-29+(pos/100)*58;

    const loadFactor=load/20000;
    const deflection=(
        .7*loadFactor*(1+stiffness/100)+change*.035
    );
    const strain=deflection*42.5+12;
    const vibration=.12+deflection*.035;

    $("deflection").textContent=deflection.toFixed(2)+" mm";
    $("strain").textContent=strain.toFixed(1)+" με";
    $("vibration").textContent=vibration.toFixed(3);

    const attention=deflection>=threshold ||
        change>=5 || stiffness>=5;

    specialSensors.forEach(s=>s.visible=attention);
    $("extraCount").textContent=attention?"66 / 66":"0 / 66";

    if(attention){
        $("status").textContent="● SPECIAL ATTENTION ACTIVE";
        $("status").className="red";
        $("message").textContent=
            "The simulated response crossed an attention condition. " +
            "Additional sensor channels are now displayed.";
    } else {
        $("status").textContent="● NORMAL MONITORING";
        $("status").className="green";
        $("message").textContent=
            "No simulated attention condition is currently active.";
    }

    $("locationValue").textContent=
        (pos/100*40).toFixed(1)+" m";
    $("trafficValue").textContent=$("traffic").value;

    if(pos!==lastPosition || history.length===0){
        history.push({
            time:new Date().toLocaleTimeString(),
            position:pos,
            load:load,
            deflection:deflection,
            strain:strain,
            vibration:vibration,
            special:attention
        });
        lastPosition=pos;
    }
    $("historyValue").textContent=history.length+" snapshots";
}

["position","load","stiff","change","threshold","traffic"].forEach(id=>{
    $(id).addEventListener("input",updateSimulation);
    $(id).addEventListener("change",updateSimulation);
});

$("play").onclick=()=>{
    moving=!moving;
    $("play").textContent=moving?"⏸ Pause vehicle":"▶ Move vehicle";
};

$("reset").onclick=()=>{
    moving=false;
    $("position").value=50;
    $("load").value=20000;
    $("stiff").value=0;
    $("change").value=0;
    updateSimulation();
};

$("export").onclick=()=>{
    const rows=[
        ["Time","Position %","Load N","Deflection mm",
         "Strain microstrain","Vibration","Special attention"]
    ];
    history.forEach(h=>rows.push([
        h.time,h.position,h.load,h.deflection,
        h.strain,h.vibration,h.special
    ]));
    const csv=rows.map(r=>r.join(",")).join("\\n");
    const a=document.createElement("a");
    a.href=URL.createObjectURL(
        new Blob([csv],{type:"text/csv"})
    );
    a.download="bridge_monitoring_history.csv";
    a.click();
    URL.revokeObjectURL(a.href);
};

updateSimulation();

// ANIMATION LOOP
function animate(){
    requestAnimationFrame(animate);

    if(moving){
        let p=Number($("position").value)+.15;
        if(p>100) p=0;
        $("position").value=p;
        updateSimulation();
    }

    // Gentle water motion
    water.material.roughness=.23+
        .025*Math.sin(Date.now()*.0007);

    controls.update();
    renderer.render(scene,camera);
}
animate();

// RESIZE
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
