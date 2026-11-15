
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart Bridge Monitor",
    page_icon="🌉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}

.stApp {
    background: linear-gradient(#75C8F1, #D5F0FA);
    overflow-x: hidden;
}

.block-container {
    max-width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
}

[data-testid="stPlotlyChart"] {
    padding: 0 !important;
    margin: 0 !important;
}

[data-testid="stPlotlyChart"] > div {
    width: 100% !important;
}

.st-key-top_panel,
.st-key-left_panel,
.st-key-right_panel,
.st-key-bottom_panel {
    position: fixed !important;
    z-index: 1000 !important;
    background: rgba(9, 65, 111, 0.78);
    backdrop-filter: blur(13px);
    -webkit-backdrop-filter: blur(13px);
    border: 1px solid rgba(255,255,255,0.4);
    border-radius: 15px;
    color: white !important;
    padding: 12px 16px;
    box-shadow: 0 8px 25px rgba(0,35,75,0.22);
}

.st-key-top_panel {
    top: 12px;
    left: 1.3%;
    width: 97.4%;
}

.st-key-left_panel {
    top: 112px;
    left: 1.3%;
    width: 255px;
    max-height: 67vh;
    overflow-y: auto;
}

.st-key-right_panel {
    top: 112px;
    right: 1.3%;
    width: 255px;
    max-height: 67vh;
    overflow-y: auto;
}

.st-key-bottom_panel {
    bottom: 12px;
    left: 1.3%;
    width: 97.4%;
}

.st-key-top_panel *,
.st-key-left_panel *,
.st-key-right_panel *,
.st-key-bottom_panel * {
    color: white !important;
}

.st-key-left_panel [data-testid="stSlider"],
.st-key-right_panel [data-testid="stSlider"] {
    padding-top: 0;
}

.st-key-left_panel [data-testid="stWidgetLabel"],
.st-key-right_panel [data-testid="stWidgetLabel"] {
    font-size: 0.82rem;
}

.st-key-left_panel [data-baseweb="select"],
.st-key-left_panel input {
    background-color: rgba(255,255,255,0.12);
}

.st-key-left_panel [data-testid="stButton"] button,
.st-key-bottom_panel [data-testid="stDownloadButton"] button {
    background: #159BD4;
    border: 1px solid #8ADFFF;
    color: white;
    border-radius: 9px;
}

.metric-box {
    background: rgba(255,255,255,0.12);
    padding: 9px;
    border-radius: 9px;
    margin: 5px 0;
}

.small-note {
    font-size: 11px;
    opacity: 0.8;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

# ============================================================
# TOP HEADER
# ============================================================

with st.container(key="top_panel"):
    h1, h2, h3 = st.columns([3.2, 1.5, 2])

    with h1:
        st.markdown(
            "## 🌉 SMART BRIDGE MONITOR"
            "<div class='small-note'>STRUCTURAL HEALTH MONITORING SYSTEM</div>",
            unsafe_allow_html=True
        )

    with h2:
        st.markdown("🟢 **SYSTEM ONLINE**")
        st.caption("Continuous monitoring")

    with h3:
        st.markdown(
            f"**MONITORING MODE**　📡　{datetime.now().strftime('%b %d, %Y  %H:%M:%S')}"
        )

# ============================================================
# LEFT PANEL - CONTROLS
# ============================================================

with st.container(key="left_panel"):
    st.markdown("### 🚙 Vehicle Controls")

    vehicle_position = st.slider(
        "Vehicle position",
        min_value=0.0,
        max_value=40.0,
        value=20.0,
        step=0.5
    )

    vehicle_weight = st.slider(
        "Vehicle load (N)",
        min_value=5000,
        max_value=50000,
        value=20000,
        step=1000
    )

    axle_count = st.selectbox(
        "Number of axles",
        [2, 3, 4, 5],
        index=1
    )

    axle_spacing = st.slider(
        "Axle spacing (m)",
        1.0,
        5.0,
        2.0,
        0.5
    )

    st.divider()
    st.markdown("### ⚙️ Simulation Settings")

    traffic_level = st.select_slider(
        "Traffic volume",
        options=["Low", "Medium", "High", "Very High"],
        value="Medium"
    )

    vehicle_speed = st.slider(
        "Vehicle speed",
        10,
        120,
        60,
        5
    )

    st.divider()
    st.markdown("### 🏗️ Structural Conditions")

    stiffness_reduction = st.slider(
        "Simulated stiffness reduction (%)",
        0,
        30,
        0,
        1
    )

    change_location = st.slider(
        "Change location (m)",
        0.0,
        40.0,
        20.0,
        1.0
    )

    local_change = st.slider(
        "Local change signal (%)",
        0,
        40,
        0,
        1
    )

    attention_threshold = st.slider(
        "Deflection attention threshold (mm)",
        1.0,
        20.0,
        5.0,
        0.5
    )

# ============================================================
# BRIDGE MODEL
# ============================================================

L = 40.0
E = 200e9
I = 0.08

x = np.linspace(0, L, 401)

effective_EI = E * I * (1 - stiffness_reduction / 100)

# Simplified moving-load response for visualization
axle_offsets = np.arange(axle_count) * axle_spacing
axle_positions = vehicle_position - axle_offsets

load_per_axle = vehicle_weight / axle_count

def gaussian_response(position, load, width=5.5):
    return (
        load / 10000
        * np.exp(-((x - position) / width) ** 2)
    )

response = np.zeros_like(x)

for axle in axle_positions:
    response += gaussian_response(axle, load_per_axle)

# Deflection is a simplified educational response.
deflection_m = (
    response * 0.0015
    * (1 + stiffness_reduction / 100)
)

# Persistent localized change signal
damage_shape = np.exp(
    -((x - change_location) / 3.0) ** 2
)

deflection_m += (
    local_change / 100
    * 0.003
    * damage_shape
)

deflection_mm = deflection_m * 1000

deck_base = 8.0
deck_z = deck_base - deflection_m

peak_deflection = float(np.max(np.abs(deflection_mm)))

# ============================================================
# SENSOR NETWORK
# ============================================================

sensor_x_stations = np.linspace(2, 38, 11)
sensor_y_positions = np.linspace(-3.2, 3.2, 5)

normal_x = []
normal_y = []
normal_z = []
normal_values = []

for sx in sensor_x_stations:
    idx = np.argmin(np.abs(x - sx))

    for sy in sensor_y_positions:
        normal_x.append(sx)
        normal_y.append(sy)
        normal_z.append(deck_base - deflection_m[idx] + 0.45)

        normal_values.append(
            abs(deflection_mm[idx]) * (1 + abs(sy) * 0.03)
        )

normal_x = np.array(normal_x)
normal_y = np.array(normal_y)
normal_z = np.array(normal_z)
normal_values = np.array(normal_values)

# Five channels at eleven stations = 55 normal readings.
# Six additional channels at eleven stations = 66 special readings.

persistent_change = (
    local_change >= 5 or stiffness_reduction >= 5
)

special_mode = (
    peak_deflection >= attention_threshold
    or persistent_change
)

special_x = []
special_y = []
special_z = []

special_y_positions = np.linspace(-3.5, 3.5, 6)

for sx in sensor_x_stations:
    idx = np.argmin(np.abs(x - sx))

    for sy in special_y_positions:
        special_x.append(sx)
        special_y.append(sy)
        special_z.append(
            deck_base - deflection_m[idx] + 0.85
        )

# ============================================================
# 3D BRIDGE SCENE
# ============================================================

fig = go.Figure()

# BLUE WATER
water_x = np.linspace(-5, 45, 75)
water_y = np.linspace(-35, 35, 55)
WX, WY = np.meshgrid(water_x, water_y)

WZ = (
    0.1
    + 0.035 * np.sin(WX * 0.8)
    * np.cos(WY * 0.6)
)

fig.add_trace(go.Surface(
    x=WX,
    y=WY,
    z=WZ,
    colorscale=[
        [0, "#075B91"],
        [0.35, "#1687BD"],
        [0.7, "#39A9D1"],
        [1, "#8BD9EB"]
    ],
    showscale=False,
    opacity=0.96,
    hoverinfo="skip",
    name="Water"
))

# GREEN DISTANT SHORELINE
shore_x = np.linspace(-5, 45, 75)
shore_y = np.linspace(17, 29, 35)
SX, SY = np.meshgrid(shore_x, shore_y)

SZ = (
    1.5
    + 2.5 * np.exp(-((SX - 8) / 12) ** 2)
    + 2.2 * np.exp(-((SX - 34) / 9) ** 2)
    + 0.5 * np.sin(SX / 3) * np.cos(SY / 4)
)

fig.add_trace(go.Surface(
    x=SX,
    y=SY,
    z=SZ,
    colorscale=[
        [0, "#28663B"],
        [0.4, "#428C42"],
        [0.75, "#68AD4F"],
        [1, "#A0CB70"]
    ],
    showscale=False,
    hoverinfo="skip",
    name="Green hills"
))

# FAR SHORELINE ON OPPOSITE SIDE
SY2 = -SY

fig.add_trace(go.Surface(
    x=SX,
    y=SY2,
    z=SZ,
    colorscale=[
        [0, "#28663B"],
        [0.4, "#428C42"],
        [0.75, "#68AD4F"],
        [1, "#A0CB70"]
    ],
    showscale=False,
    hoverinfo="skip",
    name="Far hills"
))

# BRIDGE DECK
deck_y = np.linspace(-4, 4, 12)
DX, DY = np.meshgrid(x, deck_y)
DZ = np.tile(deck_z, (len(deck_y), 1))

fig.add_trace(go.Surface(
    x=DX,
    y=DY,
    z=DZ,
    colorscale=[
        [0, "#AEB9C2"],
        [0.5, "#DCE3E8"],
        [1, "#FFFFFF"]
    ],
    showscale=False,
    opacity=1,
    hoverinfo="skip",
    name="Bridge deck"
))

# BRIDGE EDGE RAILINGS
for side in [-1, 1]:
    fig.add_trace(go.Scatter3d(
        x=x,
        y=np.full_like(x, side * 4),
        z=deck_z + 0.5,
        mode="lines",
        line=dict(color="#E8F4F8", width=5),
        showlegend=False,
        hoverinfo="skip"
    ))

# TWO MAIN TOWERS
tower_positions = [18, 32]

for tx in tower_positions:
    tower_bottom = 8.0
    tower_top = 28.0

    for ty in [-1.0, 1.0]:
        fig.add_trace(go.Scatter3d(
            x=[tx, tx],
            y=[ty, ty],
            z=[tower_bottom, tower_top],
            mode="lines",
            line=dict(color="#E8E8E8", width=13),
            showlegend=False,
            hoverinfo="skip"
        ))

    # Crossbeam
    fig.add_trace(go.Scatter3d(
        x=[tx, tx],
        y=[-1, 1],
        z=[tower_top, tower_top],
        mode="lines",
        line=dict(color="#F5F5F5", width=9),
        showlegend=False,
        hoverinfo="skip"
    ))

    # Cable stays on both sides
    anchor_positions = np.linspace(
        max(1, tx - 14),
        min(39, tx + 14),
        13
    )

    for anchor in anchor_positions:
        idx = np.argmin(np.abs(x - anchor))
        anchor_z = deck_z[idx] + 0.35

        for ty in [-3.5, 3.5]:
            fig.add_trace(go.Scatter3d(
                x=[tx, anchor],
                y=[0, ty],
                z=[tower_top, anchor_z],
                mode="lines",
                line=dict(
                    color="rgba(245,250,255,0.92)",
                    width=2
                ),
                showlegend=False,
                hoverinfo="skip"
            ))

# SUPPORT PIERS
for px in [8, 18, 25, 32, 39]:
    fig.add_trace(go.Scatter3d(
        x=[px, px],
        y=[0, 0],
        z=[0.3, deck_base],
        mode="lines",
        line=dict(color="#C9D2D9", width=15),
        showlegend=False,
        hoverinfo="skip"
    ))

# GREEN NORMAL SENSORS - 55 DOTS
fig.add_trace(go.Scatter3d(
    x=normal_x,
    y=normal_y,
    z=normal_z,
    mode="markers",
    marker=dict(
        size=6,
        color="#00FF55",
        line=dict(color="white", width=2),
        opacity=1
    ),
    name="55 Normal sensors",
    text=[
        f"Normal sensor {i+1}<br>Deflection: {v:.3f} mm"
        for i, v in enumerate(normal_values)
    ],
    hovertemplate="%{text}<extra></extra>"
))

# RED SPECIAL ATTENTION SENSORS - 66 DOTS
if special_mode:
    fig.add_trace(go.Scatter3d(
        x=special_x,
        y=special_y,
        z=special_z,
        mode="markers",
        marker=dict(
            size=7,
            color="#FF3030",
            line=dict(color="white", width=2),
            opacity=1
        ),
        name="66 Special attention sensors",
        text=[
            f"Special sensor {i+1}<br>Attention mode active"
            for i in range(66)
        ],
        hovertemplate="%{text}<extra></extra>"
    ))

# MOVING VEHICLE
vehicle_index = np.argmin(np.abs(x - vehicle_position))

fig.add_trace(go.Scatter3d(
    x=[vehicle_position],
    y=[0],
    z=[deck_z[vehicle_index] + 1.0],
    mode="markers+text",
    marker=dict(
        size=12,
        color="#F5F7FA",
        symbol="square",
        line=dict(color="#253D50", width=3)
    ),
    text=["🚚 VEHICLE"],
    textposition="top center",
    textfont=dict(color="white", size=12),
    name="Moving vehicle",
    hovertemplate="Vehicle position: %{x:.1f} m<extra></extra>"
))

# 3D SCENE SETTINGS
fig.update_layout(
    height=950,
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="#8CCFF0",
    plot_bgcolor="#8CCFF0",
    showlegend=False,
    scene=dict(
        bgcolor="#8CCFF0",
        xaxis=dict(
            visible=False,
            range=[-5, 45]
        ),
        yaxis=dict(
            visible=False,
            range=[-35, 35]
        ),
        zaxis=dict(
            visible=False,
            range=[0, 31]
        ),
        aspectmode="manual",
        aspectratio=dict(x=2.2, y=1.25, z=0.95),
        camera=dict(
            eye=dict(x=1.65, y=-2.5, z=1.15),
            center=dict(x=0, y=0, z=0)
        )
    )
)

# ============================================================
# MAIN FULL-SCREEN BRIDGE
# ============================================================

st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "scrollZoom": True,
        "responsive": True
    },
    key="bridge_scene"
)

