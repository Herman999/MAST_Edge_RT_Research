# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 12:50:18 2019

@author: Tomas
"""

# SCALINING PLOTS



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 14})
# ITER SCALING

# TAKIZUKA
# A = aspect ratio
# F =  A/(1- np.sqrt(2( 1 + A )))
# Pth = 0.072 * Btout**0.7  * ne20 **0.7 * S **0.9 * F**0.5

A = 1.307
F = A/ (1 - np.sqrt(2/ ( 1 + A )))

alpha=0.8


#data = db
data = pd.read_excel('shot_db_REAL_Ploss_corr.xlsx')

# FILTER SINGLE NULS
data = data[~(data.geometry=='SN')]

# filter corrupted X1Z or X
data = data[~(abs(data['X2Z_e'])>=1)]

# cut of Ploss = 0 
data = data[~(data['Ploss']==0)]
data = data[~(data['Ploss'].isnull())]
data['Ploss'] = data['Ploss'] /1e6
data['Ploss_e'] = data['Ploss_e'] /1e6
data = data[~(data['AYC_NE']=='')]

data.drop(['time_em','time_ep','BT','BT_e','IP','IP_e','KAPPA','KAPPA_e','AYE_NE_e','AYE_NE','ANE_DENSITY','ANE_DENSITY_e','AYC_TE_e','AYE_TE','AYE_TE_e','AYC_PE', 'AYC_PE_e','AYE_PE','AYE_PE_e'],axis=1,inplace=True)
AYC_NE = data #data[~(data['AYC_NE']=='')]
combined = pd.concat([AYC_NE])#,NE])
combined.drop(['AYC_TE','AYC_NE','AYC_NE_e'],axis=1)


combined['TAKIZUKY'] = 0.072 * abs(data.BTOut)**0.7 * (data.AYC_NE/1e20 )**0.7 * data.SAREA**0.9 * F**0.5


data_LH = combined[combined['transition']=='LH']
data_HL = combined[combined['transition']=='HL']



plt.figure(figsize=(13,9))
plt.title(r'MAST Pth comparison with Takizuky scaling')

# PLOT LH
x_err = np.sqrt(list(
        (data_LH['SAREA_e']/data_LH['SAREA'])**2 + (data_LH['AYC_NE_e']/data_LH['AYC_NE'])**2
        )) # perc error
x_err = x_err * data_LH['TAKIZUKY'] 

plt.errorbar(x = data_LH['TAKIZUKY'], markersize=15, y = data_LH['Ploss'],xerr = x_err, yerr = data_LH['Ploss_e'],fmt='x', label = 'LH',color = 'red')


#for i, txt in enumerate(data_LH['shot']):
#    plt.annotate(txt, (list(data_LH['X1Z'])[i], list(data_LH['Ploss']/(data_LH['NE']**alpha))[i]))

# PLOT HL   
x_err = np.sqrt(list(
        (data_HL['SAREA_e']/data_HL['SAREA'])**2 + (data_HL['AYC_NE_e']/data_HL['AYC_NE'])**2
        )) # perc error
x_err = x_err * data_HL['TAKIZUKY'] 

plt.errorbar(x = data_HL['TAKIZUKY'], markersize=15, y = data_HL['Ploss'],xerr = x_err, yerr = data_HL['Ploss_e'],fmt='x', label = 'HL',color = 'blue')


#for i, txt in enumerate(data_HL['shot']):
#    plt.annotate(txt, (list(data_HL['X1Z'])[i], list(data_HL['Ploss']/(data_HL['NE']**alpha))[i]))

#plt.ylim([3e-10,2.2e-9])
plt.plot(np.arange(0.4,80),np.arange(0.4,80))
plt.scatter(80,80,label='ITER')
plt.yscale('log')
plt.xscale('log')
plt.legend()
plt.xlabel(r'TAKIZUKY [MW]' )
plt.ylabel(r'MAST Pth [MW]')
plt.show()

