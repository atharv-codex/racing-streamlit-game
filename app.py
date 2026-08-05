import streamlit as st
from streamlit_drawable_canvas import st_canvas
import time
import random

# --- CONFIG ---
st.set_page_config(page_title="Car Racing Game", layout="wide")

# --- INITIALIZE SESSION STATE ---
if "p1" not in st.session_state:
    st.session_state.p1 = {"x": 50, "y": 300, "speed": 5, "color": "red", "laps": 0}
if "p2" not in st.session_state:
    st.session_state.p2 = {"x": 50, "y": 350, "speed": 5, "color": "blue", "laps": 0}
if "ai" not in st.session_state:
    st.session_state.ai = {"x": 50, "y": 250, "speed": 4, "color": "green", "laps": 0}
if "mode" not in st.session_state:
    st.session_state.mode = "1 Player vs AI"
if "running" not in st.session_state:
    st.session_state.running = False

# --- UI ---
st.title("🚗 Car Racing Game")
st.write("Use **WASD** for Player 1 and **Arrow Keys** for Player 2.")

st.session_state.mode = st.radio(
    "Choose Game Mode:",
    ["1 Player vs AI", "2 Player Multiplayer"]
)

start = st.button("Start Game")
stop = st.button("Stop Game")

if start:
    st.session_state.running = True
if stop:
    st.session_state.running = False

# --- CANVAS ---
canvas = st_canvas(
    fill_color="rgba(0,0,0,0)",
    stroke_width=2,
    stroke_color="#000000",
    background_color="#f0f0f0",
    height=500,
    width=800,
    drawing_mode="none",
    key="canvas"
)

# --- MOVEMENT HANDLING ---
def move_player(player, keys):
    if "w" in keys:
        player["y"] -= player["speed"]
    if "s" in keys:
        player["y"] += player["speed"]
    if "a" in keys:
        player["x"] -= player["speed"]
    if "d" in keys:
        player["x"] += player["speed"]

def move_player2(player, keys):
    if "ArrowUp" in keys:
        player["y"] -= player["speed"]
    if "ArrowDown" in keys:
        player["y"] += player["speed"]
    if "ArrowLeft" in keys:
        player["x"] -= player["speed"]
    if "ArrowRight" in keys:
        player["x"] += player["speed"]

def move_ai(ai):
    # Simple AI: moves forward and wiggles slightly
    ai["x"] += ai["speed"]
    ai["y"] += random.choice([-2, -1, 0, 1, 2])

# --- DRAW CARS ---
def draw_car(canvas, car):
    canvas.json_data["objects"].append({
        "type": "rect",
        "left": car["x"],
        "top": car["y"],
        "width": 30,
        "height": 15,
        "fill": car["color"]
    })

# --- GAME LOOP ---
if st.session_state.running:
    keys = st.session_state.get("key_pressed", [])

    # Player 1
    move_player(st.session_state.p1, keys)

    # Player 2 or AI
    if st.session_state.mode == "2 Player Multiplayer":
        move_player2(st.session_state.p2, keys)
    else:
        move_ai(st.session_state.ai)

    # Draw cars
    draw_car(canvas, st.session_state.p1)
    if st.session_state.mode == "2 Player Multiplayer":
        draw_car(canvas, st.session_state.p2)
    else:
        draw_car(canvas, st.session_state.ai)

    # Win condition
    if st.session_state.p1["x"] > 750:
        st.success("🎉 Player 1 Wins!")
        st.session_state.running = False

    if st.session_state.mode == "2 Player Multiplayer":
        if st.session_state.p2["x"] > 750:
            st.success("🎉 Player 2 Wins!")
            st.session_state.running = False
    else:
        if st.session_state.ai["x"] > 750:
            st.error("🤖 AI Wins!")
            st.session_state.running = False

    # Rerun for animation
    time.sleep(0.05)
    st.experimental_rerun()

