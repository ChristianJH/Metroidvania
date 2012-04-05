
import os

import pygame
from pygame.locals import *
from pygame.sprite import Sprite

scale = 2

SCREEN = 256*scale,224*scale

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

class PlayerTiles(TileSheet):
    _map = {
        "face_left" : (0,1),
        "face_right" : (0,2)}

    def __init__(self, image, size):
        self.image = image
        self.w,self.h = size

        
        self.tilemap = {}
        for tile,coord in self._map.items():
            if coord:
                x,y = coord
                self.tilemap[tile] = image.subsurface(x*self.w, y*self.h, self.w, self.h)

    def get(self, image):
        return self.tilemap.get(image)
    

class Player(Sprite):
    def __init__(self, tilesheet, facing):
        Sprite.__init__(self)
        self.tilesheet = tilesheet
        self.facing = facing
        if self.facing == "left":
            self.image = self.tilesheet.get("face_left")
        elif self.facing == "right":
            self.image = self.tilesheet.get("face_right")        
        self.rect = self.image.get_rect(center=(.5*SCREEN[0],.66*SCREEN[1]))


class Level(object):
    def __init__(self, name, tilesheet):
        path = os.path.join("data", "levels", name) + ".lvl"
        f = open(path, "r")
        data = f.read().replace("\r", "").strip().split("\n")
        f.close()

        self.image = tilesheet.render(data)
        

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN)
    pygame.key.set_repeat(50,50)
    facing = "right"
    player_width,player_height = 30,38
    img_tiles = load_image("zelda2nestiles", (0,200,255))
    tilesheet = TileSheet(img_tiles, (16, 16))
    
    player_tiles = load_image("images", (255,255,255))
    player_tilesheet = PlayerTiles(player_tiles, (player_width, player_height))

    level = Level("level1", tilesheet)
    player = Player(player_tilesheet,facing)
    player_right = (screen.get_width()+player_width)/2
    player_left = (screen.get_width()-player_width)/2
    player_top = (screen.get_height()*.66-player_height/2)
    player_bottom = (screen.get_height()*.66+player_height/2)
    off_x, off_y = 0,0
    
    
    
    # off_x, off_y = player.image.get_rect()  
    """
    bound_x = level.image.get_width() - (screen.get_width()-player_width)/2
    """
    
    
    
    bound_x = level.image.get_width()
        
        
        
    bound_y = level.image.get_height()
        
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
                facing = "left"
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                off_x -= 5
                facing = "right"
            elif event.type == KEYDOWN and event.key == K_UP:
                off_y += 5
            elif event.type == KEYDOWN and event.key == K_DOWN:
                off_y -= 5
        
        if off_x > player_left:
            off_x = player_left
        elif off_x < -bound_x+player_right:
            off_x = -bound_x+player_right
        if off_y > player_top:
            off_y = player_top        
        elif off_y < -bound_y + player_bottom:
            off_y = -bound_y + player_bottom
        """
        if off_y > 0:
            off_y = 0
        elif off_y < -bound_y:
            off_y = -bound_y

        print off_x, off_y, bound_x
    
        """
        print off_x
                
        screen.fill((80,80,80))
        screen.blit(level.image, (off_x,off_y))
        player = Player(player_tilesheet, facing)
               
        screen.blit(player.image, player.rect)

        pygame.display.flip()
        clock.tick(30)
        
if __name__ == "__main__":
    main()
    pygame.quit()
    print "Byebye"

