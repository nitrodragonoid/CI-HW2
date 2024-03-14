import time
from random import random
import pygame
import random
import math
import sys 

# Pygame stuff
GRAY = (155, 155, 155)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
TEXT = (255, 255, 255)
PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)

LIGHTBLUE = (0, 0, 127)

X = 1300
Y = 800
pygame.init()
screen = pygame.display.set_mode((X,Y))
game_over = False

image = 'crewmate.png'
img1 = pygame.image.load(image)
img1 = pygame.transform.scale(img1, (25,25))

image = 'imposter.png'
img2 = pygame.image.load(image)
img2 = pygame.transform.scale(img2, (25,25))

image = 'dead.png'
img3 = pygame.image.load(image)
img3 = pygame.transform.scale(img3, (25,25))

image = 'knife.png'
img4 = pygame.image.load(image)
img4 = pygame.transform.scale(img4, (25,25))

# buttons
startButton = [10,10, 100,50]

BirdsButton = [210,50, 100,50]
BirdsINC = [320, 50, 50, 50]
BirdsDEC = [150, 50, 50, 50]

BetaButton = [460,50, 100,50]
BetaINC = [570, 50, 50, 50]
BetaDEC = [400, 50, 50, 50]

AlphaButton = [710, 50, 100,50]
AlphaINC = [820, 50, 50, 50]
AlphaDEC = [650, 50, 50, 50]

GammaButton = [960,50, 100,50]
GammaINC = [1070, 50, 50, 50]
GammaDEC = [900, 50, 50, 50]

#sounds
bgm = pygame.mixer.Sound("SneakySnitch.mp3")
sus = pygame.mixer.Sound("start.mp3")
kill = pygame.mixer.Sound("kill.mp3")

#initalitizing the birds
initial = [300,300]
inertia = [-3,-4]

birds = []
velocities = []
Pbests = []
bestPos = []

food = [] #food position

obstacles = []
for i in range(0,X,10):
    obstacles.append([i,-10])
    obstacles.append([i,Y-15])
for j in range(0,Y,10):
    obstacles.append([-10,j])
    obstacles.append([X-15,j])

# Adjust these:
numberOfBirds = 30
alpha = 1.2
beta = 1
gamma = 0.8

def getDist(pos, food):
    return ((food[0]-pos[0])**2 + (food[1]-pos[1])**2)**(1/2)

def Gbest(pbests,bestPos):
    return bestPos[pbests.index(min(pbests))]



