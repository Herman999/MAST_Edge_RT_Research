# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 19:12:09 2018

@author: rbatt

Experiements using YP's code
Based on Yan-Peter Baehner's MSc project code
"""
#import pickle
import matplotlib.pyplot as plt
import numpy as np
from data_access_funcs import load_signal_data, signals
from plotter import plot_data, plot_residuals

#shotnos = [20841, 20480, 14546]
shotnos = [#24425,24426,24428,24430,24431, # 10FEB10 infulence of IP, mix of ELMy modes
	       27765,27766,27767,27769,27771,27772,27773,27774,27775, #07dec11 Density dependance l/h power
	       27776,27778,27781,27784,27786,27787,27788,27789 #08dec11 l-h threshold density scaling 
          ]
data = [{} for shot in shotnos]

# data is a list of shots
# each shot contains a dictionary, signal names are the keys
# keyvalues are a dictionary of data, errors, time and units

notloaded = [] # list of signals that could not be loaded because file !exist

#%% load data into 'data'
for i,shot in enumerate(shotnos): #(1,2,3... i,j,k...)
    for sig in signals:
        try:
            filename = str(shot) + '_' + sig + '.p'
            data[i][sig] = load_signal_data(filename)
        except FileNotFoundError:
            notloaded.append(sig + '_' + str(shot))
        
if not notloaded: # if notloaded is empty
    print('All signals loaded.')
else: # some signals not loaded
    print('Signals not loaded: ', *notloaded)

#%%
    
class Shot():
    def __init__(self, ShotNumber):
#       must define signals dictionary here based on shot number/session series
        self.data = {} # initialise data dictionary
        self.ShotNumber = ShotNumber
        for sig in signals:
            try:
                fn = str(ShotNumber) + '_' + sig + '.p'
                self.data[sig] = load_signal_data(fn)
            except FileNotFoundError:
                pass
    
    def signals_present(self):
        return self.data.keys()
    
    def print_signal(self, SignalName):
        # this should go into another file anyway with plotting stuff
        x,y = self.data[SignalName]['time'], self.data[SignalName]['data']
        try:
            plt.plot(x,y)
        except:
            print('Can\'t deal with this signal yet')
    
#%%
    
    
shotnos2 = shotnos[-5:]
data2 = data[-5:]

#%%
# test print of simple (no profile) variables 
# eg IP, VOL, Dalphint, Q95, NE0

for i,shot in enumerate(shotnos2):
    for thing in ['IP', 'Dalphint','Q95']:
        x,y = data2[i][thing]['time'], data2[i][thing]['data'] # y is 34 values across cord for NE etc
        yer = data2[i][thing]['errors']
        units = data2[i][thing]['units']
#        print(len(x),len(y),len(xer))
        plt.figure(thing)
        plt.errorbar(x,y, yerr=yer, label=str(shot))
#        plot_data(x, y,  xLabel = '$t$', dataname=thing, linestyle='-' )
#        plot_data(x, np.nanmean(y,axis=1), xLabel = '$t$', dataname=thing, linestyle='-' )
plt.legend()
        
        
#%%
# plotting NE profiles and change in radii position
# this for early shots only, ie R2_CTS doesn't exist after 2008

dd = data[0]
import math
N=len(dd['NE']['data'])
#N=2

for i in range(0,N):# range(len(dd['NE']['data'])):
    profile = list(dd['NE']['data'][i])
    profile_err = list(dd['NE']['errors'][i])
    radii = list(dd['R2_CTS']['data'][i])
    radii_err = list(dd['R2_CTS']['errors'][i])
    nan_inds = []
    for n in range(len(profile)): #check for nans
        if math.isnan(profile[n]):
            nan_inds.append(n)
    
    if nan_inds:
          for j in nan_inds[::-1]: #delete nan entries
              #print(profile[j], profile_err[j], radii[j], radii_err[j])
         
              del profile[j]
              del profile_err[j]
              del radii[j]
              del radii_err[j]
    ne_t = 0
    ne_t_err = 0
    plt.figure(1)
    #plt.plot(radii)
    plt.errorbar(range(len(radii)),radii, yerr=radii_err, color= str(1-0.9*i/N))
    plt.figure(2)
    plt.plot(radii,profile, label=np.round(dd['NE']['time'][i],3), color = str(1-0.9*i/N))
    

plt.figure(1)
plt.xlabel('data point')
plt.ylabel('radius')

plt.figure(2)
plt.xlabel('radius')
plt.ylabel('NE')
    
#%%
# calculate _NE (some avg):

NE_ = []



#%%
# reasonable first plots of new data
# missing D alpha strike point data


plotsigs=['IP','WMHD','TE0','Dalphstrp','ngrad','BT','Ploss','PINJ','POHM']#,'Vloop'
plotsiglabels=['$I_p$ [',r'$\bar{n}_e$ [$10^{19}$','$W_{MHD}$ [k','Core $T_e$ [k',r'$D_{\alpha}$ at strike point',r'edge $\nabla n_e$ [$10^{21}$','|$B_{T}$| [','$P_{loss}$ [M','$P_{NBI}$ [','$P_{ohmic}$ [M']#,'$V_{loop}$ ['
norm=[1,1e19,1e3,1e3,1e18,1e21,-1,1e6,1,1e6]#,1

plotsigs=  ['IP', 'AYC_NE0', 'BT', 'POHM', 'Ploss','AYC_NE']
norm = [1e3, 1e19,1,1e6, 1e6, 1e19]

for i,shot in enumerate(shotnos2):
    fig,ax = plt.subplots(len(plotsigs),sharex=True,figsize=(11, 7))
    fig.subplots_adjust(top=0.935,bottom=0.09,left=0.08,right=0.975,hspace=0.0,wspace=0.2)

    fig.suptitle('Experiment shot #%d' %shot)

    for j,sig in enumerate(plotsigs):
        if sig == 'AYC_NE':
            avgs = np.nanmean(data2[i]['AYC_NE']['data'], axis=1)
            errs = np.nanmean(data2[i]['AYC_NE']['errors'], axis=1)
            ax[j].errorbar(data2[i][sig]['time'], avgs/norm[j], yerr = errs/norm[j])
        else:
            ax[j].plot(data2[i][sig]['time'], data2[i][sig]['data']/norm[j])
        ax[j].set_ylabel(sig+'/'+data2[i][sig]['units'])
        ax[j].set_xlim(0,)
    
    plt.xlim(0,0.5)
    
    
    
    #%%
    
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
#            
#            ax[k].plot(data[i][sig]['time'], data[i][sig]['data'])
            # mark Ruby TS time
#            ax[k].axvline(data[i]['NE12_R']['time'][0], c='0.4', lw=1, ls='--', clip_on=False)
            # plot error as shadow around data-line:
#            try:
#                ax[k].fill_between(data[i][sig]['time'], (data[i][sig]['data']-data[i][sig]['errors'])/norm[j], (data[i][sig]['data']+data[i][sig]['errors'])/norm[j],alpha=0.3)
#            except TypeError:
#                pass
#        else:
#            k=len(plotsigs) - 3 #plot last 3 signals in the same subplot
         
#        # set limits of plot range and label data
#        ind = (data[i][sig]['time'] > tlims[i][0]) &  (data[i][sig]['time'] < tlims[i][1])  # find indices of plotted range
#        if sig == 'Dalphstrp':
#            ax[k].set(xlim=tlims[i],ylim=[0,np.nanmax(data[i][sig]['data'][ind])/norm[j]])#/2
#            ax[k].annotate(plotsiglabels[j], xy=(0.01,0.7),xycoords='axes fraction',fontsize=11)
#            # label L-H and H-L transition
#            trans = ax[k].get_xaxis_transform()
#            ax[k].annotate('L-H', xy=(tLH[i]+0.001,0.75), xycoords=trans, fontsize=11,color='g')
#            ax[k].annotate('H-L', xy=(tHL[i]-0.006,0.75), xycoords=trans, fontsize=11,color='r')
#            # label Ruby TS time
#            ax[k].annotate('Ruby TS', xy=(data[i]['NE12_R']['time'][0]+0.001,0.5), xycoords=trans, fontsize=9,color='0.4')
#        # handling of power signals plotted in the same subplot:
#        if sig== 'Ploss':
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
    #save figure:
#    if i<8:
#        figname='../Plots_and_graphics/shot_plots/D%d.png'%shot
#    else:
#        figname='../Plots_and_graphics/shot_plots/He%d.png'%shot
#    plt.savefig(figname,format='png',dpi=100)