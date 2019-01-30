# -*- coding: utf-8 -*-
"""
Created on Mo Aug 06 2018

@author: jb4317, Jan-Peter Baehner

Programme to analyse shots of X-point height variation studies.
Shots loaded (including H-mode phases):
         13042, 13043, 13044, 13045, 13046, 13047,                     26MAY05 (6)
         13704, 13705, 13706, 13707, 13708, 13709, 13710, 13711,       10AUG05 (8)
         14545, 14546, 14547, 14548, 14552, 14554, 14555,              08NOV05 (7)
         (23822, 23824, 23825, 23826, 23827, 23832, 
         23835, 23837, 23841, 23842, 23843, 23844                      09DEC09 (12))
Shots from 09DEC09 have separate Core TS and Edge TS data - had to be combined in special programme.
All other shots are missing the R2_CTS signal, i.e. the time resolved radial positions - use static R_CTS instead.
"""

import matplotlib.pyplot as plt
import math
import numpy as np
from data_access_funcs import load_signal_data,signals

# X-point hight variation sessions
shotnos=[13042, 13043, 13044, 13045, 13046, 13047,                              #26MAY05 (6)
         13704, 13705, 13706, 13707, 13708, 13709, 13710, 13711,                #10AUG05 (8)
         14545, 14546, 14547, 14548, 14552, 14554, 14555]#,                       #08NOV05 (7)
         #23822, 23824, 23825, 23826, 23827, 23832, 23835, 23837, 23841, 23842, 23843, 23844] #09DEC09 (12)

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

#%% load data and write to 'data' for special case of 09DEC09
# =============================================================================
# Originally combine edge TS and core TS data to one data set
# But resolution of core TS is good enough and core and edge TS data don't agree
# at the edge -> only take core TS data
# =============================================================================
#DEC09shots=[23822, 23824, 23825, 23826, 23827, 23832, 23835, 23837, 23841, 23842, 23843, 23844]
#DEC09signals=dict(
#            #electron density and temperatures from Thomson scattering:
#            # core TS
#            NE_CTS='AYC_NE', #electron density from core Thomson
#            TE_CTS='AYC_TE', #electron temperature from core TS
#            T0_CTS='AYC_TE_CORE', #Peak electron temperature (t)
#            PE_CTS='AYC_PE', #electron pressure from core TS
#            R_CTS='AYC_R', #major radius for core TS measurement
#            # edge TS
#            NE_ETS='AYE_NE', #electron density from edge Thomson
#            TE_ETS='AYE_TE', #electron temperature from edge TS
#            PE_ETS='AYE_PE', #electron pressure from edge TS
#            R_ETS='AYE_R', #major radius for edge TS measurement
#            # ruby TS - already loaded above
#            )
#dataDEC09=[{} for shot in DEC09shots]
#i0=len(shotnos)-len(DEC09shots)
#
#for i,shot in enumerate(DEC09shots):
#    for sig in DEC09signals:
#        filename=str(shot)+'_'+sig+'.p'
#        dataDEC09[i][sig]=load_signal_data(filename) #set data of sig to key sig
#    #combined density
#    NEi_data=dataDEC09[i]['NE_CTS']['data']#np.append(dataDEC09[i]['NE_CTS']['data'],dataDEC09[i]['NE_ETS']['data'],axis=1)#
#    NEi_errors=dataDEC09[i]['NE_CTS']['errors']#np.append(dataDEC09[i]['NE_CTS']['errors'],dataDEC09[i]['NE_ETS']['errors'],axis=1)#
#    data[i0+i]['NE']=dict(data=NEi_data,errors=NEi_errors,time=dataDEC09[i]['NE_CTS']['time'],units=dataDEC09[i]['NE_CTS']['units']) #set data of sig to key sig
#    #combined temperature
#    TEi_data=dataDEC09[i]['TE_CTS']['data']#np.append(dataDEC09[i]['TE_CTS']['data'],dataDEC09[i]['TE_ETS']['data'],axis=1)#
#    TEi_errors=dataDEC09[i]['TE_CTS']['errors']#np.append(dataDEC09[i]['TE_CTS']['errors'],dataDEC09[i]['TE_ETS']['errors'],axis=1)#
#    data[i0+i]['TE']=dict(data=TEi_data,errors=TEi_errors,time=dataDEC09[i]['TE_CTS']['time'],units=dataDEC09[i]['TE_CTS']['units']) #set data of sig to key sig
#    #core temp just from CTS
#    data[i0+i]['TE0']=dataDEC09[i]['T0_CTS']
#    #combined pressure
#    PEi_data=dataDEC09[i]['PE_CTS']['data']#np.append(dataDEC09[i]['PE_CTS']['data'],dataDEC09[i]['PE_ETS']['data'],axis=1)#
#    PEi_errors=dataDEC09[i]['PE_CTS']['errors']#np.append(dataDEC09[i]['PE_CTS']['errors'],dataDEC09[i]['PE_ETS']['errors'],axis=1)#
#    data[i0+i]['PE']=dict(data=PEi_data,errors=PEi_errors,time=dataDEC09[i]['PE_CTS']['time'],units=dataDEC09[i]['PE_CTS']['units']) #set data of sig to key sig
#    #combined radius
#    Ri_data=dataDEC09[i]['R_CTS']['data']#np.append(dataDEC09[i]['R_CTS']['data'],dataDEC09[i]['R_ETS']['data'],axis=1)#
#    Ri_errors=dataDEC09[i]['R_CTS']['errors']#np.append(dataDEC09[i]['R_CTS']['errors'],dataDEC09[i]['R_ETS']['errors'],axis=1)#
#    data[i0+i]['R_CTS']=dict(data=Ri_data,errors=Ri_errors,time=dataDEC09[i]['R_CTS']['time'],units=dataDEC09[i]['R_CTS']['units']) #set data of sig to key sig

