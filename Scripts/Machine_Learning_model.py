# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 13:45:58 2019

@author: Tomas
"""

# ML model preparation

# dummpy preparation


import pandas as pd
import numpy as np
import torch



class LinearRegressionModel(torch.nn.Module): 
  
    def __init__(self): 
        super(LinearRegressionModel, self).__init__() 
        self.linear = torch.nn.Linear(3, 1)  # One in and one out 
  
    def forward(self, x): 
        y_pred = self.linear(x) 
        return y_pred 



df = pd.DataFrame(data = [np.random.random(10),range(10), np.linspace(50,100,10)])
df = df.T
# df = x data

x_data = torch.tensor(df.values)

df[3] = df[2]
y_data = torch.tensor(df[3].values.reshape(10,1))


model = LinearRegressionModel()
model.double()

criterion = torch.nn.MSELoss(size_average = False) 
optimizer = torch.optim.SGD(model.parameters(), lr = 0.01) 



for epoch in range(50): 
  
    # Forward pass: Compute predicted y by passing  
    # x to the model 
    pred_y = model(x_data) 
  
    # Compute and print loss 
    loss = criterion(pred_y, y_data) 
  
    # Zero gradients, perform a backward pass,  
    # and update the weights. 
    optimizer.zero_grad() 
    loss.backward() 
    optimizer.step() 
    print('epoch {}, loss {}'.format(epoch, loss.data[0])) 



new_var = torch.autograd.Variable(torch.Tensor(np.array([100.,100.,100.])))
model = model.float() 
pred_y = model(new_var) 
print("predict (after training)", 4, model(new_var).data[0][0]) 



