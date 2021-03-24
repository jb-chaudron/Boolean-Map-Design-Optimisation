import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import colorsys as clrs 
import scipy.stats as st 
import random
import math
class Forme(object):
	"""Il s'agit d'une fonction qui va permettre de générer la forme et la couleur d'un objet quand on lui donnera
	les attribut qui nous intéressent. Comme ça, en recevant la forme et la couleur de l'objet, la fonction génèrera toute seule l'objet
	ça sera moins gourmant en terme de ligne.

	On aura juste à appeler la fonction par exemple; carre_bleu = Forme(square,blue).

	On peut aussi dire x = ['square','circle','triangle','star'] et y =['red','green','blue','yellow'] et ensuite,
	Forme(x.randomChoice,y.randomChoice). Comme ça on a des objets tiré au hasard qui ont une des quatres formes et une des quatres couleurs.
	"""
	def __init__(self, forme, couleur,position):
		self.forme = forme
		self.couleur = couleur
		self.position = position
		self.image = 0

	"""Cette fonction attribut à un objet une couleur particulière"""
	def set_couleur(self):
		self.image.fillColor(self.couleur)

	"""Cette fonction attribut à un objet une forme particulière"""
	def set_forme(self):
		if forme == 'sqr':
			self.image = visual.ShapeStim(win,vertices = (0.2,0.2),(0,0.2),(0,0),(0.2,0))
			self.image.draw()
		elif forme == 'circle':
			self.image = visual.Circle(win, radius=0.150, edges=50)
			self.image.draw()
		elif forme == 'triangle':
			self.image = visual.Circle(win, radius=0.2, edges = 3)
			self.image.draw()

	""" La fonction position détermine la position de l'objet par rapport à l'objet central, on déterminera 3 ou 4 position selon que l'on
		intègre l'étoile ou non"""
	def set_pos(self):
		self.image.pos(self.position)
		self.image.draw()





""" Ici on va utiliser colorsys.hls_to_rgb et/ou colorsys.rgb_to_hls, le système HLS permettant d'avoir
un système de coordonées continues du rouge au jaune au vert et au bleu. Ainsi on pourra definir une fonction
qui tirera un nombre au hasard selon la distribution gamma_inverse qui sera modifiée selon les échecs et les réussites
des sujets"""

def couleur(tabl,colo=None):
	#Ça sert à poser la moyenne en terme de RGB, ça servira pour la traduction rouge-0 = RGB(255,0,0)
	RGB = {'R':[255,0,0],'V':(0,255,0),'B':(0,0,255),'J':(255,255,0)}
	conjug = {'R':'V','V':'R','B':'J','J':'B'}
	op = {'RG':'NRG','RD':'NRD','NRG':'RG','NRD':'RD'}
	rd_col = 0
	if colo == None:
		chx_col = random.sample(RGB.keys(),1) #On choisit la couleur de l'objet central
	else:
		chx_col = colo 
	chx_dist = random.sample(list(tabl.index),1) #On choisit la couleur, opposé ou non, couleur adjacente par la gauche ou la droite
	strat = random.sample([0,1,2],1) #On choisit la stratégie, choix : aléatoire, aléatoire-normal, aléatoire à 2sig et +
	chx_cot = 1
	compt = 0
	
	if chx_dist == tabl.index[2] or chx_dist == tabl.index[3]: #On choisit la moyenne sur laquelle on se base pour choisir la couleur
		chx_col = conjug[chx_col]

	if chx_dist == tabl.index[0] or chx_dist == tabl.index[2]: #On choisit 
		chx_cot = -1

	""" On détermine la moyenne et l'écart type de la loi normale
		La moyenne : Correspond à la couleur choisie
		L'écart type : Correspond à un écart type tiré au hasard selon une distribution gamma inverse qui code la probabilité
		de l'écart type selon un modèle hierarchique bayesien"""
	
	mean = clrs.rgb_to_hls(RGB[chx_col][0],RGB[chx_col][1],RGB[chx_col][2])
	
	for l in tabl.loc[chx_dist,chx_col]:
		for m in l:
			print(m)
	
	car_ecart= sum([(x-mean[0])*(x-mean[0]) for x in tabl.loc[chx_dist,chx_col][0]])/2
	
	ectp = [10000]
	while st.invgamma.sf(x=ectp[0],a=len(tabl.loc[chx_dist,chx_col])/2,scale=car_ecart) < 0.6:
		ectp = st.invgamma.rvs(a=len(tabl.loc[chx_dist,chx_col])/2,scale=car_ecart, size=1)
	

	"""On code la stratégie précédemment choisie"""
	if strat[0] == 0 :
		rd_col = np.random.uniform(low = 0,high=360,size = 1)
	elif strat[0] == 1 :
		while rd_col in range(math.floor((mean[0]+180)*chx_cot)) and compt==0:
			rd_col = np.random.normal(loc=mean[0], scale=ectp, size=1)
			rd_col = math.floor(rd_col)
			compt = 1
	else :
		while rd_col in range(math.floor((mean[0]+2*ectp)*chx_cot)) and compt==0:
			rd_col = np.random.normal(loc=mean[0], scale=ectp, size=1)
			rd_col = math.floor(rd_col)
			compt = 1

	"""rd_col, qui est la valeur de la couleur récupérée, est changée pour correspondre aux standard HLS,
		c'est à dire qu'elle soit comprise entre 0 et 360. Ensuite, elle sera transformée en rgb 
		pour pouvoir être injectée dans le code principale"""

	while rd_col < 0:
		rd_col += 360
	while rd_col > 360:
		rd_col -= 360

	return clrs.hls_to_rgb(rd_col,mean[1],mean[2]),chx_dist,op[chx_dist]
	
	

def mouvement(x_dep,y_dep):
	"""Ce bout de code sert à définir les coordonnées x et y d'arrivée et donne deux vecteur qui nous permettrons de
	produire le déplacement"""
	esp_choix=range(-0.7,0.7) #Ici on a les limites de l'espace de coordonées cartésiennes
	x_coord = random.choice(esp_choix) # Ici on choisit une coordonées "x" et une "y" au hasard qui seront les points d'arrivé
	y_coord = random.choice(esp_choix)
	mouv_x = np.arrange(x_dep,x_coord,0.01) #Ici on produit deux vecteur avec les valeurs intermédiaires par lesquelles
	mouv_y = np.arrange(y_dep,y_coord,((y_dep-y_coord)/len(mouv_x)))	#les objets doivent passer
	
	return mouv_x,mouv_y