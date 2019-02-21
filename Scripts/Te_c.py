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
d3= Shot(27039, LHt=[(0.2607,0.260,0.261)], HLt = [(0.3247, 0.3246, 0.3252)])

x1 = Shot(27453, LHt=[(0.295,0.2945,0.2955)], HLt=[(0.3105,0.3099,0.311)])
x2 = Shot(24328, LHt=[(0.251, 0.2506, 0.2514)],HLt=[(0.2895, 0.2894, 0.2896)])
x3 = Shot(24132, LHt=[(0.2637,0.262,0.264),(0.2945,0.294,0.295)], HLt=[(0.283,0.282,0.2835),(0.340,0.339,0.341)])

for shot in [d1,d2,d3, x1,x2,x3]:
    shot.plot_JP(plot_thomson=4, label_thomson=True)
    

#%%
# d2 = 27036
good = []
bad = []
for i in range(0,85): #0,1,...,81
    res, t, xys, canvas = x3.fit_tanh_pedestal(i)
    fig = bh.ohno(canvas, '0')
    yesno = fig.do_verify()
    if yesno == True:
        good.append(i)
    else:
        bad.append(i)
#%% Saving and laoding data from pickle
import pickle        
with open(r"24132_goodbad_indexs.pickle", "wb") as output_file:
     pickle.dump([good,bad], output_file)

##%%
#with open(r"27039_goodbad_indexs.pickle", "rb") as input_file:
#     go, ba = pickle.load(input_file)
#%%
# TE data generally not good enough for xpoint height scan shots x1,x2,x3
# So want to check by hand the values
with open(r"24132_goodbad_indexs.pickle", 'rb') as input_file:
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

plt.figure('Te/c', figsize=(7,5))

for shotno, shotclass in zip([27035,27036,27039], [d1,d2,d3]):
#for shotno, shotlcass in zip([27453,24328,24132], [x1,x2,x3]):
   with open(r"{}_goodbad_indexs.pickle".format(shotno), "rb") as input_file:
        good, bad = pickle.load(input_file) # indicies
   shotclass.Te_Tec_all(good, A=832)

plt.xlabel('$Te_c\ (eV)$')
plt.ylabel('$Te\ (eV)$')
plt.xlim(0,140)
plt.ylim(-20,150)

xs = [-20,300]
plt.plot(xs,np.array(xs), lw=1, ls='--', alpha=0.5, c='k')
plt.scatter(-1,-1, marker='x', c='r', label='L')   
plt.scatter(-1,-1, marker='x', c='g', label='H')
plt.scatter(-1,-1, marker='x', c='blue', label='HL')
plt.legend(title=r"$Mode$")        