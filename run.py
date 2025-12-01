import pygame, sys 
from pygame.locals import *
from constants import *
from random import randint

pygame.init()

class MyGameText:
    def __init__(self):
        print("Inicializando biblioteca...")
        
    def create_text(self, msg, size, color, font=None):

        if font == None:
            font = "comicsansms"
            
        font = pygame.font.SysFont(font, size, True, False)
        mensagem = f"{msg}"
        text_formatted = font.render(mensagem, False, color)
        return text_formatted

mgt = MyGameText()

window = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))

cursorX = 0
cursorY = 0

targetX = randint(10, 1000-45)
targetY = randint(10, 600)

target = pygame.image.load("Assets/CircleTarget.png").convert_alpha()
target = pygame.transform.scale(target, (64*1.8, 64*1.8))

counter = 1000
speed = 2.5

clock = pygame.time.Clock()

debug = False

while counter:
    window.fill(COLORS["gray"])
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    delta_time = clock.tick(FPS) / 1000

    XeY = pygame.mouse.get_pos()
    cursorX, cursorY = XeY[0], XeY[1]

    crosshair = pygame.image.load(r"Assets/crosshair.png").convert_alpha()
    crosshair = pygame.transform.scale(crosshair, (32//1.3, 32//1.3))
    crosshairRect = crosshair.get_rect(center = (cursorX, cursorY))

    targetRect = target.get_rect(center = (targetX, targetY))

    timer = mgt.create_text(f"Timer:{counter}", 25, (0,0,0))
    current_FPS = mgt.create_text(f"FPS:{FPS}", 25, (0,100,0))
    current_speed = mgt.create_text(f"SPEED:{speed}", 25, (0,100,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            
            if event.key == K_LEFT:
                FPS = 30
            if event.key == K_DOWN:
                FPS = 60
            if event.key == K_RIGHT:
                FPS = 120
            
            if event.key == K_F3:
                if debug == True:
                    debug = False
                else:
                    debug = True
        
        if event.type == MOUSEBUTTONDOWN:
            if crosshairRect.colliderect(targetRect):
                counter += 100
                targetX = randint(10, 1000-45)
                targetY = randint(10, 600)

    if FPS >= 120:
        if counter >= 2000:
            speed = 1.5
            counter -= speed
        else:
            speed = 0.5
            counter -= speed
    elif FPS >= 60:
        if counter >= 2000:
            speed = 2
            counter -= speed
        else:
            speed = 1
            counter -= speed
    else:
        if counter >= 2000:
            speed = 2.5
            counter -= speed
        else:
            speed = 1.5
            counter -= speed

    window.blit(target, targetRect)
    window.blit(crosshair, crosshairRect)
    window.blit(timer, (0, 0))
    if debug == True:
        window.blit(current_FPS, (875, 10))
        window.blit(current_speed, (865, 35))
    else:
        pass
    pygame.display.flip()