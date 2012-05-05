#!/usr/bin/env python

import pygame
import sys
from pygame.locals import *

## Settings

FPS = 1

#Colors
BLACK = 0,0,0
WHITE = 255,255,255

class Block(pygame.sprite.Sprite):
    def __init__(self, xPosition):
        pygame.sprite.Sprite.__init__(self)
        self.old = (0, 0, 0, 0)
        self.image = pygame.image.load('square.bmp')
        

def game(width,height,scale):

    screen = pygame.display.set_mode((width*scale, height*scale))

    clock = pygame.time.Clock()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == KEYUP and event.key == K_ESCAPE:
                done = True
            screen.fill(WHITE)
            print "Hi"
            pygame.display.flip()
            clock.tick(FPS)

game(256,224,1)


