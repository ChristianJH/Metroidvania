
import os

import pygame
from pygame.locals import *
from pygame.sprite import Sprite


scale = 1

FPS = 1000

SCREEN = 256*scale,224*scale

def rel_rect(rect,parent):
    return Rect((rect.x-parent.x, rect.y-parent.y), rect.size)

def load_image(name, colorkey=None):
    path = os.path.join("data", "images", name) + ".bmp"

    image = pygame.image.load(path).convert()
    if colorkey:
        image.set_colorkey(colorkey)
    return image

class Camera(object):
    def __init__(self, target, bounds, size):
        self.bounds = bounds
        self.rect = Rect((0,0), size)

    def update(self, target):
        self.rect.center = target.center
        self.rect.clamp_ip(self.bounds)
    def draw_background(self, surf, bg):
        surf.blit(bg, (-self.rect.x,-self.rect.y))
    def draw_sprite(self, surf, sprite):
        if self.rect.colliderect(sprite.rect):
            surf.blit(sprite.image,rel_rect(sprite.rect, self.rect))

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
        print "PRINTT"

    

class PlayerTiles(TileSheet):
    _map = {
        "face_left" : (0,1),
        "face_right" : (0,2)}

    def __init__(self, image, size, off_x, off_y):
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
    def __init__(self, tilesheet, facing,playerx,playery):
        Sprite.__init__(self)
        self.tilesheet = tilesheet
        self.facing = facing
        if self.facing == "left":
            self.image = self.tilesheet.get("face_left")
        elif self.facing == "right":
            self.image = self.tilesheet.get("face_right")        
        self.rect = self.image.get_rect(center=(0+playerx,playery))


class Level(object):
    def __init__(self, name, tilesheet):
        path = os.path.join("data", "levels", name) + ".lvl"
        f = open(path, "r")
        data = f.read().replace("\r", "").strip().split("\n")
        f.close()

        self.image = tilesheet.render(data)
        
        self.bounds = Rect((0,0),(100,100))

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN)
    pygame.key.set_repeat(50,50)
    off_x, off_y = 0,0
    facing = "right"
    player_width,player_height = 30,38
    img_tiles = load_image("zelda2nestiles", (0,200,255))
    tilesheet = TileSheet(img_tiles, (16, 16), off_x, off_y)


    player_tiles = load_image("images", (255,255,255))
    player_tilesheet = PlayerTiles(player_tiles, (player_width, player_height), off_x, off_y)

    level = Level("level1", tilesheet)
    player = Player(player_tilesheet,facing, off_x, off_y)

    camera = Camera(player, level.bounds, (40,40)) 

    #player_right = (screen.get_width()+player_width)/2
    #player_left = (screen.get_width()-player_width)/2
    #player_top = (screen.get_height()*.66-player_height/2)
    #player_bottom = (screen.get_height()*.66+player_height/2)

    
    
    # off_x, off_y = player.image.get_rect()  
    """
    bound_x = level.image.get_width() - (screen.get_width()-player_width)/2
    """
    
    
    
    bound_x = level.image.get_width()
    
    playerx = 100
    playery = 100   

    xstartspeed = 2
    xspeed = 0
    xaccelrate = .25
    daccelrate = .2
    xmaxspeed = 4  
    slowing = False
    moving = False    

    jumping = False
    gravityaccel = 0.5
    startjumpspeed = 10
    jumpspeed = 10   
        
    bound_y = level.image.get_height()
        
    done = False
    clock = pygame.time.Clock()
    while not done:
        
    
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            if event.type == KEYUP and event.key == K_ESCAPE:
                done = True
            if event.type == KEYDOWN and event.key == K_LEFT:
                slowing = False
                moving = True
                if xspeed == 0:
                    xspeed = xstartspeed
                playerx -= xspeed
                if xspeed < xmaxspeed:
                    xspeed += xaccelrate
                facing = "left"
            if event.type == KEYDOWN and event.key == K_RIGHT:
                slowing = False
                moving = True
                playerx += xspeed
                if xspeed < xmaxspeed:
                    xspeed += xaccelrate
                facing = "right"
            if event.type == KEYDOWN and event.key == K_SPACE and jumping == False:
                jumping = True
                startheight = playery
            if event.type == KEYUP and event.key == K_LEFT and facing == "left":
                slowing = True
                moving = False
            if event.type == KEYUP and event.key == K_RIGHT and facing == "right":
                slowing = True
                moving = False
            #if event.type == KEYDOWN and event.key == K_DOWN:
                #playery += 5

        if moving == True:
            if xspeed < xmaxspeed:
                xspeed += xaccelrate
            if facing == "left":
                playerx -= xspeed
            elif facing == "right":
                playerx += xspeed

        if slowing == True:
            if xspeed > 0:
                xspeed -= daccelrate
                if facing == "left":
                    playerx -= xspeed
                elif facing == "right":
                    playerx += xspeed
            elif xspeed < 0:
                xspeed = 0
                slowing = False

        if jumping == True:
            playery -= jumpspeed
            jumpspeed -= gravityaccel
            if playery >= startheight:
                playery = startheight
                jumpspeed = startjumpspeed
                jumping = False 
            #print jumpspeed

        
        #if off_x > player_left:
            #off_x = player_left
        #elif off_x < -bound_x+player_right:
            #off_x = -bound_x+player_right
        #if off_y > player_top:
            #off_y = player_top        
        #elif off_y < -bound_y + player_bottom:
            #off_y = -bound_y + player_bottom
        """
        if off_y > 0:
            off_y = 0
        elif off_y < -bound_y:
            off_y = -bound_y

        print off_x, off_y, bound_x
    
        """
        #print off_x
        #print xspeed        
        
        screen.fill((80,80,80))
        screen.blit(level.image, (off_x,off_y))
        player = Player(player_tilesheet, facing, playerx, playery)
        blocks = Block(off_x, off_y, 1, 80, 80)
        
        #off_x,off_y=playerx,playery



        screen.blit(blocks.image, blocks.rect)      
        screen.blit(player.image, player.rect)
        playergroup = pygame.sprite.Group(player)
        blockgroup = pygame.sprite.Group(blocks) 
        
        #for sprite in tilesheet.OrangeBlocks:
            #print sprite.rect
        #print player.ghost
        for i in range(2):
            blockgroup.add(Block(off_x, off_y, i, 80, 80))
        #Block(off_x, off_y, 1)
        #print blockgroup

        if pygame.sprite.groupcollide(playergroup, tilesheet.OrangeBlocks, False, False):
            print "COLLIDES"
        else:
            print "NO"




        pygame.display.flip()
        clock.tick(FPS)
        
if __name__ == "__main__":
    main()
    pygame.quit()
    print "Byebye"

