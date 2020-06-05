import pygame
from pygame import *
import pytmx

from classe import*



class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha = True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render (self,surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

    


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(1280 / 2)
        y = -target.rect.centery + int(720 / 2)


        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - 1280), x)  # right
        y = max(-(self.height - 720), y)  # bottom
        self.camera = pygame.Rect(x, y, self.width, self.height)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self,game, x, y, w, h):
        self.groups = game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.rect = pygame.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vx = 0
            sprite.hit_rect.centerx = sprite.x
    if dir == 'y':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vy = 0
            sprite.hit_rect.centery = sprite.y

            




class Portal(pygame.sprite.Sprite):
    def __init__(self,game,direction,x,y,w,h):
        self.group = game.portal_group
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.group)
        self.rect = pygame.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        
    def update(self):
        if collide_with_object(self.game.perso,self.group) == True:
            self.game.generer_map(self.direction)

def collide_with_object(sprite,group):
    hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        print('hit')
        return(True)


                
    
            
    

