import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import colorsys as clrs 
import scipy.stats as st 
import itertools
import time
import Fonction as fct




pool_forme=['sqr','circle','triangle']
x=0
y=0
cmpt = 0
pool_pos=[(0.3)]
distracteur = [0,0,0]
pool_dis =[0,0,0]
pos_targ = [0,0]
pool_pos =[(pos_targ[0]-0.3,pos_targ[1]+0.3),(pos_targ[0]+0.3,pos_targ[1]+0.3),(pos_targ[0],pos_targ[1]-0.3)]
test_proc_couleur = 10
t_targ = 0
tabl_couleur = pd.DataFrame(index=['RG','RD','NRG','NRD'],columns=['R','V','B','J'])
df = pd.DataFrame(columns=['sexe','age','n_essai','rt','perf','obj','clr_dép','clr_arriv','clr_target'])

for i,j in itertools.product(tabl_couleur.index,tabl_couleur.columns):
	tabl_couleur.loc[i,j] = [1,1,1,1]
coco = fct.couleur(tabl_couleur,'R')

exp = True
target = 0
for a in range(60):
"""C'est le début de la boucle de l'expérience, on va commencer par créer l'objet à suivre, ensuite on créera les autres objets
		
		On le positionne à (0,0), l'objet ne sera pas au centre puisqu'on lui attribuera ensuite une position au hasard, l'initialisation
		de la position permettra de positionner les autres formes par rapport à cette position de référence

		clr renvoie à la fonction de choix des couleurs que j'ai pas encore construit mais c'est histoire de bien définir comment ça évoluera"""
	target = fct.Forme(random.choice(pool_forme),couleur = random.choice(tabl_couleur.columns),(pos_targ[0],pos_targ[1]))
	pool = set(pool_forme) #l'avantage de passer la liste en ensemble est de pouvoir utiliser la fonction set.remove() qui permet de ne pas s'inquiéter de la position de l'objet dans la liste
	t0 = time.time()

	#Une boucle pour produire les distracteurs
	for i in range(len(distracteur)):
		"""ici on attribut une des trois formes aux objets distracteurs"""
		pool_dis[i] = random.choice(pool_forme)
		pool_forme.remove(a) #Ici on enlève l'objet a de l'ensemble, pour les prochains tour de la boucle il n'y aura plus l'objet tiré au hasard à ce tour ci
		distracteur[i] = Forme(pool_dis[i],clr,pool_pos[i])


	#Ensuite on positionne les objets au hasard sur l'espace
	esp_choix=range(-0.7,0.7) #Ici on a les limites de l'espace de coordonées cartésiennes
	x_coord = random.choice(esp_choix) # Ici on choisit une coordonées "x" et une "y" au hasard qui seront les points d'arrivé
	y_coord = random.choice(esp_choix)
	target.set_position(position=(x_coord,y_coord))
	#Une fois qu'on a mis à jour la position de la cible on met à jours les positons des distracteurs
	for i in range(len(distracteur)):
		distracteur[i].set_position(position=(pool_pos[i]))
	x,y = fct.mouvement(target.position)
	while exp:
		if cmpt <= len(x):
			target.set_position(position=(x[cmpt],y[cmpt]))
			for i in range(len(distracteur)):
				distracteur[i].set_position(position=(pool_pos[i]))
		else :
			x,y=fct.mouvement(target.position)



		#Maintenant il faut déclancher le changement de couleur au hasard
		# 1 Choisir la forme qui va changer de couleur, on va mettre une Pb plus élevé pour que ce soit un des objets
		#	Périphérique qui change
				# Pour ça il faut calculer le nombre de fois où on devra faire le choix (normalement 1fois toutes les 0.0001 secondes)
				# et le nombre de fois où on aimerait qu'une forme change de couleur.
		# 2 Modifier la couleur au hasard avec la foncion
		# 3 Appliquer une horloge pour le timeStamped
			#Comme on a que deux touches, si le changement de couleur proc pour deux objets périphériques, on ne pourra pas savoir
			#Pour lequel il s'agit, on essaira d'éviter au pire. Pour ce qui est de l'objet central on peu poser deux horloges distinctes.
		# 4 Lorsque le sujet a appuyé sur la touche il faut consigner l'expérience. On laisse 3s de plus au sujet pour appuyer sur
		#   la touche de l'obj central
		# 5 Le résultat ira dans deux tableaux, tabl_couleur, dans lequel il s'agira d'un 1 ou d'un 0. Le tableau des résultats
		#   généraux dans lequel on consignera, le sexe, l'age, la main directrice, le numéro de l'essai. On consignera en plus, le temps de
		#	réaction, la réussite ou l'échec, l'objet qui a changé de couleur (périphérique ou non), la couleur de base, la couleur
		#	d'arrivé et la couleur de l'objet au centre.
		touche = event.getKeys(keyList = ['0'],timeStamped=True)
		if random.choice(range(100)) == in range(5) and test_proc_couleur > 3 :
			
			t_init_per = time.time()
			xch = random.choice([0,1,2])
			coulp_init = distracteur[xch].couleur
			coulzer = fct.couleur(tabl_couleur,target.couleur)
			distracteur[xch].set_couleur(coulzer[0])
			coulp_nouv = distracteur[xch].couleur

			test_proc_couleur = 0
		elif test_proc_couleur <= 3:
			test_proc_couleur = time.time() - t_init_per
		else:
			pass

		if random.choice(range(1000)) == 1 and proc == False :
			coult_init = target.couleur
			target.set_couleur(fct.couleur(tabl_couleur,target.couleur))
			proc = True
			t_targ = time.time()
			if time.time() - t0 >= 17: #C'est pour donner 3 secondes au sujet pour remarquer le changement
				t0 = time.time() - 17
		else:
			pass		

		#Pour afficher les objets
		win.flip()
	    core.wait(0.0001)
	    
	    esp_test = event.getKeys(keyList=['space'])
	    test_lgr = time.time()-t0
	    rt = time.time()-t_targ
	    rt_dist = time.time()-t_init_per
	    if 'space' in touche or test_lgr >= 20 or rt >= 3 :
	    	exp = False
	    	perf = 1
	    	if proc == False or not 'space' in touche:
	    		perf = 0
	    		rt = 0
	    	df.append([sexe,age,a,rt,perf,'target',coult_init,target.couleur,target.couleur])
	    elif '0' in touche or rt_dist >= 3:
	    	perf = 1
	    	if rt_dist >= 3:
	    		perf = 0
	    		tabl_couleur.loc[coulzer[2],target.couleur].append(1)
	    	else:
	    		tabl_couleur.loc[coulzer[1],target.couleur].append(1)

	    	df.append([sexe,age,a,rt_dist,perf,'distracteur',coulp_init,coulzer[0],target.couleur])
	    	
	    	exp = True
	    
	    
	print("fin de l'essai, ",60-a,"essais restants")
    
"""il faudrait faire un while qui coupe la boucle soit quand le chemin est fini, soit quand quelqu'un appuie sur une touche et
donc enregistrer sont temps de réponse, la boucle reprend là où le chemin s'est arrêté, on met un if toucheappuyé var=0 
et if chemin_fini var = 0, et à chaque itération de la boucle stocker la variable """