#Simulation runner
start = False
# pygame.mixer.Sound.play(bgm,loops = -1)
while game_over == False:
    screen.fill(BLACK)
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.MOUSEBUTTONDOWN: 

            mouse = pygame.mouse.get_pos() 
            if start == False and startButton[0] <= mouse[0] <= startButton[0]+startButton[2] and startButton[1] <= mouse[1] <= startButton[1]+startButton[3]: 
                start = True
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(sus)
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(bgm,loops = -1)
                for i in range(numberOfBirds):
                    birds.append([random.randint(0, 700),random.randint(0, 700)])
                    velocities.append([random.randint(0, 11),random.randint(0, 11)])
                    bestPos.append(initial)
                    d = []
                    for f in food:
                        d.append(getDist(initial,f))
                    Pbests.append(min(d))
                    
            elif start == False and BirdsINC[0] <= mouse[0] <= BirdsINC[0]+BirdsINC[2] and BirdsINC[1] <= mouse[1] <= BirdsINC[1]+BirdsINC[3]: 
                numberOfBirds += 1
            elif start == False and BirdsDEC[0] <= mouse[0] <= BirdsDEC[0]+BirdsDEC[2] and BirdsDEC[1] <= mouse[1] <= BirdsDEC[1]+BirdsDEC[3]: 
                numberOfBirds -= 1
                
            elif start == False and BetaINC[0] <= mouse[0] <= BetaINC[0]+BetaINC[2] and BetaINC[1] <= mouse[1] <= BetaINC[1]+BetaINC[3]: 
                beta += 0.1
            elif start == False and BetaDEC[0] <= mouse[0] <= BetaDEC[0]+BetaDEC[2] and BetaDEC[1] <= mouse[1] <= BetaDEC[1]+BetaDEC[3]: 
                beta -= 0.1
                
            elif start == False and AlphaINC[0] <= mouse[0] <= AlphaINC[0]+AlphaINC[2] and AlphaINC[1] <= mouse[1] <= AlphaINC[1]+AlphaINC[3]: 
                alpha += 0.1
            elif start == False and AlphaDEC[0] <= mouse[0] <= AlphaDEC[0]+AlphaDEC[2] and AlphaDEC[1] <= mouse[1] <= AlphaDEC[1]+AlphaDEC[3]: 
                alpha -= 0.1
                
            elif start == False and GammaINC[0] <= mouse[0] <= GammaINC[0]+GammaINC[2] and GammaINC[1] <= mouse[1] <= GammaINC[1]+GammaINC[3]: 
                gamma += 0.1
            elif start == False and GammaDEC[0] <= mouse[0] <= GammaDEC[0]+GammaDEC[2] and GammaDEC[1] <= mouse[1] <= GammaDEC[1]+GammaDEC[3]: 
                gamma -= 0.1
                
            elif event.button == 1:
                food.append([mouse[0],mouse[1],100])
            elif event.button == 3:
                obstacles.append([mouse[0],mouse[1]])
     
    #drawing the obstacles
    for o in obstacles:
        pygame.draw.rect(screen, GRAY, [o[0], o[1], 25, 25])
        
    #drawing the food source
    for f in food:
        if f[2] > 0:
            screen.blit(img2, (f[0], f[1]))
        else:
            screen.blit(img3, (f[0], f[1]))
            
    if start == False:
       
        pygame.draw.rect(screen, RED, startButton)
        
        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render("START", True, YELLOW, RED)
        screen.blit(text, (startButton[0], startButton[1]))
        
        #birds
        text = font.render("Birds", True, BLACK, WHITE)
        screen.blit(text, (BirdsButton[0], 10))
        
        pygame.draw.rect(screen, PURPLE, BirdsButton)
        text = font.render(str(numberOfBirds), True, TEXT, PURPLE)
        screen.blit(text, (BirdsButton[0], BirdsButton[1]))
        
        pygame.draw.rect(screen, BLUE, BirdsINC)
        text = font.render("+", True, TEXT, BLUE)
        screen.blit(text, (BirdsINC[0]+10, BirdsINC[1]))
        
        pygame.draw.rect(screen, BLUE, BirdsDEC)
        text = font.render("-", True, TEXT, BLUE)
        screen.blit(text, (BirdsDEC[0]+10, BirdsDEC[1]))
        
        #beta
        beta = round(beta, 2)
        text = font.render("Beta", True, BLACK, WHITE)
        screen.blit(text, (BetaButton[0], 10))
        
        pygame.draw.rect(screen, LIGHTBLUE, BetaButton)
        text = font.render(str(beta), True, TEXT, LIGHTBLUE)
        screen.blit(text, (BetaButton[0], BetaButton[1]))
        
        pygame.draw.rect(screen, BLUE, BetaINC)
        text = font.render("+", True, TEXT, BLUE)
        screen.blit(text, (BetaINC[0]+10, BetaINC[1]))
        
        pygame.draw.rect(screen, BLUE, BetaDEC)
        text = font.render("-", True, TEXT, BLUE)
        screen.blit(text, (BetaDEC[0]+10, BetaDEC[1]))
        
        #alpha
        alpha = round(alpha, 2)
        text = font.render("Alpha", True, BLACK, WHITE)
        screen.blit(text, (AlphaButton[0], 10))
        
        pygame.draw.rect(screen, RED, AlphaButton)
        text = font.render(str(alpha), True, TEXT, RED)
        screen.blit(text, (AlphaButton[0], AlphaButton[1]))
        
        pygame.draw.rect(screen, BLUE, AlphaINC)
        text = font.render("+", True, TEXT, BLUE)
        screen.blit(text, (AlphaINC[0]+10, AlphaINC[1]))
        
        pygame.draw.rect(screen, BLUE, AlphaDEC)
        text = font.render("-", True, TEXT, BLUE)
        screen.blit(text, (AlphaDEC[0]+10, AlphaDEC[1]))
        
        #gamma
        gamma = round(gamma, 2)
        text = font.render("Gamma", True, BLACK, WHITE)
        screen.blit(text, (GammaButton[0], 10))
        
        pygame.draw.rect(screen, GREEN, GammaButton)
        text = font.render(str(gamma), True, TEXT, GREEN)
        screen.blit(text, (GammaButton[0], GammaButton[1]))
        
        pygame.draw.rect(screen, BLUE, GammaINC)
        text = font.render("+", True, TEXT, BLUE)
        screen.blit(text, (GammaINC[0]+10, GammaINC[1]))
        
        pygame.draw.rect(screen, BLUE, GammaDEC)
        text = font.render("-", True, TEXT, BLUE)
        screen.blit(text, (GammaDEC[0]+10, GammaDEC[1]))
        
        
        text = font.render("Right click to create obstacles and left click to create food", True, BLACK, WHITE)
        screen.blit(text, (250, 750))
    
    
    
                    
    if start == True:
        

        #PSO   
        for bird in range(len(birds)):
            #Update velocities 
            velocities[bird][0] = gamma*velocities[bird][0] + beta*random.random()*(Gbest(Pbests,bestPos)[0]-birds[bird][0]) + alpha*random.random()*(bestPos[bird][0]-birds[bird][0]) 
            velocities[bird][1] = gamma*velocities[bird][1] + beta*random.random()*(Gbest(Pbests,bestPos)[1]-birds[bird][1]) + alpha*random.random()*(bestPos[bird][1]-birds[bird][1])

            #Update positions
            newpos = [velocities[bird][0] + birds[bird][0], velocities[bird][1] + birds[bird][1]]
            
            #If moved near obstacle
            for o in obstacles:
                if getDist(newpos,o) <= 25: # check if near obstacle and repel from obstacle
                    velocities[bird][0] = gamma*velocities[bird][0] - beta*(newpos[0]-birds[bird][0])
                    velocities[bird][1] = gamma*velocities[bird][1] - beta*(newpos[1]-birds[bird][1]) 
            
            birds[bird] = newpos    

            #Find new distance and pdate the best fitness
            for f in food:
                dist = getDist(newpos, f)
                if f[2] > 0:
                    if dist < Pbests[bird]:
                        Pbests[bird] = dist
                        bestPos[bird] = newpos
                    if dist <= 20: # if near food decrease food value
                        f[2] -= 1
                        if f[2] == 0:
                            pygame.mixer.Sound.play(kill)
                            pygame.mixer.music.stop()
                            for b in range(len(birds)):
                                for f2 in food:
                                    newDist = getDist(birds[b], f2)
                                    if f2 != f:
                                        Pbests[b] = math.inf
                                        if newDist < Pbests[b]:
                                            Pbests[b] = newDist
                                            bestPos[bird] = initial


        #drawing all our birds
        for bird in birds:
            screen.blit(img1, (bird[0], bird[1]))
            
            for f in food: # if close to food take out knife
                dist = getDist(newpos, f)
                if dist <= 20 and f[2] > 0:
                    screen.blit(img4, (bird[0], bird[1]))

    time.sleep(0.2)
    pygame.display.flip()
