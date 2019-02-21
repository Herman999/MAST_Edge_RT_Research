# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 10:37:24 2019

@author: Tomas
"""

# Pedestal parameters dependance on average density

from signal_dict_13_DEC_PULL import signals
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({'font.size': 14})


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
    
    
    
    result, time, (x,y,x_er,y_er), canvas = s.fit_tanh_pedestal(index, scaling = 1./0.9, sig='NE', preview=True, guess=[3e19,2e19,1.47,0.05,1e19,1.,1.])
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
for shot_str in shots:
    test = True
    s=eval(shot_str)
    
    #delete corrupted shots
    if s.ShotNumber in [24330,27030]:
        continue
    
    # take only good data
    if s.ShotNumber not  in [27036,27037,27444,27453]:
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
    
    
    
    # take only good data
    if s.ShotNumber not  in [24215,24330,24127,24124,27035,27036]:
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
HL_te_at_ped = te_at_ped
HL_pe_at_ped = pe_at_ped
HL_ne_average = ne_average
HL_shot_list = shot_list

HL_ne_average_e = ne_average_e
HL_te_at_ped_e = te_at_ped_e
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
fig, ax = plt.subplots(3,sharex=True,figsize=(13,9))
ax[0].set_title(r'Pedestal Characteristics on Average Density')
ax[0].errorbar(fmt='o',x=LH_ne_average,y=LH_ne_at_ped,xerr=LH_ne_average_e,c='orange',label='LH')
ax[0].errorbar(fmt='o',x=HL_ne_average,y=HL_ne_at_ped,xerr=HL_ne_average_e,c='blue',label='HL')
#ax[0].scatter(LH_ne_average,LH_ne_at_ped,c='orange',label='LH')
#ax[0].scatter(HL_ne_average,HL_ne_at_ped,c='blue',label='HL')

for i, txt in enumerate(LH_shot_list):
    ax[0].annotate(txt, (LH_ne_average[i], LH_ne_at_ped[i]))
    
for i, txt in enumerate(HL_shot_list):
    ax[0].annotate(txt, (HL_ne_average[i], HL_ne_at_ped[i]))

# lin fit
(res,cov) = np.polyfit(ne_average,ne_at_ped,deg=1,cov=True)
neav = np.linspace(min(ne_average),max(ne_average))
nefit = res[1] + res[0] * neav
ax[0].plot(neav,nefit,'--',label=r'fit k={0}$\pm${1} '.format("{:.2E}".format(res[0]),"{:.2E}".format(cov[0,0]),"{:.2E}".format(res[1])))
    
ax[0].set_xlabel(r'$\overline{N_e}$')
ax[0].set_ylabel(r'$Ne_{ped} [M^{-3}]$')
ax[0].legend()
#ax[0].set_ylim([0,0.05e21])

# TE
#ax[1].scatter(LH_ne_average,LH_te_at_ped,c='orange',label='LH')
#ax[1].scatter(HL_ne_average,HL_te_at_ped,c='blue',label='HL')
ax[1].errorbar(fmt='o',x=LH_ne_average,y=LH_te_at_ped,xerr=LH_ne_average_e,yerr=LH_te_at_ped_e,c='orange',label='LH')
ax[1].errorbar(fmt='o',x=HL_ne_average,y=HL_te_at_ped,xerr=HL_ne_average_e,yerr=HL_te_at_ped_e,c='blue',label='HL')
for i, txt in enumerate(LH_shot_list):
    ax[1].annotate(txt, (LH_ne_average[i], LH_te_at_ped[i]))
    
for i, txt in enumerate(HL_shot_list):
    ax[1].annotate(txt, (HL_ne_average[i], HL_te_at_ped[i]))

(res,cov) = np.polyfit(ne_average,te_at_ped,w=1/np.sqrt(np.array(ne_average_e)**2+np.array(te_at_ped)**2),deg=1,cov=True)
neav = np.linspace(min(ne_average),max(ne_average))
nefit = res[1] + res[0] * neav
ax[1].plot(neav,nefit,'--',label=r'fit k={0}$\pm${1} '.format("{:.2E}".format(res[0]),"{:.2E}".format(cov[0,1]),"{:.2E}".format(res[1])))

#attempt for error calculation
#nefitm = res[1] + (res[0] ) * neav - cov[0,0]
#nefitp = res[1] + (res[0] ) * neav + cov[0,0]
#ax[1].plot(neav,nefitm,color = 'orange',linestyle = 'dashed', alpha = 0.5)
#ax[1].plot(neav,nefitp,color = 'orange',linestyle = 'dashed', alpha = 0.5)
#ax[1].set_ylim([0,455])
#ax[1].set_xlim([0,4e19])
ax[1].set_xlabel(r'$\overline{N_e}$')
ax[1].set_ylabel(r'$Te_{ped} [eV]$')
ax[1].legend()

# PE
#ax[2].scatter(LH_ne_average,LH_pe_at_ped,c='orange',label='LH')
#ax[2].scatter(HL_ne_average,HL_pe_at_ped,c='blue',label='HL')
ax[2].errorbar(fmt='o',x=LH_ne_average,y=LH_pe_at_ped,xerr=LH_ne_average_e,yerr=LH_pe_at_ped_e,c='orange',label='LH')
ax[2].errorbar(fmt='o',x=HL_ne_average,y=HL_pe_at_ped,xerr=HL_ne_average_e,yerr=HL_pe_at_ped_e,c='blue',label='HL')
for i, txt in enumerate(LH_shot_list):
    ax[2].annotate(txt, (LH_ne_average[i], LH_pe_at_ped[i]))
    
for i, txt in enumerate(HL_shot_list):
    ax[2].annotate(txt, (HL_ne_average[i], HL_pe_at_ped[i]))
    

#(res,cov) = np.polyfit(ne_average,pe_at_ped,deg=1,cov=True)
(res,cov) = np.polyfit(ne_average,pe_at_ped,w=1/np.sqrt(np.array(ne_average_e)**2+np.array(pe_at_ped)**2),deg=1,cov=True)
neav = np.linspace(min(ne_average),max(ne_average))
nefit = res[1] + res[0] * neav
ax[2].plot(neav,nefit,'--',label=r'fit k={0}$\pm${1} '.format("{:.2E}".format(res[0]),"{:.2E}".format(cov[0,0]),"{:.2E}".format(res[1])))

ax[2].set_xlabel(r'$\overline{N_e}$')
ax[2].set_ylabel(r'$Pe_{ped} [a.u.]$')
ax[2].legend()

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
    
writer = pd.ExcelWriter('shot_peddb_only_good_shots.xlsx')
ped_db.to_excel(writer,'Sheet1')
writer.save()





    






























