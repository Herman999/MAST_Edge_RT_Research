# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 11:26:47 2019

@author: rbatt

Psi 95 justification or not
"""
import numpy as np

#%% data import
from Shot_Class import Shot
session = '06-Oct-11'  #Measure LH power threshold at a range of densities.
geometry = 'CND'
#buggy runfile command hopefully works here
runfile('C:/Users/rbatt/MAST_Edge_RT_Research/Scripts/Shot_Class.py', wdir='C:/Users/rbatt/MAST_Edge_RT_Research/Scripts')
from signal_dict_06_OCT_11 import signals
#s1= Shot(27030, LHt=[(0.1928, 0.193, 0.1927)], HLt=[(0.1963, 0.1963,0.19637)]) ### bad shot
s2= Shot(27035, LHt=[(0.2868,0.2865,0.287)], HLt = [(0.3096,0.3096,0.3098)])
s3= Shot(27036, LHt = [(0.2565, 0.2545,0.258)], HLt = [(0.3261,0.3261,0.327)])
s4= Shot(27037, LHt=[(0.2607,0.260,0.261)], HLt = [(0.3247, 0.3246, 0.3252)])

#%% show data
s2.plot_JP(plot_thomson=4,label_thomson=True)
s3.plot_JP(plot_thomson=4,label_thomson=True)
s4.plot_JP(plot_thomson=4,label_thomson=True)

#%% Get Psi's

#for s2
inds = np.arange(69,75) # 69 to 74
pguess=[3.0e19,2.0e19,1.47,0.03,1.0e19,1,1] # parameter guess for skinny pedestals
for i in inds:
    print(i)
    result, time, data = s2.fit_tanh_pedestal(i,guess=pguess)
    knee, width, max_slope, ne_max_slope, ne_at_knee = s2._tanh_params(result)
    
    