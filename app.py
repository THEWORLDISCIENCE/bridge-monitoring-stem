
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import csv, io
from datetime import datetime

st.set_page_config(
    page_title="Intelligent Bridge Monitoring",
    page_icon="🌉",
    layout="wide"
)

st.markdown("""
<style>
.block-container {max-width:1250px;padding-top:1rem;}
section[data-testid="stSidebar"] {background:#f1f5f9;}
div[data-testid="stMetric"] {
    background:white;border:1px solid #dbe4ee;
    padding:12px;border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🌉 Intelligent Bridge Monitoring System")
st.caption("Structural response • Continuous sensing • Adaptive attention • Change detection")

L, E, I = 30.0, 200e9, 0.08
x = np.linspace(0, L, 301)
sensor_positions = np.array([5, 10, 15, 20, 25])

# LEFT SIDEBAR: ALL CONTROLS
st.sidebar.header("Vehicle Simulation")
weight = st.sidebar.slider("Vehicle weight (N)", 5000, 100000, 20000, 5000)
axles = st.sidebar.slider("Number of axles", 2, 5, 4)
spacing = st.sidebar.slider("Axle spacing (m)", 2.0, 8.0, 3.0, 0.5)

st.sidebar.header("Adaptive Monitoring")
trigger = st.sidebar.slider("Attention trigger (mm)", 0.1, 5.0, 0.7, 0.1)

st.sidebar.header("Structural Change Experiment")
stiffness_change = st.sidebar.slider("Stiffness reduction (%)", 0, 30, 15, 5)

st.sidebar.header("Localization Demonstration")
local_location = st.sidebar.slider("Simulated change location (m)", 5, 25, 15, 5)
local_reduction = st.sidebar.slider("Local change signal (%)", 5, 30, 15, 5)


# BEAM SIMULATION
def beam_response(vehicle_position, inertia):
    moment = np.zeros_like(x)
    deflection = np.zeros_like(x)
    axle_load = weight / axles

    for i in range(axles):
        a = vehicle_position - i * spacing
        if 0 <= a <= L:
            b = L - a

            moment += np.where(
                x <= a,
                axle_load * b * x / L,
                axle_load * a * (L-x) / L
            )

            left = x <= a
            right = ~left

            deflection[left] += (
                axle_load * b * x[left] *
                (L**2-b**2-x[left]**2)
                / (6*L*E*inertia)
            )

            deflection[right] += (
                axle_load*a*(L-x[right]) *
                (L**2-a**2-(L-x[right])**2)
                / (6*L*E*inertia)
            )

    return moment, deflection


# Compare identical vehicle loading on both bridge conditions
vehicle_positions = np.linspace(-axles*spacing, L, 120)
changed_inertia = I * (1-stiffness_change/100)

moment_envelope = np.zeros_like(x)
baseline_envelope = np.zeros_like(x)
current_envelope = np.zeros_like(x)

for position in vehicle_positions:
    moment, d_base = beam_response(position, I)
    _, d_current = beam_response(position, changed_inertia)

    moment_envelope = np.maximum(moment_envelope, moment)
    baseline_envelope = np.maximum(baseline_envelope, np.abs(d_base))
    current_envelope = np.maximum(current_envelope, np.abs(d_current))

baseline_peak = float(np.max(baseline_envelope)*1000)
changed_peak = float(np.max(current_envelope)*1000)
peak_moment = float(np.max(moment_envelope))
peak_deflection = changed_peak

response_increase = (
    (changed_peak-baseline_peak)/baseline_peak*100
    if baseline_peak else 0
)

# Sensors use the CURRENT changed bridge response
sensor_readings = np.interp(
    sensor_positions, x, current_envelope
)*1000
sensor_attention = sensor_readings > trigger

persistent_change = response_increase >= 5.0

# Simplified location illustration
distances = np.abs(sensor_positions-local_location)
local_signal = local_reduction*np.exp(-(distances**2)/(2*4**2))
detected_index = int(np.argmax(local_signal))
detected_position = int(sensor_positions[detected_index])


# FIVE COMPACT TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview & Bridge",
    "📡 Live Sensors",
    "🔍 Change Detection",
    "📍 Localization",
    "📈 History & Long-Term Trends"
])


# TAB 1: OVERVIEW AND 3D BRIDGE
with tab1:
    st.subheader("Simulation Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Maximum bending moment", f"{peak_moment:,.0f} Nm")
    c2.metric("Maximum deflection", f"{peak_deflection:.3f} mm")
    c3.metric("Sensors needing attention", f"{int(np.sum(sensor_attention))}/5")

    st.subheader("3D Bridge: Sensor Locations")
    st.caption("🔴 Suspected location  •  🔵 Main sensors  •  🟢 Additional sensors")

    fig3d = go.Figure()
    fig3d.add_trace(go.Mesh3d(
        x=[0,30,30,0], y=[-2,-2,2,2], z=[2,2,2,2],
        i=[0,0], j=[1,2], k=[2,3],
        color="lightblue", opacity=0.8, name="Bridge deck"
    ))

    for y_side in [-1.5, 1.5]:
        fig3d.add_trace(go.Scatter3d(
            x=[0,30], y=[y_side,y_side], z=[1.5,1.5],
            mode="lines", line=dict(color="gray",width=8),
            name="Support beam",
            showlegend=(y_side == -1.5)
        ))

    for xpos in [0,30]:
        fig3d.add_trace(go.Scatter3d(
            x=[xpos,xpos], y=[0,0], z=[0,2],
            mode="lines", line=dict(color="gray",width=8),
            name="Bridge support",
            showlegend=(xpos == 0)
        ))

    colors = [
        "red" if i == detected_index else "royalblue"
        for i in range(5)
    ]

    fig3d.add_trace(go.Scatter3d(
        x=sensor_positions, y=[0]*5, z=[2.3]*5,
        mode="markers+text",
        text=[f"S{i+1}" for i in range(5)],
        textposition="top center",
        marker=dict(size=9,color=colors),
        name="Main sensors"
    ))

    fig3d.add_trace(go.Scatter3d(
        x=list(sensor_positions)*2,
        y=[-1.35]*5+[1.35]*5,
        z=[2.18]*10,
        mode="markers",
        marker=dict(size=4,color="green"),
        name="Additional sensors"
    ))

    fig3d.update_layout(
        height=420,
        margin=dict(l=5,r=5,t=25,b=5),
        scene=dict(
            xaxis=dict(title="Length (m)",range=[0,30]),
            yaxis=dict(title="Width",range=[-2.5,2.5]),
            zaxis=dict(title="Height",range=[0,4]),
            aspectratio=dict(x=2.5,y=0.6,z=0.5)
        ),
        legend=dict(orientation="h")
    )
    st.plotly_chart(fig3d,use_container_width=True)

    st.markdown(
        f"🔴 **Suspected change:** Sensor S{detected_index+1} "
        f"at {detected_position} metres"
    )
    st.markdown("🔵 **Blue:** Other main monitoring sensors")
    st.markdown("🟢 **Green:** Additional monitoring sensors")

    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure(go.Scatter(
            x=x,y=moment_envelope,mode="lines"
        ))
        fig.update_layout(
            title="Bending Moment Along Bridge",
            xaxis_title="Position (m)",yaxis_title="Moment (Nm)",
            height=300
        )
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        fig = go.Figure(go.Scatter(
            x=x,y=current_envelope*1000,mode="lines"
        ))
        fig.update_layout(
            title="Bridge Deflection",
            xaxis_title="Position (m)",yaxis_title="Deflection (mm)",
            height=300
        )
        st.plotly_chart(fig,use_container_width=True)


# TAB 2: LIVE SENSORS
with tab2:
    st.subheader("Continuous Sensor Monitoring")
    st.write("Virtual sensors continuously monitor the current simulated bridge response.")

    sensor_status = [
        "INCREASED ATTENTION" if v else "NORMAL"
        for v in sensor_attention
    ]

    st.dataframe({
        "Sensor":[f"S{i+1}" for i in range(5)],
        "Position (m)":sensor_positions,
        "Deflection (mm)":np.round(sensor_readings,3),
        "Status":sensor_status
    },use_container_width=True)

    fig = go.Figure(go.Bar(
        x=sensor_positions,y=sensor_readings,
        name="Current readings"
    ))
    fig.add_hline(
        y=trigger,line_dash="dash",
        annotation_text="Attention trigger"
    )
    fig.update_layout(
        title="Sensor Readings Along Bridge",
        xaxis_title="Sensor position (m)",
        yaxis_title="Deflection (mm)",height=330
    )
    st.plotly_chart(fig,use_container_width=True)

    if np.any(sensor_attention):
        st.warning("ADAPTIVE ATTENTION ACTIVATED")
        st.write("One or more live sensor readings exceeded the selected trigger.")
    else:
        st.success("NO SENSOR TRIGGER")
        st.write("All live sensor readings are below the selected trigger.")


# TAB 3: CHANGE DETECTION
with tab3:
    st.subheader("Persistent Structural Change Detection")
    st.write("The same vehicle loading is compared against the original bridge baseline.")

    a,b,c = st.columns(3)
    a.metric("Original response",f"{baseline_peak:.3f} mm")
    b.metric("Changed response",f"{changed_peak:.3f} mm")
    c.metric("Response increase",f"{response_increase:.1f}%")

    fig = go.Figure(go.Bar(
        x=["Original bridge","Changed bridge"],
        y=[baseline_peak,changed_peak],
        text=[f"{baseline_peak:.3f} mm",f"{changed_peak:.3f} mm"],
        textposition="outside"
    ))
    fig.update_layout(
        title="Baseline vs Changed Bridge",
        yaxis_title="Maximum deflection (mm)",height=330
    )
    st.plotly_chart(fig,use_container_width=True)

    if persistent_change and np.any(sensor_attention):
        st.warning("PERSISTENT CHANGE DETECTED — SENSOR ATTENTION ACTIVATED")
    elif persistent_change:
        st.warning("PERSISTENT CHANGE DETECTED — SENSOR TRIGGER NOT EXCEEDED")
        st.write("The overall baseline comparison detected a change, but no individual sensor crossed the selected absolute trigger.")
    elif np.any(sensor_attention):
        st.warning("SENSOR ATTENTION ACTIVATED — PERSISTENT CHANGE NOT CONFIRMED")
    else:
        st.success("NO ALERT")

    st.caption(
        "Educational simulation using a simplified beam model. "
        "These are not real bridge measurements or certified safety assessments."
    )


# TAB 4: LOCALIZATION
with tab4:
    st.subheader("Structural Change Localization")
    st.write("Illustrative sensor-pattern demonstration around the selected simulated location.")

    fig = go.Figure(go.Bar(
        x=[f"S{i+1} ({sensor_positions[i]} m)" for i in range(5)],
        y=local_signal,
        marker_color=[
            "red" if i == detected_index else "green"
            for i in range(5)
        ]
    ))
    fig.update_layout(
        title="Illustrative Sensor Signal",
        yaxis_title="Signal strength (%)",height=330
    )
    st.plotly_chart(fig,use_container_width=True)

    st.info(
        f"Strongest simulated response: Sensor S{detected_index+1} "
        f"at {detected_position} metres."
    )
    st.caption("Simplified mathematical illustration, not a verified real-world crack locator.")


# TAB 5: HISTORY
with tab5:
    st.subheader("Bridge History & Long-Term Trends")
    st.write("Save simulation snapshots and compare them over time.")

    if "bridge_history" not in st.session_state:
        st.session_state.bridge_history = []

    if st.button("Save Current Reading"):
        st.session_state.bridge_history.append({
            "Saved at":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Vehicle weight (N)":int(weight),
            "Axles":int(axles),
            "Spacing (m)":float(spacing),
            "Stiffness reduction (%)":int(stiffness_change),
            "Baseline (mm)":round(baseline_peak,3),
            "Current (mm)":round(changed_peak,3),
            "Increase (%)":round(response_increase,1),
            "Sensors needing attention":int(np.sum(sensor_attention))
        })
        st.success("Reading saved!")

    history = st.session_state.bridge_history

    if history:
        st.metric("Saved simulation records",len(history))

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[r["Saved at"] for r in history],
            y=[r["Baseline (mm)"] for r in history],
            mode="lines+markers",name="Baseline"
        ))
        fig.add_trace(go.Scatter(
            x=[r["Saved at"] for r in history],
            y=[r["Current (mm)"] for r in history],
            mode="lines+markers",name="Current response"
        ))
        fig.update_layout(
            title="Bridge Response History",
            xaxis_title="Saved simulation",
            yaxis_title="Deflection (mm)",height=330
        )
        st.plotly_chart(fig,use_container_width=True)

        st.dataframe(history,use_container_width=True,height=230)

        output = io.StringIO()
        writer = csv.DictWriter(output,fieldnames=history[0].keys())
        writer.writeheader()
        writer.writerows(history)

        st.download_button(
            "Download History CSV",
            output.getvalue(),
            file_name="bridge_history.csv",
            mime="text/csv"
        )

        if st.button("Clear History"):
            st.session_state.bridge_history = []
            st.rerun()
    else:
        st.info("No readings saved yet. Click Save Current Reading to begin.")

    st.caption(
        "History is stored for this active session. Download the CSV to preserve it "
        "after Colab restarts. These are simulation snapshots, not real sensor records."
    )
