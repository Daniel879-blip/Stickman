import streamlit as st

st.set_page_config(
    page_title="Level 3 Stickman Juggle",
    page_icon="⚽",
    layout="centered"
)

# ---------------------- SIDEBAR ----------------------
st.sidebar.title("⚙️ Controls")
mode = st.sidebar.selectbox("Mode", ["Day Mode", "Night Mode"])
st.sidebar.markdown("---")

st.sidebar.title("⚽ Game Settings")
gravity = st.sidebar.slider("Gravity Strength", 0.1, 1.2, 0.45)
ball_bounce = st.sidebar.slider("Bounce Force", 5, 20, 12)
stickman_speed = st.sidebar.slider("Stickman Speed", 3, 15, 7)
st.sidebar.markdown("---")

st.sidebar.title("🎨 Appearance")
crowd = st.sidebar.toggle("Show Crowd Animation", True)
lights = st.sidebar.toggle("Show Stadium Lights", True)

# ---------------------- BACKGROUND ----------------------
bg_day = "https://i.imgur.com/1eT8O4u.jpeg"
bg_night = "https://i.imgur.com/3OzN6Eq.jpeg"
background = bg_day if mode == "Day Mode" else bg_night

# ---------------------- CSS & JS ----------------------
st.markdown(f"""
<style>
body {{
    background: url('{background}');
    background-size: cover;
    overflow: hidden;
}}

#stickman {{
    position: absolute;
    top: 60vh;
    left: 45vw;
    width: 80px;
    height: 160px;
    transform: translate(-50%, -50%);
}}

.head {{
    width: 50px;
    height: 50px;
    border: 4px solid black;
    border-radius: 50%;
    background: white;
    margin-left: 15px;
}}

.body {{
    width: 4px;
    height: 70px;
    background: black;
    margin-left: 38px;
}}

.arm {{
    width: 50px;
    height: 4px;
    background: black;
    margin-top: -50px;
}}

.left-arm {{
    margin-left: -10px;
    transform: rotate(20deg);
}}

.right-arm {{
    margin-left: 38px;
    transform: rotate(-20deg);
}}

.leg {{
    width: 4px;
    height: 70px;
    background: black;
    margin-top: -10px;
}}

.left-leg {{
    margin-left: 28px;
    transform: rotate(10deg);
}}

.right-leg {{
    margin-left: 44px;
    transform: rotate(-10deg);
}}

#ball {{
    position: absolute;
    top: 20vh;
    left: 50vw;
    width: 45px;
    height: 45px;
    border-radius: 50%;
    background: radial-gradient(circle, white 40%, black 90%);
}}

.score {{
    position: absolute;
    top: 5vh;
    left: 50%;
    transform: translateX(-50%);
    font-size: 40px;
    font-weight: 800;
    color: yellow;
    text-shadow: 2px 2px 6px black;
}}

.crowd {{
    position: absolute;
    bottom: 0px;
    width: 100%;
    height: 120px;
    background: repeating-linear-gradient(
        45deg,
        #111,
        #111 10px,
        #222 10px,
        #222 20px
    );
    animation: wave 2s infinite ease-in-out;
}}

@keyframes wave {{
    0%   {{ transform: translateX(0px); }}
    50%  {{ transform: translateX(-25px); }}
    100% {{ transform: translateX(0px); }}
}}

.lights {{
    position: absolute;
    top: 5vh;
    right: 5vw;
    width: 160px;
    height: 160px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,200,0.8), transparent);
    animation: blink 1.5s infinite;
}}

@keyframes blink {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.4; }}
}}
</style>
""", unsafe_allow_html=True)

# ---------------------- HTML/JS PHYSICS ----------------------
st.markdown(f"""
<div id="stickman">
    <div class="head"></div>
    <div class="body"></div>
    <div class="arm left-arm"></div>
    <div class="arm right-arm"></div>
    <div class="leg left-leg"></div>
    <div class="leg right-leg"></div>
</div>

<div id="ball"></div>
<div class="score" id="score">0</div>

{('<div class="crowd"></div>' if crowd else '')}
{('<div class="lights"></div>' if lights else '')}

<script>
let ball = document.getElementById("ball");
let stick = document.getElementById("stickman");
let scoreEl = document.getElementById("score");

let x = window.innerWidth / 2;
let y = 200;
let vx = 2;
let vy = 0;

let score = 0;

document.addEventListener("keydown", function(e) {{
    let left = stick.offsetLeft;
    if (e.key === "ArrowLeft") stick.style.left = (left - {stickman_speed}) + "px";
    if (e.key === "ArrowRight") stick.style.left = (left + {stickman_speed}) + "px";
}});

function physics() {{
    vy += {gravity};
    x += vx;
    y += vy;

    if (x <= 0 || x >= window.innerWidth - 50) vx *= -1;
    if (y >= window.innerHeight - 80) {{
        vy = -{ball_bounce};
    }}

    let stickTop = stick.offsetTop - 50;
    let stickLeft = stick.offsetLeft;
    let stickRight = stickLeft + 80;

    if (y > stickTop && y < stickTop + 50 && x > stickLeft && x < stickRight) {{
        vy = -{ball_bounce};
        score++;
        scoreEl.innerHTML = score;
    }}

    ball.style.left = x + "px";
    ball.style.top = y + "px";

    requestAnimationFrame(physics);
}}

physics();
</script>
""", unsafe_allow_html=True)
