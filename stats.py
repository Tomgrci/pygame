from classe import *


class stats_monstre:
    def __init__(self,nom,vie,attaque,image):
        self.nom = nom
        self.vie = vie
        self.attaque = attaque
        self.image = image

all_mob = list()

slime_bleu = stats_monstre('slime_bleu',70,3,'slime-blue.png')
slime_vert = stats_monstre('slime_bleu',60,5,'slime-green.png')


all_mob.append(slime_bleu)
all_mob.append(slime_vert)
