import pygame
from pygame import *
import pytmx

from classe import *

#fenetre
pygame.init()
largeur = 1280
hauteur = 720
fenetre = pygame.display.set_mode((largeur, hauteur))


perso = hero(100,5,300)

vitesse = (0,0)
clock = pygame.time.Clock()
FPS = 60


niveau = TiledMap('chunk/moldytown.tmx')
camera = Camera(niveau.width,niveau.height)
map_img = niveau.make_map()
map_rect = map_img.get_rect()


runing = True
while runing == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
            pygame.quit()


        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                deplacement(perso,(perso.vitesse,0))
            if event.key == K_LEFT:
                deplacement(perso,(-perso.vitesse,0))
            if event.key == K_UP:
                deplacement(perso,(0,-perso.vitesse))
            if event.key == K_DOWN:
                deplacement(perso,(0,perso.vitesse))
            
        elif event.type == KEYUP:
            if event.key == K_RIGHT:
                deplacement(perso,(-perso.vitesse,0))
            if event.key == K_LEFT:
                deplacement(perso,(perso.vitesse,0))
            if event.key == K_UP:
                deplacement(perso,(0,perso.vitesse))
            if event.key == K_DOWN:
                deplacement(perso,(0,-perso.vitesse))

                
    dt = clock.tick(75)/1000
    
    changer_position(perso,dt)
    print(perso.rect.topleft)

    
    
    #affichage ecran
    camera.update(perso)
    fenetre.blit(map_img,camera.apply_rect(map_rect))
    

    fenetre.blit(perso.image,perso.rect)
    pygame.display.set_caption("{:.2f}".format(clock.get_fps()))
    

    pygame.display.flip()
