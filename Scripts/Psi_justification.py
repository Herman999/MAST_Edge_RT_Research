# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 11:26:47 2019
@author: rbatt
Psi 95 justification or not
PLOTS THE PSI98 != R_MAX_SLOPE PLOT

1. Press Play 
"""
import numpy as np
import matplotlib.pyplot as plt
#import ByHand as bh

#the following is the method used to generate data which is stored in pickle and is used in plot below

##%% data import
#from Shot_Class import Shot
#session = '06-Oct-11'  #Measure LH power threshold at a range of densities.
#geometry = 'CND'
##buggy runfile command hopefully works here
#runfile('C:/Users/rbatt/MAST_Edge_RT_Research/Scripts/Shot_Class.py', wdir='C:/Users/rbatt/MAST_Edge_RT_Research/Scripts')
#from signal_dict_06_OCT_11 import signals
##s1= Shot(27030, LHt=[(0.1928, 0.193, 0.1927)], HLt=[(0.1963, 0.1963,0.19637)]) ### bad shot
#s2= Shot(27035, LHt=[(0.2868,0.2865,0.287)], HLt = [(0.3096,0.3096,0.3098)])
#s3= Shot(27036, LHt = [(0.2565, 0.2545,0.258)], HLt = [(0.3261,0.3261,0.327)])
#s4= Shot(27037, LHt=[(0.2607,0.260,0.261)], HLt = [(0.3247, 0.3246, 0.3252)])
################################################################################
#session = '10-Nov-11'  #Effect of RMPS on DND
#geometry = 'maybe CND'
##buggy runfile command hopefully works here
#runfile('C:/Users/rbatt/MAST_Edge_RT_Research/Scripts/Shot_Class.py', wdir='C:/Users/rbatt/MAST_Edge_RT_Research/Scripts')
#from signal_dict_10_NOV_11 import signals
#s11= Shot(27444, LHt=[(0.259,0.2545,0.2595)], HLt=[(0.324,0.323,0.325)])
#s12= Shot(27446, LHt=[(0.276,0.274,0.2765)], HLt=[(0.3074,0.307,0.308)])
#s13= Shot(27448, LHt=[(0.110,0.105,0.118)], HLt=[(0.2894,0.2893,0.2895)])
#s14= Shot(27449, LHt=[(0.115,0.110,0.120)], HLt=[(0.301,0.300,0.306)])
#s15= Shot(27450, LHt=[(0.116,0.110,0.118)], HLt=[(0.305,0.303,0.306)])
##s16= 'Shot(27451, LHt=[(0.2665,0.266,0.267),(0.2847,0.284,0.2855)], HLt=[(0.273,0.2725,0.2735),(0.287,0.287,0.289)])
#s17= Shot(27453, LHt=[(0.295,0.2945,0.2955)], HLt=[(0.3105,0.3099,0.311)])
#s18= Shot(27454, LHt=[(0.277,0.276,0.278)], HLt=[(0.2893,0.289,0.290)])
################################################################################
#session = '22-Jan-10' #Characterise the dynamics of the L-H transition by measuring density and temperature profile evolution with the enhanced Thomson scattering.
#geometry = 'maybe CND'
#runfile('C:/Users/rbatt/MAST_Edge_RT_Research/Scripts/Shot_Class.py', wdir='C:/Users/rbatt/MAST_Edge_RT_Research/Scripts')
#from signal_dict_13_DEC_PULL import signals
#s21= Shot(24134, LHt=[(0.3018,0.3016,0.302)], HLt=[(0.3448,0.344,0.345)])
#s22= Shot(24133, LHt=[(0.2818,0.2815,0.282),(0.3286,0.3275,0.329)], HLt=[(0.3255,0.325,0.326),(0.3315,0.331,0.332)])
#s23= Shot(24132, LHt=[(0.2637,0.262,0.264),(0.2945,0.294,0.295)], HLt=[(0.283,0.282,0.2835),(0.340,0.339,0.341)])
#s24= Shot(24131, LHt=[(0.2905,0.290,0.291)], HLt=[(0.3366,0.3365,0.344)])
#s25= Shot(24130, LHt=[(0.285,0.2845,0.2855)], HLt=[(0.3325,0.332,0.333)])
#s26= Shot(24129, LHt=[(0.2922,0.290,0.295)], HLt=[(0.3174,0.317,0.318)])
#s27= Shot(24128, LHt=[(0.2572,0.257,0.258)], HLt=[(0.3435,0.343,0.344)])
#s28= Shot(24127, LHt=[(0.2738,0.273,0.274)], HLt=[(0.311,0.3105,0.3115)])
#s29= Shot(24126, LHt=[(0.2781,0.278,0.2815)], HLt=[(0.3435,0.343,0.344)])
#s210= Shot(24125, LHt=[(0.2856,0.285,0.286)], HLt=[(0.3232,0.323,0.3235)])
#s211= Shot(24124, LHt=[(0.246,0.242,0.260)], HLt=[(0.2896,0.280,0.2897)])
##%% show data
#for s in [s2,s3,s4,s11,s12,s13,s14,s15,s17,s18]:
#    s.plot_JP(plot_thomson=4,label_thomson=True)

#%% Get Psi's
# the following is the method used to generate data which is stored in pickle and is used in plot below
##for s2
#inds = np.arange(69,75) # 69 to 74
#pguess=[3.0e19,2.0e19,1.47,0.05,1.0e19,1,1] # parameter guess for skinny pedestals
#
#shots_inds = [[s2,np.arange(69,75),True], # shot class, indexes, whether should use altered pguess or not
#              [s3,np.arange(63,79),True],
#              [s4,np.arange(63,78),True],
#              [s11,np.arange(62,77),False],
#              [s12,np.arange(66,74),False],
#              [s13,np.arange(64,72),False],
#              [s14,np.arange(64,72),False],
#              [s15,np.arange(64,72),False],
#              [s21, [79],False],
#              [s22,np.arange(64,80),False],
#              [s23,np.arange(72,80),False],
#              [s24,np.arange(72,80),False],
#              [s25,np.arange(65,78),False],
#              [s27,np.arange(64,80),False],
#              [s28,np.arange(64,75),False],
#              [s29,np.arange(64,80),False],
#              [s210,np.arange(72,79),False],
#              ]
#good_data = []
#for shot,inds,vrai in shots_inds:
#    for i in inds:
#        print(i)
#        
#        #generate the tanh fits, with preview
#        if vrai:
#            result, time, data, canvas_name = shot.fit_tanh_pedestal(i,guess=pguess, preview=True)
#        else:
#            result, time, data, canvas_name = shot.fit_tanh_pedestal(i, preview=True)
#        
#        # find the relevant variables from fit
#        knee, width, max_slope, ne_max_slope, ne_at_knee = shot._tanh_params(result)
#        # get Psi data
#        PsiTime, Psi100, Psi95, Psi90 = [shot.data['EFM_R_PSI100_OUT']['time'], 
#                                         shot.data['EFM_R_PSI100_OUT']['data'],
#                                         shot.data['EFM_R_PSI95_OUT']['data'],
#                                         shot.data['EFM_R_PSI90_OUT']['data'] ] 
#        P100, P95, P90 = [np.interp(time, PsiTime, Psi100),
#                          np.interp(time, PsiTime, Psi95),
#                          np.interp(time, PsiTime, Psi90) ] # now in form R = ... m
#        P98 = np.interp(98, [95,100], [P95, P100]) # radii of Psi98
#        
#        # check whether width is physical
#        outside = knee+width
#        if outside>1.55: # the width is way too large. Don't even check it by hand
#            good = False 
#        else: # fit may be good
#            check = bh.ohno(canvas_name, 'fit')
#            good = check.do_verify()
#        
#        if good: # can add to plot
#            plt.figure('comp54')
#            plt.scatter(knee+width/2.,P100, c='g', marker='o')
#            plt.scatter(knee+width/2.,P98, c='r', marker='x')
#            plt.scatter(knee+width/2.,P95, c='b', marker='^')
#            plt.text(knee+width/2.,P95, shot.ShotNumber)
#            good_data.append([knee+width/2., P100, P98, P95])
#    
#%%
# with open(r"Psi_Justification_data.pickle", "wb") as output_file:
#     pickle.dump(good_data, output_file)
#%%
import pickle

with open(r"Psi_Justification_data.pickle", "rb") as intput_file:
     good_data = pickle.load(intput_file)


plt.figure(figsize=(10,7.2))
plt.rcParams.update({'font.size': 14})

for rf, r100, r98, r95 in good_data: # in good data is sets of [R_max_slope, R_Psi100, R_Psi98, R_Psi95]
        plt.scatter(rf,r100, c='g', marker='o')
        plt.scatter(rf,r98, c='r', marker='x')
        plt.scatter(rf,r95, c='b', marker='^')

plt.title('Comparison of $\Psi$ to pedestal fitting')
plt.xlabel(r'$R_{max\ slope\ from\ ne\ pedestal} \ [m]$')
plt.ylabel(r'$R_{\Psi} \ [m]$')

plt.scatter(0,0, c='g', marker='o', label=r'$\Psi_{100}$')
plt.scatter(0,0, c='r', marker='x', label=r'$\Psi_{98}$')
plt.scatter(0,0, c='b', marker='^', label=r'$\Psi_{95}$')
plt.legend()
plt.ylim(1.35,1.55)
plt.xlim(1.35,1.55)

xst = np.arange(1.3,1.6, 0.01)
plt.plot(xst,xst, c='k', ls='--')    
