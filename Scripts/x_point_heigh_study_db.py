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
data = pd.read_excel('shot_db_REAL_Ploss_corr.xlsx')

# sellect desired configuration
#data = data[(data['geometry']=='SN')]
#data = data[(data['geometry']=='CND') ]#(data['geometry']=='maybe CND')]
#data = data[(data['geometry']=='maybe CND')]
data = data[(data['geometry']=='CND') | (data['geometry']=='maybe CND')]

# filter by session
#data = data[(data['session']=='IP_scan+IP on E_R')]


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


# PLOT LH

y_err = np.sqrt(list((data_LH['Ploss_e']/data_LH['Ploss'])**2 + (data_LH['AYC_NE_e']/data_LH['AYC_NE'])**2)) # perc error
y_err = y_err * data_LH['Ploss']/(data_LH['AYC_NE']**alpha) # * data
for xpt,ploss,ne,xpt_err,y_err,IP in zip(data_LH[X],data_LH['Ploss'],data_LH['AYC_NE'],data_LH[Xe],y_err,data_LH['IP']):
    if IP < 740:
        marker = 'x'
        col = 'darkred'
    elif IP < 780:
        marker='1'
        col='r'
    else:
        marker='s'
        col='khaki'
    plt.errorbar(xpt, ploss/ne**alpha,xerr=xpt_err,yerr=y_err, markersize=15, fmt='.', label='LH',color=col)
#plt.errorbar(x = data_LH[X], markersize=15, y = data_LH['Ploss']/(data_LH['AYC_NE']**alpha),xerr = data_LH[Xe], yerr = y_err ,fmt='x', label = 'LH',color = 'red')


#for i, txt in enumerate(data_LH['shot']):
#    plt.annotate(txt, (list(data_LH[X])[i], list(data_LH['Ploss']/(data_LH['AYC_NE']**alpha))[i]))



# PLOT HL   
# =============================================================================
# y_err = np.sqrt(list((data_HL['Ploss_e']/data_HL['Ploss'])**2 + (data_HL['AYC_NE_e']/data_HL['AYC_NE'])**2)) # perc error
# y_err = y_err * data_HL['Ploss']/(data_HL['AYC_NE']**alpha) # * data
# plt.errorbar(x = data_HL[X], markersize=15, y = data_HL['Ploss']/(data_HL['AYC_NE']**alpha),xerr = data_HL[Xe], yerr = y_err ,fmt='x', label = 'HL',color = 'blue')
# =============================================================================

#for i, txt in enumerate(data_HL['shot']):
#    plt.annotate(txt, (list(data_HL[X])[i], list(data_HL['Ploss']/(data_HL['AYC_NE']**alpha))[i]))

plt.ylim([0,2.6e-9])
plt.xlim([0.28,0.65])
#plt.legend()
plt.xlabel(r'X point height [m]' )
plt.ylabel(r'$P_{loss}/N_e^\alpha$ [Wm^3]')
plt.show()
