# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 13:15:40 2019

@author: Tomas
"""

import os

from signal_dict_SEP_08 import signals

shots = [
'Shot(20377, LHt=[(0.2339,0.2338,0.2340)], HLt=[(0.335,0.3349,0.3351)])',

'Shot(20378, LHt=[(0.2332,0.23309,0.23321)], HLt=[(0.2987,0.29869,0.29871)])',

'Shot(20379, LHt=[(0.2805,0.28049,0.28051)], HLt=[(0.314,0.308,0.3141)])',

'Shot(20380, LHt=[(0.2496,0.24959,0.24961)], HLt=[(0.2954,0.29539,0.29541)])',

'Shot(20381, LHt=[(0.2342,0.2341,0.2343)], HLt=[(0.3108,0.31079,0.31081)])',

'Shot(20476, LHt=[(0.2196,0.2195,0.2197)], HLt=[(0.3038,0.3037,0.3039)])',

'Shot(20479, LHt=[(0.1909,0.1908,0.1910)], HLt=[(0.3116,0.3115,0.3117)])',

'Shot(20480, LHt=[(0.1975,0.1974,0.1976)], HLt=[(0.267,0.2669,0.2671)])']

for shot in shots:
    s = eval(shot)
    os.chdir("C:/Users/Tomas/MAST_Edge_RT_Research/Scripts/MASTdata")
    try:
        os.rename(str(s.ShotNumber) + '_NE.p', str(s.ShotNumber) + '_AYC_NE.p')
    except: pass
    try:
        os.rename(str(s.ShotNumber) + '_TE.p', str(s.ShotNumber) + '_AYC_TE.p')
    except: pass
    try:
        os.rename(str(s.ShotNumber) + '_PE.p', str(s.ShotNumber) + '_AYC_PE.p')
    except: pass

print('blody done')

os.chdir("C:/Users/Tomas/MAST_Edge_RT_Research/Scripts/")
from signal_dict_10_NOV_11 import signals

shots = [
'Shot(20377, LHt=[(0.2339,0.2338,0.2340)], HLt=[(0.335,0.3349,0.3351)])',

'Shot(20378, LHt=[(0.2332,0.23309,0.23321)], HLt=[(0.2987,0.29869,0.29871)])',

'Shot(20379, LHt=[(0.2805,0.28049,0.28051)], HLt=[(0.314,0.308,0.3141)])',

'Shot(20380, LHt=[(0.2496,0.24959,0.24961)], HLt=[(0.2954,0.29539,0.29541)])',

'Shot(20381, LHt=[(0.2342,0.2341,0.2343)], HLt=[(0.3108,0.31079,0.31081)])',

'Shot(20476, LHt=[(0.2196,0.2195,0.2197)], HLt=[(0.3038,0.3037,0.3039)])',

'Shot(20479, LHt=[(0.1909,0.1908,0.1910)], HLt=[(0.3116,0.3115,0.3117)])',

'Shot(20480, LHt=[(0.1975,0.1974,0.1976)], HLt=[(0.267,0.2669,0.2671)])']

for shot in shots:
    s = eval(shot)
    s.plot_compare(['IP','BT','WMHD','AYC_NE','AYC_TE','Dalphint','ngrad','Ploss','PINJ' ])
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    