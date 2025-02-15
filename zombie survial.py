import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Clock for FPS control
clock = pygame.time.Clock()
FPS = 60

# Player variables
player_pos = [WIDTH // 2, HEIGHT // 2]
player_size = 30
player_speed = 5
player_health = 100

# Bullet variables
bullets = []
bullet_speed = 10

# Zombie variables
zombies = []
zombie_speed = 2
zombie_spawn_rate = 30  # Frames between spawns

# Score
score = 0

# Font
font = pygame.font.Font(None, 36)

def draw_player():
    pygame.draw.circle(screen, BLUE, player_pos, player_size)

def draw_bullets():
    for bullet in bullets:
        pygame.draw.circle(screen, RED, (bullet[0], bullet[1]), 5)

def draw_zombies():
    for zombie in zombies:
        pygame.draw.circle(screen, GREEN, (zombie[0], zombie[1]), 20)

def move_bullets():
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

def move_zombies():
    global player_health
    for zombie in zombies[:]:
        dx, dy = player_pos[0] - zombie[0], player_pos[1] - zombie[1]
        dist = math.hypot(dx, dy)
        zombie[0] += zombie_speed * dx / dist
        zombie[1] += zombie_speed * dy / dist

        # Check collision with player
        if math.hypot(zombie[0] - player_pos[0], zombie[1] - player_pos[1]) < player_size + 20:
            zombies.remove(zombie)
            player_health -= 10

def check_bullet_zombie_collision():
    global score
    for bullet in bullets[:]:
        for zombie in zombies[:]:
            if math.hypot(bullet[0] - zombie[0], bullet[1] - zombie[1]) < 20:
                bullets.remove(bullet)
                zombies.remove(zombie)
                score += 1
                break

# Main game loop
running = True
frame_count = 0

while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_pos[1] += player_speed
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed

    # Shooting bullets
    if keys[pygame.K_SPACE]:
        if len(bullets) < 10:  # Limit number of bullets
            bullets.append([player_pos[0], player_pos[1]])

    # Spawn zombies
    if frame_count % zombie_spawn_rate == 0:
        zombie_x = random.choice([0, WIDTH])
        zombie_y = random.choice([0, HEIGHT])
        zombies.append([zombie_x, zombie_y])

    # Update bullets and zombies
    move_bullets()
    move_zombies()

    # Check for collisions
    check_bullet_zombie_collision()

    # Draw everything
    draw_player()
    draw_bullets()
    draw_zombies()

    # Draw HUD
    health_text = font.render(f"Health: {player_health}", True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(health_text, (10, 10))
    screen.blit(score_text, (10, 50))

    # End game if health is 0
    if player_health <= 0:
        game_over_text = font.render("Game Over!", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    pygame.display.flip()
    frame_count += 1

pygame.quit()
