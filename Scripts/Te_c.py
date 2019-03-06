# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 12:02:35 2019

@author: rbatt
Te/c plot
"""
import numpy as np
import matplotlib.pyplot as plt
import ByHand as bh

#%% data import
from Shot_Class import Shot
session = '06-Oct-11'  #Measure LH power threshold at a range of densities.
geometry = 'CND'
#buggy runfile command hopefully works here
runfile('C:/Users/rbatt/MAST_Edge_RT_Research/Scripts/Shot_Class.py', wdir='C:/Users/rbatt/MAST_Edge_RT_Research/Scripts')
from signal_dict_06_OCT_11 import signals
#s1= Shot(27030, LHt=[(0.1928, 0.193, 0.1927)], HLt=[(0.1963, 0.1963,0.19637)]) ### bad shot
d1= Shot(27035, LHt=[(0.2868,0.2865,0.287)], HLt = [(0.3096,0.3096,0.3098)])
d2= Shot(27036, LHt = [(0.2565, 0.2545,0.258)], HLt = [(0.3261,0.3261,0.327)])
d3= Shot(27039, LHt=[(0.298,0.297,0.295)], HLt = [(0.330, 0.3299, 0.3301)])
#%%

x1 = Shot(27453, LHt=[(0.295,0.2945,0.2955)], HLt=[(0.3105,0.3099,0.311)])
x2 = Shot(24328, LHt=[(0.251, 0.2506, 0.2514)],HLt=[(0.2895, 0.2894, 0.2896)])
x3 = Shot(24132, LHt=[(0.2637,0.262,0.264),(0.2945,0.294,0.295)], HLt=[(0.283,0.282,0.2835),(0.340,0.339,0.341)])

for shot in [d1,d2,d3, x1,x2,x3]:
    shot.plot_JP(plot_thomson=4, label_thomson=True)

#%% more Z-x-pt data, to try again...
from signal_dict_10_NOV_11 import signals
z1 = Shot(20480, LHt=[(0.1975,0.1974,0.1976)], HLt=[(0.267,0.2669,0.2671)])
from signal_dict_13_DEC_PULL import signals
z2 = Shot(24130, LHt=[(0.285,0.2845,0.2855)], HLt=[(0.3325,0.332,0.333)])
from signal_dict_10_NOV_11 import signals
z3 = Shot(27449, LHt=[(0.115,0.110,0.120)], HLt=[(0.301,0.300,0.306)])

for shot in [z3]:
    shot.plot_JP(plot_thomson=4, label_thomson=True)

#%%
# IP scan shots
runfile('C:/Users/rbatt/MAST_Edge_RT_Research/Scripts/Shot_Class.py', wdir='C:/Users/rbatt/MAST_Edge_RT_Research/Scripts')
from signal_dict_2019_IP import signals
i1= Shot(30351, LHt=[(0.300, 0.295, 0.334)],HLt=[(0.620, 0.615, 0.622)])
i2= Shot(30356, LHt=[(0.273, 0.270, 0.275)],HLt=[(0.2791, 0.2790, 0.2794)]) # very very limited h mode. Will it produce any Te>Tec?
i3= Shot(30358, LHt=[(0.1975, 0.19745, 0.1976)],HLt=[(0.3425, 0.342, 0.343)])

for shot in [i1,i2,i3]:
    shot.plot_JP(plot_thomson=4,label_thomson=True)

#%%

# d2 = 27036
good = []
bad = []
for i in range(0,94): #0,1,...,81
    res, t, xys, canvas = i3.fit_tanh_pedestal(i)
    fig = bh.ohno(canvas, '0')
    yesno = fig.do_verify()
    if yesno == True:
        good.append(i)
    else:
        bad.append(i)
#%% Saving and laoding data from pickle
import pickle        
with open(r"27449_goodbad_indexs.pickle", "wb") as output_file:
     pickle.dump([good,bad], output_file)

with open(r"27039_goodbad_indexs.pickle", "rb") as input_file:
     go, ba = pickle.load(input_file)

#%%     
def dumpgoodbads(shotclass):
    with open(r"{}_goodbad_indexs.pickkle".format(shotclass.ShotNumber),'wb') as output_file:
        pickle.dump([good,bad], output_file)
        
def goodbads(shotclass):
    with open(r"{}_goodbad_indexs.pickle".format(shotclass.ShotNumber), 'rb') as input_file:
        go, ba = pickle.load(input_file)
    return goo,baa

#%%
# TE data generally not good enough for xpoint height scan shots x1,x2,x3
# So want to check by hand the values
with open(r"27449_goodbad_indexs.pickle", 'rb') as input_file:
    good, bad = pickle.load(input_file)


tgood = []
tbad = []
for ind in good:
    te, tec = x3.Te_Tec(ind)
    res,t,xys,canvas = x2.fit_tanh_pedestal(ind, sig='TE')
    
    res,t,xys,canv = x2.fit_tanh_pedestal(ind)
    knee, width, maxs, nemaxs,neknee = x2._tanh_params(res)
    plt.axvline(knee+width/2., c='purple')
    
    fig = bh.ohno(canvas, 'Te = {}'.format(te))
    yesno = fig.do_verify()
    if yesno == True:
        tgood.append(ind)
    else:
        tbad.append(ind)
#%%
import pickle

plt.figure('Te/c', figsize=(6,5))

#for shot in [i1]:
for shot in [i2]:
#for shot in [d1,d2,d3]:
#for shot in [x1,x2,x3]:
   with open(r"{}_goodbad_indexs.pickle".format(shot.ShotNumber), "rb") as input_file:
        good, bad = pickle.load(input_file) # indicies
   for ind in good:
       Te,Tec = shot.Te_Tec(ind)
       if Te<0: #sanity checks
           shot.fit_tanh_pedestal(ind)
           shot.fit_tanh_pedestal(ind, sig='TE')
   shot.Te_Tec_all(good, A=832, label=True)

#%%

plt.xlabel('$T_{ec}\ (eV)$')
plt.ylabel('$T_{e}\ (eV)$')
plt.xlim(0,145)
plt.ylim(0,145)

xs = [-20,300]
plt.plot(xs,np.array(xs), lw=1, ls='--', alpha=0.5, c='k')
plt.scatter(-1,-1, marker='x', c='r', label='L')   
plt.scatter(-1,-1, marker='x', c='g', label='H')
plt.scatter(-1,-1, marker='x', c='blue', label='HL')
#plt.legend(title=r"$Mode$")        