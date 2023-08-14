import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Spaceship settings
spaceship_width = 50
spaceship_height = 50
spaceship = pygame.Rect(width // 2 - spaceship_width // 2, height - 70, spaceship_width, spaceship_height)
spaceship_speed = 5

# Enemy settings
enemies = []
enemy_width = 40
enemy_height = 40
enemy_speed = 2

# Bullet settings
bullet = pygame.Rect(0, 0, 5, 15)
bullet_color = (255, 0, 0)
bullet_speed = 5
bullet_state = "ready"  # "ready" or "fired"

# Scoring and Lives
score = 0
font = pygame.font.Font(None, 36)
lives = 3  # Initial number of lives

# Game over
game_over = False

# Spawn timer for enemies
enemy_spawn_timer = pygame.time.get_ticks()
enemy_spawn_interval = 1000  # Spawn an enemy every 1 second

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_state = "fired"
                bullet.x = spaceship.x + spaceship.width // 2 - bullet.width // 2
                bullet.y = spaceship.y

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and spaceship.x > 0:
            spaceship.x -= spaceship_speed
        if keys[pygame.K_RIGHT] and spaceship.x < width - spaceship.width:
            spaceship.x += spaceship_speed

        if bullet_state == "fired":
            bullet.y -= bullet_speed
            if bullet.y <= 0:
                bullet_state = "ready"

        # Spawn enemies
        current_time = pygame.time.get_ticks()
        if current_time - enemy_spawn_timer > enemy_spawn_interval:
            enemy = pygame.Rect(
                random.randint(0, width - enemy_width),
                0,
                enemy_width,
                enemy_height,
            )
            enemies.append(enemy)
            enemy_spawn_timer = current_time

        # Update enemy positions
        for enemy in enemies:
            enemy.y += enemy_speed

            if enemy.colliderect(bullet):
                bullet_state = "ready"
                bullet.y = spaceship.y
                enemies.remove(enemy)
                score += 10

            if enemy.colliderect(spaceship):
                lives -= 1
                spaceship.x = width // 2 - spaceship_width // 2
                spaceship.y = height - 70
                if lives == 0:
                    game_over = True

        # Clear the screen
        screen.fill(black)

        # Draw spaceship, enemies, and bullet
        pygame.draw.rect(screen, white, spaceship)
        for enemy in enemies:
            pygame.draw.rect(screen, white, enemy)
        if bullet_state == "fired":
            pygame.draw.rect(screen, bullet_color, bullet)

        # Draw score and lives
        score_text = font.render("Score: " + str(score), True, white)
        lives_text = font.render("Lives: " + str(lives), True, white)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (width - 100, 10))

        if game_over:
            screen.fill(black)
            final_score_text = font.render("Final Score: " + str(score), True, white)
            screen.blit(final_score_text, (width // 2 - 120, height // 2))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

pygame.quit()
quit()
