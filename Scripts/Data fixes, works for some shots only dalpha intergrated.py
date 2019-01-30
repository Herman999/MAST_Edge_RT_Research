# -*- coding: utf-8 -*-
"""
Created on Mo Aug 06 2018

@author: jb4317, Jan-Peter Baehner

Programme to analyse shots helium experiment studies and reference shots in deuterium.
Shots loaded (including H-mode phases):
Deuterium18SEP08
    20377
    20378
    20379
    20380
    20381 
Deuterium25SEP08
    (20474 - 2 H-modes) TS times are off
    (20475) TS times are off
    20476
    20479 - 2 H-modes
    20480 - 2 H-modes    
Helium06NOV08:
    (20832 - ref shot) - only Ip, Ne0 and ne0 signal, not inlcuded here
    20841
    20842
    20843
    20848
    20849
    20850
    20852
Helium11NOV08:
    20856
    20859
    20861 - no Ruby TS data!
    20862
    20863
Helium10JUN09:
    22647 - ref shot
    22649
    22650
    22652
    22653
    22656    
"""

import matplotlib.pyplot as plt
import math
import numpy as np
from data_access_funcs import load_signal_data,signals

# Helium and Deuterium L-H sessions
shotnos=[20377, 20378, 20379, 20380, 20381,               #Deuterium18SEP08 [0-4] 5
         20476, 20479, 20480,                             #Deuterium25SEP08 [5-7] 3
         20841, 20842, 20843, 20848, 20849, 20850,20852,  #Helium06NOV08 [8-13] 7
         20856, 20859, 20861, 20862, 20863,               #Helium11NOV08 [14-18] 5
         22647, 22649, 22650, 22652, 22653, 22656]        #Helium10JUN09 [19-24] 6
        
shotnos = [24426]#,24430]  # some good shots       

data=[{} for shot in shotnos]
# =============================================================================
# data is a list of shots
# each shot contains a dictionary, where the names of the signals are the keys
# and the keyvalues are again a dictionary of data, errors, time and units
# =============================================================================
notloaded=[] #list of signals that could not be loaded, because the corresponding file does not exist.

#%% load data and write to 'data'

for i,shot in enumerate(shotnos):
    for sig in signals:
        try:
            filename=str(shot)+'_'+sig+'.p'
            data[i][sig]=load_signal_data(filename) #set data of sig to key sig
        except FileNotFoundError:
            if sig not in notloaded:
                notloaded.append(sig)
# print out confirmation on loaded signals
if not notloaded:
    print('All signals could be loaded.')
else:
    print('Signals that could not be loaded: ',*notloaded)


#%%
    
# fix for NE
corrupted_sigs = ['NE','NE0','R_CTS','TE0']

for i,shot in enumerate(shotnos):
    for sig in corrupted_sigs:
        try:
            filename=str(shot)+'_'+sig+'.p'
            data[i][sig]=load_signal_data(filename) #set data of sig to key sig
        except FileNotFoundError:
            sig='AYC_'+sig
            try:
                data[i][sig]=load_signal_data(filename)
            except:
                pass
            
#%% 20861 has no Ruby TS data - make up for it
#data[shotnos.index(20861)]['NE12_R']=dict(data=[],units='',time=[0])

