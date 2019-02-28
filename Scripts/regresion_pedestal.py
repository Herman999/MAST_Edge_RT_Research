# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 11:11:28 2019

@author: Tomas
"""

# Regression EDGE PEDESTAL PARAMS


# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 13:45:58 2019
@author: Tomas
"""

# ML Data from data file 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


dd = pd.read_excel('ML_data_new.xlsx')
#dd is all original data

#ddnum is the test data to be used.
ddnum = dd.copy()
ddnum = ddnum.sample(frac=1)
ddnum.drop(labels=[ 'session', 'geometry','shot_time',  'time_em', 'time',
                   'time_ep', 'Ploss_e', 'BT_e', 'BT', 'BTOut_e', 
                   'IP_e', 'KAPPA_e', 'AYC_NE_e',  'AYC_TE_e', 'AYC_TE', 'SAREA_e',
                   'AYC_PE', 'AYC_PE_e', 'X1Z_e',  'X2Z_e',
                   'AYE_NE', 'AYE_NE_e', 'ANE_DENSITY',
                   'ANE_DENSITY_e', 'AYE_TE', 'AYE_TE_e', 'AYE_PE', 'AYE_PE_e',
                   
                   ],axis=1, inplace=True)
# now ddnum.columns = 'Ploss', 'BT', 'IP', 'AYC_NE' only
ddnum.dropna(inplace=True)
ddnum = ddnum[~(ddnum['AYC_NE']=='')] # delete rows with no density data
#ddnum = ddnum[(ddnum['X1Z']<=2)] # take only meaningful X1Z data

ddnum['AYC_NE'] =ddnum['AYC_NE']/1e20 
ddnum['Ploss'] = ddnum['Ploss']/0.0488 *np.e**+0.057

peddf = pd.read_excel('shot_peddb_only_good_shots.xlsx')

cols = list(peddf.columns)
cols.extend(['IP','X1Z','X2Z','BT','SAREA','KAPPA','Ploss','e']) # here puts things that we want from main df
combined = pd.DataFrame(columns=cols)
combined.columns

for i in range(len(peddf)):
    shot = peddf.iloc[i]['shot']
    transition = peddf.iloc[i]['transition']
    if shot in [24330,27036,27037,27035,27448]: continue
    ip = ddnum[(ddnum['shot']==shot)&(ddnum['transition']==transition)]['IP'].values
    x1z = ddnum[(ddnum['shot']==shot)&(ddnum['transition']==transition)]['X1Z'].values
    x2z = ddnum[(ddnum['shot']==shot)&(ddnum['transition']==transition)]['X2Z'].values
    bt = ddnum[(ddnum['shot']==shot)&(ddnum['transition']==transition)]['BTOut'].values
    sarea = ddnum[(ddnum['shot']==shot)&(ddnum['transition']==transition)]['SAREA'].values
    kappa = ddnum[(ddnum['shot']==shot)&(ddnum['transition']==transition)]['KAPPA'].values
    ploss = ddnum[(ddnum['shot']==shot)&(ddnum['transition']==transition)]['Ploss'].values
    try:
        if len(ip)==2:
            ip=ip[0]
            x1z=x1z[0]
            x2z=x2z[0]
            bt=bt[0]
            sarea=sarea[0]
            kappa=kappa[0]
            ploss=ploss[0]
    except: pass
    
    
    values = [shot,transition]
    values.extend(list(np.float64(peddf.iloc[i, peddf.columns != 'transition']))[1:] )# .iloc[2].values),dtype=float32)
    values.extend([float(ip),float(x1z),float(x2z),float(bt),float(sarea),float(kappa),float(ploss)])
    values.extend([np.e])
    combined.loc[i]=values




combined.drop(labels=['shot', 'transition', 'ne_average_e', 
                      'ne_at_ped_e', 'te_at_ped_e', 'pe_at_ped_e',
                      'X2Z', 'BT','IP', 'SAREA', 'KAPPA'
                   ],axis=1, inplace=True)
    
print(combined.columns)



#inputs = ddnum.iloc[0:-20].copy()
inputs = combined.copy()



inputs.drop(labels=['Ploss'],axis=1,inplace=True)
print(inputs.columns)
cols = inputs.columns
targets=combined['Ploss']  #ddnum.iloc[0:-20]['Ploss']

