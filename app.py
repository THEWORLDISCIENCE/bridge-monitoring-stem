# ===== BRIGHT OUTDOOR ENVIRONMENT =====

st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        180deg,
        #9BD9F5 0%,
        #D7F0FA 35%,
        #EAF5F7 100%
    );
    color: #17324D;
}
h1, h2, h3, p, label {
    color: #17324D !important;
}
.block-container {
    max-width: 1600px;
    padding-top: 1rem;
}
.metric-card {
    background: rgba(255,255,255,0.88);
    border: 1px solid #B5D8E8;
    border-radius: 13px;
    padding: 15px;
}
.panel {
    background: rgba(255,255,255,0.88);
    border: 1px solid #B5D8E8;
    border-radius: 14px;
    padding: 16px;
}
</style>
""", unsafe_allow_html=True)

# ===== ENVIRONMENT FOR THE 3D BRIDGE =====

# Green landscape behind the bridge
land_x = np.linspace(-8, 38, 100)
land_y = np.linspace(-20, 20, 50)
LX, LY = np.meshgrid(land_x, land_y)

land_z = (
    1.2
    + 1.8 * np.exp(-((LX - 3) / 9) ** 2)
    + 2.2 * np.exp(-((LX - 27) / 8) ** 2)
    + 0.5 * np.sin(LX / 4) * np.cos(LY / 5)
)

fig.add_trace(go.Surface(
    x=LX,
    y=LY,
    z=land_z,
    colorscale=[
        [0, "#477C43"],
        [0.4, "#579B4E"],
        [0.75, "#79B95B"],
        [1, "#A3CF76"]
    ],
    showscale=False,
    opacity=1,
    hoverinfo="skip",
    name="Green landscape"
))

# Blue water beneath the bridge
water_x = np.linspace(-5, 35, 100)
water_y = np.linspace(-18, 18, 60)
WX, WY = np.meshgrid(water_x, water_y)

water_z = (
    0.15
    + 0.07 * np.sin(WX * 0.8) * np.cos(WY * 0.7)
)

fig.add_trace(go.Surface(
    x=WX,
    y=WY,
    z=water_z,
    colorscale=[
        [0, "#12618E"],
        [0.35, "#2389B5"],
        [0.7, "#53B5D4"],
        [1, "#9ADDED"]
    ],
    showscale=False,
    opacity=0.94,
    hoverinfo="skip",
    name="Blue water"
))

# Natural daylight sky and clean scene
fig.update_layout(
    paper_bgcolor="#A9DDF4",
    scene=dict(
        bgcolor="#A9DDF4",
        xaxis=dict(
            title="Bridge length (m)",
            color="#23445B",
            gridcolor="rgba(255,255,255,0.35)",
            showbackground=True,
            backgroundcolor="#B9E4F5"
        ),
        yaxis=dict(
            title="Bridge width",
            color="#23445B",
            gridcolor="rgba(255,255,255,0.35)",
            showbackground=True,
            backgroundcolor="#B9E4F5"
        ),
        zaxis=dict(
            title="Height",
            color="#23445B",
            gridcolor="rgba(255,255,255,0.35)",
            showbackground=True,
            backgroundcolor="#B9E4F5"
        ),
        camera=dict(
            eye=dict(x=1.7, y=-2.1, z=1.25)
        )
    )
)
