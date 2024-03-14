import time
import pygame  
import pygame
from pygame.locals import *
from sys import exit

# images
image = 'imposter.png'
img1 = pygame.image.load(image)
img1 = pygame.transform.scale(img1, (100,100))



# colors
grey = (155, 155, 155)
red = (255,0,0) 
blue = (0,0,255)  
empty = (50,50,50)
white = (255,255,255)  
black = (0,0,0)
yellow = (255,255,0)
green = (0,255,0)

# initialization
pygame.init()  
X = 700
Y = 700
screen = pygame.display.set_mode((X, Y))  
done = False  

color = empty
x = 100
y = 100 

display_surface = pygame.display.set_mode((X, Y))
# music = pygame.mixer.music.load(os.path.join(s, 'Boing.mp3'))

# sound 
boing = pygame.mixer.Sound("Boing.mp3")
sus = pygame.mixer.Sound("Amogus.mp3")
  
flip = True

screen.fill(black)
first = True

while not done:  
 
    screen.fill(black)
    move = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                move = True
                
                
    if move == True:
        pygame.draw.polygon
        pygame.draw.rect(screen, black, [x, y, 70, 70]) 
        x+=10
        pygame.draw.rect(screen, grey, [x, y, 70, 70]) 
    
    
    # ---------Displays the text---------
    pygame.display.set_caption('Show Text')
    font = pygame.font.Font('freesansbold.ttf', 70)
    text = font.render("TEXT", True, black, grey)
    textRect = text.get_rect()
    textRect.center = (300, 50)
    display_surface.blit(text, textRect)
    
    # pygame.draw.ellipse(screen, color, [100, 100, 70, 70]) 
    
    # pygame.draw.rect(screen,yellow,[x,100,100,50])
    # pygame.draw.ellipse(screen,red,[x, 100, 100, 100])
    
    # img1 = pygame.transform.rotate(img1, 10)

    rotated_image = pygame.transform.rotate(image, 10)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

    screen.blit(rotated_image, rotated_image_rect)
    # img1 = pygame.transform.scale(img1, (100,100))
    
    # screen.blit(img1, (x, 100))
    
    pygame.draw.rect(screen,blue,[600,100,50,150])
    pygame.draw.rect(screen,green,[50,100,50,150])
    if first == True:
        pygame.mixer.Sound.play(sus)
        pygame.mixer.music.stop()
        first = False

    if (x >= 500):
        # pygame.mixer.music.stop()
        pygame.mixer.Sound.play(boing)
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(sus)
        flip = False
    
    if (x <= 100):
        # pygame.mixer.music.stop()
        pygame.mixer.Sound.play(boing)
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(sus)
        flip = True
        
    if flip == True:
        x += 10
    else:
        x -= 10
    
    
    time.sleep(0.1)
    
    pygame.display.flip()  
