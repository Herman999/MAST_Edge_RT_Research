# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 10:47:49 2019

@author: rbatt

Useful shot initialisations for testing various stuff.
"""
from Shot_Class import Shot

#%%
session = '06-Oct-11'  #Measure LH power threshold at a range of densities.
geometry = 'CND'

from signal_dict_06_NOV_11 import signals

s1= Shot(27030, LHt=[(0.1928, 0.193, 0.1927)], HLt=[(0.1963, 0.1963,0.19637)])
s2= Shot(27035, LHt=[(0.2868,0.2865,0.287)], HLt = [(0.3096,0.3096,0.3098)])
s3= Shot(27036, LHt = [(0.2565, 0.2545,0.258)], HLt = [(0.3261,0.3261,0.327)])
s4= Shot(27037, LHt=[(0.2607,0.260,0.261)], HLt = [(0.3247, 0.3246, 0.3252)])

#%%
session = '10-Nov-11'  #Effect of RMPS on DND
geometry = 'maybe CND'

from signal_dict_10_NOV_11 import signals

s1= Shot(27444, LHt=[(0.259,0.2545,0.2595)], HLt=[(0.324,0.323,0.325)])
s2= Shot(27446, LHt=[(0.276,0.274,0.2765)], HLt=[(0.3074,0.307,0.308)])
s3= Shot(27448, LHt=[(0.110,0.105,0.118)], HLt=[(0.2894,0.2893,0.2895)])
s4= Shot(27449, LHt=[(0.115,0.110,0.120)], HLt=[(0.301,0.300,0.306)])
s5= Shot(27450, LHt=[(0.116,0.110,0.118)], HLt=[(0.305,0.303,0.306)])
#s6= 'Shot(27451, LHt=[(0.2665,0.266,0.267),(0.2847,0.284,0.2855)], HLt=[(0.273,0.2725,0.2735),(0.287,0.287,0.289)])
s7= Shot(27453, LHt=[(0.295,0.2945,0.2955)], HLt=[(0.3105,0.3099,0.311)])
s8= Shot(27454, LHt=[(0.277,0.276,0.278)], HLt=[(0.2893,0.289,0.290)])

#%%
session = '22-Jan-10' #Characterise the dynamics of the L-H transition by measuring density and temperature profile evolution with the enhanced Thomson scattering.
geometry = 'maybe CND'

from signal_dict_13_DEC_PULL import signals

s1= Shot(24134, LHt=[(0.3018,0.3016,0.302)], HLt=[(0.3448,0.344,0.345)])
s2= Shot(24133, LHt=[(0.2818,0.2815,0.282),(0.3286,0.3275,0.329)], HLt=[(0.3255,0.325,0.326),(0.3315,0.331,0.332)])
s3= Shot(24132, LHt=[(0.2637,0.262,0.264),(0.2945,0.294,0.295)], HLt=[(0.283,0.282,0.2835),(0.340,0.339,0.341)])
s4= Shot(24131, LHt=[(0.2905,0.290,0.291)], HLt=[(0.3366,0.3365,0.344)])
s5= Shot(24130, LHt=[(0.285,0.2845,0.2855)], HLt=[(0.3325,0.332,0.333)])
s6= Shot(24129, LHt=[(0.2922,0.290,0.295)], HLt=[(0.3174,0.317,0.318)])
s7= Shot(24128, LHt=[(0.2572,0.257,0.258)], HLt=[(0.3435,0.343,0.344)])
s8= Shot(24127, LHt=[(0.2738,0.273,0.274)], HLt=[(0.311,0.3105,0.3115)])
s9= Shot(24126, LHt=[(0.2781,0.278,0.2815)], HLt=[(0.3435,0.343,0.344)])
s10= Shot(24125, LHt=[(0.2856,0.285,0.286)], HLt=[(0.3232,0.323,0.3235)])
s11= Shot(24124, LHt=[(0.246,0.242,0.260)], HLt=[(0.2896,0.280,0.2897)])
 

