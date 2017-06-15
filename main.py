import pygame
import time
import random
from pygame.locals import *


try:
    import android
except ImportError:
    android = None

pygame.init()

if android:
    android.init()
    android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

smallfont = pygame.font.SysFont("comicsansms", 25)   #FONT OBJECT

medfont = pygame.font.SysFont("comicsansms", 40)
largefont = pygame.font.SysFont("comicsansms", 55)

img = pygame.image.load('snakehead.png')

appleimg = pygame.image.load('apple.png')

block_size = 20
AppleThickness = 30

FPS = 20
direction = "right"


def main():


    intro = True

    while intro:

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         quit()
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_c:
        #             intro = False
        #         elif event.key == pygame.K_q:
        #             pygame.quit()
        #             quit()
        gameDisplay.fill(white)
        message_to_screen("Welcome to Snake Charm", green, -100, "large")
        message_to_screen("The objective of the game is to eat red apples", black, -30)
        message_to_screen("The more apples you eat the longer you get", black, 10)
        message_to_screen("If you run into your self or the edges you die!!!", black, 50)
        message_to_screen("Press c to play or p to pause or q to quit", black, 180)
        pygame.display.update()
        clock.tick(15)

def snake(block_size, snakelist):

    if direction == "right":
        head = pygame.transform.rotate(img, 270)
    elif direction == "left":
        head = pygame.transform.rotate(img, 90)
    elif direction == "up":
        head = img
    elif direction == "down":
        head = pygame.transform.rotate(img, 180)
    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))
    for XnY in snakelist[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])

def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width/2, display_height/2 + y_displace)
    gameDisplay.blit(textSurf, textRect)

def randAppleGen():
    randAppleX = round(random.randrange(0, display_width - AppleThickness))#/20.0)*20.0
    randAppleY = round(random.randrange(0, display_height - AppleThickness))#/20.0)*20.0
    return randAppleX, randAppleY

def score(score):
    text = smallfont.render("Score: " + str(score), True, black)
    gameDisplay.blit(text, [0, 0])

def pause():

    paused = True

    message_to_screen("Paused", black, -100, "large")
    message_to_screen("Press c to continue or q to quit", black, 25)
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        #gameDisplay.fill(white)

        clock.tick(5)
display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Charm')

icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)
pygame.display.update()

clock = pygame.time.Clock()



def gameLoop():
    global direction
    snakelist = []
    snakeLength = 1

    gameExit = False
    gameOver = False

    lead_x = display_width/2
    lead_y = display_height/2
    lead_x_change = 10
    lead_y_change = 0

    randAppleX, randAppleY = randAppleGen()
    randAppleX, randAppleY = randAppleGen()

    while not gameExit:

        if gameOver == True:
            message_to_screen("GAME OVER", red, -50, size = "large")
            message_to_screen("Press c to Play Again or q to Quit", black, 50, size = "medium")
            pygame.display.update()

        while gameOver == True:
            direction = "right"

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False

                    if event.key == pygame.K_c:
                        gameLoop()
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:

                    if direction == "right":
                        continue
                    else:
                        direction = "left"
                        lead_x_change = -block_size
                        lead_y_change = 0

                elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:

                    if direction == "left":
                        continue
                    else:
                        direction = "right"
                        lead_x_change = block_size
                        lead_y_change = 0

                elif event.key == pygame.K_UP or event.key == pygame.K_KP8:

                    if direction == "down":
                        continue
                    else:
                        direction = "up"
                        lead_y_change = -block_size
                        lead_x_change = 0

                elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                    if direction == "up":
                        continue
                    else:
                        direction = "down"
                        lead_y_change = block_size
                        lead_x_change = 0

                elif event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    pause()

        if lead_x >= display_width or lead_x < 0 or lead_y >=display_height or lead_y < 0:
            gameOver = True
            # for i in range(0, len(snakelist)-1):
            #     snakelist[i].first -= display_width

            pygame.display.update()



        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(white)
        #pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, AppleThickness, AppleThickness])
        gameDisplay.blit(appleimg, (randAppleX, randAppleY))
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakelist.append(snakeHead)

        if len(snakelist) > snakeLength:
            del snakelist[0]

        for eachSegment in snakelist[ : -1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(block_size, snakelist)

        score(snakeLength - 1)
        pygame.display.update()

        if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:
            if lead_y > randAppleY and lead_y < randAppleY + AppleThickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:
               randAppleX, randAppleY = randAppleGen()
               randAppleX, randAppleY = randAppleGen()
               snakeLength += 1
        clock.tick(FPS)
    pygame.quit()
    quit()

# main()
gameLoop()


# This isn't run on Android.
if __name__ == "__main__":
    main()
