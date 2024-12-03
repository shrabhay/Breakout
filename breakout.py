import pygame
import sys
import random

# Initialise PyGame
pygame.init()

# Screen Dimensions
HEIGHT, WIDTH = 600, 800

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('THE BREAKOUT GAME')

# Clock for Controlling the Frame Rate
clock = pygame.time.Clock()

# Paddle Setup
PADDLE_HEIGHT, PADDLE_WIDTH = 10, 100
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_speed = 7

# Ball Setup
BALL_RADIUS = 10
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed_x, ball_speed_y = random.choice([-4, 4]), -4

# Bricks Setup
ROWS, COLS = 6, 10
BRICK_WIDTH = WIDTH // COLS
BRICK_HEIGHT = 30
bricks = []

for row in range(ROWS):
    for col in range(COLS):
        brick_x = col * BRICK_WIDTH
        brick_y = row * BRICK_HEIGHT
        bricks.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))

# Score
score = 0
font = pygame.font.Font(None, 36)


# Game Loop
def main():
    global ball_speed_x, ball_speed_y, score
    running = True

    while running:
        screen.fill(BLACK)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Paddle Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.move_ip(-paddle_speed, 0)
        if keys[pygame.K_RIGHT] and paddle.right > 0:
            paddle.move_ip(paddle_speed, 0)

        # Ball Movement
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Ball Collision with Walls
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed_x = -ball_speed_x
        if ball.top <= 0:
            ball_speed_y = -ball_speed_y

        # Ball Collision with Paddle
        if ball.colliderect(paddle):
            ball_speed_y = -ball_speed_y

        # Ball Collision with Bricks
        for brick in bricks:
            if ball.colliderect(brick):
                ball_speed_y = -ball_speed_y
                bricks.remove(brick)
                score += 1

        # Balls Falls Below Screen
        if ball.bottom >= HEIGHT:
            running = False

        # Draw Everything
        pygame.draw.rect(screen, WHITE, paddle)
        pygame.draw.ellipse(screen, YELLOW, ball)
        for brick in bricks:
            pygame.draw.rect(screen, BLUE, brick)

        # Display Score
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        # Update the Display
        pygame.display.flip()

        # Frame Rate
        clock.tick(60)

    # Game Over Message
    game_over_text = font.render('GAME OVER! Press any key to quit...', True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.event.clear()
    pygame.event.wait()


if __name__ == '__main__':
    main()
