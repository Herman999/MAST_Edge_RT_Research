# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 16:27:24 2019

@author: Tomas

THIS STUFF IS JP PLOT 
1. PRESS PLAY AND ENJOY!
"""



# X point height study using data from db
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

alpha = 0.77 

#load from db
data = pd.read_excel('shot_db_REAL_Ploss_corr.xlsx')


# filter corrupted X1Z or X
data = data[~(abs(data['X2Z_e'])>=1)]
# cut of Ploss = 0 
data = data[~(data['Ploss']==0)]


# FILTER SINGLE NULS
data = data[(data.geometry=='SN')]

# filter corrupted X1Z or X
data = data[~(abs(data['X1Z_e'])>=1)]

# cut of Ploss = 0 
#data = data[~(data['AYC_NE']=='')]


# drop unnecessary columns
data.drop(['time_em','time_ep','BT','BT_e','KAPPA','KAPPA_e','ANE_DENSITY','ANE_DENSITY_e','AYC_TE_e','AYE_TE','AYE_TE_e','AYC_PE', 'AYC_PE_e','AYE_PE','AYE_PE_e'],axis=1,inplace=True)

combined = data # legacy compatibility

# filter LH





#%%


# set X1
X='X1Z'
Xe='X1Z_e'

data_LH = combined[combined['transition']=='LH']
data_HL = combined[combined['transition']=='HL']

data_LH = data_LH[~(data_LH['Ploss']==0)]
data_LH = data_LH[~(data_LH['Ploss'].isnull())]
data_HL = data_HL[~(data_HL['Ploss']==0)]
data_HL = data_HL[~(data_HL['Ploss'].isnull())]

fig, ax = plt.subplots(3,sharex=True,figsize=(11.5,8))


textstr = r'$I_p=500-700$kA $B_t=-0.425$T'

ax[0].set_title(r'LH and HL transition characteristics on X1 height')

 
# PLOT LH
y_err = np.sqrt(list((data_LH['Ploss_e']/data_LH['Ploss'])**2 + (data_LH['AYC_NE_e']/data_LH['AYC_NE'])**2)) # perc error
y_err = y_err * data_LH['Ploss']/(data_LH['AYC_NE']**alpha) # * data
ax[0].errorbar(data_LH[X], data_LH['Ploss']/(data_LH['AYC_NE']**alpha),xerr=data_LH[Xe],yerr=y_err, markersize=15, fmt='.', label='LH',c='r')
#alpha = 0.55
y_err = np.sqrt(list((data_HL['Ploss_e']/data_HL['Ploss'])**2 + (data_HL['AYC_NE_e']/data_HL['AYC_NE'])**2)) # perc error
y_err = y_err * data_HL['Ploss']/(data_HL['AYC_NE']**alpha) # * data
ax[0].errorbar(data_HL[X], data_HL['Ploss']/(data_HL['AYC_NE']**alpha),xerr=data_HL[Xe],yerr=y_err, markersize=15, fmt='.', label='HL',c='b')

#ax[0].set_ylim([0,9.6e-9])
#ax[0].set_xlim([0.43,0.54])
ax[0].axvline(x=0.5,color='orange',linestyle='dashed')
ax[0].legend()
ax[2].set_xlabel(r'X point height [m]' )
ax[0].set_ylabel(r'$P_{loss}/N_e^\alpha$ [Wm^3]')

# Plot 2


data_LH = combined[combined['transition']=='LH']
data_HL = combined[combined['transition']=='HL']

data_LH = data_LH[~(data_LH['AYE_NE']==0)]
data_LH = data_LH[~(data_LH['AYE_NE']=='')]
data_LH = data_LH[~(data_LH['AYE_NE'].isnull())]
data_HL = data_HL[~(data_HL['AYE_NE']==0)]
data_HL = data_HL[~(data_HL['AYE_NE']=='')]
data_HL = data_HL[~(data_HL['AYE_NE'].isnull())]

ax[1].errorbar(data_LH[X], data_LH['AYE_NE'],xerr=data_LH[Xe],yerr=data_LH['AYE_NE_e'], markersize=15, fmt='.', label='LH',c='r')
ax[1].errorbar(data_HL[X], data_HL['AYE_NE'],xerr=data_HL[Xe],yerr=data_HL['AYE_NE_e'], markersize=15, fmt='.', label='HL',c='b')
ax[1].axvline(x=0.5,color='orange',linestyle='dashed')
ax[1].legend()
ax[1].set_ylabel(r'$ne_{ped}$ [$m^{-3}$]')

# plot 3
data_LH = combined[combined['transition']=='LH']
data_HL = combined[combined['transition']=='HL']

data_LH = data_LH[~(data_LH['AYC_NE']==0)]
data_LH = data_LH[~(data_LH['AYC_NE']=='')]
data_LH = data_LH[~(data_LH['AYC_NE'].isnull())]
data_HL = data_HL[~(data_HL['AYC_NE']==0)]
data_HL = data_HL[~(data_HL['AYC_NE']=='')]
data_HL = data_HL[~(data_HL['AYC_NE'].isnull())]


ax[2].errorbar(data_LH[X], data_LH['AYC_NE'],xerr=data_LH[Xe],yerr=data_LH['AYC_NE_e'], markersize=15, fmt='.', label='LH',c='r')
ax[2].errorbar(data_HL[X], data_HL['AYC_NE'],xerr=data_HL[Xe],yerr=data_HL['AYC_NE_e'], markersize=15, fmt='.', label='HL',c='b')
ax[2].axvline(x=0.5,color='orange',linestyle='dashed')
ax[2].legend()
ax[2].set_ylabel(r'$\overline{ne}$ [$m^{-3}$]')









