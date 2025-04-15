import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Load images
snake_head_img = pygame.image.load("snake_head.png")
apple_img = pygame.image.load("apple.png")

# Scale images
snake_head_img = pygame.transform.scale(snake_head_img, (GRID_SIZE, GRID_SIZE))
apple_img = pygame.transform.scale(apple_img, (GRID_SIZE, GRID_SIZE))

# Load sound effects
#eat_sound = pygame.mixer.Sound("eat.wav")
#game_over_sound = pygame.mixer.Sound("game_over.wav")

# Create game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Sprites")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Snake class
class Snake:
    def __init__(self):
        self.body = [[100, 100]]
        self.direction = "RIGHT"
        self.growing = False

    def move(self):
        head_x, head_y = self.body[0]
        
        if self.direction == "UP":
            head_y -= GRID_SIZE
        elif self.direction == "DOWN":
            head_y += GRID_SIZE
        elif self.direction == "LEFT":
            head_x -= GRID_SIZE
        elif self.direction == "RIGHT":
            head_x += GRID_SIZE

        new_head = [head_x, head_y]

        # Check for collisions
        if new_head in self.body or head_x < 0 or head_y < 0 or head_x >= WIDTH or head_y >= HEIGHT:
            game_over_sound.play()
            return False

        self.body.insert(0, new_head)

        if not self.growing:
            self.body.pop()
        else:
            self.growing = False

        return True

    def grow(self):
        self.growing = True

    def change_direction(self, new_direction):
        if new_direction == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        elif new_direction == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        elif new_direction == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif new_direction == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"

# Apple class
class Apple:
    def __init__(self):
        self.position = [random.randrange(0, WIDTH, GRID_SIZE), random.randrange(0, HEIGHT, GRID_SIZE)]

    def spawn(self, snake_body):
        while True:
            self.position = [random.randrange(0, WIDTH, GRID_SIZE), random.randrange(0, HEIGHT, GRID_SIZE)]
            if self.position not in snake_body:
                break

# Main game loop
def game_loop():
    snake = Snake()
    apple = Apple()
    running = True
    score = 0

    while running:
        screen.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction("RIGHT")
                elif event.key == pygame.K_r:  # Restart game
                    game_loop()

        # Move snake
        if not snake.move():
            break  # End game if collision occurs

        # Check if snake eats apple
        if snake.body[0] == apple.position:
            eat_sound.play()
            snake.grow()
            apple.spawn(snake.body)
            score += 1

        # Draw snake
        for segment in snake.body:
            screen.blit(snake_head_img, (segment[0], segment[1]))

        # Draw apple
        screen.blit(apple_img, (apple.position[0], apple.position[1]))

        # Display score
        font = pygame.font.SysFont(None, 30)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(10)

# Start game
game_loop()
pygame.quit()
