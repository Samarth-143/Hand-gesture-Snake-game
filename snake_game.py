import pygame
import random
from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class SnakeGame:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.block_size = 20
        self.speed = 5  # Reduced speed for smoother movement
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (213, 50, 80)
        self.GREEN = (0, 255, 0)
        self.BLUE = (50, 153, 213)
        # Font (pygame.init() must be called before this, now guaranteed in main.py)
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 35)
        self.reset()
    
    def reset(self):
        """Reset the game to initial state"""
        self.direction = Direction.RIGHT
        self.head = [self.width // 2, self.height // 2]
        self.snake = [
            self.head,
            [self.head[0] - self.block_size, self.head[1]],
            [self.head[0] - (2 * self.block_size), self.head[1]]
        ]
        self.score = 0
        self.food = None
        self.place_food()
        self.game_over = False
        
    def place_food(self):
        """Place food at a random location"""
        x = random.randint(0, (self.width - self.block_size) // self.block_size) * self.block_size
        y = random.randint(0, (self.height - self.block_size) // self.block_size) * self.block_size
        self.food = [x, y]
        
        # Make sure food doesn't appear on snake
        if self.food in self.snake:
            self.place_food()
    
    def change_direction(self, new_direction):
        """Change snake direction (prevent 180 degree turns)"""
        if new_direction == Direction.UP and self.direction != Direction.DOWN:
            self.direction = new_direction
        elif new_direction == Direction.DOWN and self.direction != Direction.UP:
            self.direction = new_direction
        elif new_direction == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = new_direction
        elif new_direction == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = new_direction
    
    def move(self):
        """Move the snake in the current direction"""
        x = self.head[0]
        y = self.head[1]
        
        if self.direction == Direction.UP:
            y -= self.block_size
        elif self.direction == Direction.DOWN:
            y += self.block_size
        elif self.direction == Direction.LEFT:
            x -= self.block_size
        elif self.direction == Direction.RIGHT:
            x += self.block_size
        
        self.head = [x, y]
    
    def check_collision(self):
        """Check if snake collided with wall or itself"""
        # Check wall collision
        if (self.head[0] >= self.width or self.head[0] < 0 or 
            self.head[1] >= self.height or self.head[1] < 0):
            return True
        
        # Check self collision
        if self.head in self.snake[1:]:
            return True
        
        return False
    
    def update(self):
        """Update game state"""
        if self.game_over:
            return
        
        self.move()
        
        # Check collision
        if self.check_collision():
            self.game_over = True
            return
        
        # Add new head
        self.snake.insert(0, list(self.head))
        
        # Check if food eaten
        if self.head == self.food:
            self.score += 1
            self.place_food()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def draw(self):
        """Draw the game on its surface"""
        self.surface.fill(self.BLACK)
        # Draw food
        pygame.draw.rect(self.surface, self.RED, 
                        [self.food[0], self.food[1], self.block_size, self.block_size])
        # Draw snake
        for i, segment in enumerate(self.snake):
            if i == 0:  # Head
                pygame.draw.rect(self.surface, self.BLUE,
                               [segment[0], segment[1], self.block_size, self.block_size])
            else:  # Body
                pygame.draw.rect(self.surface, self.GREEN,
                               [segment[0], segment[1], self.block_size, self.block_size])
        # Draw score
        self.show_score()
    
    def show_score(self):
        """Display the score"""
        value = self.score_font.render(f"Score: {self.score}", True, self.WHITE)
        self.surface.blit(value, [10, 10])
    
    def show_message(self, msg, color):
        """Display a message on screen"""
        mesg = self.font_style.render(msg, True, color)
        self.surface.blit(mesg, [self.width / 6, self.height / 3])
    
    def play_step(self):
        """Execute one game step"""
        self.update()
        self.draw()
        self.clock.tick(self.speed)
        return not self.game_over
    
    def quit(self):
        """Clean up and quit"""
        pygame.quit()
