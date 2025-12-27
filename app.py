
import streamlit as st
import cv2
import numpy as np
import pygame
from snake_game import SnakeGame, Direction
from hand_detector import HandDetector

pygame.init()

st.set_page_config(page_title="Snake Game with Hand Control", layout="wide")
st.title("Snake Game with Hand Gesture Control")

# Instructions
with st.expander("Instructions", expanded=True):
    st.write("""
    - Show your hand to the camera
    - Point your hand in the direction you want the snake to move
    - The snake will follow the direction your hand is pointing
    - Press 'q' to quit (in the original game window)
    - Press 'r' to restart after game over
    """)

# Start/stop button

# Start/stop button
start_game = st.button("Start Game")

# If Start Game is pressed, reset session state for a fresh start
if start_game:
    if 'cap' in st.session_state and st.session_state.cap is not None:
        try:
            st.session_state.cap.release()
        except Exception:
            pass
        st.session_state.cap = None
    st.session_state.detector = HandDetector()
    st.session_state.game = SnakeGame(width=640, height=480)
    st.session_state.running = False

def init_camera():
    for idx in range(2):  # Try first two camera indices
        cap = cv2.VideoCapture(idx)
        cap.set(3, 320)
        cap.set(4, 240)
        if cap.isOpened():
            return cap
        else:
            cap.release()
    return None

if 'cap' not in st.session_state or st.session_state.cap is None or not hasattr(st.session_state.cap, 'isOpened') or not st.session_state.cap.isOpened():
    st.session_state.cap = init_camera()
if 'detector' not in st.session_state:
    st.session_state.detector = HandDetector()
if 'game' not in st.session_state:
    st.session_state.game = SnakeGame(width=640, height=480)
if 'running' not in st.session_state:
    st.session_state.running = False

col1, col2 = st.columns(2)


import time

if start_game or st.session_state.running:
    st.session_state.running = True
    cap = st.session_state.cap
    detector = st.session_state.detector
    game = st.session_state.game

    if cap is None or not cap.isOpened():
        st.error("No available camera found. Please check your camera connection and ensure no other app is using it.")
    else:
        cam_placeholder = col1.empty()
        game_placeholder = col2.empty()
        restart_btn_placeholder = st.empty()

        while st.session_state.running:
            success, img = cap.read()
            if not success or img is None:
                st.error("Failed to read from camera. Make sure your camera is not in use by another app.")
                st.session_state.running = False
                break
            img = cv2.flip(img, 1)
            img = detector.find_hands(img)
            direction_str = detector.get_hand_direction(img)
            if direction_str == 'UP':
                game.change_direction(Direction.UP)
            elif direction_str == 'DOWN':
                game.change_direction(Direction.DOWN)
            elif direction_str == 'LEFT':
                game.change_direction(Direction.LEFT)
            elif direction_str == 'RIGHT':
                game.change_direction(Direction.RIGHT)
            game.play_step()
            # Convert game surface to image
            game_img = pygame.surfarray.array3d(game.surface)
            game_img = np.transpose(game_img, (1, 0, 2))
            # Show both camera and game side by side
            cam_placeholder.image(img, channels="BGR", caption="Camera Feed")
            game_placeholder.image(game_img, channels="RGB", caption="Snake Game")
            if game.game_over:
                st.warning("Game Over!")
                if restart_btn_placeholder.button("Restart Game"):
                    st.session_state.game = SnakeGame(width=640, height=480)
                    st.session_state.running = True
                    restart_btn_placeholder.empty()
                    break  # Exit loop, Streamlit will rerun and start new game
                st.session_state.running = False
                break
            time.sleep(0.05)
