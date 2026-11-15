
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
    #MainMenu, footer, header,
    [data-testid="stHeader"],
    [data-testid="stSidebar"],
    [data-testid="stToolbar"] {
        display: none !important;
    }
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        border: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    overflow: hidden;
    font-family: Inter, Arial, sans-serif;
    background: #8ec9ec;
}
#scene {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
}
canvas { display: block; }

.panel {
    position: absolute;
    background: rgba(9, 28, 43, .79);
    color: white;
    border: 1px solid rgba(255,255,255,.22);
    border-radius: 13px;
    padding: 13px;
    backdrop-filter: blur(13px);
    box-shadow: 0 8px 30px rgba(0,0,0,.20);
    font-size: 12px;
}
.panel h3 {
    margin: 0 0 10px;
    font-size: 13px;
    letter-spacing: .5px;
}
#top {
    top: 14px;
    left: 16px;
    right: 16px;
    height: 65px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.brand { font-size: 19px; font-weight: 800; }
.sub { color: #b9d4e4; font-size: 10px; margin-top: 4px; }
.status { color: #75f5a4; font-weight: 700; }
#left {
    top: 95px;
    left: 16px;
    width: 225px;
}
#right {
    top: 95px;
    right: 16px;
    width: 255px;
}
#bottom {
    left: 16px;
    right: 16px;
    bottom: 15px;
    min-height: 110px;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    gap: 15px;
}
.metric {
    background: rgba(255,255,255,.09);
    padding: 9px;
    border-radius: 8px;
    margin: 7px 0;
}
.value {
    font-size: 20px;
    font-weight: 800;
    margin-top: 5px;
}
.muted { color: #b8cfdd; font-size: 10px; }
.green { color: #6af2a0; }
.red { color: #ff7777; }
.blue { color: #7bd6ff; }
input[type=range] { width: 100%; accent-color: #63d6ff; }
button {
    border: 0;
    border-radius: 7px;
    padding: 9px 11px;
    cursor: pointer;
    font-weight: 700;
    background: #2d9bc9;
    color: white;
    margin: 4px 2px;
}
button.secondary { background: #425d70; }
select {
    width: 100%;
    padding: 7px;
    border-radius: 6px;
    margin: 5px 0;
}
.sensor {
    display: flex;
    justify-content: space-between;
    padding: 7px 0;
    border-bottom: 1px solid rgba(255,255,255,.12);
}
#loading {
    position: absolute;
    inset: 0;
    display: grid;
    place-items: center;
    color: white;
    background: #75b5d8;
    z-index: 20;
    font-size: 20px;
    font-weight: 700;
}
#message {
    color: #ffd37b;
    font-size: 10px;
    margin-top: 8px;
}
@media(max-width: 850px) {
    #left { width: 185px; }
    #right { width: 200px; }
    #bottom { grid-template-columns: 1fr 1fr; }
    .brand { font-size: 14px; }
}
</style>
</head>

<body>
<div id="scene"></div>
<div id="loading">Loading 3D bridge environment...</div>

<div class="panel" id="top">
    <div>
        <div class="brand">🌉 INTELLIGENT BRIDGE MONITORING</div>
        <div class="sub">CONTINUOUS STRUCTURAL HEALTH SIMULATION</div>
    </div>
    <div>
        <div class="status">● SYSTEM ONLINE</div>
        <div class="sub" id="mode">NORMAL MONITORING MODE</div>
    </div>
    <div class="muted">LIVE SIMULATION · EDUCATIONAL MODEL</div>
</div>

<div class="panel" id="left">
    <h3>VEHICLE SIMULATION</h3>

    <div class="muted">Vehicle load</div>
    <div class="value" id="weightLabel">25 tons</div>
    <input id="weight" type="range" min="5" max="80" value="25">

    <div class="muted">Vehicle speed</div>
    <div class="value" id="speedLabel">60 km/h</div>
    <input id="speed" type="range" min="10" max="120" value="60">

    <div class="muted">Traffic volume</div>
    <select id="traffic">
        <option value="normal">Normal traffic</option>
        <option value="busy">Busy traffic</option>
        <option value="heavy">Heavy traffic</option>
    </select>

    <button id="start">▶ Start vehicle</button>
    <button class="secondary" id="pause">Ⅱ Pause</button>

    <hr style="border-color:#ffffff33">

    <h3>SIMULATED CHANGE</h3>
    <div class="muted">Structural change signal</div>
    <input id="change" type="range" min="0" max="20" value="0">
    <div class="value" id="changeLabel">0%</div>

    <div class="muted">Change location</div>
    <input id="location" type="range" min="10" max="90" value="50">
    <div id="message">No simulated change selected.</div>

    <button class="secondary" id="reset">Reset simulation</button>
</div>

<div class="panel" id="right">
    <h3>STRUCTURAL SENSOR NETWORK</h3>
    <div class="sensor"><span>Always-on sensors</span><b class="green">55 ACTIVE</b></div>
    <div class="sensor"><span>Additional sensors</span><b id="extra" class="muted">66 STANDBY</b></div>
    <div class="sensor"><span>Deflection</span><b id="deflection">0.00 mm</b></div>
    <div class="sensor"><span>Strain index</span><b id="strain">0.00</b></div>
    <div class="sensor"><span>Vibration index</span><b id="vibration">0.00</b></div>
    <div class="sensor"><span>Temperature</span><b>24.5 °C</b></div>

    <hr style="border-color:#ffffff33">

    <h3>EVENT DETECTION</h3>
    <div id="alert" class="green">● No event detected</div>
    <div class="muted" style="margin-top:8px">
        Additional sensor attention activates when the simulated event threshold is exceeded.
    </div>
</div>

<div class="panel" id="bottom">
    <div>
        <h3>TRAFFIC INFORMATION</h3>
        <div class="value" id="trafficCount">Normal</div>
        <div class="muted">Traffic condition</div>
    </div>
    <div>
        <h3>BRIDGE LOCATION</h3>
        <div class="value">SPAN A — B</div>
        <div class="muted">Simulated sensor network</div>
    </div>
    <div>
        <h3>SENSOR HISTORY</h3>
        <div class="value" id="history">0</div>
        <div class="muted">Recorded simulation updates</div>
    </div>
    <div>
        <h3>CAMERA CONTROLS</h3>
        <div class="muted">Drag to rotate · Scroll to zoom</div>
        <button class="secondary" id="camera">Reset camera</button>
        <button class="secondary" id="csv">Export CSV</button>
    </div>
</div>

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

const MODEL_URL =
"https://raw.githubusercontent.com/experimentscience/bridge-monitoring-stem/main/assets/cable-stayed-bridge.glb";

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x8ec9ec);
scene.fog = new THREE.Fog(0x9acbe0, 250, 850);

const camera = new THREE.PerspectiveCamera(
    45, window.innerWidth/window.innerHeight, 0.1, 2000
);
camera.position.set(110, 85, 150);

const renderer = new THREE.WebGLRenderer({
    antialias: true,
    alpha: false
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
document.getElementById("scene").appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.target.set(0, 15, 0);
controls.maxPolarAngle = Math.PI * 0.48;
controls.minDistance = 35;
controls.maxDistance = 420;

scene.add(new THREE.HemisphereLight(0xd9f1ff, 0x52714a, 2.0));

const sun = new THREE.DirectionalLight(0xfff0d7, 3.3);
sun.position.set(-100, 180, 90);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.left = -250;
sun.shadow.camera.right = 250;
sun.shadow.camera.top = 250;
sun.shadow.camera.bottom = -250;
scene.add(sun);

const sky = new Sky();
sky.scale.setScalar(10000);
sky.material.uniforms.turbidity.value = 7;
sky.material.uniforms.rayleigh.value = 2;
sky.material.uniforms.mieCoefficient.value = 0.004;
sky.material.uniforms.mieDirectionalG.value = 0.8;
scene.add(sky);

const water = new THREE.Mesh(
    new THREE.PlaneGeometry(2000, 2000),
    new THREE.MeshPhysicalMaterial({
        color: 0x268fbd,
        roughness: 0.24,
        metalness: 0.18,
        clearcoat: 0.8
    })
);
water.rotation.x = -Math.PI / 2;
water.position.y = -1.2;
water.receiveShadow = true;
scene.add(water);

const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(2000, 250),
    new THREE.MeshStandardMaterial({
        color: 0x55864a,
        roughness: 1
    })
);
ground.rotation.x = -Math.PI / 2;
ground.position.set(0, -1.0, -300);
ground.receiveShadow = true;
scene.add(ground);

// Distant green hills
for (let i = 0; i < 18; i++) {
    const hill = new THREE.Mesh(
        new THREE.SphereGeometry(1, 32, 24),
        new THREE.MeshStandardMaterial({
            color: i % 2 ? 0x588c54 : 0x719d60,
            roughness: 1
        })
    );
    hill.scale.set(35 + Math.random()*45, 15 + Math.random()*25, 28);
    hill.position.set(-380 + i*45, 4, -260 - Math.random()*90);
    scene.add(hill);
}

const bridgeGroup = new THREE.Group();
scene.add(bridgeGroup);

const alwaysMarkers = new THREE.Group();
const extraMarkers = new THREE.Group();
scene.add(alwaysMarkers, extraMarkers);

function makeMarker(color, radius=0.75) {
    const mesh = new THREE.Mesh(
        new THREE.SphereGeometry(radius, 16, 16),
        new THREE.MeshStandardMaterial({
            color,
            emissive: color,
            emissiveIntensity: 1.1,
            roughness: 0.25
        })
    );
    mesh.castShadow = true;
    return mesh;
}

function addSensorMarkers() {
    alwaysMarkers.clear();
    extraMarkers.clear();

    for (let i=0; i<11; i++) {
        const x = -85 + i*17;
        const green = makeMarker(0x27ff8b, 0.85);
        green.position.set(x, 10, 0);
        alwaysMarkers.add(green);

        const red = makeMarker(0xff3434, 0.65);
        red.position.set(x, 13, 2);
        extraMarkers.add(red);
    }

    for (let x of [-45, 45]) {
        const m = makeMarker(0x27ff8b, 1);
        m.position.set(x, 38, 0);
        alwaysMarkers.add(m);
    }
    extraMarkers.visible = false;
}

addSensorMarkers();

let bridgeLoaded = false;
let bridgeLength = 190;
let vehicle;
let vehicleMoving = false;
let vehiclePosition = -105;
let historyCount = 0;
let csvRows = [["time","vehicle_load_tons","speed_kmh",
    "deflection_mm","change_percent","attention_mode"]];

const loader = new GLTFLoader();

loader.load(
    MODEL_URL,
    (gltf) => {
        const model = gltf.scene;
        const box = new THREE.Box3().setFromObject(model);
        const size = box.getSize(new THREE.Vector3());
        const center = box.getCenter(new THREE.Vector3());

        const longest = Math.max(size.x, size.y, size.z);
        const scale = 200 / longest;
        model.scale.setScalar(scale);

        model.position.sub(center.multiplyScalar(scale));

        // Place the model's lowest point on the scene ground.
        const scaledBox = new THREE.Box3().setFromObject(model);
        model.position.y -= scaledBox.min.y;

        model.traverse((obj) => {
            if (obj.isMesh) {
                obj.castShadow = true;
                obj.receiveShadow = true;
                if (obj.material) {
                    obj.material.needsUpdate = true;
                }
            }
        });

        bridgeGroup.add(model);
        bridgeLoaded = true;

        const finalBox = new THREE.Box3().setFromObject(model);
        const finalSize = finalBox.getSize(new THREE.Vector3());
        bridgeLength = Math.max(finalSize.x, finalSize.z);

        controls.target.set(0, finalSize.y * 0.45, 0);
        camera.position.set(
            bridgeLength * 0.45,
            finalSize.y * 1.8,
            bridgeLength * 0.65
        );
        controls.update();

        document.getElementById("loading").style.display = "none";
    },
    undefined,
    (error) => {
        document.getElementById("loading").innerHTML =
        "Could not load the bridge model. Check that the GLB file is committed at assets/cable-stayed-bridge.glb in the main branch.";
        console.error(error);
    }
);

// Simple simulated vehicle
const vehicleGroup = new THREE.Group();

const body = new THREE.Mesh(
    new THREE.BoxGeometry(9, 3, 4),
    new THREE.MeshStandardMaterial({
        color: 0xe6e9ed,
        metalness: 0.35,
        roughness: 0.35
    })
);
body.position.y = 2;
vehicleGroup.add(body);

const cabin = new THREE.Mesh(
    new THREE.BoxGeometry(4, 2, 3.4),
    new THREE.MeshStandardMaterial({
        color: 0x347fa4,
        metalness: 0.5,
        roughness: 0.2
    })
);
cabin.position.set(-1, 4.2, 0);
vehicleGroup.add(cabin);

vehicle = vehicleGroup;
scene.add(vehicle);

const $ = id => document.getElementById(id);

$("start").onclick = () => vehicleMoving = true;
$("pause").onclick = () => vehicleMoving = false;

$("weight").oninput = e =>
    $("weightLabel").textContent = e.target.value + " tons";

$("speed").oninput = e =>
    $("speedLabel").textContent = e.target.value + " km/h";

$("change").oninput = e =>
    $("changeLabel").textContent = e.target.value + "%";

$("traffic").onchange = e =>
    $("trafficCount").textContent =
        e.target.value.charAt(0).toUpperCase() + e.target.value.slice(1);

$("reset").onclick = () => {
    vehicleMoving = false;
    vehiclePosition = -105;
    $("change").value = 0;
    $("changeLabel").textContent = "0%";
    $("alert").textContent = "● No event detected";
    $("alert").className = "green";
    $("extra").textContent = "66 STANDBY";
    $("extra").className = "muted";
    extraMarkers.visible = false;
};

$("camera").onclick = () => {
    camera.position.set(110, 85, 150);
    controls.target.set(0, 15, 0);
    controls.update();
};

$("csv").onclick = () => {
    const csv = csvRows.map(row => row.join(",")).join("\n");
    const blob = new Blob([csv], {type:"text/csv"});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "bridge-monitoring-history.csv";
    a.click();
    URL.revokeObjectURL(url);
};

let lastRecord = 0;

function updateSimulation(dt) {
    const weight = Number($("weight").value);
    const speed = Number($("speed").value);
    const change = Number($("change").value);
    const location = Number($("location").value);
    const traffic = $("traffic").value;

    if (vehicleMoving) {
        vehiclePosition += dt * (speed / 18);
        if (vehiclePosition > 105) vehiclePosition = -105;
    }

    vehicle.position.set(vehiclePosition, 0, 0);

    const distance = Math.abs(vehiclePosition);
    const loadFactor = Math.max(0, 1 - distance/105);
    const deflection = (weight/25) * loadFactor * 1.8;
    const vibration = loadFactor * (speed/60) * 1.4;
    const strain = deflection * 0.75;

    $("deflection").textContent = deflection.toFixed(2) + " mm";
    $("vibration").textContent = vibration.toFixed(2);
    $("strain").textContent = strain.toFixed(2);

    const triggered = deflection > 1.2 || change >= 5;

    if (triggered) {
        $("mode").textContent = "SPECIAL ATTENTION MODE";
        $("extra").textContent = "66 ACTIVE";
        $("extra").className = "red";
        $("alert").textContent =
            change >= 5
            ? "● Persistent change signal detected"
            : "● Temporary load event detected";
        $("alert").className = "red";
        extraMarkers.visible = true;
    } else {
        $("mode").textContent = "NORMAL MONITORING MODE";
        $("extra").textContent = "66 STANDBY";
        $("extra").className = "muted";
        $("alert").textContent = "● No event detected";
        $("alert").className = "green";
        extraMarkers.visible = false;
    }

    $("message").textContent = change > 0
        ? "Simulated structural change at " + location + "% of span."
        : "No simulated change selected.";

    const markerIndex = Math.round(location/10);
    extraMarkers.children.forEach((marker, i) => {
        marker.material.color.set(i === markerIndex ? 0xffcc33 : 0xff3434);
        marker.material.emissive.set(i === markerIndex ? 0xffcc33 : 0xff3434);
    });

    const now = performance.now();
    if (now - lastRecord > 1000) {
        lastRecord = now;
        historyCount++;
        $("history").textContent = historyCount;
        csvRows.push([
            new Date().toISOString(),
            weight, speed, deflection.toFixed(3),
            change, triggered ? "Special attention" : "Normal"
        ]);
    }
}

let previous = performance.now();

function animate() {
    requestAnimationFrame(animate);
    const now = performance.now();
    const dt = Math.min((now-previous)/1000, 0.05);
    previous = now;

    updateSimulation(dt);
    controls.update();
    renderer.render(scene, camera);
}
animate();

window.addEventListener("resize", () => {
    camera.aspect = window.innerWidth/window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
</script>
</body>
</html>
"""

components.html(html, height=1050, scrolling=False)
