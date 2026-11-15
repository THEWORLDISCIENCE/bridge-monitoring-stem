
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import io

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Intelligent Bridge Monitoring",
    page_icon="🌉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# FUTURISTIC DASHBOARD STYLING
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 15% 0%, #142b48 0%, transparent 42%),
        linear-gradient(145deg, #07111f 0%, #0b1728 55%, #101d30 100%);
    color: #eaf4ff;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 2rem;
    max-width: 1600px;
}

h1, h2, h3 {
    color: #f2f8ff !important;
    font-weight: 700 !important;
}

p, label, span {
    color: #c5d5e8;
}

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #142a43, #0d1d30);
    border: 1px solid #254766;
    padding: 17px;
    border-radius: 14px;
    box-shadow: 0 5px 22px #00000030;
}

div[data-testid="stMetricLabel"] {
    color: #9db7d2 !important;
}

div[data-testid="stMetricValue"] {
    color: #eaf6ff !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 9px;
    background: #0d1c2e;
    padding: 8px;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    background: #14283e;
    border-radius: 9px;
    color: #c6d8ec;
    padding: 10px 18px;
}

.stTabs [aria-selected="true"] {
    background: #155c78 !important;
    color: white !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #29435d;
}

.stButton button, .stDownloadButton button {
    background: linear-gradient(90deg, #087e9e, #1767a5);
    color: white;
    border: 0;
    border-radius: 9px;
    font-weight: 600;
}

hr {
    border-color: #29435d;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div style="
    display:flex;
    align-items:center;
    justify-content:space-between;
    flex-wrap:wrap;
    gap:15px;
    padding:12px 4px 20px 4px;
">
    <div>
        <div style="
            color:#48d8f0;
            font-size:12px;
            letter-spacing:3px;
            font-weight:700;
        ">SMART INFRASTRUCTURE • LIVE SIMULATION</div>

        <div style="
            color:#f0f7ff;
            font-size:32px;
            font-weight:800;
            margin-top:5px;
        ">INTELLIGENT BRIDGE MONITORING</div>

        <div style="color:#91abc5; font-size:13px; margin-top:5px;">
            Structural intelligence • Adaptive sensing • Predictive monitoring
        </div>
    </div>

    <div style="
        background:#103c43;
        border:1px solid #1a9c8b;
        color:#5fffd0;
        padding:10px 16px;
        border-radius:10px;
        font-size:12px;
        font-weight:700;
    ">● SIMULATION ONLINE</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR CONTROLS
# ============================================================

st.sidebar.markdown("## ⚙️ SIMULATION CONTROL")
st.sidebar.caption("Adjust the bridge and traffic conditions.")

st.sidebar.markdown("### 🚗 Traffic")

vehicle_weight = st.sidebar.slider(
    "Vehicle weight (N)",
    5000, 50000, 20000, 1000
)

axles = st.sidebar.slider(
    "Number of axles",
    2, 6, 3
)

axle_spacing = st.sidebar.slider(
    "Axle spacing (m)",
    1.0, 5.0, 2.0, 0.5
)

vehicle_position = st.sidebar.slider(
    "Vehicle position (m)",
    0.0, 30.0, 15.0, 0.5
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏗️ Structural conditions")

stiffness_reduction = st.sidebar.slider(
    "Global stiffness reduction (%)",
    0, 30, 0
)

local_change = st.sidebar.slider(
    "Local change signal (%)",
    0, 40, 0
)

change_location = st.sidebar.slider(
    "Simulated change location (m)",
    2.0, 28.0, 15.0, 0.5
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🚨 Attention settings")

attention_threshold = st.sidebar.slider(
    "Deflection attention threshold (mm)",
    0.1, 5.0, 1.0, 0.1
)

st.sidebar.caption(
    "The simulation activates special attention when "
    "the response exceeds the selected threshold or "
    "a persistent baseline difference is detected."
)

# ============================================================
# BRIDGE MODEL
# ============================================================

L = 30.0
E = 200e9
I = 0.08

x = np.linspace(0, L, 401)
stations = np.linspace(2, 28, 11)

total_load = vehicle_weight
load_per_axle = total_load / axles

axle_positions = [
    vehicle_position - i * axle_spacing
    for i in range(axles)
]

def point_load_deflection(P, a, x_values):
    """Educational simply-supported beam point-load model."""

    a = float(np.clip(a, 0.0, L))
    b = L - a

    result = np.zeros_like(x_values, dtype=float)

    if a <= 0.001 or b <= 0.001:
        return result

    left = x_values <= a
    right = ~left

    result[left] = (
        P * b * x_values[left] /
        (6 * L * E * I)
    ) * (
        L**2 - b**2 - x_values[left]**2
    )

    result[right] = (
        P * a * (L - x_values[right]) /
        (6 * L * E * I)
    ) * (
        L**2 - a**2 - (L - x_values[right])**2
    )

    return result


def bridge_response(positions):
    """Combine the responses from all vehicle axles."""

    deflection = np.zeros_like(x)
    moment = np.zeros_like(x)

    for position in positions:
        if 0 <= position <= L:
            a = position
            b = L - a

            deflection += point_load_deflection(
                load_per_axle, a, x
            )

            moment += np.where(
                x <= a,
                load_per_axle * b * x / L,
                load_per_axle * a * (L - x) / L
            )

    return deflection, moment


baseline_deflection, baseline_moment = bridge_response(
    axle_positions
)

# ============================================================
# STRUCTURAL CHANGE MODEL
# ============================================================

global_factor = max(
    0.25, 1 - stiffness_reduction / 100
)

distance_from_change = np.abs(x - change_location)

local_influence = np.exp(
    -(distance_from_change / 3.0) ** 2
)

local_factor = (
    1 - (local_change / 100) * local_influence
)

local_factor = np.clip(local_factor, 0.3, 1.0)

current_deflection = (
    baseline_deflection /
    (global_factor * local_factor)
)

current_moment = (
    baseline_moment /
    global_factor
)

baseline_peak = float(np.max(np.abs(baseline_deflection)))
current_peak = float(np.max(np.abs(current_deflection)))

baseline_peak_mm = baseline_peak * 1000
current_peak_mm = current_peak * 1000

if baseline_peak_mm > 0.000001:
    response_increase = (
        (current_peak_mm - baseline_peak_mm)
        / baseline_peak_mm
    ) * 100
else:
    response_increase = 0.0

# ============================================================
# SENSOR CHANNELS
# ============================================================

always_on_types = [
    "Deflection",
    "Strain",
    "Vibration",
    "Temperature",
    "Traffic Load"
]

special_types = [
    "Tilt",
    "Humidity",
    "Corrosion",
    "Crack Width",
    "Acoustic Activity",
    "Joint Displacement"
]

def interpolate_at_stations(values):
    return np.interp(stations, x, values)


station_baseline = interpolate_at_stations(
    baseline_deflection
)

station_current = interpolate_at_stations(
    current_deflection
)

station_moment = interpolate_at_stations(
    current_moment
)

sensor_records = []

for i, station in enumerate(stations):

    deflection_mm = abs(station_current[i]) * 1000

    strain_proxy = (
        abs(station_moment[i]) * 0.000001
    )

    vibration_proxy = (
        abs(station_current[i]) * 0.2
    )

    temperature = (
        24 + 1.5 * np.sin(station / 4)
    )

    traffic_index = (
        vehicle_weight / 50000 * 100
    )

    values = [
        deflection_mm,
        strain_proxy,
        vibration_proxy,
        temperature,
        traffic_index
    ]

    for sensor_type, value in zip(
        always_on_types, values
    ):
        sensor_records.append({
            "Station": round(float(station), 2),
            "Sensor": sensor_type,
            "Reading": round(float(value), 4),
            "Mode": "Always-on"
        })

always_on_df = pd.DataFrame(sensor_records)

# ============================================================
# EVENT-TRIGGERED SPECIAL ATTENTION
# ============================================================

threshold_trigger = (
    current_peak_mm >= attention_threshold
)

persistent_trigger = (
    response_increase >= 5.0
    and (
        stiffness_reduction > 0
        or local_change > 0
    )
)

special_mode = bool(
    threshold_trigger or persistent_trigger
)

special_records = []

if special_mode:

    for station in stations:

        proximity = np.exp(
            -((station - change_location) / 4) ** 2
        )

        special_values = [
            0.2 + 2.0 * proximity,
            55 + 10 * proximity,
            0.1 + (local_change / 10) * proximity,
            0.02 + (local_change / 100) * proximity,
            0.3 + (local_change / 15) * proximity,
            0.1 + (local_change / 20) * proximity
        ]

        for sensor_type, value in zip(
            special_types, special_values
        ):
            special_records.append({
                "Station": round(float(station), 2),
                "Sensor": sensor_type,
                "Reading": round(float(value), 4),
                "Mode": "Special attention"
            })

special_df = pd.DataFrame(special_records)

# ============================================================
# SENSOR COUNTS
# ============================================================

always_count = len(always_on_df)
special_count = len(special_df)
total_sensor_count = always_count + special_count

# ============================================================
# 3D BRIDGE GENERATOR
# ============================================================

def create_bridge():

    fig = go.Figure()

    # --------------------------------------------------------
    # BRIDGE DECK
    # --------------------------------------------------------

    deck_x = [0, L, L, 0]
    deck_y = [-3, -3, 3, 3]
    deck_z = [0, 0, 0, 0]

    fig.add_trace(go.Mesh3d(
        x=deck_x,
        y=deck_y,
        z=deck_z,
        i=[0, 0],
        j=[1, 2],
        k=[2, 3],
        color="#163d59",
        opacity=0.95,
        flatshading=False,
        name="Bridge deck",
        hoverinfo="skip",
        lighting=dict(
            ambient=0.45,
            diffuse=0.9,
            specular=0.8,
            roughness=0.35,
            fresnel=0.3
        )
    ))

    # --------------------------------------------------------
    # ROAD SURFACE
    # --------------------------------------------------------

    road_x = [0, L, L, 0]
    road_y = [-2.3, -2.3, 2.3, 2.3]
    road_z = [0.08] * 4

    fig.add_trace(go.Mesh3d(
        x=road_x,
        y=road_y,
        z=road_z,
        i=[0, 0],
        j=[1, 2],
        k=[2, 3],
        color="#101c2c",
        opacity=1,
        name="Road surface",
        hoverinfo="skip"
    ))

    # --------------------------------------------------------
    # LANE MARKINGS
    # --------------------------------------------------------

    for lane_y in [-0.8, 0.8]:

        for start in np.arange(0.5, L, 3):

            end = min(start + 1.5, L)

            fig.add_trace(go.Scatter3d(
                x=[start, end],
                y=[lane_y, lane_y],
                z=[0.12, 0.12],
                mode="lines",
                line=dict(
                    color="#55a9c8",
                    width=3
                ),
                showlegend=False,
                hoverinfo="skip"
            ))

    # --------------------------------------------------------
    # DECK EDGE LIGHTS
    # --------------------------------------------------------

    for side in [-2.8, 2.8]:

        fig.add_trace(go.Scatter3d(
            x=[0, L],
            y=[side, side],
            z=[0.16, 0.16],
            mode="lines",
            line=dict(
                color="#23c8ee",
                width=6
            ),
            showlegend=False,
            hoverinfo="skip"
        ))

    # --------------------------------------------------------
    # SUPPORT BEAMS
    # --------------------------------------------------------

    for position in np.arange(0, L + 0.1, 2):

        fig.add_trace(go.Scatter3d(
            x=[position, position],
            y=[-3, 3],
            z=[-0.18, -0.18],
            mode="lines",
            line=dict(
                color="#416782",
                width=3
            ),
            showlegend=False,
            hoverinfo="skip"
        ))

    # --------------------------------------------------------
    # MAIN TOWERS
    # --------------------------------------------------------

    tower_positions = [10, 20]

    for tower_x in tower_positions:

        # Two tower legs
        for side in [-0.85, 0.85]:

            fig.add_trace(go.Scatter3d(
                x=[tower_x, tower_x],
                y=[side, side],
                z=[0, 10],
                mode="lines",
                line=dict(
                    color="#78c9ed",
                    width=13
                ),
                showlegend=False,
                hoverinfo="skip"
            ))

        # Tower crossbar
        fig.add_trace(go.Scatter3d(
            x=[tower_x, tower_x],
            y=[-0.85, 0.85],
            z=[10, 10],
            mode="lines",
            line=dict(
                color="#8ceaff",
                width=9
            ),
            showlegend=False,
            hoverinfo="skip"
        ))

        # Tower illuminated center
        fig.add_trace(go.Scatter3d(
            x=[tower_x, tower_x],
            y=[0, 0],
            z=[0, 10],
            mode="lines",
            line=dict(
                color="#20bfe8",
                width=3
            ),
            showlegend=False,
            hoverinfo="skip"
        ))

    # --------------------------------------------------------
    # CABLES
    # --------------------------------------------------------

    for tower_x in tower_positions:

        for side in [-1, 1]:

            for anchor_x in np.linspace(
                max(0, tower_x - 9),
                min(L, tower_x + 9),
                13
            ):

                if abs(anchor_x - tower_x) < 0.01:
                    continue

                cable_height = (
                    9.8 -
                    abs(anchor_x - tower_x) * 0.65
                )

                fig.add_trace(go.Scatter3d(
                    x=[tower_x, anchor_x],
                    y=[side * 0.85, side * 2.8],
                    z=[10, 0.12],
                    mode="lines",
                    line=dict(
                        color="#63b8df",
                        width=2
                    ),
                    showlegend=False,
                    hoverinfo="skip"
                ))

    # --------------------------------------------------------
    # PYLON BASES
    # --------------------------------------------------------

    for tower_x in tower_positions:

        fig.add_trace(go.Scatter3d(
            x=[tower_x, tower_x],
            y=[-1.2, 1.2],
            z=[0.18, 0.18],
            mode="lines",
            line=dict(
                color="#b0eaff",
                width=15
            ),
            showlegend=False,
            hoverinfo="skip"
        ))

    # --------------------------------------------------------
    # ALWAYS-ON SENSOR DOTS
    # --------------------------------------------------------

    sensor_x = []
    sensor_y = []
    sensor_z = []
    sensor_hover = []

    for row, sensor_type in enumerate(always_on_types):

        for index, station in enumerate(stations):

            sensor_x.append(station)

            sensor_y.append(
                -2.0 + row * 0.95
            )

            sensor_z.append(
                0.27 + row * 0.035
            )

            reading = always_on_df[
                (always_on_df["Station"] == round(float(station), 2))
                & (always_on_df["Sensor"] == sensor_type)
            ]["Reading"].iloc[0]

            sensor_hover.append(
                f"<b>{sensor_type}</b><br>"
                f"Station: {station:.1f} m<br>"
                f"Reading: {reading:.4f}"
            )

    fig.add_trace(go.Scatter3d(
        x=sensor_x,
        y=sensor_y,
        z=sensor_z,
        mode="markers",
        marker=dict(
            size=5,
            color="#39f5a2",
            opacity=0.95,
            line=dict(
                color="#b4ffe0",
                width=1
            )
        ),
        text=sensor_hover,
        hovertemplate="%{text}<extra></extra>",
        name="55 Always-on sensors"
    ))

    # --------------------------------------------------------
    # SPECIAL ATTENTION SENSOR DOTS
    # --------------------------------------------------------

    if special_mode:

        special_x = []
        special_y = []
        special_z = []
        special_hover = []

        for row, sensor_type in enumerate(special_types):

            for station in stations:

                special_x.append(station)

                special_y.append(
                    -2.0 + row * 0.75
                )

                special_z.append(
                    0.65 + row * 0.04
                )

                reading = special_df[
                    (special_df["Station"] == round(float(station), 2))
                    & (special_df["Sensor"] == sensor_type)
                ]["Reading"].iloc[0]

                special_hover.append(
                    f"<b>{sensor_type}</b><br>"
                    f"Station: {station:.1f} m<br>"
                    f"Reading: {reading:.4f}"
                )

        fig.add_trace(go.Scatter3d(
            x=special_x,
            y=special_y,
            z=special_z,
            mode="markers",
            marker=dict(
                size=5,
                color="#ff4e70",
                symbol="diamond",
                opacity=1,
                line=dict(
                    color="#ffd1dc",
                    width=1
                )
            ),
            text=special_hover,
            hovertemplate="%{text}<extra></extra>",
            name="66 Special-attention sensors"
        ))

    # --------------------------------------------------------
    # MOVING VEHICLE
    # --------------------------------------------------------

    car_x = vehicle_position
    car_y = 0.0
    car_z = 0.48

    # Main vehicle body
    fig.add_trace(go.Mesh3d(
        x=[
            car_x - 0.8, car_x + 0.8,
            car_x + 0.8, car_x - 0.8,
            car_x - 0.8, car_x + 0.8,
            car_x + 0.8, car_x - 0.8
        ],
        y=[
            -0.55, -0.55, 0.55, 0.55,
            -0.55, -0.55, 0.55, 0.55
        ],
        z=[
            car_z, car_z, car_z, car_z,
            car_z + 0.55, car_z + 0.55,
            car_z + 0.55, car_z + 0.55
        ],
        i=[0, 0, 4, 4, 0, 0, 1, 1, 2, 2, 3, 3],
        j=[1, 2, 5, 6, 1, 5, 2, 6, 3, 7, 0, 4],
        k=[2, 3, 6, 7, 5, 4, 6, 5, 7, 6, 4, 7],
        color="#f4a340",
        opacity=1,
        flatshading=True,
        name="Simulated vehicle",
        hovertemplate="Vehicle position: %{x:.1f} m<extra></extra>"
    ))

    # Vehicle wheels
    for wheel_x in [car_x - 0.5, car_x + 0.5]:

        for wheel_y in [-0.48, 0.48]:

            fig.add_trace(go.Scatter3d(
                x=[wheel_x],
                y=[wheel_y],
                z=[0.42],
                mode="markers",
                marker=dict(
                    size=8,
                    color="#09121e"
                ),
                showlegend=False,
                hoverinfo="skip"
            ))

    # Vehicle position indicator
    fig.add_trace(go.Scatter3d(
        x=[car_x],
        y=[0],
        z=[1.2],
        mode="markers",
        marker=dict(
            size=5,
            color="#ffca65"
        ),
        name="Vehicle location",
        hovertemplate=f"Vehicle: {car_x:.1f} m<extra></extra>"
    ))

    # --------------------------------------------------------
    # LAYOUT
    # --------------------------------------------------------

    fig.update_layout(
        height=650,
        margin=dict(l=0, r=0, t=15, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        scene=dict(
            bgcolor="rgba(5,15,29,0)",
            xaxis=dict(
                title="Bridge length (m)",
                range=[-2, 32],
                backgroundcolor="#0a1728",
                gridcolor="#203b53",
                zerolinecolor="#203b53",
                color="#9cb9d3"
            ),
            yaxis=dict(
                title="Width",
                range=[-5, 5],
                backgroundcolor="#0a1728",
                gridcolor="#203b53",
                zerolinecolor="#203b53",
                color="#9cb9d3"
            ),
            zaxis=dict(
                title="Height",
                range=[-1, 13],
                backgroundcolor="#0a1728",
                gridcolor="#203b53",
                zerolinecolor="#203b53",
                color="#9cb9d3"
            ),
            aspectmode="manual",
            aspectratio=dict(
                x=2.7,
                y=0.8,
                z=0.9
            ),
            camera=dict(
                eye=dict(
                    x=1.7,
                    y=-2.0,
                    z=1.25
                )
            )
        ),
        legend=dict(
            orientation="h",
            y=1.02,
            x=0.02,
            font=dict(color="#d7eaff"),
            bgcolor="rgba(7,17,31,0.65)"
        ),
        hoverlabel=dict(
            bgcolor="#102940",
            font_color="white",
            bordercolor="#2dc8e8"
        )
    )

    return fig


# ============================================================
# CHART HELPER
# ============================================================

def style_chart(fig, height=350):

    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#c7d9ec",
            family="Inter"
        ),
        margin=dict(l=20, r=20, t=55, b=35),
        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        ),
        xaxis=dict(
            gridcolor="#243c53",
            zerolinecolor="#243c53"
        ),
        yaxis=dict(
            gridcolor="#243c53",
            zerolinecolor="#243c53"
        )
    )

    return fig


# ============================================================
# DASHBOARD SUMMARY
# ============================================================

st.markdown("### SYSTEM OVERVIEW")

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Bridge length",
    "30 m"
)

m2.metric(
    "Always-on sensors",
    always_count
)

m3.metric(
    "Special sensors",
    special_count,
    delta="ACTIVE" if special_mode else "STANDBY"
)

m4.metric(
    "Peak deflection",
    f"{current_peak_mm:.3f} mm"
)

# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌉 Bridge Overview",
    "📡 Sensor Network",
    "🔍 Change Detection",
    "📍 Localization",
    "📈 History & Trends"
])

