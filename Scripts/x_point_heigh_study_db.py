# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 12:22:54 2019

@author: Tomas/Ronan

PLOT Pth v XPT seperated by IP

1. press play
"""


# X point height study using data from db
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

alpha = 0.8

#load from db
data = pd.read_excel('shot_db_REAL_Ploss_corr.xlsx')

# sellect desired configuration
#data = data[(data['geometry']=='SN')]
#data = data[(data['geometry']=='CND') ]#(data['geometry']=='maybe CND')]
#data = data[(data['geometry']=='maybe CND')]
data = data[(data['geometry']=='CDN') | (data['geometry']=='DN')]

# filter corrupted X1Z or X
data = data[~(abs(data['X2Z_e'])>=1)]
# cut of Ploss = 0 
data = data[~(data['Ploss']==0)]
# drop unnecessary columns
data.drop(['time_em','time_ep','BT','BT_e','KAPPA','KAPPA_e','AYE_NE_e','AYE_NE','ANE_DENSITY','ANE_DENSITY_e','AYC_TE_e','AYE_TE','AYE_TE_e','AYC_PE', 'AYC_PE_e','AYE_PE','AYE_PE_e'],axis=1,inplace=True)
# select diagnostic for NE --> I use AYC because cross-session compatible
AYC_NE = data[~(data['AYC_NE']=='')]
#NE = data[~(data['NE']=='')]
# copy AYC_NE into NE columns
#AYC_NE.loc[:,'NE'] = AYC_NE.loc[:,'AYC_NE']
#AYC_NE.loc[:,'NE_e'] = AYC_NE.loc[:,'AYC_NE_e'] 
# combine
combined = pd.concat([AYC_NE])#,NE])
#drop unnecessary columns
combined.drop(['AYC_TE','AYC_NE','AYC_NE_e'],axis=1)

# filter LH
data_LH = combined[combined['transition']=='LH']
data_HL = combined[combined['transition']=='HL']

#%%
# PLot 
X='X1Z'
Xe='X1Z_e'

plt.figure(figsize=(11.5,8))
plt.title(r'All data {1} Point Height Study ($\alpha={0}$)'.format(alpha,X))

x_high_i = []
y_high_i = []
x_low_i = []
y_low_i = []
zs=[]

# PLOT LH
y_err = np.sqrt(list((data_LH['Ploss_e']/data_LH['Ploss'])**2 + (data_LH['AYC_NE_e']/data_LH['AYC_NE'])**2)) # perc error
y_err = y_err * data_LH['Ploss']/(data_LH['AYC_NE']**alpha) # * data
for xpt,ploss,ne,xpt_err,y_err,IP,sesh,shot in zip(data_LH[X],data_LH['Ploss'],data_LH['AYC_NE'],data_LH[Xe],y_err,data_LH['IP'],data_LH['session'],data_LH['shot']):
    
    if IP < 755:
        marker = 'x'
        col = 'b' # lowest IP
        x_low_i.append(xpt)
        y_low_i.append(ploss/ne**alpha)
        
    elif IP < 775:
        marker='1'
        col='r' # average IP
        if ploss/ne**alpha >0:
            x_high_i.append(xpt)
            y_high_i.append(ploss/ne**alpha)
        
    else:
        marker='s'
        col='khaki' # highest IP
        
#    if '17FEB10-Hmodebetascan' in sesh:
#        col='g'
#        plt.annotate(shot, (xpt, ploss/ne**alpha))
        
    plt.annotate(shot,(xpt, ploss/ne**alpha))
    plt.errorbar(xpt, ploss/ne**alpha,xerr=xpt_err,yerr=y_err, markersize=15, fmt='.', label='LH',c=col)

# PLOT HL   
# =============================================================================
y_err = np.sqrt(list((data_HL['Ploss_e']/data_HL['Ploss'])**2 + (data_HL['AYC_NE_e']/data_HL['AYC_NE'])**2)) # perc error
y_err = y_err * data_HL['Ploss']/(data_HL['AYC_NE']**alpha) # * data
for xpt,ploss,ne,xpt_err,y_err,IP,sesh,shot in zip(data_HL[X],data_HL['Ploss'],data_HL['AYC_NE'],data_HL[Xe],y_err,data_HL['IP'],data_HL['session'],data_HL['shot']):
    if IP < 755:
        marker = 'x'
        col = 'b' # lowest IP
        x_low_i.append(xpt)
        y_low_i.append(ploss/ne**alpha)
    elif IP < 775:
        marker='1'
        col='r' # average IP
        if ploss/ne**alpha >0:
            x_high_i.append(xpt)
            y_high_i.append(ploss/ne**alpha)
    else:
        marker='s'
        col='khaki' # highest IP
    
    plt.annotate(shot,(xpt, ploss/ne**alpha))
    #plt.annotate(str(int(np.round(IP,-1))),(xpt, ploss/ne**alpha) )
    plt.errorbar(xpt, ploss/ne**alpha,xerr=xpt_err,yerr=y_err, markersize=15, fmt='.', label='LH',c=col)
# =============================================================================
plt.gray()
plt.ylim([0,2.6e-9])
plt.xlim([0.28,0.65])
#plt.legend()
plt.xlabel(r'X point height [m]' )
plt.ylabel(r'$P_{loss}/N_e^\alpha$ [Wm^3]')
plt.show()
#p = np.poly1d(np.polyfit(x_high_i,y_high_i,1))
#stx = np.arange(0.3,0.7,0.05)
#plt.plot(stx,p(stx), c='r')
#p = np.poly1d(np.polyfit(x_low_i,y_low_i,1))
#stx = np.arange(0.3,0.7,0.05)
#plt.plot(stx,p(stx), c='b')

#%%
# plot Dalpha with IP seperation
