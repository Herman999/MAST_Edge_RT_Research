# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 12:22:54 2019

@author: Tomas/Ronan

PLOT Pth v XPT seperated by IP

1. press play

'OLD METHOD' SPLITS BY CURRENT
"""


# X point height study using data from db
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

alpha = 0.77 

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


# FILTER SINGLE NULS
data = data[~(data.geometry=='SN')]

# filter corrupted X1Z or X
data = data[~(abs(data['X1Z_e'])>=1)]

# cut of Ploss = 0 
#data = data[~(data['Ploss']==0)]
#data = data[~(data['Ploss'].isnull())]
data = data[~(data['AYC_NE']=='')]


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

# OLD APPROACH
"""
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
    
    if IP < 750:
        marker = 'x'
        col = 'b' # lowest IP
        x_low_i.append(xpt)
        y_low_i.append(ploss/ne**alpha)
        
    elif IP < 770:
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
    if IP < 750:
        marker = 'x'
        col = 'b' # lowest IP
        x_low_i.append(xpt)
        y_low_i.append(ploss/ne**alpha)
    elif IP < 770:
        marker='1'
        col='r' # average IP
        if ploss/ne**alpha >0:
            x_high_i.append(xpt)
            y_high_i.append(ploss/ne**alpha)
    else:
        marker='s'
        col='khaki' # highest IP
    
    #plt.annotate(shot,(xpt, ploss/ne**alpha))
    plt.annotate(str(int(np.round(IP,-1))),(xpt, ploss/ne**alpha) )
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
"""
#%%

#  4 PLOT SEPARATION IP D Alpha plot Dalpha with IP seperation

# LH together

# set X1
X='X1Z'
Xe='X1Z_e'

# below 750
# filter LH
data_LH = combined[(combined['transition']=='LH')&(combined['IP']<750)]
data_HL = combined[(combined['transition']=='HL')&(combined['IP']<750)]

data_LH = data_LH[~(data_LH['Ploss']==0)]
data_LH = data_LH[~(data_LH['Ploss'].isnull())]
data_HL = data_HL[~(data_HL['Ploss']==0)]
data_HL = data_HL[~(data_HL['Ploss'].isnull())]

#plt.figure(figsize=(11.5,8))
plt.figure(figsize=(11.5,7.2))
plt.rcParams.update({'font.size': 14})
alpha=0.77
plt.title(r'$P_{th}$ dependance on $Z^{lower}_{x-pt}$ $n_e^{0.77}$ norm.')
 

textstr = r'$670<I_p<750$kA'
plt.text(0.4513, 9.05e-9, textstr, fontsize=14)   
textstr=r'$-0.375<B_t<-0.425$T'
plt.text(0.446, 8.5e-9, textstr, fontsize=14)   
 
# PLOT LH
y_err = np.sqrt(list((data_LH['Ploss_e']/data_LH['Ploss'])**2 + (data_LH['AYC_NE_e']/data_LH['AYC_NE'])**2)) # perc error
y_err = y_err * data_LH['Ploss']/(data_LH['AYC_NE']**alpha) # * data
plt.errorbar(data_LH[X], data_LH['Ploss']/(data_LH['AYC_NE']**alpha),xerr=data_LH[Xe],yerr=y_err, markersize=15, fmt='.', label='LH',c='r')
#alpha = 0.55
y_err = np.sqrt(list((data_HL['Ploss_e']/data_HL['Ploss'])**2 + (data_HL['AYC_NE_e']/data_HL['AYC_NE'])**2)) # perc error
y_err = y_err * data_HL['Ploss']/(data_HL['AYC_NE']**alpha) # * data
plt.errorbar(data_HL[X], data_HL['Ploss']/(data_HL['AYC_NE']**alpha),xerr=data_HL[Xe],yerr=y_err, markersize=15, fmt='.', label='HL',c='b')

plt.ylim([0,9.6e-9])
plt.xlim([0.43,0.54])
plt.axvline(x=0.5,color='orange',linestyle='dashed')
plt.legend(loc=2)
plt.xlabel(r'$Z^{lower}_{x-pt}$ [m]')
plt.ylabel(r'$P_{th}/N_e^{0.77}$ [$\times 10^{-8}$ Wm$^3$]')

plt.show()

#%%
# Plot 2

# below 750
# filter LH
data_LH = combined[(combined['transition']=='LH')&(combined['IP']<770)&(combined['IP']>750)]
data_HL = combined[(combined['transition']=='HL')&(combined['IP']<770)&(combined['IP']>750)]

data_LH = data_LH[~(data_LH['Ploss']==0)]
data_LH = data_LH[~(data_LH['Ploss'].isnull())]
data_HL = data_HL[~(data_HL['Ploss']==0)]
data_HL = data_HL[~(data_HL['Ploss'].isnull())]

#plt.figure(figsize=(11.5,8))
plt.figure(figsize=(11.5,7.2))
plt.rcParams.update({'font.size': 14})
plt.title(r'$P_{th}$ dependance on $Z^{lower}_{x-pt}$ $n_e^{0.77}$ norm')#.format(str(alpha),X,770))



textstr = r'$750<I_p<770$kA'
plt.text(0.4513, 9.05e-9, textstr, fontsize=14)   
textstr=r'$-0.375<B_t<-0.425$T'
plt.text(0.446, 8.5e-9, textstr, fontsize=14)   
 
 
# PLOT LH
#alpha = 0.77
y_err = np.sqrt(list((data_LH['Ploss_e']/data_LH['Ploss'])**2 + (data_LH['AYC_NE_e']/data_LH['AYC_NE'])**2)) # perc error
y_err = y_err * data_LH['Ploss']/(data_LH['AYC_NE']**alpha) # * data
plt.errorbar(data_LH[X], data_LH['Ploss']/(data_LH['AYC_NE']**alpha),xerr=data_LH[Xe],yerr=y_err, markersize=15, fmt='.', label='LH',c='r')
#alpha = 0.55
y_err = np.sqrt(list((data_HL['Ploss_e']/data_HL['Ploss'])**2 + (data_HL['AYC_NE_e']/data_HL['AYC_NE'])**2)) # perc error
y_err = y_err * data_HL['Ploss']/(data_HL['AYC_NE']**alpha) # * data
plt.errorbar(data_HL[X], data_HL['Ploss']/(data_HL['AYC_NE']**alpha),xerr=data_HL[Xe],yerr=y_err, markersize=15, fmt='.', label='HL',c='b')

#plt.ylim([0,9.4e-9])
plt.ylim([0,9.6e-9])
plt.xlim([0.43,0.54])
plt.axvline(x=0.5,color='orange',linestyle='dashed')
plt.legend(loc=2)
plt.xlabel(r'$Z^{lower}_{x-pt}$ [m]')
#plt.xscale('log')
#plt.yscale('log')
plt.ylabel(r'$P_{th}/N_e^{0.77}$ [$\times 10^{-8}$ Wm$^3$]')

plt.show()

#%%
"""
# L and H separated
# below 750
# filter LH
data_LH = combined[(combined['transition']=='LH')&(combined['IP']<750)]
data_HL = combined[(combined['transition']=='HL')&(combined['IP']<750)]

