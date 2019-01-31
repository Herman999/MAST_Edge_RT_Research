# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 10:37:24 2019

@author: Tomas
"""

# Pedestal parameters dependance on average density

from signal_dict_13_DEC_PULL import signals
import matplotlib.pyplot as plt
import numpy as np



slices = 1


# need plot like x = ne average, y = ne at pedestal knee

# to get value at knee --> resutls
ne_average = []
ne_at_ped = []

def NE_point_at_pedestal(s,ne_at_ped,ne_average,slice_time,t1):
     # now got what we need
    slices = 1
    res = s.fit_after_time(t1, slices, edge=True, sig='NE',prev=False)
    # result structure t0: (knee, width, max_slope, ne|max slope, ne at knee)
    #print(res)
    #print(slice_time)
    ne_at_ped.append(res[slice_time][4])
    try:
        index = np.where(s.data['AYC_NE']['time']==slice_time)
        ne_average.append(\
                          np.nanmean(s.data['AYC_NE']['data'][index]))
    except: pass
    try:
        index = np.where(s.data['NE']['time']==slice_time)
        ne_average.append(\
                          np.nanmean(s.data['NE']['data'][index]))
    except: pass
    return ne_at_ped,ne_average
#%%


    
#%%
    #here load up shot session
#%%
for shot_str in shots:

    s=eval(shot_str)
    
    #delete corrupted shots
    if s.ShotNumber in [24330]:
        continue
#s = Shot(24129, LHt=[(0.2922,0.290,0.295)], HLt=[(0.3174,0.317,0.318)])
    # LH
    t0 = s._LHt[0][0]
    t1 = s._LHt[0][1]
    t2 = s._LHt[0][2]
    
    
    res = s.fit_after_time(t0, slices, edge=True, sig='NE',prev=False)
    slice_time = list(res.keys())[0]
    
    if slice_time < t2: # after transition time
        ne_at_ped,ne_average = NE_point_at_pedestal(s,ne_at_ped,ne_average,slice_time,slice_time-0.00001)
    else: # after trans time - error before
        res = s.fit_after_time(t1, slices, edge=True, sig='NE',prev=False)
        slice_time = list(res.keys())[0]
        if slice_time < t2:
            ne_at_ped,ne_average = NE_point_at_pedestal(s,ne_at_ped,ne_average,slice_time,t1)
        else:
            print('AYE not within transition times')
#%%
plt.figure('LH Pedestal Params test')
plt.scatter(ne_average,ne_at_ped)
plt.xlabel('ne average')
plt.ylabel('ne at pedestal')





