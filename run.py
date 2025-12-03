import pygame, sys, os
from pygame.locals import *
from constants import *
from random import randint

pygame.init()

class MyGameText:
    def __init__(self):
        pass
        
    def create_text(self, msg, size, color, font=None):

        if font == None:
            font = "comicsansms"
            
        font = pygame.font.SysFont(font, size, True, False)
        mensagem = f"{msg}"
        text_formatted = font.render(mensagem, False, color)
        return text_formatted

mgt = MyGameText()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.imageX = randint(10, 1000-45)
        self.imageY = randint(10, 600)
                               
        self.image = pygame.image.load("Assets/CircleTarget.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (64*1.8, 64*1.8))
        self.rect = self.image.get_rect(center = (self.imageX, self.imageY))
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        self.rect.x = randint(10, 1000-45)
        self.rect.y = randint(10, 600)

class CrossHair(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        XeY = pygame.mouse.get_pos()

        self.image = pygame.image.load(r"Assets/crosshair.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (32//1.3, 32//1.3))
        self.rect = self.image.get_rect()
        self.rect.center = XeY
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        XeY = pygame.mouse.get_pos()
        self.rect.center = XeY
        
target = Target()
crosshair = CrossHair()

target_group = pygame.sprite.Group()
crosshair_group = pygame.sprite.Group()

target_group.add(target)
crosshair_group.add(crosshair)

all_my_sprites = pygame.sprite.Group()
all_my_sprites.add(target_group)
all_my_sprites.add(crosshair_group)

counter = 1000
speed = 2.5

clock = pygame.time.Clock()

debugMode = False

while counter:
    window.fill(COLORS["gray"])
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    delta_time = clock.tick(FPS) / 1000

    XeY = pygame.mouse.get_pos()
    cursorX, cursorY = XeY[0], XeY[1]

    timer = mgt.create_text(f"Timer:{int(counter)}", 25, (0,0,0))
    current_FPS = mgt.create_text(f"FPS:{int(clock.get_fps())}", 25, (0,175,0))
    current_speed = mgt.create_text(f"SPEED:{speed}", 25, (0,175,0))

    crosshair.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == MOUSEBUTTONDOWN:
            if pygame.sprite.spritecollide(crosshair, target_group, False, pygame.sprite.collide_mask):
                counter += 150
                target.update()

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
                if debugMode == True:
                    debugMode = False
                else:
                    debugMode = True

    if FPS >= 120:
        if counter >= 2000:
            speed = 1.2
            counter -= speed
        else:
            speed = 0.5
            counter -= speed
    elif FPS >= 60:
        if counter >= 2000:
            speed = 1.7
            counter -= speed
        else:
            speed = 1
            counter -= speed
    else:
        if counter >= 2000:
            speed = 2.2
            counter -= speed
        else:
            speed = 1.5
            counter -= speed

    window.blit(timer, (0, 0))

    if debugMode == True:
        window.blit(current_FPS, (865, 10))
        window.blit(current_speed, (860, 35))
    else:
        pass

    all_my_sprites.draw(window)
    pygame.display.flip()