import os
import pygame
from pygame.locals import *
from pygame.sprite import Sprite

import block
from block import Block, SolidBlock



class TileSheet(object):
    _map = {
        ".": None,
        ";": (1,1),
        "#": (12,2),
        "&": (6,1),
        "*": (5,7),
        "^": (5,6),
    }
        
    def __init__(self, image, size, off_x, off_y):
        self.image = image
        self.w,self.h = size
        self.off_x,self.off_y = off_x, off_y

        self.OrangeBlocks = pygame.sprite.Group()

        self.tilemap = {}
        for tile,coord in self._map.items():
            if coord:
                x,y = coord
                self.tilemap[tile] = image.subsurface(x*self.w, y*self.h, self.w, self.h)
            

    
    def render(self, data):

        rows = len(data)
        cols = len(data[0])

        surf = pygame.Surface((cols * self.w, rows *self.h))


        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                tile = self.tilemap.get(cell)
                key = self.tilemap.get(x)
                if tile:
                    surf.blit(tile, (x*self.w, y*self.h))
                    if cell == ";":
                        cell = Block(x*self.w,y*self.h, 3, self.w, self.h)
                        self.OrangeBlocks.add(cell)
                    else:
                        pass

        for sprite in self.OrangeBlocks:
            print sprite.rect
        return surf
    

class Level(object):
    def __init__(self, name, tilesheet):
        path = os.path.join("data", "levels", name) + ".lvl"
        f = open(path, "r")
        data = f.read().replace("\r", "").strip().split("\n")
        f.close()

        self.image = tilesheet.render(data)
        
        self.bounds = Rect((0,0),(100,100))

