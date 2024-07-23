from typing import Any
import pygame
from pygame import mixer
from pygame.locals import *
import random

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

#define fps
clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invasion Game")

#define fonts
pygame.font.init()
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)

#Load sounds and music
explosion_fx = pygame.mixer.Sound("Game-Space-Invasion/bullet_shot.wav")
explosion_fx.set_volume(0.5)

explosion2_fx = pygame.mixer.Sound("Game-Space-Invasion/bullet_shot.wav")
explosion2_fx.set_volume(0.25)

game_over_sound = pygame.mixer.Sound("Game-Space-Invasion/game_over.wav")
game_over_sound.set_volume(0.4)

pygame.mixer.music.load("Game-Space-Invasion/background_music.mp3")

#screen game variables 
rows = 5
cols = 5
alien_cooldown = 1000               #bullet cooldown in milli-seconds
last_alien_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0                       #0 is no game over, 1 means player has won, -1 means player has lost

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

#load image 
bg = pygame.image.load("Game-Space-Invasion/bg_game.png")
bg = pygame.transform.scale(bg, (800, 600))

def draw_bg():
    screen.blit(bg, (0, 0))

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

#create spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Game-Space-Invasion/player.png")
        self.image = pygame.transform.scale(self.image, (116, 92.33))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.health_start = health
        self.health_rem = health
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        speed = 8                           #set movement speed
        cooldown = 500                      #set cooldown variable in milli-seconds
        game_over = 0
        key = pygame.key.get_pressed()      #get key press
        
        if (key[pygame.K_LEFT] or key[pygame.K_a]) and self.rect.left>0:
            self.rect.x -= speed
        if (key[pygame.K_RIGHT] or key[pygame.K_a]) and self.rect.right < screen_width:
            self.rect.x += speed
    
        #record current time
        time_now = pygame.time.get_ticks()
        
        #shoot
        if key[pygame.K_SPACE] and (time_now-self.last_shot > cooldown):
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet) 
            self.last_shot = time_now
        
        #update mask
        self.mask = pygame.mask.from_surface(self.image)

        #draw health bar
        pygame.draw.rect(screen, RED, (self.rect.x, (self.rect.bottom+10), self.rect.width, 15))
        
        if self.health_rem > 0:
            pygame.draw.rect(screen, GREEN, (self.rect.x, (self.rect.bottom+10), int(self.rect.width*(self.health_rem/self.health_start)), 15))
    
        elif self.health_rem <= 0:
            explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            game_over_sound.play()
            self.kill()
            game_over = -1
            game_over_sound.play()
        return game_over

#create bullets class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Game-Space-Invasion/bullet.png")
        self.image = pygame.transform.scale(self.image, (90, 91.5))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        
    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 200:
            self.kill()

        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()
            explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)

#create aliens class
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Game-Space-Invasion/alien"+str(random.randint(1,6))+".png")
        self.image = pygame.transform.scale(self.image, (48, 27))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.move_counter = 0
        self.move_direction = 1
        
    def update(self):
        self.rect.x += 1 * self.move_direction
        self.move_counter += 1 
        if abs(self.move_counter)>75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

#create aliens' bullets class
class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Game-Space-Invasion/alien_bullet.png")
        self.image = pygame.transform.scale(self.image, (90, 91.5))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        
    def update(self):
        self.rect.y += 5
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            spaceship.health_rem -= 1               #reduce spaceship health
            explosion2_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)

#create explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []                    #list to hold the explosion images
        for num in range(1,5):
            img = pygame.image.load(f"Game-Space-Invasion/explosion{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20,20))
            if size == 2:
                img = pygame.transform.scale(img, (40,40))
            if size == 3:
                img = pygame.transform.scale(img, (160,160))
            
            self.images.append(img)         #add the image to the list 

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.counter = 0
   
    def update(self):
        explosion_speed = 3
        self.counter += 1                   #update explosion animation
        if self.counter >= explosion_speed and self.index<len(self.images)-1:
            self.counter = 0
            self.index += 1 
            self.image = self.images[self.index]
        
        #if the animation is complete, delete explosion
        if self.index >= len(self.images)-1 and self.counter>=explosion_speed:
            self.kill()

#create sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

def create_aliens():
    #generate aliens
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100+item*100, 100+row*70)
            alien_group.add(alien)

create_aliens()

#create player
spaceship = Spaceship(int(screen_width/2), screen_height-100, 3)
spaceship_group.add(spaceship)
        
pygame.mixer.music.play(-1)                 #Play background music indefinitely
run = True
while run:
    clock.tick(fps)

    draw_bg()                               #draw bachground
    if countdown == 0:
        #create random alien bullets
        #record current time
        time_now = pygame.time.get_ticks()

        #shoot
        if time_now-last_alien_shot > alien_cooldown and len(alien_bullet_group)<5 and len(alien_group)>0 :
            attacking_alien = random.choice(alien_group.sprites())
            alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            alien_bullet_group.add(alien_bullet)
            last_alien_shot = time_now

        #check if all the aliens have been killed 
        if len(alien_group) == 0:
            game_over = 1

        if game_over == 0:
            game_over = spaceship.update()          #update spaceship
            bullet_group.update()                   #update sprite groups
            alien_group.update()
            alien_bullet_group.update()
        else: 
            if game_over == -1:
                pygame.mixer.music.stop()
                draw_text('GAME OVER!', font40, WHITE, int(screen_width/2-110), int(screen_height/2+50))
                creator_text = font30.render("Credits: Ish Agar", True, WHITE)
                screen.blit(creator_text, int(screen_width/2-110), int(screen_height/2+100))
                game_over_sound.play()
                pygame.time.delay(3000)  # Display the "Game Over!" message for 3 seconds before quitting
                
            if game_over == 1:
                pygame.mixer.music.stop()
                draw_text('YOU WIN!', font40, WHITE, int(screen_width/2-110), int(screen_height/2+50))
                creator_text = font30.render("Credits: Ish Agar", True, WHITE)
                screen.blit(creator_text, (int(screen_width/2-110), int(screen_height/2+100)))
                game_over_sound.play()
                pygame.time.delay(3000)  # Display the "Game Over!" message for 3 seconds before quitting

    if countdown > 0:
        draw_text('GET READY', font40, WHITE, int(screen_width/2-110), int(screen_height/2+50))
        creator_text = font30.render("Credits: Ish Agar", True, WHITE)
        screen.blit(creator_text, (int(screen_width/2-110), int(screen_height/2+100)))
        draw_text(str(countdown), font40, WHITE, int(screen_width/2-10), int(screen_height/2+150))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer

    explosion_group.update()                    #update explosion group

    spaceship_group.draw(screen)                #draw sprite groups
    bullet_group.draw(screen)   
    alien_group.draw(screen)   
    alien_bullet_group.draw(screen) 
    explosion_group.draw(screen)     
    
    # Event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_q: 
            run = False 

    pygame.display.update()

pygame.quit()
