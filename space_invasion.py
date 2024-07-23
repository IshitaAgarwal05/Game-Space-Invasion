import pygame
import sys
import random
import time 

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invasion Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#Setup game sounds
pygame.mixer.music.load("small python projects/Games/space_invasion/background_music.mp3")
bullet_sound = pygame.mixer.Sound("small python projects/Games/space_invasion/bullet_shot.wav")
game_over_sound = pygame.mixer.Sound("small python projects/Games/space_invasion/game_over.wav")

# Spaceship
player_img = pygame.image.load("small python projects/Games/space_invasion/player.png")
player_img = pygame.transform.scale(player_img, (116, 92.33))
player_rect = player_img.get_rect()
player_rect.centerx = WIDTH // 2
player_rect.bottom = HEIGHT - 20
player_speed = 5
player_energy = 100
player_lives = 3

# Bullet 
bullet_img = pygame.image.load("small python projects/Games/space_invasion/bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (90, 91.5))
bullet_rect = bullet_img.get_rect()
bullet_speed = 10
bullet_state = "ready"  # "ready" means the bullet is ready to fire, "fire" means it's currently moving

# Alien
alien_img = pygame.image.load("small python projects/Games/space_invasion/alien"+str(random.randint(1,6))+".png")
alien_img = pygame.transform.scale(alien_img, (150, 150))
alien_rect = alien_img.get_rect()
alien_rect.x = random.randint(50, WIDTH-50)
alien_rect.y = random.randint(50, HEIGHT//3)
alien_speed = 2
alien_energy = 100  # Initialize alien_energy

# Alien bullets
alien_bullet_img = pygame.image.load("small python projects/Games/space_invasion/alien_bullet.png")
alien_bullet_img = pygame.transform.scale(alien_bullet_img, (96, 54))
alien_bullet_rect = alien_bullet_img.get_rect()
alien_bullet_speed = 5
alien_bullet_state = "ready"

# Fonts
font = pygame.font.SysFont(None, 30)

# Levels
levels = [
    {"level": 1, "alien_speed": 2, "alien_energy": 100, "alien_bullet_speed": 3},
    {"level": 2, "alien_speed": 3, "alien_energy": 150, "alien_bullet_speed": 4},
    {"level": 3, "alien_speed": 4, "alien_energy": 200, "alien_bullet_speed": 5},
    {"level": 4, "alien_speed": 5, "alien_energy": 250, "alien_bullet_speed": 6},
    {"level": 5, "alien_speed": 6, "alien_energy": 300, "alien_bullet_speed": 7}
]
current_level = 0

# Function to display player energy and lives
def show_stats():
    energy_text = font.render(f"Energy: {player_energy}%", True, WHITE)
    screen.blit(energy_text, (10, 10))

    lives_text = font.render(f"Lives: {player_lives}", True, WHITE)
    screen.blit(lives_text, (WIDTH - 100, 10))

    alien_energy_text = font.render(f"Alien Energy: {alien_energy}%", True, WHITE)
    screen.blit(alien_energy_text, (10, 40))

    level_text = font.render(f"Level: {levels[current_level]['level']}", True, WHITE)
    screen.blit(level_text, (WIDTH - 100, 40))

# Function to display instructions
def show_instructions():
    instructions_text = font.render("You'll have 3 lives and 5 levels,", True, WHITE)
    screen.blit(instructions_text, (50, HEIGHT // 2 - 90))
    
    instructions_text = font.render("with your energy level 100% at the beginning.", True, WHITE)
    screen.blit(instructions_text, (50, HEIGHT // 2 - 50))
    
    instructions_text = font.render("Compete with the alien spaceship.", True, WHITE)
    screen.blit(instructions_text, (50, HEIGHT // 2 - 10))
    
    instructions_text2 = font.render("1. Press space bar to shoot.", True, BLUE)
    screen.blit(instructions_text2, (50, HEIGHT // 2 + 20))

    instructions_text2 = font.render("2. Press the arrow keys (or 'A' and 'D' keys) to move sideways.", True, BLUE)
    screen.blit(instructions_text2, (50, HEIGHT // 2 + 50))

# Main game loop
def main():
    global bullet_state 
    global alien_speed
    global alien_bullet_state
    global player_energy
    global alien_energy  # Declare alien_energy as global
    global player_lives  # Declare player_lives as global
    global bullet_speed
    global alien_bullet_speed
    global bullet_rect
    global alien_bullet_rect

    # Show instructions
    screen.fill(BLACK)
    show_instructions()
    pygame.display.flip()
    time.sleep(5)  # Display instructions for 5 seconds

    player_energy = 100
    alien_energy = 100
    player_lives = 3
    alien_speed = levels[current_level]["alien_speed"]
    alien_bullet_state = "ready"
    bullet_speed = 10
    alien_bullet_speed = levels[current_level]["alien_bullet_speed"]
    bullet_rect = bullet_img.get_rect()
    alien_bullet_rect = alien_bullet_img.get_rect()
    pygame.mixer.music.play(-1)  # Play background music indefinitely
    running = True
    
    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += player_speed

        # Ensure player doesn't go off-screen
        if player_rect.left < 0:
            player_rect.left = 0
        elif player_rect.right > WIDTH:
            player_rect.right = WIDTH    

        #Fire command by space
        if keys[pygame.K_SPACE] and bullet_state == "ready":
            bullet_rect.centerx = player_rect.centerx
            bullet_rect.top = player_rect.top
            bullet_state = "fire"
        
        # Move bullet
        if bullet_state == "fire":
            bullet_rect.y -= bullet_speed
            if bullet_rect.y <= 0:
                bullet_state = "ready"
        
        # Move alien
        alien_rect.x += alien_speed
        if alien_rect.right >= WIDTH:
            alien_speed = -abs(alien_speed)  # Move left
        elif alien_rect.left <= 0:
            alien_speed = abs(alien_speed)  # Move right
        
        # Move alien bullet
        if alien_bullet_state == "ready":
            alien_bullet_rect.centerx = alien_rect.centerx
            alien_bullet_rect.centery = alien_rect.bottom
            alien_bullet_state = "fire"
        elif alien_bullet_state == "fire":
            alien_bullet_rect.y += alien_bullet_speed
            if alien_bullet_rect.y >= HEIGHT:
                alien_bullet_state = "ready"

        # Check collision between player bullet and alien
        if bullet_rect.colliderect(alien_rect):
            player_energy -= 10
            bullet_state = "ready"
            if player_energy <= 0:
                player_lives -= 1
                player_energy = 100
                if player_lives <= 0:
                    game_over()
            alien_energy -= 10
            if alien_energy <= 0:
                next_level()

        # Check collision between alien bullet and player
        if alien_bullet_rect.colliderect(player_rect):
            alien_bullet_state = "ready"
            player_energy -= 10
            if player_energy <= 0:
                player_lives -= 1
                player_energy = 100
                if player_lives <= 0:
                    game_over()

        # Nullify bullets if they collide
        if bullet_rect.colliderect(alien_bullet_rect):
            bullet_state = "ready"
            alien_bullet_state = "ready"

        # Draw everything
        screen.blit(player_img, player_rect)
        screen.blit(alien_img, alien_rect)
        if bullet_state == "fire":
            screen.blit(bullet_img, bullet_rect)
        if alien_bullet_state == "fire":
            screen.blit(alien_bullet_img, alien_bullet_rect)
        show_stats()

        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()

def game_over():
    pygame.mixer.music.stop()
    game_over_sound.play()
    font = pygame.font.SysFont(None, 60)
    game_over_text = font.render("Game Over!", True, RED)
    creator_text = font.render("Credits: Ish Agar", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 30))
    screen.blit(creator_text, (WIDTH // 2 - 200, HEIGHT // 2 + 30))
    pygame.display.flip()
    pygame.time.delay(3000)  # Display the "Game Over!" message for 3 seconds before quitting
    pygame.quit()
    sys.exit()

def game_won():
    pygame.mixer.music.stop()
    game_over_sound.play()
    font = pygame.font.SysFont(None, 60)
    game_won_text = font.render("You Won!", True, RED)
    creator_text = font.render("Credits: Ish Agar", True, WHITE)
    screen.blit(game_won_text, (WIDTH // 2 - 150, HEIGHT // 2 - 30))
    screen.blit(creator_text, (WIDTH // 2 - 200, HEIGHT // 2 + 30))
    pygame.display.flip()
    pygame.time.delay(3000)  # Display the "You Won!" message for 3 seconds before quitting
    pygame.quit()
    sys.exit()

def next_level():
    global current_level, alien_speed, alien_energy, alien_bullet_speed
    current_level += 1
    if current_level >= len(levels):
        game_over()
    else:
        level = levels[current_level]
        alien_speed = level["alien_speed"]
        alien_energy = level["alien_energy"]
        alien_bullet_speed = level["alien_bullet_speed"]
        alien_rect.x = random.randint(50, WIDTH - 50)
        alien_rect.y = random.randint(50, HEIGHT // 3)

        # Display level message
        font = pygame.font.SysFont(None, 60)
        level_text = font.render(f"Level {current_level + 1}", True, WHITE)
        screen.blit(level_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()
        time.sleep(5)  # Display level message for 5 seconds

# Start the game
main()