data_LH = data_LH[~(data_LH['Ploss']==0)]
data_LH = data_LH[~(data_LH['Ploss'].isnull())]
data_HL = data_HL[~(data_HL['Ploss']==0)]
data_HL = data_HL[~(data_HL['Ploss'].isnull())]

plt.figure(figsize=(11.5,8))

alpha=0.77
plt.title(r'L\to H Pth dependance on {1} ($\alpha={0}$) IP Separation <{2}'.format(alpha,X,750))

 
# PLOT LH
y_err = np.sqrt(list((data_LH['Ploss_e']/data_LH['Ploss'])**2 + (data_LH['AYC_NE_e']/data_LH['AYC_NE'])**2)) # perc error
y_err = y_err * data_LH['Ploss']/(data_LH['AYC_NE']**alpha) # * data
plt.errorbar(data_LH[X], data_LH['Ploss']/(data_LH['AYC_NE']**alpha),xerr=data_LH[Xe],yerr=y_err, markersize=15, fmt='.', label='LH',c='r')
plt.ylim([0,9.6e-9])
plt.xlim([0.43,0.54])
plt.axvline(x=0.5,color='orange',linestyle='dashed')
plt.legend()
#plt.yscale('log')
plt.xlabel(r'X point height [m]' )
plt.ylabel(r'$P_{loss}/N_e^\alpha$ [Wm^3]')

plt.show()
data_LH = combined[(combined['transition']=='LH')&(combined['IP']<750)]
data_HL = combined[(combined['transition']=='HL')&(combined['IP']<750)]

