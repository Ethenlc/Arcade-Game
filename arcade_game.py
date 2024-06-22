import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Racing Game")

# Load background image
background_img = pygame.image.load('road.png') 
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# Set up clock
clock = pygame.time.Clock()

# Load car image
car_img = pygame.image.load('car_image.png')
car_img = pygame.transform.scale(car_img, (70, 120))

# Load obstacle image
obstacle_img = pygame.image.load('obstacle.png')
obstacle_img = pygame.transform.scale(obstacle_img, (70, 120))

# Load car sounds
car_sound1 = pygame.mixer.Sound('car_sound1.mp3')
car_sound2 = pygame.mixer.Sound('car_sound2.mp3')

# Player car properties
car_rect = car_img.get_rect()
car_pos = [screen_width // 2 - car_rect.width // 2, screen_height - car_rect.height - 10]
car_speed = 5

# Obstacle properties
obstacle_width, obstacle_height = 70, 120  # Adjust size to match obstacle_img size
obstacle_speed = 5
obstacles = []
obstacle_positions = [180, 305, 430, 555]  # Different lane locations

def create_obstacle():
    x_pos = random.choice(obstacle_positions)
    y_pos = -obstacle_height
    obstacles.append([x_pos, y_pos])

# Create the first obstacle
create_obstacle()

# Initialize font (None)
pygame.font.init()
font = pygame.font.Font(None, 36)

score = 0

def show_score(screen, score):
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

def check_collision(rect1, rect2):
    return (
        rect1[0] < rect2[0] + rect2[2] and
        rect1[0] + rect1[2] > rect2[0] and
        rect1[1] < rect2[1] + rect2[3] and
        rect1[1] + rect1[3] > rect2[1]
    )

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key states
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_pos[0] > 135:
        car_pos[0] -= car_speed
        car_sound1.play()
    if keys[pygame.K_RIGHT] and car_pos[0] < screen_width- 135 - car_rect.width:
        car_pos[0] += car_speed
        car_sound2.play()

    # Move obstacles
    for obs in obstacles:
        obs[1] += obstacle_speed

    # Create new obstacle if the last one has moved a certain distance
    if obstacles[-1][1] > 200:
        create_obstacle()

    # Check for collisions
    for obs in obstacles:
        obs_rect = pygame.Rect(obs[0], obs[1], obstacle_width, obstacle_height)
        if obs_rect.colliderect(car_rect.move(car_pos)):
            running = False

    # Update score
    score += 1

    # Draw background
    screen.blit(background_img, (0, 0))

    # Draw the player car
    screen.blit(car_img, car_pos)

    # Draw obstacles
    for obs in obstacles:
        screen.blit(obstacle_img, (obs[0], obs[1]))

    # Display score
    show_score(screen, score)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Game over
screen.fill((255, 255, 255))
game_over_text = font.render("Game Over", True, (0, 0, 0))
final_score_text = font.render(f"Final Score: {score}", True, (0, 0, 0))
screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 50))
screen.blit(final_score_text, (screen_width // 2 - final_score_text.get_width() // 2, screen_height // 2 + 10))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
sys.exit()
