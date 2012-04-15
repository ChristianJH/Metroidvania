import os
import pygame
from pygame.locals import *
from pygame.sprite import Sprite

class Block(Sprite):
    def __init__(self, off_x, off_y, type, width, height):
        Sprite.__init__(self)
        self.width = width
        self.height = height
        self.color = (255,255,255)
        self.rect = pygame.Rect(off_x,off_y,self.width,self.height)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill(self.color)
        self.type = type
    #def collide(self):
        
       
class SolidBlock(Block):
    def __init__(self):
        Block.__init__(self)
    def collide(self):
        print "PRINT"
