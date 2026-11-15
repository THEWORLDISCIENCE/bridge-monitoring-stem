
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import csv
import io
from datetime import datetime

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Intelligent Bridge Monitoring",
    page_icon="🌉",
    layout="wide",
)

st.markdown("""
<style>
.stApp {
    background-color: #0b1220;
    color: #e2e8f0;
}
.block-container {
    max-width: 1550px;
    padding-top: 1rem;
}
section[data-testid="stSidebar"] {
    background-color: #111c30;
}
section[data-testid="stSidebar"] * {
    color: #e2e8f0;
}
h1, h2, h3 {
    color: #f8fafc !important;
}
div[data-testid="stMetric"] {
    background: #17243a;
    border: 1px solid #334155;
    padding: 14px;
    border-radius: 12px;
}
div[data-testid="stMetric"] label {
    color: #94a3b8 !important;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #f8fafc !important;
}
.stTabs [data-baseweb="tab"] {
    color: #cbd5e1;
}
.stTabs [aria-selected="true"] {
    color: #38bdf8 !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🌉 INTELLIGENT BRIDGE MONITORING")
st.caption(
    "DIGITAL TWIN  |  CONTINUOUS MONITORING  |  "
    "ADAPTIVE SENSOR NETWORK  |  STRUCTURAL CHANGE DETECTION"
)

# ==========================================================
# BRIDGE MODEL
# ==========================================================

L = 30.0
E = 200e9
I = 0.08

x = np.linspace(0, L, 401)
sensor_positions = np.linspace(2.0, 28.0, 11)

# ==========================================================
# SIDEBAR CONTROLS
# ==========================================================

st.sidebar.title("🎛️ CONTROL CENTER")

st.sidebar.subheader("Vehicle Simulation")

weight = st.sidebar.slider(
    "Vehicle weight (N)",
    5000, 100000, 20000, 5000
)

axles = st.sidebar.slider(
    "Number of axles",
    2, 5, 4
)

spacing = st.sidebar.slider(
    "Axle spacing (m)",
    2.0, 8.0, 3.0, 0.5
)

vehicle_position = st.sidebar.slider(
    "Vehicle position on bridge (m)",
    0.0, 30.0, 15.0, 0.5
)

st.sidebar.divider()
st.sidebar.subheader("Adaptive Monitoring")

trigger = st.sidebar.slider(
    "Deflection attention trigger (mm)",
    0.1, 5.0, 0.7, 0.1
)

st.sidebar.divider()
st.sidebar.subheader("Structural Change Experiment")

stiffness_change = st.sidebar.slider(
    "Global stiffness reduction (%)",
    0, 30, 15, 5
)

st.sidebar.divider()
st.sidebar.subheader("Localization Demonstration")

local_location = st.sidebar.slider(
    "Simulated change location (m)",
    3, 27, 15, 3
)

local_reduction = st.sidebar.slider(
    "Local change signal (%)",
    5, 30, 15, 5
)

# ==========================================================
# BEAM RESPONSE
# ==========================================================

def beam_response(vehicle_position, inertia):

    moment = np.zeros_like(x)
    deflection = np.zeros_like(x)

    axle_load = weight / axles

    for axle_index in range(axles):

        a = vehicle_position - axle_index * spacing

        if 0 <= a <= L:

            b = L - a

            moment += np.where(
                x <= a,
                axle_load * b * x / L,
                axle_load * a * (L - x) / L
            )

            left = x <= a
            right = ~left

            deflection[left] += (
                axle_load * b * x[left]
                * (L**2 - b**2 - x[left]**2)
                / (6 * L * E * inertia)
            )

            deflection[right] += (
                axle_load * a * (L - x[right])
                * (L**2 - a**2 - (L - x[right])**2)
                / (6 * L * E * inertia)
            )

    return moment, deflection


# ==========================================================
# BASELINE AND CURRENT STRUCTURAL RESPONSE
# ==========================================================

changed_inertia = I * (1 - stiffness_change / 100)

vehicle_positions = np.linspace(
    -axles * spacing,
    L,
    140
)

moment_envelope = np.zeros_like(x)
baseline_envelope = np.zeros_like(x)
current_envelope = np.zeros_like(x)

for position in vehicle_positions:

    moment, baseline_deflection = beam_response(
        position, I
    )

    _, current_deflection = beam_response(
        position, changed_inertia
    )

    moment_envelope = np.maximum(
        moment_envelope, moment
    )

    baseline_envelope = np.maximum(
        baseline_envelope,
        np.abs(baseline_deflection)
    )

    current_envelope = np.maximum(
        current_envelope,
        np.abs(current_deflection)
    )

baseline_peak = float(
    np.max(baseline_envelope) * 1000
)

changed_peak = float(
    np.max(current_envelope) * 1000
)

peak_moment = float(
    np.max(moment_envelope)
)

response_increase = (
    (changed_peak - baseline_peak) / baseline_peak * 100
    if baseline_peak > 0 else 0
)

# ==========================================================
# ALWAYS-ON SENSOR DATA
# ==========================================================

deflection_mm = (
    np.interp(sensor_positions, x, current_envelope) * 1000
)

baseline_deflection_mm = (
    np.interp(sensor_positions, x, baseline_envelope) * 1000
)

curvature = np.gradient(
    np.gradient(current_envelope, x), x
)

strain_micro = (
    np.interp(sensor_positions, x, np.abs(curvature))
    * 0.5 * 1e6
)

vibration_index = 0.15 + deflection_mm * 4

temperature_c = (
    22 + 3 * np.sin(np.pi * sensor_positions / L)
)

traffic_load_index = np.clip(
    (weight / 100000)
    * 100
    * (0.65 + 0.35 * np.sin(np.pi * sensor_positions / L)),
    0, 100
)

normal_data = {
    "Deflection (mm)": np.round(deflection_mm, 3),
    "Strain proxy (µε)": np.round(strain_micro, 2),
    "Vibration index": np.round(vibration_index, 3),
    "Temperature (°C)": np.round(temperature_c, 2),
    "Traffic/load index (%)": np.round(traffic_load_index, 1),
}

sensor_attention = deflection_mm > trigger

persistent_change = response_increase >= 5

special_mode = bool(
    np.any(sensor_attention) or persistent_change
)

# ==========================================================
# SPECIAL ATTENTION SENSOR DATA
# ==========================================================

local_shape = np.exp(
    -((sensor_positions - local_location) ** 2)
    / (2 * 4.0**2)
)

tilt_degrees = np.round(
    deflection_mm * 0.002, 4
)

humidity_percent = np.round(
    48 + 17 * np.sin(2 * np.pi * sensor_positions / L), 1
)

corrosion_indicator = np.round(
    np.clip((humidity_percent - 45) * 2, 0, 100), 1
)

crack_width_proxy = np.round(
    local_reduction / 1000 * local_shape, 4
)

acoustic_activity_proxy = np.round(
    local_reduction * local_shape * 1.8, 1
)

joint_displacement_mm = np.round(
    deflection_mm * 0.18 + local_shape * 0.03, 4
)

special_data = {
    "Tilt proxy (°)": tilt_degrees,
    "Humidity (%)": humidity_percent,
    "Corrosion indicator (%)": corrosion_indicator,
    "Crack-width proxy (mm)": crack_width_proxy,
    "Acoustic activity proxy": acoustic_activity_proxy,
    "Joint displacement proxy (mm)": joint_displacement_mm,
}

# ==========================================================
# INTERACTIVE 3D BRIDGE FUNCTION
# ==========================================================

def create_bridge():

    fig = go.Figure()

    deck_height = 2.0
    bridge_width = 4.0

    bridge_x = np.linspace(0, L, 100)

    # ---------------- BRIDGE ROAD DECK ----------------

    deck_x = np.tile(bridge_x, (2, 1))

    deck_y = np.array([
        [-bridge_width / 2] * len(bridge_x),
        [bridge_width / 2] * len(bridge_x)
    ])

    deck_z = np.full_like(deck_x, deck_height)

    fig.add_trace(go.Surface(
        x=deck_x,
        y=deck_y,
        z=deck_z,
        colorscale=[
            [0, "#26364d"],
            [0.5, "#475569"],
            [1, "#64748b"]
        ],
        showscale=False,
        name="Bridge road deck",
        hoverinfo="skip",
        opacity=1
    ))

    # ---------------- ROAD EDGE LINES ----------------

    for side in [-1.8, 1.8]:

        fig.add_trace(go.Scatter3d(
            x=bridge_x,
            y=[side] * len(bridge_x),
            z=[deck_height + 0.04] * len(bridge_x),
            mode="lines",
            line=dict(
                color="#cbd5e1",
                width=5
            ),
            showlegend=False,
            hoverinfo="skip"
        ))

    # ---------------- SUPPORT BEAMS ----------------

    for side in [-1.5, 1.5]:

        fig.add_trace(go.Scatter3d(
            x=bridge_x,
            y=[side] * len(bridge_x),
            z=[1.5] * len(bridge_x),
            mode="lines",
            line=dict(
                color="#94a3b8",
                width=11
            ),
            name="Main support beam" if side < 0 else None,
            showlegend=(side < 0),
            hoverinfo="skip"
        ))

    # ---------------- BRIDGE TOWERS ----------------

    tower_locations = [8, 22]

    for tower_x in tower_locations:

        for side in [-1.5, 1.5]:

            fig.add_trace(go.Scatter3d(
                x=[tower_x, tower_x],
                y=[side, side],
                z=[deck_height, 11],
                mode="lines",
                line=dict(
                    color="#dbeafe",
                    width=13
                ),
                name="Bridge tower" if (
                    tower_x == 8 and side == -1.5
                ) else None,
                showlegend=(
                    tower_x == 8 and side == -1.5
                ),
                hoverinfo="skip"
            ))

    # ---------------- CABLES ----------------

    for tower_x in tower_locations:

        if tower_x == 8:
            anchors = np.arange(1, 8, 1)
        else:
            anchors = np.arange(23, 30, 1)

        for anchor in anchors:

            fig.add_trace(go.Scatter3d(
                x=[tower_x, anchor],
                y=[0, 0],
                z=[11, deck_height],
                mode="lines",
                line=dict(
                    color="#38bdf8",
                    width=3
                ),
                showlegend=False,
                hoverinfo="skip"
            ))

    # ---------------- CROSS SUPPORTS ----------------

    for support_x in [0, 5, 10, 15, 20, 25, 30]:

        fig.add_trace(go.Scatter3d(
            x=[support_x, support_x],
            y=[-1.5, 1.5],
            z=[1.5, 1.5],
            mode="lines",
            line=dict(
                color="#64748b",
                width=5
            ),
            showlegend=False,
            hoverinfo="skip"
        ))

    # ======================================================
    # ALWAYS-ON SENSOR NETWORK
    # ======================================================

    normal_channels = [
        ("Deflection", deflection_mm),
        ("Strain", strain_micro),
        ("Vibration", vibration_index),
        ("Temperature", temperature_c),
        ("Traffic/load", traffic_load_index),
    ]

    normal_x = []
    normal_y = []
    normal_z = []
    normal_text = []

    for channel_index, (channel_name, values) in enumerate(
        normal_channels
    ):

        y_pos = -1.25 + channel_index * 0.55

        for i, station in enumerate(sensor_positions):

            normal_x.append(station)
            normal_y.append(y_pos)
            normal_z.append(deck_height + 0.18)

            normal_text.append(
                f"<b>{channel_name}</b>"
                f"<br>Station: {station:.1f} m"
                f"<br>Reading: {values[i]}"
            )

    fig.add_trace(go.Scatter3d(
        x=normal_x,
        y=normal_y,
        z=normal_z,
        mode="markers",
        marker=dict(
            size=4.5,
            color="#22c55e",
            opacity=0.95,
            line=dict(
                color="#dcfce7",
                width=1
            )
        ),
        name="55 Always-on sensors",
        text=normal_text,
        hovertemplate="%{text}<extra></extra>"
    ))

    # ======================================================
    # SPECIAL ATTENTION SENSOR NETWORK
    # ======================================================

    if special_mode:

        special_channels = [
            ("Tilt", tilt_degrees),
            ("Humidity", humidity_percent),
            ("Corrosion", corrosion_indicator),
            ("Crack-width", crack_width_proxy),
            ("Acoustic activity", acoustic_activity_proxy),
            ("Joint displacement", joint_displacement_mm),
        ]

        special_x = []
        special_y = []
        special_z = []
        special_text = []

        for channel_index, (channel_name, values) in enumerate(
            special_channels
        ):

            y_pos = -1.35 + channel_index * 0.52

            for i, station in enumerate(sensor_positions):

                special_x.append(station)
                special_y.append(y_pos)
                special_z.append(deck_height + 0.35)

                special_text.append(
                    f"<b>{channel_name}</b>"
                    f"<br>Station: {station:.1f} m"
                    f"<br>Reading: {values[i]}"
                )

        fig.add_trace(go.Scatter3d(
            x=special_x,
            y=special_y,
            z=special_z,
            mode="markers",
            marker=dict(
                size=4.5,
                color="#ef4444",
                opacity=0.95,
                symbol="diamond",
                line=dict(
                    color="#fee2e2",
                    width=1
                )
            ),
            name="66 Special-attention sensors",
            text=special_text,
            hovertemplate="%{text}<extra></extra>"
        ))

    # ======================================================
    # SIMULATED VEHICLE
    # ======================================================

    car_x = vehicle_position
    car_y = 0
    car_z = deck_height + 0.42

    # Vehicle body
    fig.add_trace(go.Mesh3d(
        x=[
            car_x - 0.9,
            car_x + 0.9,
            car_x + 0.9,
            car_x - 0.9,
            car_x - 0.65,
            car_x + 0.65,
            car_x + 0.65,
            car_x - 0.65
        ],
        y=[
            -0.55, -0.55, 0.55, 0.55,
            -0.42, -0.42, 0.42, 0.42
        ],
        z=[
            car_z, car_z, car_z, car_z,
            car_z + 0.65, car_z + 0.65,
            car_z + 0.65, car_z + 0.65
        ],
        i=[0, 0, 0, 4, 4, 5, 1, 2, 3, 7],
        j=[1, 2, 3, 5, 6, 6, 5, 6, 7, 4],
        k=[4, 5, 7, 1, 2, 2, 2, 3, 0, 6],
        color="#f59e0b",
        opacity=1,
        name="Simulated vehicle",
        hovertemplate=(
            "Simulated vehicle"
            f"<br>Position: {vehicle_position:.1f} m"
            f"<br>Weight: {weight:,} N"
            "<extra></extra>"
        )
    ))

    # Vehicle wheels
    for wheel_x in [car_x - 0.55, car_x + 0.55]:

        for wheel_y in [-0.48, 0.48]:

            fig.add_trace(go.Scatter3d(
                x=[wheel_x],
                y=[wheel_y],
                z=[car_z],
                mode="markers",
                marker=dict(
                    size=7,
                    color="#111827"
                ),
                showlegend=False,
                hoverinfo="skip"
            ))

    # ---------------- VEHICLE POSITION MARKER ----------------

    fig.add_trace(go.Scatter3d(
        x=[car_x],
        y=[0],
        z=[deck_height + 1.3],
        mode="text",
        text=["VEHICLE"],
        textfont=dict(
            color="#fbbf24",
            size=11
        ),
        showlegend=False,
        hoverinfo="skip"
    ))

    # ======================================================
    # 3D SCENE STYLE
    # ======================================================

    fig.update_layout(
        height=680,
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220",
        font=dict(
            color="#e2e8f0",
            size=11
        ),
        scene=dict(
            bgcolor="#0b1220",
            xaxis=dict(
                title="BRIDGE LENGTH (m)",
                range=[-1, 31],
                backgroundcolor="#0b1220",
                gridcolor="#334155",
                zerolinecolor="#475569"
            ),
            yaxis=dict(
                title="BRIDGE WIDTH (m)",
                range=[-3, 3],
                backgroundcolor="#0b1220",
                gridcolor="#334155",
                zerolinecolor="#475569"
            ),
            zaxis=dict(
                title="HEIGHT (m)",
                range=[0, 13],
                backgroundcolor="#0b1220",
                gridcolor="#334155",
                zerolinecolor="#475569"
            ),
            aspectratio=dict(
                x=2.5,
                y=0.85,
                z=1.0
            ),
            camera=dict(
                eye=dict(
                    x=1.7,
                    y=-1.8,
                    z=1.2
                )
            )
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        margin=dict(
            l=0,
            r=0,
            t=30,
            b=0
        )
    )

    return fig


# ==========================================================
# FIVE DASHBOARD TABS
# ==========================================================

tab_overview, tab_sensors, tab_change, tab_localization, tab_history = st.tabs([
    "📊 Overview & Bridge",
    "📡 Sensor Network",
    "🔍 Change Detection",
    "📍 Localization",
    "📈 History & Long-Term Trends"
])

# ==========================================================
# TAB 1 - OVERVIEW AND DIGITAL TWIN
# ==========================================================

with tab_overview:

    st.subheader("SYSTEM OVERVIEW")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Maximum bending moment",
        f"{peak_moment:,.0f} Nm"
    )

    c2.metric(
        "Maximum deflection",
        f"{changed_peak:.3f} mm"
    )

    c3.metric(
        "Always-on readings",
        "55"
    )

    c4.metric(
        "Special-attention readings",
        "66" if special_mode else "0"
    )

    st.divider()

    # STATUS
    if special_mode:

        st.warning(
            "🔴 SPECIAL ATTENTION ACTIVE — "
            "Additional sensor channels are reporting."
        )

    else:

        st.success(
            "🟢 NORMAL MONITORING — "
            "Additional sensor channels are on standby."
        )

    st.subheader("🌉 LIVE 3D BRIDGE DIGITAL TWIN")

    st.caption(
        "Drag to rotate • Scroll to zoom • Hover over sensors "
        "to inspect readings"
    )

    bridge_figure = create_bridge()

    st.plotly_chart(
        bridge_figure,
        width="stretch",
        config={
            "scrollZoom": True,
            "displayModeBar": True,
            "displaylogo": False
        }
    )

    # SENSOR LEGEND
    st.markdown("""
    🟢 **Green dots:** Always-on sensor network (55 readings)

    🔴 **Red diamonds:** Additional special-attention network (66 readings)

    🟠 **Orange vehicle:** Movable simulated vehicle
    """)

    st.divider()

    # BRIDGE RESPONSE CHARTS

    left, right = st.columns(2)

    with left:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=x,
            y=moment_envelope,
            mode="lines",
            fill="tozeroy",
            line=dict(
                color="#38bdf8",
                width=3
            ),
            name="Bending moment"
        ))

        fig.update_layout(
            title="BENDING MOMENT DISTRIBUTION",
            xaxis_title="Bridge position (m)",
            yaxis_title="Moment (Nm)",
            height=330,
            paper_bgcolor="#0b1220",
            plot_bgcolor="#17243a",
            font=dict(color="white")
        )

        st.plotly_chart(fig, width="stretch")

    with right:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=x,
            y=current_envelope * 1000,
            mode="lines",
            fill="tozeroy",
            line=dict(
                color="#22c55e",
                width=3
            ),
            name="Current deflection"
        ))

        fig.update_layout(
            title="BRIDGE DEFLECTION PROFILE",
            xaxis_title="Bridge position (m)",
            yaxis_title="Deflection (mm)",
            height=330,
            paper_bgcolor="#0b1220",
            plot_bgcolor="#17243a",
            font=dict(color="white")
        )

        st.plotly_chart(fig, width="stretch")


# ==========================================================
# TAB 2 - SENSOR NETWORK
# ==========================================================

with tab_sensors:

    st.subheader("📡 SENSOR NETWORK")

    st.write(
        "Five continuously reporting sensor types "
        "at 11 stations = **55 always-on readings**."
    )

    normal_table = {
        "Station (m)": np.round(sensor_positions, 1)
    }

    normal_table.update(normal_data)

    st.dataframe(
        normal_table,
        width="stretch",
        hide_index=True,
        height=360
    )

    normal_chart = go.Figure()

    normal_chart.add_trace(go.Scatter(
        x=sensor_positions,
        y=deflection_mm,
        mode="lines+markers",
        name="Deflection (mm)"
    ))

    normal_chart.add_trace(go.Scatter(
        x=sensor_positions,
        y=vibration_index,
        mode="lines+markers",
        name="Vibration index"
    ))

    normal_chart.add_trace(go.Scatter(
        x=sensor_positions,
        y=traffic_load_index / 20,
        mode="lines+markers",
        name="Load index ÷ 20"
    ))

    normal_chart.update_layout(
        title="ALWAYS-ON SENSOR PATTERNS",
        xaxis_title="Bridge position (m)",
        yaxis_title="Reading / visual scale",
        height=350,
        paper_bgcolor="#0b1220",
        plot_bgcolor="#17243a",
        font=dict(color="white")
    )

    st.plotly_chart(normal_chart, width="stretch")

    st.divider()

    st.subheader("ADDITIONAL SPECIAL-ATTENTION SENSORS")

    if special_mode:

        st.warning(
            "ACTIVE: 6 additional sensor types "
            "at 11 stations = 66 additional readings."
        )

        special_table = {
            "Station (m)": np.round(sensor_positions, 1)
        }

        special_table.update(special_data)

        st.dataframe(
            special_table,
            width="stretch",
            hide_index=True,
            height=360
        )

        special_chart = go.Figure()

        special_chart.add_trace(go.Scatter(
            x=sensor_positions,
            y=tilt_degrees,
            mode="lines+markers",
            name="Tilt proxy"
        ))

        special_chart.add_trace(go.Scatter(
            x=sensor_positions,
            y=crack_width_proxy,
            mode="lines+markers",
            name="Crack-width proxy"
        ))

        special_chart.add_trace(go.Scatter(
            x=sensor_positions,
            y=joint_displacement_mm,
            mode="lines+markers",
            name="Joint displacement"
        ))

        special_chart.update_layout(
            title="SPECIAL-ATTENTION SENSOR PATTERNS",
            xaxis_title="Bridge position (m)",
            yaxis_title="Modeled indicator",
            height=350,
            paper_bgcolor="#0b1220",
            plot_bgcolor="#17243a",
            font=dict(color="white")
        )

        st.plotly_chart(special_chart, width="stretch")

    else:

        st.info(
            "STANDBY: Additional sensor types are not "
            "collecting special-mode readings."
        )

    st.caption(
        "Non-deflection channels are educational simulated "
        "indicators, not calibrated physical measurements."
    )


# ==========================================================
# TAB 3 - CHANGE DETECTION
# ==========================================================

with tab_change:

    st.subheader("🔍 STRUCTURAL CHANGE DETECTION")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Baseline peak",
        f"{baseline_peak:.3f} mm"
    )

    c2.metric(
        "Current peak",
        f"{changed_peak:.3f} mm"
    )

    c3.metric(
        "Response increase",
        f"{response_increase:.1f}%"
    )

    st.divider()

    st.write(
        f"Deflection attention trigger: **{trigger:.2f} mm**"
    )

    st.write(
        f"Stations exceeding trigger: "
        f"**{int(np.sum(sensor_attention))} of 11**"
    )

    if persistent_change and np.any(sensor_attention):

        st.warning(
            "PERSISTENT CHANGE DETECTED — SPECIAL ATTENTION ACTIVE"
        )

    elif persistent_change:

        st.warning(
            "PERSISTENT CHANGE DETECTED — SPECIAL ATTENTION ACTIVE"
        )

    elif np.any(sensor_attention):

        st.warning(
            "SENSOR ATTENTION ACTIVE — "
            "PERSISTENT CHANGE NOT CONFIRMED"
        )

    else:

        st.success(
            "NORMAL MODE — SPECIAL-ATTENTION SENSORS ON STANDBY"
        )

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=["Original bridge", "Changed bridge"],
        y=[baseline_peak, changed_peak],
        text=[
            f"{baseline_peak:.3f} mm",
            f"{changed_peak:.3f} mm"
        ],
        textposition="outside",
        marker_color=["#38bdf8", "#f97316"]
    ))

    fig.update_layout(
        title="BASELINE VS CHANGED BRIDGE RESPONSE",
        yaxis_title="Maximum deflection (mm)",
        height=350,
        paper_bgcolor="#0b1220",
        plot_bgcolor="#17243a",
        font=dict(color="white")
    )

    st.plotly_chart(fig, width="stretch")

    sensor_plot = go.Figure()

    sensor_plot.add_trace(go.Bar(
        x=sensor_positions,
        y=deflection_mm,
        name="Deflection",
        marker_color="#38bdf8"
    ))

    sensor_plot.add_hline(
        y=trigger,
        line_dash="dash",
        line_color="red",
        annotation_text="Attention trigger"
    )

    sensor_plot.update_layout(
        title="ALWAYS-ON DEFLECTION STATIONS",
        xaxis_title="Station (m)",
        yaxis_title="Deflection (mm)",
        height=350,
        paper_bgcolor="#0b1220",
        plot_bgcolor="#17243a",
        font=dict(color="white")
    )

    st.plotly_chart(sensor_plot, width="stretch")

    st.caption(
        "The persistent-change criterion is a modeled "
        "5% response increase, not an engineering inspection rule."
    )


# ==========================================================
# TAB 4 - LOCALIZATION
# ==========================================================

with tab_localization:

    st.subheader("📍 STRUCTURAL CHANGE LOCALIZATION")

    st.write(
        "Illustrative sensor-response pattern around "
        "the selected location."
    )

    local_signal = local_reduction * local_shape

    nearest_index = int(np.argmax(local_signal))

    nearest_position = float(
        sensor_positions[nearest_index]
    )

    loc_fig = go.Figure()

    loc_fig.add_trace(go.Bar(
        x=[f"{p:.1f} m" for p in sensor_positions],
        y=local_signal,
        marker_color=[
            "#ef4444" if i == nearest_index else "#22c55e"
            for i in range(len(sensor_positions))
        ]
    ))

    loc_fig.update_layout(
        title="ILLUSTRATIVE LOCAL SENSOR SIGNAL",
        xaxis_title="Sensor station",
        yaxis_title="Signal strength (%)",
        height=350,
        paper_bgcolor="#0b1220",
        plot_bgcolor="#17243a",
        font=dict(color="white")
    )

    st.plotly_chart(loc_fig, width="stretch")

    st.info(
        f"Strongest modeled response: "
        f"station at {nearest_position:.1f} m."
    )

    st.caption(
        "This Gaussian pattern is an educational "
        "demonstration, not a verified crack-location algorithm."
    )


# ==========================================================
# TAB 5 - HISTORY AND LONG-TERM TRENDS
# ==========================================================

with tab_history:

    st.subheader("📈 BRIDGE HISTORY & LONG-TERM TRENDS")

    st.write(
        "Save simulation snapshots and compare "
        "different structural scenarios."
    )

    if "bridge_history" not in st.session_state:

        st.session_state.bridge_history = []

    if st.button(
        "💾 Save Current Simulation Reading",
        key="save_history"
    ):

        st.session_state.bridge_history.append({

            "Saved at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "Vehicle weight (N)": int(weight),

            "Vehicle position (m)": float(vehicle_position),

            "Axles": int(axles),

            "Axle spacing (m)": float(spacing),

            "Stiffness reduction (%)": int(stiffness_change),

            "Baseline deflection (mm)": round(
                baseline_peak, 3
            ),

            "Current deflection (mm)": round(
                changed_peak, 3
            ),

            "Response increase (%)": round(
                response_increase, 1
            ),

            "Special mode": bool(special_mode),

            "Always-on alerts": int(
                np.sum(sensor_attention)
            )
        })

        st.success(
            "Simulation snapshot saved in this session."
        )

    history = st.session_state.bridge_history

    if history:

        st.metric(
            "Saved snapshots",
            len(history)
        )

        hist_fig = go.Figure()

        hist_fig.add_trace(go.Scatter(
            x=[r["Saved at"] for r in history],
            y=[
                r["Baseline deflection (mm)"]
                for r in history
            ],
            mode="lines+markers",
            name="Baseline"
        ))

        hist_fig.add_trace(go.Scatter(
            x=[r["Saved at"] for r in history],
            y=[
                r["Current deflection (mm)"]
                for r in history
            ],
            mode="lines+markers",
            name="Current"
        ))

        hist_fig.update_layout(
            title="SAVED SIMULATION RESPONSE HISTORY",
            xaxis_title="Saved snapshot",
            yaxis_title="Deflection (mm)",
            height=350,
            paper_bgcolor="#0b1220",
            plot_bgcolor="#17243a",
            font=dict(color="white")
        )

        st.plotly_chart(hist_fig, width="stretch")

        st.dataframe(
            history,
            width="stretch",
            hide_index=True,
            height=280
        )

        buffer = io.StringIO()

        writer = csv.DictWriter(
            buffer,
            fieldnames=list(history[0].keys())
        )

        writer.writeheader()
        writer.writerows(history)

        st.download_button(
            "⬇️ Download History CSV",
            buffer.getvalue(),
            file_name="bridge_history.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "No snapshots saved yet. Change the settings "
            "and click Save Current Simulation Reading."
        )

    st.caption(
        "Session history may clear when the app restarts. "
        "Download CSV to preserve records."
    )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "INTELLIGENT BRIDGE MONITORING SYSTEM | "
    "Educational digital-twin simulation. "
    "Simplified beam mechanics and modeled sensor indicators; "
    "not a real bridge measurement or certified safety system."
)