# ============================================================
# TAB 1 — BRIDGE OVERVIEW
# ============================================================

with tab1:

    st.markdown("### 3D STRUCTURAL DIGITAL TWIN")

    st.caption(
        "Interactive bridge simulation • Drag to rotate • Scroll to zoom • "
        "Hover over sensors for readings"
    )

    if special_mode:
        st.warning(
            "SPECIAL ATTENTION ACTIVE — Additional sensor channels are enabled."
        )
    else:
        st.success(
            "NORMAL MONITORING — Always-on sensor network is operating."
        )

    bridge_fig = create_bridge()

    st.plotly_chart(
        bridge_fig,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "scrollZoom": True,
            "displaylogo": False
        },
        key="bridge_3d"
    )

    st.markdown("#### SENSOR LEGEND")

    leg1, leg2, leg3 = st.columns(3)

    leg1.markdown(
        "<span style='color:#39f5a2;font-size:20px'>●</span> "
        "Always-on sensors",
        unsafe_allow_html=True
    )

    leg2.markdown(
        "<span style='color:#ff4e70;font-size:20px'>◆</span> "
        "Special-attention sensors",
        unsafe_allow_html=True
    )

    leg3.markdown(
        "<span style='color:#f4a340;font-size:20px'>■</span> "
        "Moving vehicle",
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("#### LIVE STRUCTURAL RESPONSE")

    response_fig = go.Figure()

    response_fig.add_trace(go.Scatter(
        x=x,
        y=baseline_deflection * 1000,
        mode="lines",
        name="Baseline",
        line=dict(
            color="#43c9ef",
            width=2,
            dash="dash"
        )
    ))

    response_fig.add_trace(go.Scatter(
        x=x,
        y=current_deflection * 1000,
        mode="lines",
        name="Current response",
        line=dict(
            color="#36edaa",
            width=3
        ),
        fill="tozeroy",
        fillcolor="rgba(54,237,170,0.08)"
    ))

    response_fig.update_layout(
        title="Bridge deflection profile",
        xaxis_title="Bridge position (m)",
        yaxis_title="Deflection (mm)"
    )

    st.plotly_chart(
        style_chart(response_fig),
        use_container_width=True
    )

# ============================================================
# TAB 2 — SENSOR NETWORK
# ============================================================

with tab2:

    st.markdown("### DISTRIBUTED SENSOR NETWORK")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Always-on channels",
        "5"
    )

    c2.metric(
        "Stations",
        "11"
    )

    c3.metric(
        "Always-on readings",
        always_count
    )

    st.markdown("#### ALWAYS-ON SENSOR READINGS")

    st.dataframe(
        always_on_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.markdown("#### SPECIAL-ATTENTION SENSOR READINGS")

    if special_mode:

        st.success(
            f"Additional monitoring active: {special_count} readings."
        )

        st.dataframe(
            special_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Special-attention sensors are currently on standby. "
            "They activate when the trigger conditions are met."
        )

        st.dataframe(
            pd.DataFrame({
                "Sensor type": special_types,
                "Status": ["Standby"] * len(special_types)
            }),
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    st.markdown("#### SENSOR CHANNEL COVERAGE")

    coverage = pd.DataFrame({
        "Sensor category": always_on_types + special_types,
        "Stations": [11] * 11,
        "Status": (
            ["Active"] * 5 +
            (["Active"] * 6 if special_mode else ["Standby"] * 6)
        )
    })

    coverage_fig = go.Figure()

    coverage_fig.add_trace(go.Bar(
        x=coverage["Sensor category"],
        y=coverage["Stations"],
        marker_color=[
            "#39dba3" if status == "Active" else "#52677d"
            for status in coverage["Status"]
        ],
        text=coverage["Status"],
        textposition="outside"
    ))

    coverage_fig.update_layout(
        title="Sensor coverage by channel",
        xaxis_title="Sensor type",
        yaxis_title="Number of stations"
    )

    st.plotly_chart(
        style_chart(coverage_fig),
        use_container_width=True
    )

# ============================================================
# TAB 3 — CHANGE DETECTION
# ============================================================

with tab3:

    st.markdown("### STRUCTURAL CHANGE DETECTION")

    a, b, c = st.columns(3)

    a.metric(
        "Baseline deflection",
        f"{baseline_peak_mm:.3f} mm"
    )

    b.metric(
        "Current deflection",
        f"{current_peak_mm:.3f} mm"
    )

    c.metric(
        "Response change",
        f"{response_increase:.1f}%"
    )

    st.divider()

    st.markdown("#### BASELINE VS CURRENT RESPONSE")

    compare_fig = go.Figure()

    compare_fig.add_trace(go.Scatter(
        x=x,
        y=baseline_deflection * 1000,
        name="Baseline",
        mode="lines",
        line=dict(
            color="#42bfe9",
            width=3
        )
    ))

    compare_fig.add_trace(go.Scatter(
        x=x,
        y=current_deflection * 1000,
        name="Current",
        mode="lines",
        line=dict(
            color="#ffb454",
            width=3
        )
    ))

    compare_fig.update_layout(
        title="Structural response comparison",
        xaxis_title="Bridge position (m)",
        yaxis_title="Deflection (mm)"
    )

    st.plotly_chart(
        style_chart(compare_fig),
        use_container_width=True
    )

    st.markdown("#### DETECTION RESULT")

    if persistent_trigger:

        st.error(
            "PERSISTENT STRUCTURAL CHANGE INDICATED"
        )

        st.write(
            "The current response differs from the baseline "
            "by at least the simulation's 5% comparison threshold."
        )

    elif threshold_trigger:

        st.warning(
            "ATTENTION TRIGGERED — RESPONSE THRESHOLD EXCEEDED"
        )

        st.write(
            "The current response exceeded the selected "
            "deflection attention threshold."
        )

    else:

        st.success(
            "NO SIMULATED CHANGE TRIGGER DETECTED"
        )

        st.write(
            "The current response has not activated either "
            "special-attention trigger."
        )

    st.caption(
        "This is an educational simulation. It does not diagnose "
        "real structural damage or determine whether a bridge is safe."
    )

# ============================================================
# TAB 4 — LOCALIZATION
# ============================================================

with tab4:

    st.markdown("### STRUCTURAL CHANGE LOCALIZATION")

    st.caption(
        "Explore how the simulated response varies along the bridge."
    )

    location_fig = go.Figure()

    location_fig.add_trace(go.Scatter(
        x=x,
        y=current_deflection * 1000,
        mode="lines",
        name="Current response",
        line=dict(
            color="#37dcb0",
            width=3
        )
    ))

    location_fig.add_vline(
        x=change_location,
        line_dash="dash",
        line_color="#ff5979",
        annotation_text="Simulated change location"
    )

    location_fig.update_layout(
        title="Response along bridge length",
        xaxis_title="Bridge position (m)",
        yaxis_title="Deflection (mm)"
    )

    st.plotly_chart(
        style_chart(location_fig),
        use_container_width=True
    )

    # Sensor station response differences
    differences = (
        np.abs(station_current - station_baseline) * 1000
    )

    location_df = pd.DataFrame({
        "Station (m)": stations,
        "Baseline (mm)": np.abs(station_baseline) * 1000,
        "Current (mm)": np.abs(station_current) * 1000,
        "Difference (mm)": differences
    })

    location_df = location_df.round(4)

    st.markdown("#### STATION COMPARISON")

    st.dataframe(
        location_df,
        use_container_width=True,
        hide_index=True
    )

    if local_change > 0 or stiffness_reduction > 0:

        st.info(
            f"Simulated change input location: {change_location:.1f} m"
        )

    else:

        st.info(
            "No structural change has been added to the simulation."
        )

# ============================================================
# TAB 5 — HISTORY AND TRENDS
# ============================================================

with tab5:

    st.markdown("### HISTORICAL MONITORING")

    if "history" not in st.session_state:
        st.session_state.history = []

    col_a, col_b = st.columns([1, 1])

    with col_a:

        if st.button(
            "➕ Save current simulation snapshot",
            use_container_width=True
        ):

            snapshot = {
                "Timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "Vehicle weight (N)": vehicle_weight,
                "Axles": axles,
                "Vehicle position (m)": vehicle_position,
                "Stiffness reduction (%)": stiffness_reduction,
                "Local change (%)": local_change,
                "Baseline deflection (mm)": baseline_peak_mm,
                "Current deflection (mm)": current_peak_mm,
                "Response increase (%)": response_increase,
                "Always-on readings": always_count,
                "Special readings": special_count,
                "Special mode": special_mode
            }

            st.session_state.history.append(snapshot)

            st.success("Simulation snapshot saved.")

    with col_b:

        if st.button(
            "🗑️ Clear session history",
            use_container_width=True
        ):

            st.session_state.history = []

            st.success("Session history cleared.")

    st.divider()

    if st.session_state.history:

        history_df = pd.DataFrame(
            st.session_state.history
        )

        st.markdown("#### SAVED SIMULATION RECORDS")

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        history_fig = go.Figure()

        history_fig.add_trace(go.Scatter(
            x=list(range(1, len(history_df) + 1)),
            y=history_df["Current deflection (mm)"],
            mode="lines+markers",
            name="Current deflection",
            line=dict(
                color="#39d9ac",
                width=3
            ),
            marker=dict(size=9)
        ))

        history_fig.add_trace(go.Scatter(
            x=list(range(1, len(history_df) + 1)),
            y=history_df["Baseline deflection (mm)"],
            mode="lines+markers",
            name="Baseline deflection",
            line=dict(
                color="#4cb9ed",
                width=2,
                dash="dash"
            )
        ))

        history_fig.update_layout(
            title="Deflection history",
            xaxis_title="Saved snapshot",
            yaxis_title="Deflection (mm)"
        )

        st.plotly_chart(
            style_chart(history_fig),
            use_container_width=True
        )

        csv_data = history_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download history as CSV",
            data=csv_data,
            file_name="bridge_monitoring_history.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:

        st.info(
            "No snapshots saved yet. Save a simulation snapshot "
            "to begin building your history."
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown("""
<div style="
    text-align:center;
    color:#7794ae;
    font-size:12px;
    padding:10px;
">
    INTELLIGENT BRIDGE MONITORING SYSTEM<br>
    Educational structural monitoring simulation • 30 m beam model<br>
    Simulated sensor readings only — not a real bridge safety system
</div>
""", unsafe_allow_html=True)