#%% average density (from core TS) over profile for each timeslot:
# in this average the points are weighted by their radial distance to neighbouring points
ne_=[[] for shot in shotnos] #empty list for average
ne_err=[[] for shot in shotnos] #empty list for average
for i in range(len(shotnos)):
    shot = shotnos[i] 
    
    # prepare the iterative range with switch to signal
    try:
        a= range(len(data[i]['NE']['data']))
        ne_sig = 'NE'
    except:
        a=range(len(data[i]['AYC_NE']['data']))
        ne_sig = 'AYC_NE'
    for j in  a: # loop through time slots
        
        if shot > 20350 and shot < 22660:
            nej=list(data[i][ne_sig]['data'][j]) # density profile for time j
            nej_err=list(data[i][ne_sig]['errors'][j]) # error of density profile for time j
            Rj=list(data[i]['R2_CTS']['data'][j]) # radii for time j
            Rj_err=list(data[i]['R2_CTS']['errors'][j]) # error of radii for time j
            nan_indices=[]
            for n in range(len(nej)): # find 'nan' values
                if math.isnan(nej[n]):
                    nan_indices.append(n)
            for k in range(len(nan_indices)): # delete 'nan' entries and corresponding positions in R
                del nej[nan_indices[k]-k]
                del nej_err[nan_indices[k]-k]
                del Rj[nan_indices[k]-k]
            
            if len(nej)<3: # for the case that nej is too short or empty because too many values were 'nan'
                nej=[0,0,0]
                nej_err=[0,0,0]
                Rj=[data[i]['R2_CTS']['data'][j][0],data[i]['R2_CTS']['data'][j][round(len(data[i]['R2_CTS']['data'][j])/2)],data[i]['R2_CTS']['data'][j][-1]]
                
            ne_t=0 # time average at that timeslot
            ne_t_err_sq=0 # square of error of average at that timeslot
            
            ne_t+=nej[0]*abs(Rj[1]-Rj[0]) #first entry
            for n in range(len(nej)-2): #all entries between first and last
                ne_t+=nej[n+1]*abs(Rj[n+2]-Rj[n])/2
            ne_t+=nej[-1]*abs(Rj[-1]-Rj[-2]) #last entry
            ne_t=ne_t/abs(Rj[-1]-Rj[0]) #divide by whole range of R
            ne_[i].append(ne_t)
            
            ne_t_err_sq+=(ne_t + nej[0] + nej[1]/2)**2*Rj_err[0]**2 + (nej[-2]/2+nej[-1]-ne_t)**2*Rj_err[-1]**2 + (Rj[1]-Rj[0])**2*nej_err[0]**2 + (Rj[-1]-Rj[-2])**2*nej_err[-1]**2
            for n in range(len(nej)-2): #all entries between first and last
                ne_t_err_sq+=( (nej[n]-nej[n+2])**2*Rj_err[n+1]**2 + (Rj[n]-Rj[n+2])**2*nej_err[n+1]**2 )/4
            
            ne_err[i].append(np.sqrt(ne_t_err_sq)/abs(Rj[-1]-Rj[0]))
            
        if shot < 20350:
            Rj = data[i]['R12_R']
        if shot > 22660:
            
            #ne_average=[]
            #for TS_cut in range(len(data[i]['AYC_NE']['time'])): # this iterates across time
            #    ne_average.append(np.nanmean(data[i]['AYC_NE']['data'][TS_cut,:]))
            #print(len(data[i]['AYC_NE']['data']))
            try:
                ne_average = [np.nanmean(data[i]['AYC_NE']['data'][TS_cut,:]) for TS_cut in range(len(data[i]['AYC_NE']['time']))]
                data[i]['AYC_NE']['data']=np.asarray(ne_average)
        
            except:  pass
            try:
                neerr_average = [np.nanmean(data[i]['AYC_NE']['errors'][TS_cut,:]) for TS_cut in range(len(data[i]['AYC_NE']['time']))]
                data[i]['AYC_NE']['errors']=np.asarray(neerr_average)
            
            except: pass
        
            
        
        

        
        
    #ne_[i]=np.array(ne_[i])
    #ne_err[i]=np.array(ne_err[i])
    #nei_dict=dict(data=ne_[i],errors=ne_err[i],time=data[i]['NE']['time'],units=data[i]['NE']['units'])
    #data[i]['NE_']=nei_dict

#%% plot important signals of shots 

# time limits for each shot:
tlims=[[0.22,0.36],[0.22,0.31],[0.22,0.3166],[0.22,0.298],[0.22,0.35],                  #Deuterium18SEP08
       [0.18,0.325],[0.18,0.35],[0.18,0.3],                                             #Deuterium25SEP08
       [0.1,0.325],[0.1,0.35],[0.1,0.33],[0.1,0.327],[0.1,0.327],[0.1,0.36],[0.1,0.35], #Helium06NOV08
       [0.24,0.35],[0.24,0.336],[0.24,0.315],[0.24,0.43],[0.24,0.395],                  #Helium11NOV08
       [0.1,0.325],[0.1,0.46],[0.1,0.305],[0.1,0.3],[0.1,0.3],[0.2,0.315]]              #Helium10JUN09
