import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH = 600
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("sohans_space")

GOLD = (255, 215, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BODRER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)  # Center vertical line

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("assets", "Gun+Silencer.mp3"))

HEALTH_FONT = pygame.font.SysFont("comicsans", 20)
WINNER_FONT = pygame.font.SysFont("comicsans", 50)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH = 50
SPACESHIP_HEIGHT = 45

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "spaceship_yellow.png"))
YELLOW_SPACE_SHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACE_SHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),90)

RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "spaceship_red.png"))
RED_SPACE_SHIP = pygame.transform.rotate( pygame.transform.scale(RED_SPACE_SHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.image.load(os.path.join("Assets", "space.png"))
SPACE = pygame.transform.scale(SPACE, (WIDTH, HEIGHT))

def draw_window(red, yellow, RED_BULLETS, YELLOW_BULLETS , red_health, yellow_health):
    WIN.blit(SPACE, (0, 0)) 
    pygame.draw.rect(WIN, BLACK, BODRER) 
  
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1,RED)  
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, YELLOW)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))   
    WIN.blit(yellow_health_text, (10, 10))
    
    WIN.blit(YELLOW_SPACE_SHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACE_SHIP, (red.x, red.y))
    
    
    for bullet in RED_BULLETS:
        pygame.draw.rect(WIN, RED, bullet)
        
    for bullet in YELLOW_BULLETS:
        pygame.draw.rect(WIN, YELLOW, bullet)
        
    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
        if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # Prevent moving out of bounds
            yellow.x -= VEL
        if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BODRER.x:  # Prevent moving out of bounds
            yellow.x += VEL
        if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # Prevent moving out of bounds
            yellow.y -= VEL 
        if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT:
            yellow.y += VEL
 
def red_handle_movement(keys_pressed, red):
        if keys_pressed[pygame.K_LEFT] and red.x - VEL > BODRER.x + BODRER.width:  # Prevent moving out of bounds
            red.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # Prevent moving out of bounds
            red.x += VEL
        if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # Prevent moving out of bounds
            red.y -= VEL 
        if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT:
            red.y += VEL           

def handle_bullets(yellow_bullets, red_bullets, yellow, red):   
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
            
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
            
def draw_winner(text):            
    draw_text = WINNER_FONT.render(text, 1, GOLD)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    
    pygame.display.update()
    pygame.time.delay(5000)
         
  
def main():
    red = pygame.Rect(WIDTH - SPACESHIP_WIDTH - 10, HEIGHT//2 - SPACESHIP_HEIGHT//2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(10, HEIGHT//2 - SPACESHIP_HEIGHT//2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    red_bullets = []
    yellow_bullets = []
    
    red_health = 10
    yellow_health = 10
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                      
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
                
            if event.type == YELLOW_HIT:    
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
                
        winner_text = ""
        if red_health <= 0:
            winner_text = "YELLOW WINS!"
     
           
        if yellow_health <= 0:
            winner_text = "RED WINS!"
           
        if winner_text != "": 
            draw_winner(winner_text)
            break   
              
            
       
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, 
                    red_health, yellow_health)
        
    main() 

if __name__ == "__main__":
    main()

