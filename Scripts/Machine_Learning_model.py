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

inputs = np.array([np.linspace(0,100,10),np.linspace(0,10,10)]).T
targets = inputs[:,0] + inputs[:,1]

# transform to tensors
inputs = torch.from_numpy(inputs).float()
targets = torch.from_numpy(targets).float()


train_ds = TensorDataset(inputs, targets) # careful about T
batch_size = 5
train_dl = DataLoader(train_ds, batch_size, shuffle=True)


model = nn.Linear(2, 1)



# Define optimizer
opt = torch.optim.SGD(model.parameters(), lr=1e-5)


# Define loss function
loss_fn = F.mse_loss


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
    
fit(1000, model, loss_fn, opt)