# time of L-H transition for each shot:
tLH=[0.2339,0.2332,0.2805,0.2496,0.2342,               #Deuterium18SEP08
     0.2196,0.1909,0.1975,                             #Deuterium25SEP08
     0.2722,0.269, 0.2606,0.2744,0.2785,0.2753,0.2646, #Helium06NOV08
     0.2785,0.286, 0.2709,0.401,0.3,                   #Helium11NOV08
     0.2118,0.263,0.2364,0.2325,0.2433,0.2715]         #Helium10JUN09

tLH_err=[[None,None],[None,None],[None,None],[None,None],[None,None],                                                   #Deuterium18SEP08
         [None,None],[None,None],[None,None],                                                                           #Deuterium25SEP08
         [0.2664,0.2793],[0.2586,0.2734],[0.2559,0.2632],[0.2665,0.2785],[0.272,0.2799],[0.2695,0.2784],[0.26,0.2877],  #Helium06NOV08
         [0.2743,0.2785],[0.286,0.2868],[0.2709,0.2723],[None,None],[0.2996,0.3013],                                    #Helium11NOV08
         [None,None],[None,None],[0.2296,0.2364],[0.2281,0.2325],[0.2402,0.2457],[0.2715,0.298]]                        #Helium10JUN09
# time of H-L transition for each shot:
tHL=[0.335,0.2987,0.314,0.2954,0.3108,                  #Deuterium18SEP08
     0.3038,0.3116,0.267,                               #Deuterium25SEP08
     0.2855,0.3306,0.3181,0.3097,0.3031,0.3152,0.3442,  #Helium06NOV08
     0.2883,0.3221,0.2784,0.4115,0.3125,                #Helium11NOV08
     0.319,0.436,0.2715,0.284,0.2775,0.312]             #Helium10JUN09

tHL_err=[[None,None],[None,None],[0.308,0.314],[None,None],[None,None],                                                     #Deuterium18SEP08
         [None,None],[None,None],[None,None],                                                                               #Deuterium25SEP08
         [0.2855,0.2876],[0.3306,0.3325],[0.3152,0.3216],[0.3075,0.3147],[0.3031,0.3131],[0.3135,0.3152],[0.3442,0.3454],   #Helium06NOV08
         [0.2883,0.2906],[0.3221,0.3247],[0.2784,0.2971],[None,None],[0.31,0.3125],                                         #Helium11NOV08
         [None,None],[None,None],[None,None],[None,None],[None,None],[None,None]]                                           #Helium10JUN09

tLH=[0.236,0.20,0.20]
tHL=[0.334,0.2665,0.26]
tlims=[[0.2,0.35],[0.15,0.3],[0.15,0.3]]

plotsigs=['IP','WMHD','AYC_TE0','Dalphstrp','ngrad','BT','Ploss','PINJ','POHM']#,'Vloop'

plotsigs=['IP','AYC_NE','AYC_TE0','Dalphstrp','ngrad','BT','Ploss','PINJ','POHM']#,'Vloop'

#plotsiglabels=['$I_p$ [',r'$\bar{n}_e$ [$10^{19}$','$W_{MHD}$ [k','Core $T_e$ [k',r'$D_{\alpha}$ at strike point',r'edge $\nabla n_e$ [$10^{21}$','|$B_{T}$| [','$P_{loss}$ [M','$P_{NBI}$ [','$P_{ohmic}$ [M']#,'$V_{loop}$ ['
plotsiglabels=['$I_p$ [',r'$\bar{n}_e$ [$10^{19}$','Core $T_e$ [k',r'$D_{\alpha}$ at strike point',r'edge $\nabla n_e$ [$10^{21}$','|$B_{T}$| [','$P_{loss}$ [M','$P_{NBI}$ [','$P_{ohmic}$ [M']#,'$V_{loop}$ ['
norm=[1,1e19,1e3,1e3,1e18,1e21,-1,1e6,1,1e6]#,1