data_LH = data_LH[~(data_LH['Ploss']==0)]
data_LH = data_LH[~(data_LH['Ploss'].isnull())]
data_HL = data_HL[~(data_HL['Ploss']==0)]
data_HL = data_HL[~(data_HL['Ploss'].isnull())]

plt.figure(figsize=(11.5,8))
alpha = 0.55
plt.title(r'H\to L Pth dependance on {1} ($\alpha={0}$) IP Separation <{2}'.format(alpha,X,750))

 


y_err = np.sqrt(list((data_HL['Ploss_e']/data_HL['Ploss'])**2 + (data_HL['AYC_NE_e']/data_HL['AYC_NE'])**2)) # perc error
y_err = y_err * data_HL['Ploss']/(data_HL['AYC_NE']**alpha) # * data
plt.errorbar(data_HL[X], data_HL['Ploss']/(data_HL['AYC_NE']**alpha),xerr=data_HL[Xe],yerr=y_err, markersize=15, fmt='.', label='HL',c='b')

plt.ylim([0,9.6e-9])
plt.xlim([0.43,0.54])
plt.axvline(x=0.5,color='orange',linestyle='dashed')
plt.legend()
plt.xlabel(r'X point height [m]' )
plt.ylabel(r'$P_{loss}/N_e^\alpha$ [Wm^3]')
#plt.yscale('log')
plt.show()

# Plot 2

# below 750
# filter LH
data_LH = combined[(combined['transition']=='LH')&(combined['IP']<770)&(combined['IP']>750)]
data_HL = combined[(combined['transition']=='HL')&(combined['IP']<770)&(combined['IP']>750)]

data_LH = data_LH[~(data_LH['Ploss']==0)]
data_LH = data_LH[~(data_LH['Ploss'].isnull())]
data_HL = data_HL[~(data_HL['Ploss']==0)]
data_HL = data_HL[~(data_HL['Ploss'].isnull())]

plt.figure(figsize=(11.5,8))
alpha = 0.77
plt.title(r'L\to H Pth dependance on {1} ($\alpha={0}$) Separation 750<IP{2}'.format(alpha,X,770))

 
# PLOT LH

y_err = np.sqrt(list((data_LH['Ploss_e']/data_LH['Ploss'])**2 + (data_LH['AYC_NE_e']/data_LH['AYC_NE'])**2)) # perc error
y_err = y_err * data_LH['Ploss']/(data_LH['AYC_NE']**alpha) # * data
plt.errorbar(data_LH[X], data_LH['Ploss']/(data_LH['AYC_NE']**alpha),xerr=data_LH[Xe],yerr=y_err, markersize=15, fmt='.', label='LH',c='r')
plt.axvline(x=0.5,color='orange',linestyle='dashed')
plt.xlim([0.43,0.54])
plt.legend()
plt.xlabel(r'X point height [m]' )
#plt.xscale('log')
#plt.yscale('log')
plt.ylabel(r'$P_{loss}/N_e^\alpha$ [Wm^3]')

plt.show()


data_LH = combined[(combined['transition']=='LH')&(combined['IP']<770)&(combined['IP']>750)]
data_HL = combined[(combined['transition']=='HL')&(combined['IP']<770)&(combined['IP']>750)]

data_LH = data_LH[~(data_LH['Ploss']==0)]
data_LH = data_LH[~(data_LH['Ploss'].isnull())]
data_HL = data_HL[~(data_HL['Ploss']==0)]
data_HL = data_HL[~(data_HL['Ploss'].isnull())]

plt.figure(figsize=(11.5,8))

alpha = 0.55
plt.title(r'H\to L Pth dependance on {1} ($\alpha={0}$) Separation 750<IP{2}'.format(alpha,X,770))

y_err = np.sqrt(list((data_HL['Ploss_e']/data_HL['Ploss'])**2 + (data_HL['AYC_NE_e']/data_HL['AYC_NE'])**2)) # perc error
y_err = y_err * data_HL['Ploss']/(data_HL['AYC_NE']**alpha) # * data
plt.errorbar(data_HL[X], data_HL['Ploss']/(data_HL['AYC_NE']**alpha),xerr=data_HL[Xe],yerr=y_err, markersize=15, fmt='.', label='HL',c='b')

