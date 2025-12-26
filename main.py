import cv2
import pygame
import numpy as np
from hand_detector import HandDetector
from snake_game import SnakeGame, Direction

def main():
    # Initialize pygame first
    pygame.init()
    # Initialize camera
    cap = cv2.VideoCapture(0)
    cap.set(3, 320)  # Width (smaller for side panel)
    cap.set(4, 240)  # Height
    # Initialize hand detector
    detector = HandDetector()
    # Initialize snake game with extra width for camera feed
    game = SnakeGame(width=640, height=480)  # Game width
    # Create a display for both game and camera feed side by side
    total_width = 640 + 320  # Game width + camera width
    total_height = 480
    display = pygame.display.set_mode((total_width, total_height))
    pygame.display.set_caption('Hand Gesture Snake Game')
    
    # Variables for gesture control
    last_direction = None
    direction_hold_frames = 0
    frames_threshold = 2  # Lowered for faster response
    
    print("Hand Gesture Snake Game")
    print("=" * 50)
    print("Instructions:")
    print("- Show your hand to the camera")
    print("- Point your hand in the direction you want the snake to move")
    print("- The snake will follow the direction your hand is pointing")
    print("- Press 'q' to quit")
    print("- Press 'r' to restart after game over")
    print("=" * 50)
    
    running = True
    paused = False
    show_start = True
    game_over_anim = False
    game_over_anim_timer = 0
    game_over_anim_duration = 60  # frames

    while running:
        if show_start:
            display.fill((0, 0, 0))
            font_big = pygame.font.SysFont("comicsansms", 60)
            font_small = pygame.font.SysFont("arial", 30)
            title = font_big.render("Snake Game", True, (0, 255, 0))
            instr1 = font_small.render("Show your hand to the camera", True, (255, 255, 255))
            instr2 = font_small.render("Point to move the snake", True, (255, 255, 255))
            instr3 = font_small.render("Press SPACE to start", True, (255, 255, 0))
            display.blit(title, (80, 100))
            display.blit(instr1, (80, 200))
            display.blit(instr2, (80, 240))
            display.blit(instr3, (80, 320))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        show_start = False
            continue

        # Read camera frame
        success, img = cap.read()
        if not success:
            print("Failed to read from camera")
            break

        # Flip image for mirror effect
        img = cv2.flip(img, 1)

        # Detect hand and get direction
        img = detector.find_hands(img)
        direction_str = detector.get_hand_direction(img)
        # Display current direction on camera feed
        if direction_str:
            cv2.putText(img, f"Direction: {direction_str}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Convert camera image to pygame surface
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_rgb = np.rot90(img_rgb)
        img_rgb = np.flipud(img_rgb)
        cam_surface = pygame.surfarray.make_surface(img_rgb)

        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_r and game.game_over:
                    game.reset()
                    game_over_anim = False
                if event.key == pygame.K_p and not game.game_over:
                    paused = not paused
                if event.key == pygame.K_SPACE and paused:
                    paused = False

        if paused:
            display.fill((30, 30, 30))
            font = pygame.font.SysFont("comicsansms", 50)
            pause_text = font.render("Paused", True, (255, 255, 0))
            display.blit(pause_text, (220, 200))
            pygame.display.update()
            continue

        # Stabilize direction input (require consistent direction for multiple frames)
        if not game.game_over:
            if direction_str == last_direction:
                direction_hold_frames += 1
            else:
                last_direction = direction_str
                direction_hold_frames = 0

            # Change snake direction if gesture is held for threshold frames
            if direction_hold_frames >= frames_threshold and direction_str:
                if direction_str == 'UP':
                    game.change_direction(Direction.UP)
                elif direction_str == 'DOWN':
                    game.change_direction(Direction.DOWN)
                elif direction_str == 'LEFT':
                    game.change_direction(Direction.LEFT)
                elif direction_str == 'RIGHT':
                    game.change_direction(Direction.RIGHT)

        # Update and draw game
        if not game.game_over:
            game.play_step()
        else:
            if not game_over_anim:
                game_over_anim = True
                game_over_anim_timer = 0
            # Game over animation: flash background
            if game_over_anim_timer < game_over_anim_duration:
                color = (255, 0, 0) if (game_over_anim_timer // 10) % 2 == 0 else (0, 0, 0)
                game.surface.fill(color)
                game.draw()
                game.show_message("Game Over!", (255, 255, 255))
                game_over_anim_timer += 1
            else:
                game.draw()
                game.show_message("Game Over! Press R to Restart or Q to Quit", game.RED)

        # Show the game and camera feed in the pygame window
        display.fill((0, 0, 0))
        display.blit(game.surface, (0, 0))  # Game on the left (640x480)
        display.blit(cam_surface, (640, 0))  # Camera on the right (320x240)
        # Add text labels
        font = pygame.font.SysFont("arial", 20)
        cam_label = font.render("Camera Feed", True, (255, 255, 255))
        display.blit(cam_label, (640 + 10, 10))  # Adjusted position for camera label
        pygame.display.update()

    # Cleanup
    pygame.quit()
    print("\nGame ended!")
    print(f"Final Score: {game.score}")

if __name__ == "__main__":
    main()
