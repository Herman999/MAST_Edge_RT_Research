# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 13:45:58 2019
@author: Tomas
"""

# ML model preparation

# dummpy preparation


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
inputs = torch.from_numpy(inputs.values).float()
targets = torch.from_numpy(targets.values).float()

#%%

train_ds = TensorDataset(inputs, targets) # careful about T
batch_size = 3
train_dl = DataLoader(train_ds, batch_size, shuffle=True)


model = nn.Linear(5, 1)



# Define optimizer
opt = torch.optim.SGD(model.parameters(), lr=1e-5)


# Define loss function
loss_fn = F.mse_loss

losstrack = []
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
    
fit(700, model, loss_fn, opt)
plt.figure()
plt.plot(losstrack)


#%%
# out of sample test



plt.figure()
#plt.scatter(range(len(test_targets)),test_targets,color='b',label='real data')
model_ret=[]
loss_test = []
for i,testin in enumerate(test_inputs.values):
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
    
#plt.scatter(range(len(test_targets)),np.array(model(torch.from_numpy(test_inputs.values).float())),color='r',label='predicted data')
plt.scatter(test_targets.values,model_ret)
plt.scatter(np.array(targets),predictions)

plt.xlabel('REAL')
plt.ylabel('PREDICTED')
plt.legend()