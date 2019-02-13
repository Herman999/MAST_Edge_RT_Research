# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 13:49:42 2019

@author: rbatt

Data prep/process
"""
import pandas as pd
import numpy as np

dd = pd.read_excel('ML_data.xlsx')
#dd is all original data

#ddnum is the test data to be used.
ddnum = dd.copy()
ddnum.drop(labels=['shot', 'session', 'geometry','shot_time', 'time', 'time_em', 
                   'time_ep', 'transition','Ploss_e', 'BT_e', 'BTOut', 'BTOut_e', 
                   'IP_e', 'KAPPA', 'KAPPA_e', 'AYC_NE_e', 'AYC_TE', 'AYC_TE_e', 
                   'AYC_PE', 'AYC_PE_e', 'X1Z', 'X1Z_e', 'X2Z', 'X2Z_e'],axis=1, inplace=True)
# now ddnum.columns = 'Ploss', 'BT', 'IP', 'AYC_NE' only

# scaling may be useful here

x = ddnum.drop(labels=['Ploss'],axis=1)
y = ddnum['Ploss']