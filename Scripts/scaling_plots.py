# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 12:50:18 2019

@author: Tomas
"""

# SCALINING PLOTS



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ITER SCALING

# TAKIZUKA
# A = aspect ratio

# Pth = 0.072 * Btout**0.7  * ne20 **0.7 * S **0.9 * 

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
data = data[~(data['AYC_NE']=='')]

# drop unnecessary columns
data.drop(['time_em','time_ep','BT','BT_e','IP','IP_e','KAPPA','KAPPA_e','AYE_NE_e','AYE_NE','ANE_DENSITY','ANE_DENSITY_e','AYC_TE_e','AYE_TE','AYE_TE_e','AYC_PE', 'AYC_PE_e','AYE_PE','AYE_PE_e'],axis=1,inplace=True)
# select diagnostic for NE --> I use AYC because cross-session compatible
AYC_NE = data #data[~(data['AYC_NE']=='')]
# combine
combined = pd.concat([AYC_NE])#,NE])
#drop unnecessary columns
combined.drop(['AYC_TE','AYC_NE','AYC_NE_e'],axis=1)
# filter LH
data_LH = combined[combined['transition']=='LH']
data_HL = combined[combined['transition']=='HL']