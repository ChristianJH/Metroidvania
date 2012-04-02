
import os

import pygame
from pygame.locals import *

def load_image(name, colorkey=None):
    path = os.path.join("data", "images", name) + ".bmp"

    image = pygame.image.load(path).convert()
    if colorkey:
        image.set_colorkey(colorkey)
    return image

class TileSheet(object):
    _map = {
        ".": None,
        ";": (1,1),
        "#": (12,2),
        "&": (6,1),
        "*": (5,7),
        "^": (5,6),
    }
        
    def __init__(self, image, size):
        self.image = image
        self.w,self.h = size


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
                if tile:
                    surf.blit(tile, (x*self.w, y*self.h))

        return surf

class Level(object):
    def __init__(self, name, tilesheet):
        path = os.path.join("data", "levels", name) + ".lvl"
        f = open(path, "r")
        data = f.read().replace("\r", "").strip().split("\n")
        f.close()

        self.image = tilesheet.render(data)

def main():
    pygame.init()
    screen = pygame.display.set_mode((200,200))
    pygame.key.set_repeat(50,50)
    

    img_tiles = load_image("zelda2nestiles", (0,200,255))
    tilesheet = TileSheet(img_tiles, (16, 16))
    level = Level("level1", tilesheet)
    off_x, off_y = 0,0
    bound_x = level.image.get_width() - screen.get_width()
    bound_y = level.image.get_height() - screen.get_height()

    done = False
    clock = pygame.time.Clock()
    while not done:

        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == KEYUP and event.key == K_ESCAPE:
                done = True
            elif event.type == KEYDOWN and event.key == K_LEFT:
                off_x += 5
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                off_x -= 5
            elif event.type == KEYDOWN and event.key == K_UP:
                off_y += 5
            elif event.type == KEYDOWN and event.key == K_DOWN:
                off_y -= 5
        
        if off_x > 0:
            off_x = 0
        elif off_x < -bound_x:
            off_x = -bound_x
        if off_y > 0:
            off_y = 0
        elif off_y < -bound_y:
            off_y = -bound_y
        print off_x, off_y, bound_x


        screen.fill((80,80,80))
        screen.blit(level.image, (off_x,off_y))


        pygame.display.flip()
        clock.tick(30)
        
if __name__ == "__main__":
    main()
    print "Byebye"

