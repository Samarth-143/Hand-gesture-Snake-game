# Hand Gesture Controlled Snake Game

A classic Snake game controlled by hand gestures using computer vision!

## Features

- **Hand Gesture Control**: Point your hand in any direction (up, down, left, right) to control the snake
- **Real-time Detection**: Uses MediaPipe for fast and accurate hand tracking
- **Classic Gameplay**: Eat food to grow longer, avoid hitting walls and yourself
- **Score Tracking**: Keep track of your score as you play

## Requirements

All required packages are already installed:
- pygame
- opencv-python
- mediapipe
- numpy

## How to Play

1. Make sure your webcam is connected
2. Run the game:
   ```
   python main.py
   ```
3. Show your hand to the camera
4. Point your hand in the direction you want the snake to move:
   - Point **up** to move up
   - Point **down** to move down
   - Point **left** to move left
   - Point **right** to move right
5. The snake will automatically follow the direction your hand is pointing
6. Eat the red food blocks to grow and increase your score
7. Avoid hitting the walls or your own body!

## Controls

- **Hand Gestures**: Control snake direction
- **R**: Restart game after game over
- **Q**: Quit the game

## Tips

- Keep your hand clearly visible to the camera
- Point your hand decisively in the direction you want to go
- The game smooths out gesture detection to avoid accidental changes
- Try to plan your movements ahead as the snake gets longer!

## Files

- `main.py`: Main game loop and integration
- `snake_game.py`: Snake game logic
- `hand_detector.py`: Hand gesture detection using MediaPipe

Enjoy playing! 🐍