# ============================================================
# SENSOR CALCULATIONS
# ============================================================

average_deflection = float(np.mean(np.abs(normal_values)))

average_strain = (
    average_deflection * 42.5 + 12
)

average_vibration = (
    0.12 + average_deflection * 0.035
)

average_temperature = 27.0

traffic_factor = {
    "Low": 0.35,
    "Medium": 0.60,
    "High": 0.82,
    "Very High": 1.0
}[traffic_level]

vehicle_count = int(1248 * traffic_factor)

alert_count = (
    3 if special_mode else 0
)

# ============================================================
# RIGHT PANEL - SENSOR READINGS AND ALERTS
# ============================================================

with st.container(key="right_panel"):
    st.markdown("### 📡 Sensor Readings")

    st.markdown(
        f"""
        <div class="metric-box">
        🟢 Normal Sensors <b style="float:right">55 / 55</b>
        </div>
        <div class="metric-box">
        🔴 Attention Sensors <b style="float:right">
        {66 if special_mode else 0} / 66
        </b>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.metric("Average strain", f"{average_strain:.2f} με")
    st.metric("Average vibration", f"{average_vibration:.3f} g")
    st.metric("Average temperature", f"{average_temperature:.1f} °C")
    st.metric("Maximum deflection", f"{peak_deflection:.3f} mm")

    st.divider()
    st.markdown("### 🚨 Alerts")

    if special_mode:
        st.error("SPECIAL ATTENTION MODE ACTIVE")
        st.warning("Structural response requires further investigation.")
        st.write("🔴 Deflection / persistent-change trigger")
    else:
        st.success("No significant simulated changes detected.")

    st.divider()
    st.markdown("### 🔍 Change Detection")

    if persistent_change:
        st.warning(
            f"Persistent change signal: {local_change}%"
        )
        st.write(
            f"Simulated change location: {change_location:.1f} m"
        )
    else:
        st.success("No persistent change signal configured.")

    if peak_deflection >= attention_threshold:
        st.warning("Deflection threshold exceeded.")
    else:
        st.success("Deflection below attention threshold.")

# ============================================================
# HISTORY
# ============================================================

snapshot = {
    "Time": datetime.now().strftime("%H:%M:%S"),
    "Vehicle position (m)": vehicle_position,
    "Peak deflection (mm)": peak_deflection,
    "Average strain (με)": average_strain,
    "Average vibration (g)": average_vibration,
    "Special attention": special_mode
}

if (
    not st.session_state.history
    or st.session_state.history[-1]["Vehicle position (m)"] != vehicle_position
    or st.session_state.history[-1]["Peak deflection (mm)"] != peak_deflection
):
    st.session_state.history.append(snapshot)

st.session_state.history = st.session_state.history[-100:]

history_df = pd.DataFrame(st.session_state.history)

# ============================================================
# BOTTOM PANEL
# ============================================================

with st.container(key="bottom_panel"):
    st.markdown("### 📊 Bridge Monitoring Overview")

    c1, c2, c3, c4 = st.columns([1.2, 1.1, 2.2, 0.9])

    with c1:
        st.markdown("**🚙 Traffic Information**")
        st.metric("Simulated vehicles", f"{vehicle_count:,}")
        st.caption(f"Traffic level: {traffic_level}")

    with c2:
        st.markdown("**📍 Localization**")
        st.metric("Vehicle position", f"{vehicle_position:.1f} m")
        st.caption("Lane: Center")

    with c3:
        st.markdown("**📈 Sensor History**")

        if len(history_df) > 1:
            chart_df = history_df.set_index("Time")[
                ["Peak deflection (mm)", "Average vibration (g)"]
            ]
            st.line_chart(chart_df, height=110)
        else:
            st.caption("Move the vehicle or adjust the simulation to build history.")

    with c4:
        st.markdown("**📥 Export**")

        csv_data = history_df.to_csv(index=False)

        st.download_button(
            "Export CSV",
            data=csv_data,
            file_name="bridge_monitoring_history.csv",
            mime="text/csv",
            use_container_width=True
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div style="
    position:fixed;
    bottom:2px;
    right:15px;
    font-size:9px;
    color:#FFFFFF;
    z-index:2000;
    text-shadow:1px 1px 3px #17445D;">
Educational simulation only | Not real bridge measurements or a certified safety system
</div>
""", unsafe_allow_html=True)
