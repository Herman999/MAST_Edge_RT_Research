# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 12:02:35 2019

@author: rbatt
Te/c plot
"""
import numpy as np
import matplotlib.pyplot as plt
#import ByHand as bh

#%% data import
#from Shot_Class import Shot
session = '06-Oct-11'  #Measure LH power threshold at a range of densities.
geometry = 'CND'
#buggy runfile command hopefully works here
#runfile('C:/Users/Tomas/MAST_Edge_RT_Research/Scripts/Shot_Class.py', wdir='C:/Users/Tomas/MAST_Edge_RT_Research/Scripts')
from signal_dict_06_OCT_11 import signals
#s1= Shot(27030, LHt=[(0.1928, 0.193, 0.1927)], HLt=[(0.1963, 0.1963,0.19637)]) ### bad shot
d1= Shot(27035, LHt=[(0.2868,0.2865,0.287)], HLt = [(0.3096,0.3096,0.3098)])
d2= Shot(27036, LHt = [(0.2565, 0.2545,0.258)], HLt = [(0.3261,0.3261,0.327)])
d3= Shot(27039, LHt=[(0.298,0.297,0.295)], HLt = [(0.330, 0.3299, 0.3301)])

x1 = Shot(27453, LHt=[(0.295,0.2945,0.2955)], HLt=[(0.3105,0.3099,0.311)])
x2 = Shot(24328, LHt=[(0.251, 0.2506, 0.2514)],HLt=[(0.2895, 0.2894, 0.2896)])
x3 = Shot(24132, LHt=[(0.2637,0.262,0.264),(0.2945,0.294,0.295)], HLt=[(0.283,0.282,0.2835),(0.340,0.339,0.341)])

# more Z-x-pt data, to try again...
from signal_dict_10_NOV_11 import signals
z1 = Shot(20480, LHt=[(0.1975,0.1974,0.1976)], HLt=[(0.267,0.2669,0.2671)])
from signal_dict_13_DEC_PULL import signals
z2 = Shot(24130, LHt=[(0.285,0.2845,0.2855)], HLt=[(0.3325,0.332,0.333)])
from signal_dict_10_NOV_11 import signals
z3 = Shot(27449, LHt=[(0.115,0.110,0.120)], HLt=[(0.301,0.300,0.306)])

# IP scan shots
#runfile('C:/Users/Tomas/MAST_Edge_RT_Research/Scripts/Shot_Class.py', wdir='C:/Users/Tomas/MAST_Edge_RT_Research/Scripts')
from signal_dict_2019_IP import signals
i1= Shot(30351, LHt=[(0.300, 0.295, 0.334)],HLt=[(0.620, 0.615, 0.622)])
i2= Shot(30356, LHt=[(0.273, 0.270, 0.275)],HLt=[(0.2791, 0.2790, 0.2794)]) # very very limited h mode. Will it produce any Te>Tec?
i3= Shot(30358, LHt=[(0.1975, 0.19745, 0.1976)],HLt=[(0.3425, 0.342, 0.343)])

#%%
# =============================================================================
# Work on 14/3/19
# =============================================================================
#high IP shots
hip1 = Shot(24524, LHt=[(0.201, 0.197, 0.202)],HLt=[(0.355, 0.354, 0.3558)])
hip2 = Shot(24522, LHt=[(0.2535, 0.253, 0.254)],HLt=[(0.3555, 0.355, 0.3558)])

#med IP shots
mip1 = Shot(24328, LHt=[(0.251, 0.2506, 0.2514)],HLt=[(0.2895, 0.2894, 0.2896)])
mip2 = Shot(24325, LHt=[(0.2515,0.2512,0.2518), (0.319, 0.317,0.321)],HLt=[(0.2845,0.2843,0.2847), (0.345,0.344,0.346)])
mip3 = Shot(24128, LHt=[(0.2572,0.257,0.258)], HLt=[(0.3435,0.343,0.344)])

#for shot in [mip1,mip2,mip3]:
for shot in [d1,d2,d3]:
    shot.plot_JP(plot_thomson=4, label_thomson=False)

#%% JP PLOTS
#for shot in [d1,d2,d3, x1,x2,x3]:
#    shot.plot_JP(plot_thomson=4, label_thomson=True)
#for shot in [z3]:
#    shot.plot_JP(plot_thomson=4, label_thomson=True)
#for shot in [i1,i2,i3]:
#    shot.plot_JP(plot_thomson=4,label_thomson=True)

#%%
#all shots with '000_goodbad_indexs.pickle'
alls = [d1,d2,d3,x1,x2,x3,z2,z3,i1,i2,i3,mip1,mip2,mip3]    

#%% generate good, bad indexes lists for shot.

# d2 = 27036
def checkne(shotclass, maxindex = 120):
    good = []
    bad = []
    for i in range(0,maxindex): #0,1,...,81
        res, t, xys, canvas = shotclass.fit_tanh_pedestal(i)
        fig = bh.ohno(canvas, '0')
        yesno = fig.do_verify()
        if yesno == True:
            good.append(i)
        else:
            bad.append(i)
    return good, bad
#%% Saving and laoding data from pickle
import pickle        
def dumpgoodbads(shotclass):
    with open(r"{}_goodbad_indexs.pickle".format(shotclass.ShotNumber),'wb') as output_file:
        pickle.dump([good,bad], output_file)
        
def goodbads(shotclass):
    with open(r"{}_goodbad_indexs.pickle".format(shotclass.ShotNumber), 'rb') as input_file:
        goo, baa = pickle.load(input_file)
    return goo,baa

#%%
# TE data generally not good enough for xpoint height scan shots x1,x2,x3
# So want to check by hand the values
def checkTe(shotclass):
    good, bad = goodbads(shotclass)
    tgood = []
    tbad = []
    for ind in good:
        te,te_er, tec, Thetac = shotclass.Te_Tec(ind)  # calculate Te/c
        res_ne,t,xys,canv = shotclass.fit_tanh_pedestal(ind, preview=False) # find (accepted) ne fit
        res,t,xys,canvas = shotclass.fit_tanh_pedestal(ind, sig='TE') # display Te pedestal
        
        knee, width, maxs, nemaxs, neknee = shotclass._tanh_params(res_ne) # get ne fit parameters
        plt.axvline(knee+width/2., c='yellow', lw=10) # show on Te pedestal the location of steepest ne
        plt.axhline(te, c='yellow', lw=10)
        try:
            plt.ylim(0,2*te) # give Te pedestal plot resonable y limits
        except:
            pass
        fig = bh.ohno(canvas, 'Te = {}'.format(te))
        yesno = fig.do_verify()
        if yesno == True:
            tgood.append(ind)
        else:
            tbad.append(ind)
        
    print('Lenght of good reduced from {} to {}'.format(len(good), len(tgood)))
#%%
import pickle

def Tecplots(shotclasslist, label_index=True, include_big_errors=True, Aconst=832, Tec_err = None, theta_transition_times=False):
    # plot Tec stuff for all shots in shotclasslist.
    plt.figure('Te/c',figsize=(10,7.2)) #figsize=(6,5))
    for shot in shotclasslist:
       with open(r"{}_goodbad_indexs.pickle".format(shot.ShotNumber), "rb") as input_file:
            good, bad = pickle.load(input_file) # indicies
       for ind in good:
           Te,Te_err,Tec,Theta_c = shot.Te_Tec(ind)
           if Te<0: #sanity checks
               shot.fit_tanh_pedestal(ind)
               shot.fit_tanh_pedestal(ind, sig='TE')
       shot.Te_Tec_all(good, A=Aconst, label=label_index, bigerrs=include_big_errors, Tec_err=Tec_err, theta_transition_times=theta_transition_times)
       
       
#%%
Tecplots([i1,i3])
Tecplots([d1,d2,d3])
Tecplots([x1,x2,x3])
#%%
Tecplots(alls,include_big_errors=False, Aconst=600, Tec_err=2)

#%%

plt.xlabel('$T_{ec}\ (eV)$')
plt.ylabel('$T_{e}\ (eV)$')
plt.xlim(0,180)
plt.ylim(0,180)#

xs = [-20,300]
plt.plot(xs,np.array(xs), lw=1, ls='--', alpha=0.5, c='k')
plt.scatter(-1,-1, marker='x', c='r', label='L')   
plt.scatter(-1,-1, marker='x', c='g', label='H')
plt.scatter(-1,-1, marker='x', c='blue', label='HL')
#plt.legend(title=r"$Mode$")        

#%% Good plot
plt.close('all')
Tecplots(alls,include_big_errors=False, Aconst=600, Tec_err=2, theta_transition_times=False)
plt.figure('Te/c')#,figsize=(10,7.2))
plt.rcParams.update({'font.size': 14})
plt.title('Guzdar $T_e/T_{ec}$ separation on MAST')
plt.xlabel('$T_{ec}\ (eV)$')
plt.ylabel('$T_{e}\ (eV)$')
plt.xlim(0,160)
plt.ylim(0,400)#

xs = [-20,300]
plt.plot(xs,np.array(xs), lw=1, ls='--', alpha=0.5, c='k')
plt.scatter(-1,-1, marker='x', c='r', label='L')   
plt.scatter(-1,-1, marker='x', c='g', label='H')
plt.scatter(-1,-1, marker='x', c='blue', label='HL')
plt.scatter(-1,-1, marker='x', c='orange', label='LH')
plt.legend()
plt.fill_betweenx(np.linspace(0,1000),np.linspace(0,1000),0, alpha=0.2)