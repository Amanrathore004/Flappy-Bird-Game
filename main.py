   
from json.tool import main
import random  # For generating random numbers
import sys
from turtle import Screen, width  # We will use sys.exit to the program
import pygame
from pygame.locals import *  # Basic pygame imports
from pygame import mixer

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'D:/flappy bird/sprites/bird1.png'
BACKGROUND = 'D:/flappy bird/sprites/background.png'
PIPE = 'D:/flappy bird/sprites/pipe.png'


def welcomeScreen():
    """"
    Show welcome image on the screen
    """
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int(SCREENWIDTH*0)
    messagey = int(SCREENHEIGHT*0)
    basex = 0
    while True:
        for event in pygame.event.get():
            # If user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                # If the user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()


def mainGame():
   
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0
# Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newPipe2[0]['y']}
    ]

    # my List of lower pipe
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newPipe2[1]['y']}
    ]

    pipeVelX = -0.2 

    playerVelY = -1
    playerMaxVelY = 0.1
    playerMinVelY = 3
    playerAccY = 0.1

    playerFlapAccv = -3.5 # velocity while flapping
    playerFlapped = False  # It is true only when the bird is flapping
   

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == k_up):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    GAME_SOUNDS['swoosh'].play()
                    playerFlapped = True
                    #GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return
        # check for score
        playerMidPas = playerx + GAME_SPRITES['player'].get_width()/2

        for pipe in upperPipes:
            pipeMidPas = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPas <= playerMidPas < pipeMidPas +4:
                score += 1
                print(f" Your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

       # move pipes to the left

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 0.1:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen , remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        """
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH- width)/2
       
        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
         """
        pygame.display.update()

       
def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery>GROUNDY -20 or playery<0:
        GAME_SOUNDS['hit'].play()
        return True        
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and (abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width() )):
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height()> pipe['y']) and (abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    return False
def getRandomPipe():
    """
    generate position of two Pipes(one botton straight and one toprotated) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset+random.randrange(0, int(SCREENHEIGHT -
                                 GAME_SPRITES['base'].get_height()-1.2*offset))
    pipeX = SCREENWIDTH+10
    y1 = pipeHeight-y2+offset
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}
    ]
    return pipe


if __name__ == "__main":
    # This will be the main point from where our game will start
    pygame.init()  # Initialize all pygame's modules

    FPSCLOCK = pygame.time.Clock()
    pygame.display.set.caption("Flappy Bird by Bajaj")
    GAME_SPRITES['numbers'] = (
        pygame.image.load('D:/flappy bird/sprites/0.png').convert_alpha(),
        pygame.image.load('D:/flappy bird/sprites/1.png').convert_alpha(),
        pygame.image.load('D:/flappy bird/sprites/2.png').convert_alpha(),
        pygame.image.load('D:/flappy bird/sprites/3.png').convert_alpha(),
        pygame.image.load('D:/flappy bird/sprites/4.png').convert_alpha(),
        pygame.image.load('D:/flappy bird/sprites/5.png').convert_alpha(),
        pygame.image.load('D:/flappy bird/sprites/6.png').convert_alpha(),
        pygame.image.load('D:/flappy bird/sprites/7.png').convert_alpha(),
        pygame.image.load('D:/flappy bird/sprites/8.png').convert_alpha(),
        pygame.image.load('D:/flappy bird/sprites/9.png').convert_alpha(),

    )
  
GAME_SPRITES['message'] = pygame.image.load(
     'D:/flappy bird/sprites/message.png').convert_alpha()
GAME_SPRITES['base'] = pygame.image.load(
    'D:/flappy bird/sprites/base.png').convert_alpha()
GAME_SPRITES['pipe'] = (
    pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
    pygame.image.load(PIPE).convert_alpha()
)


# game sounds 
mixer.init()
GAME_SOUNDS['hit'] = pygame.mixer.Sound('D:/flappy bird/audio/hit.wav')
GAME_SOUNDS['point'] = pygame.mixer.Sound('D:/flappy bird/audio/point.wav')
GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('D:/flappy bird/audio/swoosh.wav')



GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

while True:
    welcomeScreen()  # Shows welcome sreen to the user until he presses a button
    mainGame()  # this is the main game function
