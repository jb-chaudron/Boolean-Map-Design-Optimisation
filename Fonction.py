import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import colorsys as clrs 
import scipy.stats as st 
import random
import math
from psychopy import visual, core, event

class Forme(object):
	"""
		A function which will help to attribute forms and colors to an object.
	"""
	
	def __init__(self, forme, couleur,position,win):
		self.forme = forme
		self.couleur = couleur
		self.position = position
		self.image = 0
		self.win = win

	"""Assign colors to an object"""
	def set_couleur(self):
		self.image.fillColorSpace='rgb255'
		self.image.fillColor =self.couleur

	"""Assign form to an object"""
	def set_forme(self):
		if self.forme == 'sqr':
			self.image = visual.ShapeStim(self.win,vertices = [(0.1,0.1),(0,0.1),(0,0),(0.1,0)])
			self.image.draw()
		elif self.forme == 'circle':
			self.image = visual.Circle(self.win, radius=0.075, edges=50)
			self.image.draw()
		elif self.forme == 'triangle':
			self.image = visual.Circle(self.win, radius=0.075, edges = 3)
			self.image.draw()

	""" Assign position of the object"""
	def set_pos(self):
		self.image.pos= (self.position)
		self.image.draw()





""" 
	We use colorsys.hls_to_rgb and/or colorsys.rgb_to_hls. 
	The HLS system allows to use a continuous color coordinate systems.
	Thus we can go from red to yellow to green to blue.
	We can define a function that will randomly select a color, given the inverse gamma distribution that will 
	be modify given success and fails of the subjects.
"""

def couleur(tabl,colo=None):
	#Helps to write the mean in term of RBG coordinate, it will help for the translation rouge-0 = RGB(255,0,0)
	RGB = {'Red':[255,0,0],'Green':[0,255,0],'Blue':[0,0,255],'Yellow':[255,255,0]}
	conjug = {'Red':'Green','Green':'Red','Blue':'Yellow','Yellow':'Blue'}
	op = {'RG':'NRG','RD':'NRD','NRG':'RG','NRD':'RD'}
	rd_col = 0
	if colo == None:
		chx_col = random.sample(RGB.keys(),1) #Choose the target's color
	else:
		chx_col = colo 
	chx_dist = random.sample(list(tabl.index),1) #Choose color, opposite or not, or Right or Left neighbour colors
	strat = random.sample([0,1,2],1) #Choose the choice strategy : Uniform random, Normal Random, Normal random with 2sigmas or more
	chx_cot = 1
	compt = 0
	
	if chx_dist == tabl.index[2] or chx_dist == tabl.index[3]: #We choose the mean on which we base our color
		chx_col = conjug[chx_col]

	if chx_dist == tabl.index[0] or chx_dist == tabl.index[2]: #On choisit 
		chx_cot = -1

	""" 
		We determine the mean and standard deviation of the Normal distribution
		The mean : Choosen color
		Standard Deviation : Randomly selected sd, given a gamma inverse distribution
				     which code for the probability of sd, given the pass history of the subject.
				     Using the Hierarchical bayesian formalism.
	"""
	
	#Set the mean
	mean = clrs.rgb_to_hls(RGB[chx_col[0]][0],RGB[chx_col[0]][1],RGB[chx_col[0]][2])
	
	#Deviation between the succesfully noticed colors and the mean of the distribution at the time where they were noticed
	car_ecart= sum([(x-mean[0])*(x-mean[0]) for x in tabl.loc[chx_dist[0],chx_col[0]]])/2
	
	#Determine the standard deviation given the history
	ectp = [10000]
	while st.invgamma.sf(x=ectp[0],a=len(tabl.loc[chx_dist,chx_col])/2,scale=car_ecart) < 0.6: #It forces a minimal sd ?
		ectp = st.invgamma.rvs(a=len(tabl.loc[chx_dist,chx_col])/2,scale=car_ecart, size=1)
	

	"""Choose the color given the previously choosed strategy (Uniform, Normal, Normal 2sigma+)"""
	if strat[0] == 0 :
		#UNiform strategy
		rd_col = np.random.uniform(low = 0,high=360,size = 1)
	elif strat[0] == 1 :
		#Normal Strategy
		while rd_col in range(math.floor((mean[0]+180)*chx_cot)) and compt==0:
			rd_col = np.random.normal(loc=mean[0], scale=ectp, size=1)
			rd_col = math.floor(rd_col)
			compt = 1
	else :
		#Normal 2sgima +
		while rd_col in range(math.floor((mean[0]+2*ectp)*chx_cot)) and compt==0:
			rd_col = np.random.normal(loc=mean[0], scale=ectp, size=1)
			rd_col = math.floor(rd_col)
			compt = 1

	"""
		We change the basis of rd_col (the selected color), into HLS standard, then to RGB
	"""
	
	#HLS standard
	while rd_col < 0:
		rd_col += 360
	while rd_col > 360: 
		rd_col -= 360
	mean=list(mean)
	
	#Return the RBG standard
	return list(clrs.hls_to_rgb(rd_col,mean[1],mean[2])),chx_dist[0],op[chx_dist[0]]



def mouvement(x_dep,y_dep):
	"""
		Determine the path for the movement of the objects
	"""
	esp_choix=np.linspace(-0.7,0.7) #limits of the cartesian space
	
	# Choose random X and Y, end points
	x_coord = random.choice(esp_choix) 
	y_coord = random.choice(esp_choix)
	
	#Produce the coordinate path, to which the object has to go through
	mouv_x = np.linspace(x_dep,x_coord) 
	mouv_y = np.linspace(y_dep,y_coord)	
	
	return mouv_x,mouv_y

def test_central(proc,ret_coul,touche):
	if proc == 1:
		if 'space' in touche:
			
	else:
		pass
