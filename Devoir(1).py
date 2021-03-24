import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import colorsys as clrs 
import scipy.stats as st 
import itertools
import time
import Fonction as fct
import random
from psychopy import visual, core, event
import os
import csv



##%Initialisation of the parameters

#Possible formes and colors
pool_forme=['sqr','circle','triangle']
pool_col = [[255,0.5,0.5],[0.5,255,0.5],[0.5,0.5,255],[255,255,0.5]]

#?
t_init_per= 0
proc=False
x=0
y=0
cmpt = 0
pool_pos=[(0.3)]
distracteur = [0,0,0]
sexe='oop'
age='oop'
coult_init=0
coulp_init=0
pool_dis =[0,0,0]
pos_targ = [0,0]
pool_pos =[[pos_targ[0]-0.15,pos_targ[1]+0.15],[pos_targ[0]+0.15,pos_targ[1]+0.15],[pos_targ[0],pos_targ[1]-0.15]]
test_proc_couleur = 10
proc=10

##In order to keep track of the data
if not os.path.exists('output.csv'):
    df = pd.DataFrame(columns=['sexe','age','n_essai','rt','perf','obj','clr_dép','clr_arriv','clr_target'])
else:
    df = pd.read_csv('output.csv')
tabl_couleur = pd.DataFrame(index=['RG','RD','NRG','NRD'],columns=['Red','Green','Blue','Yellow'])


#Initialisation of the window
win = visual.Window([800,800],color=(256,256,256),fullscr=False,monitor="testMonitor")
for i,j in itertools.product(tabl_couleur.index,tabl_couleur.columns):
    tabl_couleur.loc[i,j] = [1,1]


##% Collecting some information on the subject (Male/Female, Age)
#Text to be displayed
text1='Entrez H ou F si vous êtes un homme ou une femme'
text2='Entrez votre age'

#Asking for the Sexe
text1_stim=visual.TextStim(win,text=text1,color=(0,0,0))
text1_stim.draw()
win.flip()
#Wait for the answer
sexe = event.waitKeys(maxWait=5.0,keyList=["h","f"])

#Asking for the age
text1_stim=visual.TextStim(win,text=text2,color=(0,0,0))
text1_stim.draw()
win.flip()
#Wait for the answer
age=event.waitKeys(maxWait=5.0,keyList=['0','1','2','3','4','5','6','7','8','9'])