# watch out here! turns out R_CTS as pulled for 09NOV09 is time resoved, using only the first timeslice
# as it is done when saving it as R_CTS to data, could result in wrong radii for data-points
#%% average density (from core TS) over profile for each timeslot to get line averaged:
# in this average the points are weighted by their radial distance to neighbouring points
ne_=[[] for shot in shotnos] #empty list for average
ne_err=[[] for shot in shotnos] #empty list for average
for i in range(len(shotnos)):
    for j in range(len(data[i]['NE']['data'])): # loop through time slots
        nej=list(data[i]['NE']['data'][j]) # density profile for time j
        nej_err=list(data[i]['NE']['errors'][j]) # error of density profile for time j
        # only R_CTS is availabe for these shots (see comment in file description)
        Rj=list(data[i]['R_CTS']['data'][0]) # radii for time j
        Rj_err=list(data[i]['R_CTS']['errors'][0]) # error of radii for time j
        nan_indices=[]
        for n in range(len(nej)): # find 'nan' values
            if math.isnan(nej[n]):
                nan_indices.append(n)
        for k in range(len(nan_indices)): # delet 'nan' entries and corresponding positions in R
            del nej[nan_indices[k]-k]
            del nej_err[nan_indices[k]-k]
            del Rj[nan_indices[k]-k]
            
        if len(nej)<3: # for the case that nej is too short or empty because too many values were 'nan'
            nej=[0,0,0]
            nej_err=[0,0,0]
            Rj=[data[i]['R_CTS']['data'][j][0],data[i]['R_CTS']['data'][j][round(len(data[i]['R_CTS']['data'][j])/2)],data[i]['R_CTS']['data'][j][-1]]
        
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
    ne_[i]=np.array(ne_[i])
    ne_err[i]=np.array(ne_err[i])
    nei_dict=dict(data=ne_[i],errors=ne_err[i],time=data[i]['NE']['time'],units=data[i]['NE']['units'])
    data[i]['NE_']=nei_dict


#%% plot important signals of shots 
#t0=0.2 # common lower plot limit
# time limits for each shot:
tlims=[[0.1,0.45],[0.1,0.346],[0.1,0.4],[0.1,0.397],[0.1,0.359],[0.1,0.388],     #26MAY05
       [0.1,0.3945],[0.1,0.3591],[0.1,0.3791],[0.1,0.3544],[0.1,0.3937],[0.1,0.3958],[0.1,0.3186],[0.1,0.3213], #10AUG05
       [0.2,0.435],[0.2,0.42],[0.2,0.345],[0.2,0.38],[0.2,0.4],[0.2,0.4],[0.2,0.35]]#, #08NOV08
