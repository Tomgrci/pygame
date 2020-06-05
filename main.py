import pygame
from pygame import *
import pytmx
from pytmx import *

from classe import *
from classe_map import *

#chargement des classes
game = Game()

game.generer_map('niveau.tmx')

runing = True

while runing == True:

    #if game.combat_start == True :



    game.update()
  
    game.affichage()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
            pygame.quit()