#plt.ylim([0,9.4e-9])
plt.xlim([0.43,0.54])
plt.axvline(x=0.5,color='orange',linestyle='dashed')
plt.legend()
plt.xlabel(r'X point height [m]' )
#plt.xscale('log')
#plt.yscale('log')
plt.ylabel(r'$P_{loss}/N_e^\alpha$ [Wm^3]')

plt.show()



"""
#%%
# PLot 3 D alpha

# filter LH
data_LH = combined[(combined['transition']=='LH')&(combined['IP']<750)]
data_HL = combined[(combined['transition']=='HL')&(combined['IP']<750)]

# filter 
data_LH = data_LH[~(data_LH.AIM_DA_TO=='')]
data_HL = data_HL[~(data_HL.AIM_DA_TO=='')]
data_LH = data_LH[data_LH.AIM_DA_TO>=0]
data_HL = data_HL[data_HL.AIM_DA_TO>=0]

#plt.figure(figsize=(11.5,8))
plt.figure(figsize=(11.5,7.2))
plt.rcParams.update({'font.size': 14})
plt.title(r'$D_{\alpha}$ dependance on $Z^{lower}_{x-pt}$')

 
textstr = r'$670<I_p<750$kA'
plt.text(0.451, 1.7e19, textstr, fontsize=14)   
textstr=r'$-0.375<B_t<-0.425$T'
plt.text(0.446, 1.6e19, textstr, fontsize=14)   

plt.text(0.43, 1.845e19, 'Testtest', color='white', 
        bbox=dict(facecolor='white', edgecolor='white'))


# PLOT LH
plt.errorbar(data_LH[X], data_LH['AIM_DA_TO'],xerr=data_LH[Xe],yerr=data_LH['AIM_DA_TO_e'], markersize=15, fmt='.', label='LH',c='r')
plt.errorbar(data_HL[X], data_HL['AIM_DA_TO'],xerr=data_HL[Xe],yerr=data_HL['AIM_DA_TO_e'], markersize=15, fmt='.', label='HL',c='b')


plt.xlabel(r'$Z^{lower}_{x-pt}$ [m]')
plt.ylabel(r'$D_{\alpha}$ $ [x10^{19} \ p^h/sr. m^{2}. s]$')
plt.xlim([0.43,0.54])
plt.ylim([0,1.8e19])
plt.axvline(x=0.5,color='orange',linestyle='dashed')
plt.legend(loc=2)


# Plot 4 D alpha


# filter LH
data_LH = combined[(combined['transition']=='LH')&(combined['IP']<770)&(combined['IP']>750)]
data_HL = combined[(combined['transition']=='HL')&(combined['IP']<770)&(combined['IP']>750)]

# filter 
data_LH = data_LH[~(data_LH.AIM_DA_TO=='')]
data_HL = data_HL[~(data_HL.AIM_DA_TO=='')]
data_LH = data_LH[data_LH.AIM_DA_TO>=0]
data_HL = data_HL[data_HL.AIM_DA_TO>=0]

#plt.figure(figsize=(11.5,8))
plt.figure(figsize=(11.5,7.2))
plt.rcParams.update({'font.size': 14})
plt.title(r'$D_{\alpha}$ dependance on $Z^{lower}_{x-pt}$')

textstr = r'$750<I_p<770$kA'
plt.text(0.451, 1.7e19, textstr, fontsize=14)   
textstr=r'$-0.375<B_t<-0.425$T'
plt.text(0.446, 1.6e19, textstr, fontsize=14)   

# test box here
plt.text(0.43, 1.845e19, 'Testtest', color='white', 
        bbox=dict(facecolor='white', edgecolor='white'))

# PLOT LH
plt.errorbar(data_LH[X], data_LH['AIM_DA_TO'],xerr=data_LH[Xe],yerr=data_LH['AIM_DA_TO_e'], markersize=15, fmt='.', label='LH',c='r')
plt.errorbar(data_HL[X], data_HL['AIM_DA_TO'],xerr=data_HL[Xe],yerr=data_HL['AIM_DA_TO_e'], markersize=15, fmt='.', label='HL',c='b')


plt.xlabel(r'$Z^{lower}_{x-pt}$ [m]')
plt.ylabel(r'$D_{\alpha}$ $ [x10^{19} \ p^h/sr. m^{2}. s]$')
plt.xlim([0.43,0.54])
plt.ylim([0,1.8e19])
plt.axvline(x=0.5,color='orange',linestyle='dashed')
plt.legend(loc=2)