#       [0.25,0.37],[0.1,0.385],[0.25,0.35],[0.25,0.37],[0.15,0.36],[0.27,0.36],[0.15,0.35],[0.27,0.36],[0.27,0.35],[0.15,0.35],[0.15,0.3],[0.27,0.345]] #09DEC09
# time of L-H transition for each shot:
tLH=[0.1524,0.1524,0.1516,0.1513,0.1511,0.1509,                #26MAY05
     0.3367,0.1123,0.1126,0.1115,0.1115,0.1114,0.1114,0.1903,      #10AUG05
     0.2718,0.3125,0.2824,0.2921,0.3083,0.3016,0.2915]#,            #08NOV08
#     0.2727,0.1704,0.25967,0.2672,0.2038,0.2953,0.1969,0.3197,0.2964,0.1955,0.1962,0.2982]       #09DEC09
tLH_err=[[0.1501,0.1537],[0.1506,0.1555],[0.1487,0.1541],[0.1497,0.1529],[0.1487,0.1533],[0.1467,0.1522], #26MAY05
         [None,None],[0.1113,0.1142],[0.1107,0.1138],[0.1107,0.1132],[0.1096,0.1124],[0.1101,0.1126],[0.1106,0.1127],[0.1896,0.1917], #10AUG05
         [0.2699,0.27295],[0.3125,0.3126],[0.2824,0.2835],[0.2664,0.2921],[None,None],[None,None],[0.2900,0.2923]] #08NOV08

# time of H-L transition for each shot:
tHL=[0.3937,0.3264,0.3460,0.3633,0.3292,0.38365,               #26MAY05
     0.3863,0.3553,0.3761,0.3529,0.3831,0.3940,0.2941,0.2946,  #10AUG05 
     0.4247,0.4172,0.3431,0.3591,0.3263,0.31175,0.3060]#,        #08NOV08