for i,shot in enumerate(shotnos):
    fig,ax=plt.subplots(len(plotsigs)-2,sharex=True,figsize=(11, 7))
    fig.subplots_adjust(top=0.935,bottom=0.09,left=0.08,right=0.975,hspace=0.0,wspace=0.2)
    if i<8:
        fig.suptitle('Deuterium experiment shot #%d' %shot)
    else:
        fig.suptitle('Helium experiment shot #%d' %shot)
    for j,sig in enumerate(plotsigs):
        if j < len(plotsigs) - 2:
            k=j
            # mark L-H and H-L transition:
            ax[k].axvline(tLH[i], c='g', lw=1, ls='--', clip_on=False)
            if tLH_err[i][0]:
                ax[k].axvline(tLH_err[i][0], c='g', lw=1, ls=':', clip_on=False)
                ax[k].axvline(tLH_err[i][1], c='g', lw=1, ls=':', clip_on=False)
            ax[k].axvline(tHL[i], c='r', lw=1, ls='--', clip_on=False)
            if tHL_err[i][0]:
                ax[k].axvline(tHL_err[i][0], c='r', lw=1, ls=':', clip_on=False)
                ax[k].axvline(tHL_err[i][1], c='r', lw=1, ls=':', clip_on=False)
            
            ax[k].plot(data[i][sig]['time'], data[i][sig]['data']/norm[j])
            # mark Ruby TS time
            #ax[k].axvline(data[i]['NE12_R']['time'][0], c='0.4', lw=1, ls='--', clip_on=False)
            
            # plot error as shadow around data-line:
            if sig!='AAYC_NE':
                try:
                    ax[k].fill_between(data[i][sig]['time'], (data[i][sig]['data']-data[i][sig]['errors'])/norm[j], (data[i][sig]['data']+data[i][sig]['errors'])/norm[j],alpha=0.3)
                except TypeError:
                    pass
        else:
            k=len(plotsigs) - 3 #plot last 3 signals in the same subplot
         
        # set limits of plot range and label data
        ind = (data[i][sig]['time'] > tlims[i][0]) &  (data[i][sig]['time'] < tlims[i][1])  # find indices of plotted range
        if sig == 'Dalphstrp':
            ax[k].set(xlim=tlims[i],ylim=[0,np.nanmax(data[i][sig]['data'][ind])/norm[j]])#/2
            ax[k].annotate(plotsiglabels[j], xy=(0.01,0.7),xycoords='axes fraction',fontsize=11)
            # label L-H and H-L transition
            trans = ax[k].get_xaxis_transform()
            ax[k].annotate('L-H', xy=(tLH[i]+0.001,0.75), xycoords=trans, fontsize=11,color='g')
            ax[k].annotate('H-L', xy=(tHL[i]-0.006,0.75), xycoords=trans, fontsize=11,color='r')
            # label Ruby TS time
            ax[k].annotate('Ruby TS', xy=(data[i]['NE12_R']['time'][0]+0.001,0.5), xycoords=trans, fontsize=9,color='0.4')
        # handling of power signals plotted in the same subplot:
        elif sig== 'Ploss':
            ax[k].annotate(plotsiglabels[j]+'%s]'%data[i][sig]['units'],color='c' , xy=(0.01,0.1),xycoords='axes fraction',fontsize=11)
            ax[k].plot(data[i][sig]['time'], data[i][sig]['data']/norm[j],color='c')
            yminloss=np.nanmin(data[i][sig]['data'][ind])/norm[j]
            ymaxloss=np.nanmax(data[i][sig]['data'][ind])/norm[j]
            # plot error as shadow around data-line:
            try:
                ax[k].fill_between(data[i][sig]['time'], (data[i][sig]['data']-data[i][sig]['errors'])/norm[j], (data[i][sig]['data']+data[i][sig]['errors'])/norm[j],alpha=0.3,color='c')
            except TypeError:
                pass
        elif sig== 'PINJ':
            ax[k].annotate(plotsiglabels[j]+'%s]'%data[i][sig]['units'],color='m' , xy=(0.01,0.4),xycoords='axes fraction',fontsize=11)
            ax[k].plot(data[i][sig]['time'], data[i][sig]['data']/norm[j],color='m')
            ymininj=np.nanmin(data[i][sig]['data'][ind])/norm[j]
            ymaxinj=np.nanmax(data[i][sig]['data'][ind])/norm[j]
            # plot error as shadow around data-line:
            try:
                ax[k].fill_between(data[i][sig]['time'], (data[i][sig]['data']-data[i][sig]['errors'])/norm[j], (data[i][sig]['data']+data[i][sig]['errors'])/norm[j],alpha=0.3,color='m')
            except TypeError:
                pass
        elif sig== 'POHM':
            ax[k].annotate(plotsiglabels[j]+'%s]'%data[i][sig]['units'],color='g', xy=(0.01,0.7),xycoords='axes fraction',fontsize=11)
            ax[k].plot(data[i][sig]['time'], data[i][sig]['data']/norm[j],color='g')
            ymin=min(yminloss,ymininj,np.nanmin(data[i][sig]['data'][ind])/norm[j])
            ymax=max(ymaxloss,ymaxinj,np.nanmax(data[i][sig]['data'][ind])/norm[j])
            ax[k].set(xlim=tlims[i],ylim=[ymin, ymax])
            # plot error as shadow around data-line:
            try:
                ax[k].fill_between(data[i][sig]['time'], (data[i][sig]['data']-data[i][sig]['errors'])/norm[j], (data[i][sig]['data']+data[i][sig]['errors'])/norm[j],alpha=0.3,color='g')
            except TypeError:
                pass
        else:
            ax[k].set(xlim=tlims[i],ylim=[np.nanmin(data[i][sig]['data'][ind])/norm[j], np.nanmax(data[i][sig]['data'][ind])/norm[j]])
            ax[k].annotate(plotsiglabels[j]+'%s]'%data[i][sig]['units'], xy=(0.01,0.7),xycoords='axes fraction',fontsize=11)
    ax[-1].set_xlabel('time [s]')
    #save figure:
