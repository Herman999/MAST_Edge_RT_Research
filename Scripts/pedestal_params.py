# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 10:37:24 2019

@author: Tomas
"""

# Pedestal parameters dependance on average density

from signal_dict_13_DEC_PULL import signals
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({'font.size': 17})


slices = 1


# need plot like x = ne average, y = ne at pedestal knee

# to get value at knee --> resutls
ne_average = []
ne_at_ped = []
te_at_ped = []
pe_at_ped = []

ne_average_e = []
te_at_ped_e = []
pe_at_ped_e = []

shot_list = []

def TE_point_at_pedestal(s,knee,t):
    index = np.where(s.data['AYC_TE']['time']==t)
    
    # remove nans
    #condition = np.where(~np.isnan(s.data['AYC_TE']['data'][index]))
    s.data['AYC_TE']['data'][index] = np.nan_to_num(s.data['AYC_TE']['data'][index])
    s.data['AYC_TE']['errors'][index] = np.nan_to_num(s.data['AYC_TE']['errors'][index])

    TE_knee = np.interp(knee,s.data['AYC_R']['data'][index][0],s.data['AYC_TE']['data'][index][0])
    TE_knee_e = np.interp(knee,s.data['AYC_R']['data'][index][0],s.data['AYC_TE']['errors'][index][0])
    
    return TE_knee,TE_knee_e
def PE_point_at_pedestal(s,knee,t):
    index = np.where(s.data['AYC_PE']['time']==t)
    
    # remove nans
    #condition = np.where(~np.isnan(s.data['AYC_TE']['data'][index]))
    s.data['AYC_PE']['data'][index] = np.nan_to_num(s.data['AYC_PE']['data'][index])
    s.data['AYC_PE']['errors'][index] = np.nan_to_num(s.data['AYC_PE']['errors'][index])
    
    PE_knee = np.interp(knee,s.data['AYC_R']['data'][index][0],s.data['AYC_PE']['data'][index][0])
    PE_knee_e = np.interp(knee,s.data['AYC_R']['data'][index][0],s.data['AYC_PE']['errors'][index][0])

    return PE_knee,PE_knee_e

def NE_point_at_pedestal(s,ne_at_ped,ne_average,slice_time,index):
     # now got what we need
    #slices = 1
    
    #res = s.fit_after_time(t1, slices, edge=True, sig='NE',prev=False)
    # result structure t0: (knee, width, max_slope, ne|max slope, ne at knee)
    #print(res)
    #print(slice_time)
    
    
    
    result, time, (x,y,x_er,y_er), canvas = s.fit_tanh_pedestal(index, scaling = 1./0.9, sig='NE', preview=False, guess=[3e19,2e19,1.47,0.05,1e19,1.,1.])
    res = s._tanh_params(result)
    
    
    ne_at_ped.append(res[4])
    try:
        index = np.where(s.data['AYC_NE']['time']==slice_time)
        ne_average.append(\
                          np.nanmean(s.data['AYC_NE']['data'][index]))
        ne_average_e.append(\
                          np.nanmean(s.data['AYC_NE']['errors'][index]))
    except: pass
    try:
        index = np.where(s.data['NE']['time']==slice_time)
        ne_average.append(\
                          np.nanmean(s.data['NE']['data'][index]))
        ne_average_e.append(\
                          np.nanmean(s.data['NE']['errors'][index]))
    except: pass
    print('Got ONE!')
    return ne_at_ped,ne_average,res[0],slice_time,ne_average_e
#%%


    
#%%
    #here load up shot session
    
#%%
from signal_dict_10_NOV_11 import signals
shots = [
'Shot(27030, LHt=[(0.1928, 0.193, 0.1927)], HLt=[(0.1963, 0.1963,0.19637)])',
'Shot(27035, LHt=[(0.2868,0.2865,0.287)], HLt = [(0.3096,0.3096,0.3098)])',
'Shot(27036, LHt = [(0.2565, 0.2545,0.258)], HLt = [(0.3261,0.3261,0.327)])',
'Shot(27037, LHt=[(0.2607,0.260,0.261)], HLt = [(0.3247, 0.3246, 0.3252)])',
'Shot(27444, LHt=[(0.259,0.2545,0.2595)], HLt=[(0.324,0.323,0.325)])',
'Shot(27446, LHt=[(0.276,0.274,0.2765)], HLt=[(0.3074,0.307,0.308)])',
'Shot(27448, LHt=[(0.110,0.105,0.118)], HLt=[(0.2894,0.2893,0.2895)])',
'Shot(27449, LHt=[(0.115,0.110,0.120)], HLt=[(0.301,0.300,0.306)])',
'Shot(27450, LHt=[(0.116,0.110,0.118)], HLt=[(0.305,0.303,0.306)])',
 #'Shot(27451, LHt=[(0.2665,0.266,0.267),(0.2847,0.284,0.2855)], HLt=[(0.273,0.2725,0.2735),(0.287,0.287,0.289)])',
'Shot(27453, LHt=[(0.295,0.2945,0.2955)], HLt=[(0.3105,0.3099,0.311)])',
'Shot(27454, LHt=[(0.277,0.276,0.278)], HLt=[(0.2893,0.289,0.290)])'
 ]    

#%%
from signal_dict_13_DEC_PULL import signals
shots = [
'Shot(24134, LHt=[(0.3018,0.3016,0.302)], HLt=[(0.3448,0.344,0.345)])',
'Shot(24133, LHt=[(0.2818,0.2815,0.282),(0.3286,0.3275,0.329)], HLt=[(0.3255,0.325,0.326),(0.3315,0.331,0.332)])',
'Shot(24132, LHt=[(0.2637,0.262,0.264),(0.2945,0.294,0.295)], HLt=[(0.283,0.282,0.2835),(0.340,0.339,0.341)])',
'Shot(24131, LHt=[(0.2905,0.290,0.291)], HLt=[(0.3366,0.3365,0.344)])',
'Shot(24130, LHt=[(0.285,0.2845,0.2855)], HLt=[(0.3325,0.332,0.333)])',
'Shot(24129, LHt=[(0.2922,0.290,0.295)], HLt=[(0.3174,0.317,0.318)])',
'Shot(24128, LHt=[(0.2572,0.257,0.258)], HLt=[(0.3435,0.343,0.344)])',
'Shot(24127, LHt=[(0.2738,0.273,0.274)], HLt=[(0.311,0.3105,0.3115)])',
'Shot(24126, LHt=[(0.2781,0.278,0.2815)], HLt=[(0.3435,0.343,0.344)])',
'Shot(24125, LHt=[(0.2856,0.285,0.286)], HLt=[(0.3232,0.323,0.3235)])',
'Shot(24124, LHt=[(0.246,0.242,0.260)], HLt=[(0.2896,0.288,0.2897)])', # I had to cut on the lower end of uncertainty here in HL
'Shot(24215, LHt=[(0.2515,0.2513,0.252)],HLt=[(0.284,0.2839,0.2841)])',
'Shot(24216, LHt=[(0.2537,0.25369,0.254), (0.3174,0.31739,0.3176)],HLt=[(0.2845,0.28449,0.2847), (0.3585,0.3579, 0.3586)])',
'Shot(24324, LHt=[(0.2535,0.2533,0.2536), (0.3181,0.3175,0.3189)],HLt=[(0.2823,0.2821,0.2824), (0.3431,0.3423,0.34311)])',
'Shot(24325, LHt=[(0.2515,0.2512,0.2518), (0.319, 0.317,0.321)],HLt=[(0.2845,0.2843,0.2847), (0.345,0.344,0.346)])',
'Shot(24326, LHt=[(0.2515, 0.251, 0.252)],HLt=[(0.284,0.2839, 0.2845)])',
'Shot(24327, LHt=[(0.2511,0.2508,0.2513)],HLt=[(0.2875, 0.2874, 0.2876)])',
'Shot(24328, LHt=[(0.251, 0.2506, 0.2514)],HLt=[(0.2895, 0.2894, 0.2896)])',
'Shot(24329, LHt=[(0.2625, 0.2624, 0.263), (0.318, 0.317, 0.319)],HLt=[(0.281, 0.2808, 0.2812), (0.3365, 0.3364, 0.3366)])',
'Shot(24330, LHt=[(0.252, 0.2517, 0.2521)],HLt=[(0.2842, 0.2841, 0.2843)])'
] 
    
#%%
# new data shots
from signal_dict_2019_IP import signals
shots = [
'Shot(30351, LHt=[(0.300, 0.295, 0.334)],HLt=[(0.620, 0.615, 0.622)])',
'Shot(30356, LHt=[(0.273, 0.270, 0.275)],HLt=[(0.2791, 0.2790, 0.2794)])',
'Shot(30358, LHt=[(0.1975, 0.19745, 0.1976)],HLt=[(0.3425, 0.342, 0.343)])',
'Shot(30358, LHt=[(0.2665, 0.266, 0.267),(0.385,0.384,0.3865)],HLt=[(0.3629, 0.3625, 0.363),(0.401,0.400,0.404)])',
'Shot(24431, LHt=[(0.2615, 0.261, 0.262)],HLt=[(0.3823, 0.382, 0.3877)])',
'Shot(24514, LHt=[(0.336, 0.335, 0.337)],HLt=[(0.3574, 0.357, 0.3575)])',
'Shot(24517, LHt=[(0.2794, 0.280, 0.285)],HLt=[(0.3086, 0.300, 0.301)])',
'Shot(24518, LHt=[(0.2907, 0.290, 0.292)],HLt=[(0.3535, 0.353, 0.3536)])',
'Shot(24522, LHt=[(0.2535, 0.253, 0.254)],HLt=[(0.3555, 0.355, 0.3558)])',
'Shot(24524, LHt=[(0.201, 0.197, 0.202)],HLt=[(0.355, 0.354, 0.3558)])',
'Shot(24524, LHt=[(0.201, 0.197, 0.202)],HLt=[(0.355, 0.354, 0.3558)])',
#H-mode Access and rotating RMP		
'Shot(29486, LHt=[(0.2681, 0.268, 0.2682)],HLt=[(0.3378, 0.3375, 0.3379)])',
'Shot(29487, LHt=[(0.2725, 0.2724, 0.2726)],HLt=[(0.378, 0.372, 0.385)])',
'Shot(29493, LHt=[(0.419, 0.418, 0.4195)],HLt=[(0.4395, 0.439, 0.4399)])',
'Shot(29496, LHt=[(0.279, 0.278, 0.280)],HLt=[(0.661, 0.660, 0.662)])',		
#L-H transition at low Ip vs Divertor Detachment		
'Shot(27571, LHt=[(0.258, 0.257, 0.259)],HLt=[(0.3065, 0.306, 0.307)])',
'Shot(27572, LHt=[(0.260, 0.255, 0.261)],HLt=[(0.2735, 0.273, 0.279)])',
'Shot(27573, LHt=[(0.268, 0.262, 0.2681)],HLt=[(0.2751, 0.275, 0.2755)])',
'Shot(27587, LHt=[(0.222, 0.221, 0.223)],HLt=[(0.268, 0.267, 0.269)])',
'Shot(27588, LHt=[(0.2222, 0.222, 0.2223)],HLt=[(0.2667, 0.265, 0.267)])',
'Shot(27589, LHt=[(0.2001, 0.200, 0.201)],HLt=[(0.329, 0.328, 0.3293)])'
]
 
#%%
for shot_str in shots:
    test = True
    s=eval(shot_str)
    
    #delete corrupted shots
    if s.ShotNumber in [24330,27030]:
        continue
    #with good fits with massive errors : [27036,27037,27444,27453,27587,27573,27571,29493,29487,30356,30351]
    # take only good data LH
    if s.ShotNumber not  in [27036,27037,27453,27571,29493,30356]:
        continue
    
    
#s = Shot(24129, LHt=[(0.2922,0.290,0.295)], HLt=[(0.3174,0.317,0.318)])
    # LH
    t0 = s._LHt[0][0]
    t1 = s._LHt[0][1]
    t2 = s._LHt[0][2]
   
    
    
    times_AYE = s.data['AYE_NE']['time'].copy()
    times_AYE -= t0
    index = np.argmin(abs(times_AYE))
    slice_time = s.data['AYE_NE']['time'][index]
    
    tolerance = 0.003
    if min(abs(times_AYE)) >= tolerance + abs(t0-t1) + abs (t2-t0):
        print('outside of tolerance')
        continue
    
    #result, time, (x,y,x_er,y_er) = s.fit_tanh_pedestal(index, scaling = 1./0.9, sig='NE', preview=True)
    #s._tanh_params(result)
    
    
    ne_at_ped,ne_average,knee,t,ne_average_e = NE_point_at_pedestal(s,ne_at_ped,ne_average,slice_time,index)
    
    te_at_ped.append(TE_point_at_pedestal(s,knee,t)[0])
    te_at_ped_e.append(TE_point_at_pedestal(s,knee,t)[1])
    
    pe_at_ped.append(PE_point_at_pedestal(s,knee,t)[0])
    pe_at_ped_e.append(PE_point_at_pedestal(s,knee,t)[1])
    shot_list.append(s.ShotNumber)
        
        
    """
    res = s.fit_after_time(t0, slices, edge=True, sig='NE',prev=False)
    slice_time = list(res.keys())[0]
    
    
    if slice_time < t2: # after transition time
        #ne
        ne_at_ped,ne_average,knee,t,ne_average_e = NE_point_at_pedestal(s,ne_at_ped,ne_average,slice_time,slice_time-0.00001)
        #te
        te_at_ped.append(TE_point_at_pedestal(s,knee,t)[0])
        te_at_ped_e.append(TE_point_at_pedestal(s,knee,t)[1])
        #pe
        pe_at_ped.append(PE_point_at_pedestal(s,knee,t)[0])
        pe_at_ped_e.append(PE_point_at_pedestal(s,knee,t)[1])
        shot_list.append(s.ShotNumber)
        
    else: # after trans time - error before
        res = s.fit_after_time(t1, slices, edge=True, sig='NE',prev=False)
        slice_time = list(res.keys())[0]
        if slice_time-0.001 < t2+0.001:
            #ne
            ne_at_ped,ne_average,knee,t,ne_average_e = NE_point_at_pedestal(s,ne_at_ped,ne_average,slice_time,slice_time-0.00001)
            #te
            te_at_ped.append(TE_point_at_pedestal(s,knee,t)[0])
            te_at_ped_e.append(TE_point_at_pedestal(s,knee,t)[1])
            #pe
            pe_at_ped.append(PE_point_at_pedestal(s,knee,t)[0])
            pe_at_ped_e.append(PE_point_at_pedestal(s,knee,t)[1])
            shot_list.append(s.ShotNumber)
            
        else:
            test = False
            print('AYE not within transition times')
    # Plot the fit and manually investigate
    #if test !=False:
        #pass
        #res = s.fit_after_time(slice_time-0.0000000000001, slices, edge=True, sig='NE',prev=True)        
    """

#%%
            
LH_ne_at_ped = ne_at_ped
LH_te_at_ped = te_at_ped
LH_pe_at_ped = pe_at_ped
LH_ne_average = ne_average
LH_shot_list = shot_list

LH_ne_average_e = ne_average_e
LH_te_at_ped_e = te_at_ped_e
LH_pe_at_ped_e = pe_at_ped_e 



#%%
#Anaylysis HL

ne_average = []
ne_at_ped = []
te_at_ped = []
pe_at_ped = []
shot_list = []

ne_average_e = []
te_at_ped_e = []
pe_at_ped_e = []

#%%
for shot_str in shots:

    s=eval(shot_str)
   
    
    #delete corrupted shots
    if s.ShotNumber in [24130,24133,27449,27444,27037]:  #24330,27030,24133,20377,27444,27449,27037]:
        print('skip')
        continue
    
    
    
    # good fits HL
    # take only good data
    if s.ShotNumber not  in [24215,24330,24127,24124,27035,27036,27587,27571]:
        continue
    
#s = Shot(24129, LHt=[(0.2922,0.290,0.295)], HLt=[(0.3174,0.317,0.318)])
    # LH
    #t0 = s._LHt[0][0]
    #t1 = s._LHt[0][1]
    #t2 = s._LHt[0][2]
    # HL
    t0 = s._HLt[0][0]
    t1 = s._HLt[0][1]
    t2 = s._HLt[0][2]
    
    
    times_AYE = s.data['AYE_NE']['time'].copy()
    times_AYE -= t0
    index = np.argmin(abs(times_AYE))
    slice_time = s.data['AYE_NE']['time'][index]
    
    tolerance = 0.002
    if min(abs(times_AYE)) >= tolerance:
        print('outside of tolerance')
        continue
    
    #result, time, (x,y,x_er,y_er) = s.fit_tanh_pedestal(index, scaling = 1./0.9, sig='NE', preview=True)
    #s._tanh_params(result)
    
    
    ne_at_ped,ne_average,knee,t,ne_average_e = NE_point_at_pedestal(s,ne_at_ped,ne_average,slice_time,index)
    
    te_at_ped.append(TE_point_at_pedestal(s,knee,t)[0])
    te_at_ped_e.append(TE_point_at_pedestal(s,knee,t)[1])
    
    pe_at_ped.append(PE_point_at_pedestal(s,knee,t)[0])
    pe_at_ped_e.append(PE_point_at_pedestal(s,knee,t)[1])
    shot_list.append(s.ShotNumber)
        
    
    """
    res = s.fit_after_time(t0, slices, edge=True, sig='NE',prev=False)
    slice_time = list(res.keys())[0]
    
    if slice_time < t2: # after transition time
        #ne
        ne_at_ped,ne_average,knee,t,ne_average_e = NE_point_at_pedestal(s,ne_at_ped,ne_average,slice_time,slice_time-0.00001)
        #te
        te_at_ped.append(TE_point_at_pedestal(s,knee,t)[0])
        te_at_ped_e.append(TE_point_at_pedestal(s,knee,t)[1])
        #pe
        pe_at_ped.append(PE_point_at_pedestal(s,knee,t)[0])
        pe_at_ped_e.append(PE_point_at_pedestal(s,knee,t)[1])
        shot_list.append(s.ShotNumber)
        
    else: # after trans time - error before
        res = s.fit_after_time(t1, slices, edge=True, sig='NE',prev=False)
        slice_time = list(res.keys())[0]
        if slice_time-0.001 < t2+0.001:
            #ne
            ne_at_ped,ne_average,knee,t,ne_average_e = NE_point_at_pedestal(s,ne_at_ped,ne_average,slice_time,slice_time-0.00001)
            #te
            te_at_ped.append(TE_point_at_pedestal(s,knee,t)[0])
            te_at_ped_e.append(TE_point_at_pedestal(s,knee,t)[1])
            #pe
            pe_at_ped.append(PE_point_at_pedestal(s,knee,t)[0])
            pe_at_ped_e.append(PE_point_at_pedestal(s,knee,t)[1])
            shot_list.append(s.ShotNumber)
            
        else:
            print('AYE not within transition times')
    """

#%%
            
HL_ne_at_ped = ne_at_ped
HL_te_at_ped = te_at_ped # exlusion of one dodgy shot
HL_pe_at_ped = pe_at_ped
HL_ne_average = ne_average
HL_shot_list = shot_list

HL_ne_average_e = ne_average_e
HL_te_at_ped_e = te_at_ped_e # exclusion of one dodgy shot
HL_pe_at_ped_e = pe_at_ped_e 

#%%

ne_average = LH_ne_average.copy()
ne_average.extend(HL_ne_average)

ne_at_ped = LH_ne_at_ped.copy()
ne_at_ped.extend(HL_ne_at_ped)


te_at_ped = LH_te_at_ped.copy()
te_at_ped.extend(HL_te_at_ped)

pe_at_ped = LH_pe_at_ped.copy()
pe_at_ped.extend(HL_pe_at_ped)

# errors

ne_average_e = LH_ne_average_e.copy()
ne_average_e.extend(HL_ne_average_e)

te_at_ped_e = LH_te_at_ped_e.copy()
te_at_ped_e.extend(HL_te_at_ped_e)

pe_at_ped_e = LH_pe_at_ped_e.copy()
pe_at_ped_e.extend(HL_pe_at_ped_e)

#%% PL<OT

# NE            
#fig, ax = plt.subplots(3,sharex=True,figsize=(13,9))

fig, ax = plt.subplots(3,sharex=True,figsize=(11.5,6))


textstr = r'$I_p$ $450-900$kA $B_t$ $0.37-0.45$T'
ax[0].text(3.65e19, 4.65e19, textstr, fontsize=14)

#ax[0].set_title(r'Pedestal Characteristics on $\overline{n_e}$')
ax[0].errorbar(fmt='o',x=LH_ne_average,y=LH_ne_at_ped,xerr=LH_ne_average_e,c='red',label='LH')
ax[0].errorbar(fmt='o',x=HL_ne_average,y=HL_ne_at_ped,xerr=HL_ne_average_e,c='blue',label='HL')
#ax[0].scatter(LH_ne_average,LH_ne_at_ped,c='orange',label='LH')
#ax[0].scatter(HL_ne_average,HL_ne_at_ped,c='blue',label='HL')

#plt.rcParams.update({'font.size': 14})
#for i, txt in enumerate(LH_shot_list):
#    ax[0].annotate(txt, (LH_ne_average[i], LH_ne_at_ped[i]))
#    
#for i, txt in enumerate(HL_shot_list):
#    ax[0].annotate(txt, (HL_ne_average[i], HL_ne_at_ped[i]))
plt.rcParams.update({'font.size': 17})
# lin fit
(res,cov) = np.polyfit(ne_average,ne_at_ped,deg=1,cov=True)
neav = np.linspace(min(ne_average),max(ne_average))
nefit = res[1] + res[0] * neav
ax[0].plot(neav,nefit,'--')#,label=r'fit k={0}$\pm${1} '.format("{:.2E}".format(res[0]),"{:.2E}".format(cov[0,0]),"{:.2E}".format(res[1])))
ax[0].set_ylim([0,4.5e19])
#ax[0].set_xlabel(r'$\overline{n_e}$ [$m^{-3}$]')
ax[0].set_ylabel(r'$ne_{ped} [M^{-3}]$')
ax[0].legend(loc=4)
#ax[0].set_ylim([0,0.05e21])

# TE
#ax[1].scatter(LH_ne_average,LH_te_at_ped,c='orange',label='LH')
#ax[1].scatter(HL_ne_average,HL_te_at_ped,c='blue',label='HL')
ax[1].errorbar(fmt='o',x=LH_ne_average,y=LH_te_at_ped,xerr=LH_ne_average_e,yerr=LH_te_at_ped_e,c='red',label='LH')
ax[1].errorbar(fmt='o',x=HL_ne_average,y=HL_te_at_ped,xerr=HL_ne_average_e,yerr=HL_te_at_ped_e,c='blue',label='HL')
#plt.rcParams.update({'font.size': 14})
#for i, txt in enumerate(LH_shot_list):
#    ax[1].annotate(txt, (LH_ne_average[i], LH_te_at_ped[i]))
#    
#for i, txt in enumerate(HL_shot_list):
#    ax[1].annotate(txt, (HL_ne_average[i], HL_te_at_ped[i]))
#plt.rcParams.update({'font.size': 17})
(res,cov) = np.polyfit(ne_average,te_at_ped,w=1/np.sqrt(np.array(ne_average_e)**2+np.array(te_at_ped)**2),deg=1,cov=True)
neav = np.linspace(min(ne_average),max(ne_average))
nefit = res[1] + res[0] * neav
#ax[1].plot(neav,nefit,'--',label=r'fit k={0}$\pm${1} '.format("{:.2E}".format(res[0]),"{:.2E}".format(cov[0,1]),"{:.2E}".format(res[1])))
ax[1].set_ylim([-10,250])
#attempt for error calculation
#nefitm = res[1] + (res[0] ) * neav - cov[0,0]
#nefitp = res[1] + (res[0] ) * neav + cov[0,0]
#ax[1].plot(neav,nefitm,color = 'orange',linestyle = 'dashed', alpha = 0.5)
#ax[1].plot(neav,nefitp,color = 'orange',linestyle = 'dashed', alpha = 0.5)
#ax[1].set_ylim([0,455])
#ax[1].set_xlim([0,4e19])
#ax[1].set_xlabel(r'$\overline{n_e}$ [$m^{-3}$]')
ax[1].set_ylabel(r'$Te_{ped} [eV]$')
#ax[1].legend()

# PE
#ax[2].scatter(LH_ne_average,LH_pe_at_ped,c='orange',label='LH')
#ax[2].scatter(HL_ne_average,HL_pe_at_ped,c='blue',label='HL')
ax[2].errorbar(fmt='o',x=LH_ne_average,y=LH_pe_at_ped,xerr=LH_ne_average_e,yerr=LH_pe_at_ped_e,c='red',label='LH')
ax[2].errorbar(fmt='o',x=HL_ne_average,y=HL_pe_at_ped,xerr=HL_ne_average_e,yerr=HL_pe_at_ped_e,c='blue',label='HL')
#plt.rcParams.update({'font.size': 17})
#for i, txt in enumerate(LH_shot_list):
#    ax[2].annotate(txt, (LH_ne_average[i], LH_pe_at_ped[i]))
#    
#for i, txt in enumerate(HL_shot_list):
#    ax[2].annotate(txt, (HL_ne_average[i], HL_pe_at_ped[i]))
#plt.rcParams.update({'font.size': 17})    

#(res,cov) = np.polyfit(ne_average,pe_at_ped,deg=1,cov=True)
(res,cov) = np.polyfit(ne_average,pe_at_ped,w=1/np.sqrt(np.array(ne_average_e)**2+np.array(pe_at_ped)**2),deg=1,cov=True)
neav = np.linspace(min(ne_average),max(ne_average))
nefit = res[1] + res[0] * neav
ax[2].plot(neav,nefit,'--',label=r'fit k={0}$\pm${1} '.format("{:.2E}".format(res[0]),"{:.2E}".format(cov[0,0]),"{:.2E}".format(res[1])))

ax[2].set_xlabel(r'$\overline{n_e}$ [$m^{-3}$]')
ax[2].set_ylabel(r'$Pe_{ped} [a.u.]$')
#ax[2].legend()

#%%

# export pedestal params into DB Pandas



import pandas as pd

# want to save SHot, LH/HL, ne average +e , ne at ped +e , te at ped +e, pe at ped +e

ped_db = pd.DataFrame(columns=['shot', 'transition', 'ne_average','ne_average_e','ne_at_ped','ne_at_ped_e','te_at_ped','te_at_ped_e','pe_at_ped','pe_at_ped_e'])

for i in range(len(LH_ne_average)):
    dic = {}
    dic['shot'] = LH_shot_list[i]
    dic['transition'] = 'LH'
    dic['ne_average'] = LH_ne_average[i]
    dic['ne_average_e'] = LH_ne_average_e[i]
    dic['ne_at_ped'] = LH_ne_at_ped[i]
    dic['ne_at_ped_e'] = 0
    dic['te_at_ped'] = LH_te_at_ped[i]
    dic['te_at_ped_e'] =  LH_te_at_ped_e[i]
    dic['pe_at_ped'] = LH_pe_at_ped[i]
    dic['pe_at_ped_e'] = LH_pe_at_ped_e[i]
    ped_db.loc[len(ped_db)]=dic
    
for i in range(len(HL_ne_average)):
    dic = {}
    dic['shot'] = HL_shot_list[i]
    dic['transition'] = 'HL'
    dic['ne_average'] = HL_ne_average[i]
    dic['ne_average_e'] = HL_ne_average_e[i]
    dic['ne_at_ped'] = HL_ne_at_ped[i]
    dic['ne_at_ped_e'] = 0
    dic['te_at_ped'] = HL_te_at_ped[i]
    dic['te_at_ped_e'] =  HL_te_at_ped_e[i]
    dic['pe_at_ped'] = HL_pe_at_ped[i]
    dic['pe_at_ped_e'] = HL_pe_at_ped_e[i]
    ped_db.loc[len(ped_db)]=dic
    
writer = pd.ExcelWriter('ML_data_PED_new.xlsx')
ped_db.to_excel(writer,'Sheet1')
writer.save()





    






























