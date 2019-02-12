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
ddnum = ddnum.sample(frac=1)
ddnum.drop(labels=['shot', 'session', 'geometry','shot_time',  'time_em', 'time',
                   'time_ep', 'transition','Ploss_e', 'BT_e', 'BT', 'BTOut_e', 
                   'IP_e', 'KAPPA', 'KAPPA_e', 'AYC_NE_e',  'AYC_TE_e', 
                   'AYC_PE', 'AYC_PE_e', 'X1Z_e', 'X2Z', 'X2Z_e'],axis=1, inplace=True)
# now ddnum.columns = 'Ploss', 'BT', 'IP', 'AYC_NE' only

inputs = ddnum.iloc[0:-20].copy()
inputs.drop(labels=['Ploss'],axis=1,inplace=True)
print(inputs.columns)
targets=ddnum.iloc[0:-20]['Ploss']

#logging
#targets = np.log(targets)
#inputs = np.abs(inputs)
#inputs = np.log(inputs)


#taking Z value normalisation
inputs = (inputs-inputs.mean())/inputs.std()
targets = (targets-targets.mean())/targets.std()


#for testing
test_inputs = ddnum.iloc[-20:].copy()
test_inputs.drop(labels=['Ploss'],axis=1,inplace=True)
#test_inputs = np.abs(test_inputs)
#test_inputs = np.log(test_inputs)

test_targets = ddnum.iloc[-20:]['Ploss']
#test_targets = np.log(test_targets)

# z norm
test_inputs = (test_inputs-test_inputs.mean())/test_inputs.std()
test_targets = (test_targets-test_targets.mean())/test_targets.std()