#    if i<8:
#        figname='../Plots_and_graphics/shot_plots/D%d.png'%shot
#    else:
#        figname='../Plots_and_graphics/shot_plots/He%d.png'%shot
#    plt.savefig(figname,format='png',dpi=100)
    
#%% get power threshold data for L-H and H-L transition (and other data)
"""
LHdata=[{} for shot in shotnos]
HLdata=[{} for shot in shotnos]
thressigs=['Ploss','NE_','KAPPA','X1Z','X2Z','BT','IP','SAREA','AMIN','RGEO','Q95','LCFS_R_in','PRAD']

for i,shot in enumerate(shotnos):
    # seperate ante transitus (at) and post transitus (pt) ####################
    for sig in thressigs:
        # take values right before and right after transition
        t=0
        while data[i][sig]['time'][t] < tLH[i]:
            indLHat = t
            t+=1
        while data[i][sig]['time'][t] < tHL[i]:
            indHLat = t
            t+=1   
        sig_LHat=data[i][sig]['data'][indLHat]
        sig_LHpt=data[i][sig]['data'][indLHat+1]
        sig_HLat=data[i][sig]['data'][indHLat]
        sig_HLpt=data[i][sig]['data'][indHLat+1]
        
        try:
            sig_err_LHat=data[i][sig]['errors'][indLHat]
            sig_err_LHpt=data[i][sig]['errors'][indLHat+1]
            sig_err_HLat=data[i][sig]['errors'][indHLat]
            sig_err_HLpt=data[i][sig]['errors'][indHLat+1]
        except TypeError:
            sig_err_LHat=None
            sig_err_LHpt=None
            sig_err_HLat=None
            sig_err_HLpt=None

        LHdata[i][sig+'at']=dict(data=sig_LHat,errors=sig_err_LHat,units=data[i][sig]['units'],time=tLH[i])
        LHdata[i][sig+'pt']=dict(data=sig_LHpt,errors=sig_err_LHpt,units=data[i][sig]['units'],time=tLH[i])
        HLdata[i][sig+'at']=dict(data=sig_HLat,errors=sig_err_HLat,units=data[i][sig]['units'],time=tHL[i])    
        HLdata[i][sig+'pt']=dict(data=sig_HLpt,errors=sig_err_HLpt,units=data[i][sig]['units'],time=tHL[i])    

#%% estimating error of Pth due to choice of transition time

# get Ploss at lower and upper limits of transition times:
for i,shot in enumerate(shotnos):
    # take values right before transition
    # L-H transition
    if tLH_err[i][0]: 
        t=0 # time-index to find indices of transition times
        indLH_err = [0,0]
        while data[i]['Ploss']['time'][t] < tLH_err[i][0]:
            indLH_err[0] = t # lower limit of transition time
            t+=1
        while data[i]['Ploss']['time'][t] < tLH_err[i][1]:
            indLH_err[1] = t # upper limit of transition time
            t+=1   
        Pth_LH_err=( abs(data[i]['Ploss']['data'][indLH_err[0]]-LHdata[i]['Plossat']['data']) + abs(data[i]['Ploss']['data'][indLH_err[1]]-LHdata[i]['Plossat']['data']) )/2
        #print('%d: Pth_LH=%.1f M%s, error=%.1f M%s, rel. error=%.2f'%(shot,LHdata[i]['Plossat']['data']/1e6,LHdata[i]['Plossat']['units'],Pth_LH_err/1e6,LHdata[i]['Plossat']['units'],Pth_LH_err/LHdata[i]['Plossat']['data']))
        if LHdata[i]['Plossat']['errors']<Pth_LH_err: # replace error of Pth if new error is larger (which should always be the case)
            LHdata[i]['Plossat']['errors']=Pth_LH_err
    # H-L transition
    if tHL_err[i][0]:
        t=0 # time-index to find indices of transition times
        indHL_err = [0,0]
        while data[i]['Ploss']['time'][t] < tHL_err[i][0]:
            indHL_err[0] = t  # lower limit of transition time
            t+=1
        while data[i]['Ploss']['time'][t] < tHL_err[i][1]:
            indHL_err[1] = t # upper limit of transition time
            t+=1   
        Pth_HL_err=( abs(data[i]['Ploss']['data'][indHL_err[0]]-HLdata[i]['Plossat']['data']) + abs(data[i]['Ploss']['data'][indHL_err[1]]-HLdata[i]['Plossat']['data']) )/2
        #print('%d: Pth_HL=%.1f M%s, error=%.1f M%s, rel. error=%.2f'%(shot,HLdata[i]['Plossat']['data']/1e6,HLdata[i]['Plossat']['units'],Pth_HL_err/1e6,HLdata[i]['Plossat']['units'],Pth_HL_err/HLdata[i]['Plossat']['data']))
        if HLdata[i]['Plossat']['errors']<Pth_HL_err: # replace error of Pth if new error is larger (which should always be the case)
            HLdata[i]['Plossat']['errors']=Pth_HL_err

#%% SELEC2007: new selection criteria for ITER like plasmas only: 10 conditions: [Y R Martin et al 2008 J. Phys.: Conf. Ser. 123 012033]
#    single null - not applicable, standard configuration for MAST is CDND
#    ion grad B drift towards the X-point  - not applicable, standard configuration for MAST is CDND
#    D plasma - obviously not aplicable for He plasma
#    *no too low plasma density n>1e19 (use NE_)
#    *no too low q95 q95>2.5 (use Q95)
#    not too close to the beginning of heat pulse (??)
#    not too large counter-NBI (P_ctr/P_NB<0.8) (could use ANB_SS_FULL_POWER and ANB_SW_FULL_POWER but how do I know which one is counter?) 
#    *no too small gaps between plasma surface and wall (d>5cm) (closest to wall at HF side midplane, assume wall at R=0.19625m (see lcfs_test.py) and use data[i]['LCFS_R_in']['data'])
#    *no too high radiation losses (P_rad/P_L<0.5) (use PRAD)
#    no ohmic or ECRH heating only (new) (true for all shots)
#    *no different from SND and too low elongation (new) kappa>1.2 

# save a boolean value for each criterion for each shot
shot_criteria=[[LHdata[i]['NE_at']['data']>1e19, # ne
                LHdata[i]['Q95at']['data']>2.5, # q95
                LHdata[i]['LCFS_R_inat']['data']>0.05+0.19625,#m gap between plasma and wall -> only one that ever fails
                LHdata[i]['PRADat']['data']/LHdata[i]['Plossat']['data']<0.5, # radiation losses
                LHdata[i]['KAPPAat']['data']>1.2 # elongation
                ] for i in range(len(shotnos))]




# create list of shots with boolean whether or not they pass all criteria:
shot_pass=[all(shot_criteria[i]) for i in range(len(shotnos))]
# print out message about 
print('He/D study: \n{}% of shots pass SELEC2007* criteria'.format(round(sum(shot_pass)/len(shot_pass)*100)))
"""