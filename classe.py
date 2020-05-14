import pygame
from pygame import *
import pytmx


#couleurs
BLEU  = (  0,  0,255)
ROUGE = (255,  0,  0)
VERT  = (  0,255,  0)
BLANC = (255,255,255)
NOIR  = (  0,  0,  0)

def deplacement(perso,acceleration):
    vx , vy = perso.deplacement
    ax , ay = acceleration
    perso.deplacement = (vx + ax , vy + ay)

def changer_position(perso,dt):
    vx , vy = perso.deplacement
    x , y = perso.pos
    x += vx * dt
    y += vy * dt
    perso.pos = (x,y)
    perso.rect.topleft = perso.pos
    
    
    
class hero(pygame.sprite.Sprite):
    def __init__(self,vie,attaque,vitesse):
        super().__init__()
        self.vie = vie
        self.vie_max = vie
        self.att = attaque
        self.vitesse = vitesse
        self.deplacement = (0,0)
        self.image = pygame.image.load('image/perso/perso_droite1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(64,64))
        self.rect = self.image.get_rect()
        self.rect.x = 640
        self.rect.y = 480
        self.pos = self.rect.topleft

    


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

        

        
        
