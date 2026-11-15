
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io

# ============================================================
# INTELLIGENT BRIDGE MONITORING — SINGLE DASHBOARD
# ============================================================

st.set_page_config(
    page_title="Intelligent Bridge Monitoring",
    page_icon="🌉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- DESIGN --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: linear-gradient(145deg, #02050B 0%, #07152E 55%, #0B1C3C 100%);
    color: #E9F7FE;
}
.block-container {
    max-width: 1600px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}
h1, h2, h3 {
    color: #E9F7FE !important;
}
.metric-card {
    background: linear-gradient(135deg, #0F2158, #102D65);
    border: 1px solid #3255BA;
    border-radius: 13px;
    padding: 15px 18px;
    min-height: 95px;
}
.metric-label {
    color: #9CBEF5;
    font-size: 12px;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.metric-value {
    color: #FFFFFF;
    font-size: 27px;
    font-weight: 800;
    margin-top: 5px;
}
.metric-note {
    color: #9CBEF5;
    font-size: 11px;
}
.panel {
    background: rgba(15, 33, 88, 0.72);
    border: 1px solid rgba(91, 125, 210, 0.45);
    border-radius: 14px;
    padding: 16px;
}
.small-label {
    color: #9CBEF5;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.status-good {
    color: #45E59B;
    font-weight: 700;
}
.status-alert {
    color: #FF6565;
    font-weight: 700;
}
div[data-testid="stSlider"] label,
div[data-testid="stNumberInput"] label {
    color: #C7D9FA !important;
}
.stButton button {
    background: #3255BA;
    color: white;
    border: 1px solid #7194F0;
    border-radius: 8px;
}
hr {
    border-color: #263D73;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------

st.markdown("""
<div style="display:flex;justify-content:space-between;align-items:center;
padding:8px 4px 18px 4px;">
  <div>
    <div style="font-size:12px;color:#9CBEF5;letter-spacing:3px;">
      STRUCTURAL HEALTH DIGITAL TWIN
    </div>
    <div style="font-size:30px;font-weight:800;color:#E9F7FE;">
      🌉 INTELLIGENT BRIDGE MONITORING
    </div>
    <div style="color:#8791A4;font-size:12px;">
      Continuous sensing · Event-triggered adaptive attention · Structural change detection
    </div>
  </div>
  <div style="text-align:right;">
    <div style="color:#45E59B;font-weight:700;">● SYSTEM ONLINE</div>
    <div style="color:#9CBEF5;font-size:12px;">SIMULATION ENVIRONMENT</div>
  </div>
</div>
""", unsafe_allow_html=True)

# -------------------- CONTROLS --------------------

with st.expander("⚙️ SIMULATION CONTROLS", expanded=True):
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        vehicle_weight = st.slider(
            "Vehicle weight (N)", 5000, 50000, 20000, 1000
        )
        vehicle_position = st.slider(
            "Vehicle position (m)", 0.0, 30.0, 15.0, 0.5
        )

    with c2:
        axle_count = st.selectbox("Number of axles", [2, 3, 4, 5], index=1)
        axle_spacing = st.slider(
            "Axle spacing (m)", 1.0, 5.0, 2.5, 0.5
        )

    with c3:
        trigger_threshold = st.slider(
            "Attention trigger (mm)", 0.1, 5.0, 1.0, 0.1
        )
        stiffness_change = st.slider(
            "Simulated stiffness reduction (%)", 0, 40, 0, 1
        )

    with c4:
        change_location = st.slider(
            "Change location (m)", 2.0, 28.0, 15.0, 0.5
        )
        local_change = st.slider(
            "Local change signal (%)", 0, 50, 0, 1
        )

# -------------------- BRIDGE MODEL --------------------

L = 30.0
E = 200e9
I = 0.08
x = np.linspace(0, L, 401)
stations = np.linspace(2, 28, 11)

def beam_response(position, inertia):
    """Simplified educational simply-supported beam response."""
    moment = np.zeros_like(x)
    deflection = np.zeros_like(x)

    axle_positions = [
        position - i * axle_spacing for i in range(axle_count)
    ]
    axle_positions = [
        p for p in axle_positions if 0 <= p <= L
    ]

    if not axle_positions:
        return moment, deflection

    axle_load = vehicle_weight / axle_count
    total_reaction = sum(
        axle_load * (L - p) / L for p in axle_positions
    )

    for j, xx in enumerate(x):
        m = total_reaction * xx
        for p in axle_positions:
            if xx >= p:
                m -= axle_load * (xx - p)
        moment[j] = m

    # Numerical integration of curvature
    curvature = moment / (E * inertia)
    slope = np.zeros_like(x)
    deflection = np.zeros_like(x)
    dx = x[1] - x[0]

    for j in range(1, len(x)):
        slope[j] = slope[j-1] + (
            curvature[j] + curvature[j-1]
        ) * dx / 2
        deflection[j] = deflection[j-1] + (
            slope[j] + slope[j-1]
        ) * dx / 2

    # Remove end drift to approximate simple supports
    deflection -= np.linspace(0, deflection[-1], len(x))
    return moment, deflection

baseline_moment, baseline_deflection = beam_response(vehicle_position, I)

inertia_factor = max(0.5, 1 - stiffness_change / 100)
changed_moment, changed_deflection = beam_response(
    vehicle_position, I * inertia_factor
)

# Localized simulated change
local_effect = (
    local_change / 100
) * np.exp(-((x - change_location) / 3.0) ** 2)

changed_deflection = changed_deflection * (1 + local_effect)

peak_deflection = float(np.max(np.abs(changed_deflection)) * 1000)
peak_moment = float(np.max(np.abs(changed_moment)))
baseline_peak = float(np.max(np.abs(baseline_deflection)) * 1000)

response_change = (
    (peak_deflection - baseline_peak) / max(baseline_peak, 0.001)
) * 100

# -------------------- SENSOR DATA --------------------

sensor_rows = []

for i, position in enumerate(stations):
    idx = np.argmin(np.abs(x - position))

    d = abs(changed_deflection[idx]) * 1000
    m = abs(changed_moment[idx])
    strain = m / (E * I) * 1000000
    vibration = min(100, 10 + d * 15 + vehicle_weight / 2500)
    temperature = 24 + 2 * np.sin(position / 5)
    traffic = min(100, vehicle_weight / 500)

    readings = [
        ("Deflection", d, "mm"),
        ("Strain proxy", strain, "με"),
        ("Vibration index", vibration, "%"),
        ("Temperature", temperature, "°C"),
        ("Traffic/load index", traffic, "%")
    ]

    for channel, value, unit in readings:
        sensor_rows.append({
            "Station": i + 1,
            "Position (m)": position,
            "Channel": channel,
            "Reading": value,
            "Unit": unit
        })

primary_df = pd.DataFrame(sensor_rows)

persistent_change = (
    stiffness_change >= 5 or local_change >= 5
)

special_mode = (
    peak_deflection >= trigger_threshold
    or persistent_change
)

special_rows = []

special_channels = [
    "Tilt proxy",
    "Humidity",
    "Corrosion indicator",
    "Crack-width proxy",
    "Acoustic activity",
    "Joint displacement"
]

for i, position in enumerate(stations):
    for j, channel in enumerate(special_channels):
        # Illustrative simulated readings
        value = (
            (local_change * 0.08)
            + (stiffness_change * 0.05)
            + (i + 1) * 0.12
            + j * 0.3
        )
        special_rows.append({
            "Station": i + 1,
            "Position (m)": position,
            "Channel": channel,
            "Reading": value
        })

special_df = pd.DataFrame(special_rows)

# -------------------- TOP METRICS --------------------

m1, m2, m3, m4, m5 = st.columns(5)

def metric_card(column, label, value, note):
    column.markdown(f"""
    <div class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-value">{value}</div>
      <div class="metric-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)

metric_card(m1, "Peak deflection", f"{peak_deflection:.3f} mm",
            "Maximum simulated bending")
metric_card(m2, "Peak bending moment", f"{peak_moment:,.0f} Nm",
            "Simplified beam model")
metric_card(m3, "Always-on sensors", "55",
            "5 channels × 11 stations")
metric_card(m4, "Special sensors", "66",
            "6 channels × 11 stations")
metric_card(m5, "Response change", f"{response_change:+.1f}%",
            "Compared with baseline")

st.write("")

# -------------------- MAIN BRIDGE VIEW --------------------

left, center, right = st.columns([1.05, 3.8, 1.15], gap="medium")

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### CONTROL CENTER")
    st.markdown('<div class="small-label">Vehicle simulation</div>',
                unsafe_allow_html=True)
    st.metric("Vehicle load", f"{vehicle_weight:,} N")
    st.metric("Vehicle location", f"{vehicle_position:.1f} m")
    st.metric("Axles", axle_count)

    st.divider()
    st.markdown('<div class="small-label">Monitoring network</div>',
                unsafe_allow_html=True)
    st.markdown("🟢 **55** Always-on sensors")
    st.markdown("🔴 **66** Adaptive sensors")
    st.markdown("📡 **11** Sensor stations")
    st.markdown("📊 **5** Primary channels")
    st.markdown('</div>', unsafe_allow_html=True)

with center:
    st.markdown("### 3D BRIDGE DIGITAL TWIN")

    fig = go.Figure()

    # Water surface
    fig.add_trace(go.Surface(
        x=[0, 30],
        y=[-12, 12],
        z=[[0, 0], [0, 0]],
        colorscale=[
            [0, "#0A3970"],
            [0.5, "#12619A"],
            [1, "#1A80B5"]
        ],
        opacity=0.48,
        showscale=False,
        hoverinfo="skip",
        name="Water"
    ))

    # Bridge deck
    deck_z = 5.0
    for ydeck in [-1.5, 1.5]:
        fig.add_trace(go.Scatter3d(
            x=x, y=np.full_like(x, ydeck),
            z=np.full_like(x, deck_z),
            mode="lines",
            line=dict(color="#D8E7F6", width=7),
            hoverinfo="skip",
            showlegend=False
        ))

    # Deck surface
    fig.add_trace(go.Mesh3d(
        x=[0, 30, 30, 0],
        y=[-1.5, -1.5, 1.5, 1.5],
        z=[deck_z, deck_z, deck_z, deck_z],
        i=[0, 0], j=[1, 2], k=[2, 3],
        color="#8791A4",
        opacity=0.9,
        name="Bridge deck",
        hoverinfo="skip"
    ))

    # Main towers
    tower_positions = [10, 20]
    for tx in tower_positions:
        for ty in [-0.7, 0.7]:
            fig.add_trace(go.Scatter3d(
                x=[tx, tx],
                y=[ty, ty],
                z=[deck_z, 17],
                mode="lines",
                line=dict(color="#E9F7FE", width=10),
                hoverinfo="skip",
                showlegend=False
            ))

        # Tower cross beam
        fig.add_trace(go.Scatter3d(
            x=[tx, tx],
            y=[-0.8, 0.8],
            z=[14, 14],
            mode="lines",
            line=dict(color="#9CBEF5", width=7),
            hoverinfo="skip",
            showlegend=False
        ))

        # Cable stays on both sides of tower
        for side in [-1, 1]:
            for anchor_x in np.linspace(
                max(0, tx - 9), min(30, tx + 9), 10
            ):
                if abs(anchor_x - tx) < 0.4:
                    continue
                anchor_y = side * 1.45
                fig.add_trace(go.Scatter3d(
                    x=[tx, anchor_x],
                    y=[side * 0.7, anchor_y],
                    z=[17, deck_z],
                    mode="lines",
                    line=dict(color="#B8D7F4", width=2),
                    hoverinfo="skip",
                    showlegend=False
                ))

    # Under-deck piers
    for px_pos in [5, 15, 25]:
        fig.add_trace(go.Scatter3d(
            x=[px_pos, px_pos],
            y=[0, 0],
            z=[0.2, deck_z],
            mode="lines",
            line=dict(color="#A7B8D0", width=9),
            hoverinfo="skip",
            showlegend=False
        ))

    # Green primary sensors: 55 total
    sensor_x, sensor_y, sensor_z = [], [], []
    sensor_hover = []

    for station_index, position in enumerate(stations):
        for channel_index in range(5):
            sensor_x.append(position)
            sensor_y.append(
                [-1.2, -0.6, 0, 0.6, 1.2][channel_index]
            )
            sensor_z.append(deck_z + 0.12 + channel_index * 0.025)
            sensor_hover.append(
                f"Station {station_index + 1}<br>"
                f"{primary_df.iloc[station_index * 5 + channel_index]['Channel']}<br>"
                f"Position: {position:.1f} m"
            )

    fig.add_trace(go.Scatter3d(
        x=sensor_x, y=sensor_y, z=sensor_z,
        mode="markers",
        marker=dict(
            size=5,
            color="#39F58A",
            line=dict(color="#D8FFE8", width=1),
            opacity=1
        ),
        text=sensor_hover,
        hovertemplate="%{text}<extra>Always-on sensor</extra>",
        name="55 Always-on sensors"
    ))

    # Red special-attention sensors: 66 total
    if special_mode:
        red_x, red_y, red_z, red_hover = [], [], [], []

        for station_index, position in enumerate(stations):
            for channel_index in range(6):
                red_x.append(position)
                red_y.append(
                    [-1.35, -0.8, -0.25, 0.25, 0.8, 1.35][channel_index]
                )
                red_z.append(deck_z + 0.35 + channel_index * 0.035)
                red_hover.append(
                    f"Station {station_index + 1}<br>"
                    f"{special_channels[channel_index]}<br>"
                    f"Position: {position:.1f} m"
                )

        fig.add_trace(go.Scatter3d(
            x=red_x, y=red_y, z=red_z,
            mode="markers",
            marker=dict(
                size=5,
                color="#FF4B5C",
                line=dict(color="#FFE0E3", width=1),
                opacity=1
            ),
            text=red_hover,
            hovertemplate="%{text}<extra>Special-attention sensor</extra>",
            name="66 Special-attention sensors"
        ))

    # Moving vehicle marker
    fig.add_trace(go.Scatter3d(
        x=[vehicle_position],
        y=[0],
        z=[deck_z + 0.7],
        mode="markers+text",
        marker=dict(
            size=11,
            color="#FFD166",
            symbol="diamond",
            line=dict(color="white", width=2)
        ),
        text=["VEHICLE"],
        textposition="top center",
        name="Moving vehicle",
        hovertemplate="Vehicle position: %{x:.1f} m<extra></extra>"
    ))

    # Bridge layout
    fig.update_layout(
        height=610,
        margin=dict(l=0, r=0, t=5, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E9F7FE"),
        legend=dict(
            orientation="h",
            y=1.02,
            x=0,
            bgcolor="rgba(2,5,11,0.5)",
            font=dict(size=10)
        ),
        scene=dict(
            bgcolor="rgba(2,5,11,0)",
            xaxis=dict(
                title="Bridge length (m)",
                range=[-1, 31],
                color="#9CBEF5",
                gridcolor="#263D73",
                zerolinecolor="#263D73"
            ),
            yaxis=dict(
                title="Width",
                range=[-12, 12],
                color="#9CBEF5",
                gridcolor="#263D73"
            ),
            zaxis=dict(
                title="Height",
                range=[0, 19],
                color="#9CBEF5",
                gridcolor="#263D73"
            ),
            aspectratio=dict(x=2.4, y=1.0, z=0.9),
            camera=dict(
                eye=dict(x=1.7, y=-2.1, z=1.25)
            )
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "scrollZoom": True,
            "displaylogo": False
        }
    )

    st.caption(
        "Drag to rotate · Scroll to zoom · Hover over sensor markers "
        "to inspect their station and channel."
    )

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### SYSTEM STATUS")

    if special_mode:
        st.markdown(
            '<div class="status-alert">● SPECIAL ATTENTION ACTIVE</div>',
            unsafe_allow_html=True
        )
        st.write("Additional sensor channels are activated.")
    else:
        st.markdown(
            '<div class="status-good">● NORMAL MONITORING</div>',
            unsafe_allow_html=True
        )
        st.write("Primary sensors are continuously monitoring.")

    st.divider()
    st.markdown("**Detection summary**")

    if persistent_change:
        st.warning("Persistent-change signal simulated")
    elif special_mode:
        st.info("Response threshold reached")
    else:
        st.success("No simulated persistent change")

    st.metric("Deflection trigger", f"{trigger_threshold:.2f} mm")
    st.metric("Measured peak", f"{peak_deflection:.3f} mm")
    st.metric("Stiffness reduction", f"{stiffness_change}%")
    st.metric("Local change signal", f"{local_change}%")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- LOWER INFORMATION PANELS --------------------

st.write("")
st.markdown("## STRUCTURAL RESPONSE ANALYSIS")

chart_left, chart_right = st.columns(2, gap="medium")

with chart_left:
    response_fig = go.Figure()
    response_fig.add_trace(go.Scatter(
        x=x,
        y=baseline_deflection * 1000,
        mode="lines",
        name="Baseline",
        line=dict(color="#53A7FF", width=2)
    ))
    response_fig.add_trace(go.Scatter(
        x=x,
        y=changed_deflection * 1000,
        mode="lines",
        name="Current simulated response",
        line=dict(color="#FFB84D", width=3)
    ))
    response_fig.update_layout(
        title="Bridge deflection profile",
        xaxis_title="Bridge position (m)",
        yaxis_title="Deflection (mm)",
        height=330,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(7,21,46,0.8)",
        font=dict(color="#E9F7FE"),
        legend=dict(orientation="h", y=1.12),
        margin=dict(l=15, r=15, t=55, b=25)
    )
    st.plotly_chart(response_fig, use_container_width=True)

with chart_right:
    moment_fig = go.Figure()
    moment_fig.add_trace(go.Scatter(
        x=x,
        y=baseline_moment,
        mode="lines",
        name="Bending moment",
        line=dict(color="#53A7FF", width=2),
        fill="tozeroy",
        fillcolor="rgba(83,167,255,0.12)"
    ))
    moment_fig.update_layout(
        title="Bending moment distribution",
        xaxis_title="Bridge position (m)",
        yaxis_title="Moment (Nm)",
        height=330,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(7,21,46,0.8)",
        font=dict(color="#E9F7FE"),
        margin=dict(l=15, r=15, t=55, b=25)
    )
    st.plotly_chart(moment_fig, use_container_width=True)

# -------------------- CHANGE DETECTION --------------------

st.markdown("## STRUCTURAL CHANGE DETECTION")

d1, d2, d3 = st.columns(3)

with d1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("**Baseline response**")
    st.metric("Peak deflection", f"{baseline_peak:.3f} mm")
    st.markdown('</div>', unsafe_allow_html=True)

with d2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("**Current response**")
    st.metric("Peak deflection", f"{peak_deflection:.3f} mm")
    st.markdown('</div>', unsafe_allow_html=True)

with d3:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("**Difference from baseline**")
    st.metric("Response difference", f"{response_change:+.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)

if persistent_change:
    st.error(
        "SIMULATED RESULT: Persistent structural-change signal detected. "
        "The model's changed parameters differ from its baseline."
    )
elif special_mode:
    st.warning(
        "SIMULATED RESULT: Temporary response threshold reached. "
        "Additional attention channels are active."
    )
else:
    st.success(
        "SIMULATED RESULT: No persistent structural-change signal "
        "has been introduced in this scenario."
    )

# -------------------- SENSOR TABLES --------------------

st.markdown("## SENSOR NETWORK")

sensor_col1, sensor_col2 = st.columns(2, gap="medium")

with sensor_col1:
    st.markdown("### 🟢 ALWAYS-ON SENSOR READINGS")
    st.dataframe(
        primary_df,
        use_container_width=True,
        hide_index=True,
        height=330
    )

with sensor_col2:
    st.markdown("### 🔴 SPECIAL-ATTENTION SENSOR READINGS")
    if special_mode:
        st.dataframe(
            special_df,
            use_container_width=True,
            hide_index=True,
            height=330
        )
    else:
        st.info(
            "Special-attention channels are simulated as available but "
            "are not active in normal monitoring mode."
        )

# -------------------- LOCALIZATION --------------------

st.markdown("## CHANGE LOCALIZATION")

if persistent_change:
    estimated_location = change_location
    st.warning(
        f"Simulated change location: approximately "
        f"{estimated_location:.1f} m along the bridge."
    )
elif special_mode:
    estimated_location = vehicle_position
    st.info(
        f"Temporary response is associated with the vehicle near "
        f"{estimated_location:.1f} m."
    )
else:
    st.success("No simulated change location to report.")

localization_fig = go.Figure()
localization_fig.add_trace(go.Scatter(
    x=stations,
    y=np.zeros(len(stations)),
    mode="lines+markers",
    line=dict(color="#53A7FF", width=8),
    marker=dict(size=13, color="#39F58A"),
    name="Sensor stations"
))

if special_mode:
    localization_fig.add_trace(go.Scatter(
        x=[estimated_location],
        y=[0],
        mode="markers+text",
        marker=dict(size=19, color="#FF4B5C", symbol="diamond"),
        text=["DETECTION"],
        textposition="top center",
        name="Simulated detection"
    ))

localization_fig.update_layout(
    height=190,
    xaxis_title="Bridge position (m)",
    yaxis=dict(visible=False, range=[-0.5, 0.7]),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(7,21,46,0.8)",
    font=dict(color="#E9F7FE"),
    margin=dict(l=15, r=15, t=15, b=35)
)
st.plotly_chart(localization_fig, use_container_width=True)

# -------------------- HISTORY AND EXPORT --------------------

st.markdown("## HISTORY & LONG-TERM TRENDS")

if "history" not in st.session_state:
    st.session_state.history = []

h1, h2 = st.columns([1, 4])

with h1:
    if st.button("＋ SAVE CURRENT SNAPSHOT", use_container_width=True):
        st.session_state.history.append({
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Vehicle position (m)": vehicle_position,
            "Vehicle weight (N)": vehicle_weight,
            "Peak deflection (mm)": peak_deflection,
            "Peak moment (Nm)": peak_moment,
            "Response change (%)": response_change,
            "Special mode": special_mode,
            "Stiffness reduction (%)": stiffness_change,
            "Local change (%)": local_change
        })
        st.success("Snapshot saved.")

with h2:
    if st.button("CLEAR HISTORY", use_container_width=True):
        st.session_state.history = []
        st.rerun()

if st.session_state.history:
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df, use_container_width=True, hide_index=True)

    history_chart = px.line(
        history_df,
        x="Timestamp",
        y="Peak deflection (mm)",
        markers=True,
        title="Saved peak-deflection snapshots"
    )
    history_chart.update_layout(
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(7,21,46,0.8)",
        font=dict(color="#E9F7FE")
    )
    st.plotly_chart(history_chart, use_container_width=True)

    csv_bytes = history_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇ DOWNLOAD HISTORY CSV",
        data=csv_bytes,
        file_name="bridge_monitoring_history.csv",
        mime="text/csv"
    )
else:
    st.info("No snapshots saved yet. Save a snapshot to begin building history.")

# -------------------- FOOTER --------------------

st.divider()
st.markdown("""
<div style="text-align:center;color:#8791A4;font-size:11px;padding:10px;">
  INTELLIGENT BRIDGE MONITORING · EDUCATIONAL SIMULATION
  <br>
  Simplified beam calculations and illustrative sensor readings.
  Not real bridge measurements or a certified structural-safety system.
</div>
""", unsafe_allow_html=True)
