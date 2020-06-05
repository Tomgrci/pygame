import pygame
from pygame import *
import pytmx
from random import *

from classe_map import*
from stats import *


#couleurs
BLEU  = (  0,  0,255)
ROUGE = (255,  0,  0)
VERT  = (  0,255,  0)
BLANC = (255,255,255)
NOIR  = (  0,  0,  0)


    
    
    
class Hero(pygame.sprite.Sprite):
    def __init__(self,game,vie,attaque,vitesse):
        super().__init__()
        self.vie = vie
        self.vie_max = vie
        self.att = attaque
        self.vitesse = vitesse
        self.image = pygame.image.load('image/perso/perso_droite1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(64,64))
        self.rect = self.image.get_rect()
        self.game = game
        
        self.x = self.rect.x
        self.y = self.rect.y
        self.vx = 0
        self.vy = 0
        self.hit_rect = pygame.Rect(0,0,40,40)
        self.hit_rect.center = self.rect.center
        
        self.walls = self.game.walls

    def spawn(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.get_keys()
        self.game.actualiser_time()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        
        self.hit_rect.centerx = self.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

        self.game.portal_group.update()
        self.game.mob_group.update()

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -self.vitesse
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = self.vitesse
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vy = -self.vitesse
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vy = self.vitesse
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071



class Game:
    def __init__(self):
        self.walls = pygame.sprite.Group()
        self.portal_group = pygame.sprite.Group()
        self.mob_group = pygame.sprite.Group()
                
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(self.fps)/1000

        self.largeur_fenetre = 1280
        self.hauteur_fenetre = 720
        self.fenetre = pygame.display.set_mode((self.largeur_fenetre, self.hauteur_fenetre))

        self.perso = Hero(self, 100, 5, 400)

        self.combat_start = False

    def actualiser_time(self):
        self.dt = self.clock.tick(self.fps)/1000
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))

    def generer_map(self, filename):

        self.walls = pygame.sprite.Group()
        self.portal_group = pygame.sprite.Group()
        
        self.niveau = TiledMap('chunk/'+filename)
        self.camera = Camera(self.niveau.width, self.niveau.height)
        self.map_img = self.niveau.make_map()
        self.map_rect = self.map_img.get_rect()

        for tile_object in self.niveau.tmxdata.objects:
            if tile_object.name == 'spawn':
                self.perso.spawn(tile_object.x, tile_object.y)
                
            if tile_object.name == 'mur':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                
            if tile_object.name == 'portal':
                Portal(self, tile_object.type, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

            if tile_object.name == 'sapwn_monstre':
                x = randint(0, (len(all_mob))-1)
                all_mob[x]
                Mob(self, all_mob[x], tile_object.x, tile_object.y)

    def update(self):
        self.perso.update()
        self.camera.update(self.perso)

    def update_combat(self):
        combat(game.perso, )

    def affichage(self):
        self.fenetre.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        self.fenetre.blit(self.perso.image, self.camera.apply_rect(self.perso.rect))
        for sprite in self.mob_group:
            self.fenetre.blit(sprite.image, self.camera.apply(sprite))
        

class Mob(pygame.sprite.Sprite):
    def __init__(self, game, stats, x, y):
        super().__init__()
        self.game = game
        self.group = game.mob_group
        pygame.sprite.Sprite.__init__(self, self.group)
                    
        self.vie = stats.vie
        self.attaque = stats.attaque
        self.image = pygame.image.load('image/mob/'+stats.image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y                  

    def update(self):
        if collide_with_object(self.game.perso, self.group) == True:
            print(self.vie)
            return(True)


def combat(perso, mob):
    while True:
        damage = perso.att
        mob.vie -= damage

        if mob.vie <= 0:
            print('victoire')
            break
        damage = mob.attaque
        perso.vie -= damage

        if perso.vie <= 0:
            print('perdu')
            break