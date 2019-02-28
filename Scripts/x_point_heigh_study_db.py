# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 12:22:54 2019

@author: Tomas
"""


# X point height study using data from db
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

alpha = 0.8

#load from db
data = pd.read_excel('shot_database_ALL_SHOTS_NewX1X2.xlsx')

# sellect desired configuration
#data = data[(data['geometry']=='SN')]
#data = data[(data['geometry']=='CND') ]#(data['geometry']=='maybe CND')]
#data = data[(data['geometry']=='maybe CND')]
data = data[(data['geometry']=='CND') | (data['geometry']=='maybe CND')]

# filter by session
data = data[(data['session']=='IP_scan+IP on E_R')]


# filter corrupted X1Z or X
data = data[~(abs(data['X2Z_e'])>=1)]

# cut of Ploss = 0 
data = data[~(data['Ploss']==0)]

# drop unnecessary columns
data.drop(['time_em','time_ep','BT','BT_e','IP','IP_e','KAPPA','KAPPA_e','AYE_NE_e','AYE_NE','ANE_DENSITY','ANE_DENSITY_e','AYC_TE_e','AYE_TE','AYE_TE_e','AYC_PE', 'AYC_PE_e','AYE_PE','AYE_PE_e'],axis=1,inplace=True)

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

plt.figure(figsize=(13,9))
plt.title(r'NEW DATA ONLY {1} Point Height Study ($\alpha={0}$, CDN and DN)'.format(alpha,X))


# PLOT LH
y_err = np.sqrt(list((data_LH['Ploss_e']/data_LH['Ploss'])**2 + (data_LH['AYC_NE_e']/data_LH['AYC_NE'])**2)) # perc error
y_err = y_err * data_LH['Ploss']/(data_LH['AYC_NE']**alpha) # * data
plt.errorbar(x = data_LH[X], markersize=15, y = data_LH['Ploss']/(data_LH['AYC_NE']**alpha),xerr = data_LH[Xe], yerr = y_err ,fmt='x', label = 'LH',color = 'red')

#for i, txt in enumerate(data_LH['shot']):
#    plt.annotate(txt, (list(data_LH['X1Z'])[i], list(data_LH['Ploss']/(data_LH['NE']**alpha))[i]))



# PLOT HL   
y_err = np.sqrt(list((data_HL['Ploss_e']/data_HL['Ploss'])**2 + (data_HL['AYC_NE_e']/data_HL['AYC_NE'])**2)) # perc error
y_err = y_err * data_HL['Ploss']/(data_HL['AYC_NE']**alpha) # * data
plt.errorbar(x = data_HL[X], markersize=15, y = data_HL['Ploss']/(data_HL['AYC_NE']**alpha),xerr = data_HL[Xe], yerr = y_err ,fmt='x', label = 'HL',color = 'blue')

#for i, txt in enumerate(data_HL['shot']):
#    plt.annotate(txt, (list(data_HL['X1Z'])[i], list(data_HL['Ploss']/(data_HL['NE']**alpha))[i]))

plt.ylim([3e-10,2.2e-9])

plt.legend()
plt.xlabel(r'X point height [m]' )
plt.ylabel(r'$P_{loss}/N_e^\alpha$ [Wm^3]')
plt.show()