#     0.3652,0.1948,0.3452,0.3508,0.2480,0.3450,0.2107,0.3277,0.3397,0.2252,0.2288,0.3412]       #09DEC09
tHL_err=[[None,None],[None,None],[None,None],[None,None],[None,None],[0.38365,0.3854], #26MAY05
         [0.3863,0.3868],[None,None],[None,None],[None,None],[0.3831,0.3896],[None,None],[None,None],[None,None], #10AUG05
         [None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[0.3056,0.3073]] #08NOV08

#plotsigs=['IP','NE_','WMHD','TE0','Dalphstrp','ngrad','KAPPA','X1Z','Ploss','PINJ','POHM']#,'X2Z'
#plotsiglabels=['$I_p$ [',r'$\bar{n}_e$ [$10^{19}$','$W_{MHD}$ [k','Core $T_e$ [k',r'$D_{\alpha}$ at strike point',r'edge $\nabla n_e$ [$10^{21}$',r'elongation $\kappa$',r'|$Z_{X-point}^{lower}$| [','$P_{loss}$ [M','$P_{NBI}$ [','$P_{ohmic}$ [M']#,r'$Z_{X-point}^{upper}$ ['
#norm=[1,1e19,1e3,1e3,1e18,1e21,1,-1,1e6,1,1e6]#,1
#
#for i,shot in enumerate(shotnos):
#    fig,ax=plt.subplots(len(plotsigs)-2,sharex=True,figsize=(11, 7))
#    fig.subplots_adjust(top=0.935,bottom=0.09,left=0.08,right=0.975,hspace=0.0,wspace=0.2)
#    fig.suptitle('X-point variation experiment shot #%d' %shot)
#    for j,sig in enumerate(plotsigs):
#        if j < len(plotsigs) - 2:
#            k=j
#            # mark L-H and H-L transition:
#            ax[k].axvline(tLH[i], c='g', lw=1, ls='--', clip_on=False)
#            if tLH_err[i][0]:
#                ax[k].axvline(tLH_err[i][0], c='g', lw=1, ls=':', clip_on=False)
#                ax[k].axvline(tLH_err[i][1], c='g', lw=1, ls=':', clip_on=False)
#            ax[k].axvline(tHL[i], c='r', lw=1, ls='--', clip_on=False)
#            if tHL_err[i][0]:
#                ax[k].axvline(tHL_err[i][0], c='r', lw=1, ls=':', clip_on=False)
#                ax[k].axvline(tHL_err[i][1], c='r', lw=1, ls=':', clip_on=False)
#            ax[k].plot(data[i][sig]['time'], data[i][sig]['data']/norm[j])   
#            # mark Ruby TS time
#            ax[k].axvline(data[i]['NE12_R']['time'][0], c='0.4', lw=1, ls='--', clip_on=False)
#            # plot error as shadow around data-line:
#            try:
#                ax[k].fill_between(data[i][sig]['time'], (data[i][sig]['data']-data[i][sig]['errors'])/norm[j], (data[i][sig]['data']+data[i][sig]['errors'])/norm[j],alpha=0.3)
#            except TypeError:
#                pass
#        else:
#            k=len(plotsigs) - 3 #plot last 3 signals in the same subplot
#         
#        # set limits of plot range and label data
#        ind = (data[i][sig]['time'] > tlims[i][0]) &  (data[i][sig]['time'] < tlims[i][1])  # find indices of plotted range
#        if sig == 'Dalphstrp':
#            ax[k].set(xlim=tlims[i],ylim=[0,np.nanmax(data[i][sig]['data'][ind])/norm[j]])
#            ax[k].annotate(plotsiglabels[j], xy=(0.01,0.7),xycoords='axes fraction',fontsize=11)
#            # label L-H and H-L transition
#            trans = ax[k].get_xaxis_transform()
#            ax[k].annotate('L-H', xy=(tLH[i]+0.002,0.75), xycoords=trans, fontsize=11,color='g')
#            ax[k].annotate('H-L', xy=(tHL[i]-0.008,0.75), xycoords=trans, fontsize=11,color='r')
#            # label Ruby TS time
#            ax[k].annotate('Ruby TS', xy=(data[i]['NE12_R']['time'][0]+0.001,0.5), xycoords=trans, fontsize=9,color='0.4')
#        elif sig== 'KAPPA':
#            ax[k].set(xlim=tlims[i],ylim=[np.nanmin(data[i][sig]['data'][ind])/norm[j], np.nanmax(data[i][sig]['data'][ind])/norm[j]])
#            ax[k].annotate(plotsiglabels[j], xy=(0.01,0.7),xycoords='axes fraction',fontsize=11)
#        # handling of X-point height plotted in the same subplot:
#        elif sig== 'X1Z':
#            # mark L-H and H-L transition:
#            ax[k].axvline(tLH[i], c='g', lw=1, ls='--', clip_on=False)
#            if tLH_err[i][0]:
#                ax[k].axvline(tLH_err[i][0], c='g', lw=1, ls=':', clip_on=False)
#                ax[k].axvline(tLH_err[i][1], c='g', lw=1, ls=':', clip_on=False)
#            ax[k].axvline(tHL[i], c='r', lw=1, ls='--', clip_on=False)
#            if tHL_err[i][0]:
#                ax[k].axvline(tHL_err[i][0], c='r', lw=1, ls=':', clip_on=False)
#                ax[k].axvline(tHL_err[i][1], c='r', lw=1, ls=':', clip_on=False)
#            # mark Ruby TS time
#            ax[k].axvline(data[i]['NE12_R']['time'][0], c='0.4', lw=1, ls='--', clip_on=False)
#            
#            ax[k].annotate(plotsiglabels[j]+'%s]'%data[i][sig]['units'], xy=(0.01,0.7),xycoords='axes fraction',fontsize=11)#,color='b' 
#            ax[k].set(xlim=tlims[i],ylim=[1, 1.5])
##            #ax[k].plot(data[i][sig]['time'], abs(data[i][sig]['data']/norm[j]))#,color='b'
#            # plot error as shadow around data-line:
#            try:
#                ax[k].fill_between(data[i][sig]['time'], (data[i][sig]['data']-data[i][sig]['errors'])/norm[j], (data[i][sig]['data']+data[i][sig]['errors'])/norm[j],alpha=0.3,color='c')
#            except TypeError:
#                pass
##        elif sig== 'X2Z':
##            ax[k].annotate(plotsiglabels[j]+'%s]'%data[i][sig]['units'],color='y' , xy=(0.01,0.3),xycoords='axes fraction',fontsize=11)
##            ax[k].plot(data[i][sig]['time'], data[i][sig]['data']/norm[j],color='y')
##            ax[k].set(xlim=tlims[i],ylim=[0.5, 1.75])
##            # plot error as shadow around data-line:
##            try:
##                ax[k].fill_between(data[i][sig]['time'], (data[i][sig]['data']-data[i][sig]['errors'])/norm[j], (data[i][sig]['data']+data[i][sig]['errors'])/norm[j],alpha=0.3,color='c')
##            except TypeError:
##                pass
#        # handling of power signals plotted in the same subplot:
#        elif sig== 'Ploss':
#            # mark L-H and H-L transition:
#            ax[k].axvline(tLH[i], c='g', lw=1, ls='--', clip_on=False)
#            if tLH_err[i][0]:
#                ax[k].axvline(tLH_err[i][0], c='g', lw=1, ls=':', clip_on=False)
#                ax[k].axvline(tLH_err[i][1], c='g', lw=1, ls=':', clip_on=False)
#            ax[k].axvline(tHL[i], c='r', lw=1, ls='--', clip_on=False)
#            if tHL_err[i][0]:
#                ax[k].axvline(tHL_err[i][0], c='r', lw=1, ls=':', clip_on=False)
#                ax[k].axvline(tHL_err[i][1], c='r', lw=1, ls=':', clip_on=False)
#            # mark Ruby TS time
#            ax[k].axvline(data[i]['NE12_R']['time'][0], c='0.4', lw=1, ls='--', clip_on=False)
#            
#            ax[k].annotate(plotsiglabels[j]+'%s]'%data[i][sig]['units'],color='c' , xy=(0.01,0.1),xycoords='axes fraction',fontsize=11)
#            ax[k].plot(data[i][sig]['time'], data[i][sig]['data']/norm[j],color='c')
#            yminloss=np.nanmin(data[i][sig]['data'][ind])/norm[j]
#            ymaxloss=np.nanmax(data[i][sig]['data'][ind])/norm[j]
#            # plot error as shadow around data-line:
#            try:
#                ax[k].fill_between(data[i][sig]['time'], (data[i][sig]['data']-data[i][sig]['errors'])/norm[j], (data[i][sig]['data']+data[i][sig]['errors'])/norm[j],alpha=0.3,color='c')
#            except TypeError:
#                pass
#        elif sig== 'PINJ':
#            ax[k].annotate(plotsiglabels[j]+'%s]'%data[i][sig]['units'],color='m' , xy=(0.01,0.4),xycoords='axes fraction',fontsize=11)
#            ax[k].plot(data[i][sig]['time'], data[i][sig]['data']/norm[j],color='m')
#            ymininj=np.nanmin(data[i][sig]['data'][ind])/norm[j]
#            ymaxinj=np.nanmax(data[i][sig]['data'][ind])/norm[j]
#            # plot error as shadow around data-line:
#            try:
#                ax[k].fill_between(data[i][sig]['time'], (data[i][sig]['data']-data[i][sig]['errors'])/norm[j], (data[i][sig]['data']+data[i][sig]['errors'])/norm[j],alpha=0.3,color='m')
#            except TypeError:
#                pass
#        elif sig== 'POHM':
#            ax[k].annotate(plotsiglabels[j]+'%s]'%data[i][sig]['units'],color='g', xy=(0.01,0.7),xycoords='axes fraction',fontsize=11)
#            ax[k].plot(data[i][sig]['time'], data[i][sig]['data']/norm[j],color='g')
#            ymin=min(yminloss,ymininj,np.nanmin(data[i][sig]['data'][ind])/norm[j])
#            ymax=max(ymaxloss,ymaxinj,np.nanmax(data[i][sig]['data'][ind])/norm[j])
#            ax[k].set(xlim=tlims[i],ylim=[ymin, ymax])
#            # plot error as shadow around data-line:
#            try:
#                ax[k].fill_between(data[i][sig]['time'], (data[i][sig]['data']-data[i][sig]['errors'])/norm[j], (data[i][sig]['data']+data[i][sig]['errors'])/norm[j],alpha=0.3,color='g')
#            except TypeError:
#                pass
#        else:
#            ax[k].set(xlim=tlims[i],ylim=[np.nanmin(data[i][sig]['data'][ind])/norm[j], np.nanmax(data[i][sig]['data'][ind])/norm[j]])
#            ax[k].annotate(plotsiglabels[j]+'%s]'%data[i][sig]['units'], xy=(0.01,0.7),xycoords='axes fraction',fontsize=11)
#    ax[-1].set_xlabel('time [s]')
#    #save figure:
##    figname='../Plots_and_graphics/shot_plots/X%d.png'%shot
##    plt.savefig(figname,format='png',dpi=100)
    
#%% get power threshold data for L-H and H-L transition and other signals

LHdata=[{} for shot in shotnos]
HLdata=[{} for shot in shotnos]
thressigs=['Ploss','NE_','KAPPA','X1Z','X2Z','BT','IP','SAREA','AMIN','RGEO','Q95','LCFS_R_in','PRAD']

for i,shot in enumerate(shotnos):
    # seperate ante transitus (at) and post transitus (pt) ####################
    for sig in thressigs:
        # take values right before and right after transition
        t=0
        # L-H transition
        while data[i][sig]['time'][t] < tLH[i]:
            indLHat = t
            t+=1
        sig_LHat=data[i][sig]['data'][indLHat] # signal data before transition
        sig_LHpt=data[i][sig]['data'][indLHat+1] # signal data after transition
        try:
            sig_err_LHat=data[i][sig]['errors'][indLHat] # signal error before transition
            sig_err_LHpt=data[i][sig]['errors'][indLHat+1] # signal error after transition
        except TypeError:
            sig_err_LHat=None
            sig_err_LHpt=None
        LHdata[i][sig+'at']=dict(data=sig_LHat,errors=sig_err_LHat,units=data[i][sig]['units'],time=tLH[i])
        LHdata[i][sig+'pt']=dict(data=sig_LHpt,errors=sig_err_LHpt,units=data[i][sig]['units'],time=tLH[i])
        
        # H-L transition
        try:
            while data[i][sig]['time'][t] < tHL[i]:
                indHLat = t
                t+=1
            sig_HLat=data[i][sig]['data'][indHLat] # signal data before transition
            sig_HLpt=data[i][sig]['data'][indHLat+1] # signal data after transition
            try:
                sig_err_HLat=data[i][sig]['errors'][indHLat] # signal error before transition
                sig_err_HLpt=data[i][sig]['errors'][indHLat+1] # signal error after transition
            except TypeError:
                sig_err_HLat=None
                sig_err_HLpt=None
            HLdata[i][sig+'at']=dict(data=sig_HLat,errors=sig_err_HLat,units=data[i][sig]['units'],time=tHL[i])    
            HLdata[i][sig+'pt']=dict(data=sig_HLpt,errors=sig_err_HLpt,units=data[i][sig]['units'],time=tHL[i])    

        except IndexError: # when H-L transition is too late and there is no data anymore at that point
            # set data and errors to 'None' value
            HLdata[i][sig+'at']=dict(data=None,errors=None,units=data[i][sig]['units'],time=tHL[i])    
            HLdata[i][sig+'pt']=dict(data=None,errors=None,units=data[i][sig]['units'],time=tHL[i])    

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
                LHdata[i]['LCFS_R_inat']['data']>0.05+0.19625,#m gap between plasma and wall
                LHdata[i]['PRADat']['data']/LHdata[i]['Plossat']['data']<0.5, # radiation losses
                LHdata[i]['KAPPAat']['data']>1.2 # elongation
                ] for i in range(len(shotnos))]

# create list of shots with boolean whether or not they pass all criteria:
shot_pass=[all(shot_criteria[i]) for i in range(len(shotnos))]
# print out message about 
print('X-point variation: \n{}% of shots pass SELEC2007* criteria'.format(round(sum(shot_pass)/len(shot_pass)*100)))