target = 0
for a in range(5): #Number of trials
    
    #Initialisation of the target
    t_targ = time.time()+20
    t_init_per=time.time()+20
    classor=0
    exp=1
    proc1=False 
    proc2=False
    nm_col=random.choice([0,1,2,3])
    target = fct.Forme(random.choice(pool_forme),couleur = pool_col[nm_col],position=(pos_targ[0],pos_targ[1]),win=win)
    t0 = time.time()
    proc=10
    
    #Loop for distractors production
    for i in range(len(distracteur)):
        """Attribution of one of the three possible forms, to each distractors"""
        pool_dis[i] = random.choice(pool_forme) #Choose the form
        clr = random.choice(pool_col) #Choose the color
        
        #Create the object to be displayed, based on color and form
        distracteur[i] = fct.Forme(pool_dis[i],clr,pool_pos[i],win)
        distracteur[i].set_forme()
        distracteur[i].set_couleur()
    
    
    #Place the object at random over the screen
    esp_choix=np.linspace(-0.7,0.7) #Ici on a les limites de l'espace de coordonées cartésiennes
    
    # Choose (x,y) coordinate that will serve as starting point for the target
    x_coord = random.choice(esp_choix)
    y_coord = random.choice(esp_choix)
    target.position = (x_coord,y_coord)
    pos_targ[0],pos_targ[1] = x_coord,y_coord
    
    #Set target attributes
    target.set_forme()
    target.set_couleur()
    target.set_pos()
    
    #Update Distractors positions
    for i in range(len(distracteur)):
        pool_pos =[[pos_targ[0]-0.15,pos_targ[1]+0.15],[pos_targ[0]+0.15,pos_targ[1]+0.15],[pos_targ[0],pos_targ[1]-0.15]]
        distracteur[i].position = pool_pos[i]
        distracteur[i].set_pos()
    
    #Compute the path of the target, with n steps
    x,y = fct.mouvement(target.position[0],target.position[1])
    
    #Experiment
    while exp==1:
        if cmpt < len(x):  #If we haven't done all the steps choosed by the fct.mouvement function
            
            #Update the target position with the next step of the path
            target.position=[x[cmpt],y[cmpt]]
            target.set_pos()
            
            #Update the distractors positions
            for i in range(len(distracteur)):
                pool_pos =[[target.position[0]-0.2,target.position[1]+0.2],[target.position[0]+0.2,target.position[1]+0.2],[target.position[0],target.position[1]-0.2]]
                distracteur[i].position = pool_pos[i]
                distracteur[i].set_pos()
            cmpt+=1
        elif cmpt != 0 : 
            x,y=fct.mouvement(target.position[0],target.position[1])
            cmpt = 0
        else:
            pass
            
        #Ask for a possible subject reponse
        touche = event.getKeys(keyList = ['k'])
        
        
        #Launch, with p=0.05, the event "proc 2" if it hasn't happend yet
        if (random.choice(range(100)) in range(5)) and (not proc2) :
            #keep track of the time
            t_init_per = time.time()
            
            #Choose one of the three distractors and update it's color
            xch = random.choice([0,1,2])
            coulp_init = distracteur[xch].couleur #Note the original color
            coulzer = fct.couleur(tabl_couleur)
            distracteur[xch].couleur=(coulzer[0])
            distracteur[xch].set_couleur()
            coulp_nouv = distracteur[xch].couleur #Note the newx color
            proc2=True
        else:
            pass
        
        #Launch, with p=0.005, the event "proc 1" which change the target's color
        if random.choice(range(200)) == 1 and not proc1 :
            coult_init = target.couleur
            coult_fin=fct.couleur(tabl_couleur)
            target.couleur=coult_fin[0]
            target.set_couleur()
            proc1= True
            t_targ = time.time()
            if time.time() - t0 >= 7: #C'est pour donner 3 secondes au sujet pour remarquer le changement
                print(t0)
                t0 = time.time() - 2.8
        else:
            pass
        
        #Shows the modifications
        win.flip()
        core.wait(0.00005)
        #Asks for any key press
        esp_test = event.getKeys(keyList=['s'])
        test_lgr = time.time()-t0
        rt = time.time()-t_targ
        #Provoque ce qu'il y a à provoquer si le temps s'est écoulé
        if time.time()-t0 >=10 or time.time()-t_targ >3: #10 seconde de durée d'expérience et 3 seconde avant de pouvoir appuyer sur 'espace' quand le stimulus apparait, l'essai s'arrête
            exp = 0
        elif time.time()-t_init_per>3: #3 seconde pour répondre aux stimuli périphériques, si la personne n'a pas appuyé, elle a raté et ça débloque la possibilité de changerla couleur d'un autre objet
            proc2 = False
            perf=0
            classor=pd.DataFrame(data=[[sexe,age,a,rt,perf,'periphérique',coulp_init,distracteur[xch].couleur,target.couleur]],columns=['sexe','age','n_essai','rt','perf','obj','clr_dép','clr_arriv','clr_target'])
            df=pd.concat([df,classor],axis=0,sort=False)
            tabl_couleur.loc[coulzer[2],tabl_couleur.columns[nm_col]] += [1]
        else:
            pass
            
            
        if proc1:#Si l'obj central a changé de couleur 
            if 's' in esp_test:# Si le sujet appui sur "s", on arrête l'expérience et on lui attribut une réussite
                perf=1
                exp=0
                tabl_couleur.loc[coult_fin[1],tabl_couleur.columns[nm_col]]+=[1]
                classor=pd.DataFrame(data=[[sexe,age,a,rt,perf,'central',coult_init,target.couleur,target.couleur]],columns=['sexe','age','n_essai','rt','perf','obj','clr_dép','clr_arriv','clr_target'])
                df=pd.concat([df,classor],axis=0,sort=False)
        elif proc2:
            if 'k' in touche:
                perf=1
                proc2=False
                tabl_couleur.loc[coulzer[1],tabl_couleur.columns[nm_col]]+=[1]
            else:
                pass
        else:
            pass
            
       
        event.clearEvents()
    texte=("fin de l'essai, ",60-a,"essais restants")
    text_stim=visual.TextStim(win,text=texte,color=(0,0,0))
    text_stim.draw()
    win.flip()
    core.wait(1.5)


if not os.path.exists('output.csv'):
    df.to_csv("output.csv")
else:
    datafile=open("output.csv","w")
    writer=csv.writer(datafile,delimiter=",")
    for i in df.index:
        writer.writerow(df.loc[i,:])



