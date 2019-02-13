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

#inputs = np.array([np.linspace(0,100,10),np.linspace(0,10,10)]).T
#targets = inputs[:,0] + inputs[:,1]

# transform to tensors
inputs = torch.from_numpy(x.values).float()
#inputs = inputs.double()
targets = torch.from_numpy(y.values).float()
#targets = targets.double()

train_ds = TensorDataset(inputs, targets) # careful about T
batch_size = 1
train_dl = DataLoader(train_ds, batch_size, shuffle=True)


model = nn.Linear(3, 1)

inputs, targets = Variable(inputs), Variable(targets)

# Define optimizer
opt = torch.optim.SGD(model.parameters(), lr=1e-15)


# Define loss function
loss_fn = F.mse_loss
#loss_fn = torch.nn.NLLLoss(size_average=False)


pred = model(inputs[0])
loss = loss_fn(pred, targets[0])
loss.backward()
opt.step()
opt.zero_grad()

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
    print('Training loss: ', loss_fn(model(inputs).squeeze(), targets))
    
fit(10, model, loss_fn, opt)