#logging
targets = np.log(targets)
inputs = np.abs(np.array(inputs.values,dtype=np.float32) )
inputs = np.log(inputs)


#taking Z value normalisation
#inputs = (inputs-inputs.mean())/inputs.std()
#targets = (targets-targets.mean())/targets.std()


#for testing
test_inputs = combined.iloc[-20:].copy()
test_inputs.drop(labels=['Ploss'],axis=1,inplace=True)
test_targets = combined.iloc[-20:]['Ploss']

#logging
test_inputs = np.abs( np.array(test_inputs.values,dtype=np.float32) )
test_inputs = np.log(test_inputs)
test_targets = np.log(test_targets)

# z norm
#test_inputs = (test_inputs-test_inputs.mean())/test_inputs.std()
#test_targets = (test_targets-test_targets.mean())/test_targets.std()



#%%


import torch 
from torch.utils.data import TensorDataset, DataLoader
import torch.nn.functional as F
import torch.nn as nn
import numpy as np
from torch.autograd import Variable

#%%
#inputs = np.array([np.linspace(0,100,10),np.linspace(0,10,10)]).T
#targets = inputs[:,0] + inputs[:,1]

# transform to tensors
#inputs = torch.from_numpy(inputs.values).float()
#targets = torch.from_numpy(targets.values).float()

inputs = torch.from_numpy(inputs).float()
targets = torch.from_numpy(targets.values).float()

#%%
# Define a utility function to train the model
def fit(num_epochs, model, loss_fn, opt):
    for epoch in range(num_epochs):
        for xb,yb in train_dl:
            # Generate predictions
            pred = model(xb)
            #print(pred.T)
            #print(yb)
            loss = loss_fn(pred.squeeze(), yb)
            # Perform gradient descent
            loss.backward()
            opt.step()
            opt.zero_grad()
        print('Training epoch {} loss: '.format(epoch), loss_fn(model(inputs).squeeze(), targets))
        losstrack.append(loss_fn(model(inputs).squeeze(), targets))

df = pd.DataFrame(columns = ['num_epochs','loss_out_sample','loss_last','loss_average','columns','weights'])
range_num_epochs = [50,100,300,500,1000,2000,5000]

for num_epochs in range_num_epochs:

    train_ds = TensorDataset(inputs, targets) # careful about T
    batch_size = 2
    train_dl = DataLoader(train_ds, batch_size, shuffle=True)
    
    
    model = nn.Linear(6, 1)
    
    # Define optimizer
    opt = torch.optim.SGD(model.parameters(), lr=1e-5)
    
    
    # Define loss function
    loss_fn = F.mse_loss
    
    losstrack = []
    
        
    fit(num_epochs, model, loss_fn, opt)
    #plt.figure()
    #plt.plot(losstrack)
    #plt.title('learning rate')
    
    # out of sample test
    
    
    
    #plt.figure()
    #plt.scatter(range(len(test_targets)),test_targets,color='b',label='real data')
    model_ret=[]
    loss_test = []
    for i,testin in enumerate(test_inputs): # .values
        model_ret.append(model(torch.from_numpy(testin).float()).detach().numpy())
        
        loss_test.append(loss_fn(
                model(torch.from_numpy(testin).float()).squeeze(), torch.tensor(np.array(test_targets)[i])
                ))
    print('Sum of out of sample loss: ', sum(loss_test))
    print(cols)
    print(model.weight)
    
    predictions = []
    
    for i in range(len(inputs)):
        predictions.append(model(inputs[i]).detach().numpy())
        
    
    #plt.scatter(test_targets.values,model_ret,label='blind test')
    #plt.scatter(np.array(targets),predictions,label='fitting data')
    #plt.plot(np.arange(0,20),np.arange(0,20),label='Ideal fit')
    
    #plt.xlabel('REAL')
    #plt.ylabel('PREDICTED')
    #plt.legend()
        
        
    df.loc[len(df)]=[num_epochs, sum(loss_test),losstrack[-1],
           np.mean([float(losstrack[x].detach().numpy()) for x in range(len(losstrack))]),
           str(list(cols)),str(model.weight)]

#%%
#saving
writer = pd.ExcelWriter('PED_ML_e.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()    
    
    
    
    
    
    
    