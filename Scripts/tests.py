# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 12:06:01 2019

@author: Tomas
"""

import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 14})

df = pd.read_excel('C:/Users/Public/data/indexes_commodities_fitted.xlsx')
df2 = pd.read_excel('C:/Users/Public/data/fx_120mins_best_fit.xlsx')



a= df['profit'].cumsum()*100
b= df2['profit'].cumsum()*100



df['profit'] = df['profit'] +1
df2['profit']= df2['profit'] +1

#a = df['profit'].cumprod()*100 - 100
#b = df2['profit'].cumprod()*100 - 100
 

plt.figure(figsize=(13,9))
plt.title('Counter-Trader Returns Backtest [2018 Coinshares Internship]')
plt.plot(a,label='Indexes')
plt.plot(b,label='FX')
plt.xlabel('# trades [summer 2018]')
plt.ylabel('% returns [exluding fees]')
plt.legend()
plt.show()