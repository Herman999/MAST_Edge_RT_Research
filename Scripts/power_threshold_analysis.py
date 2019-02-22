# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 12:02:30 2018

@author: Tomas
"""

from signal_dict_10_NOV_11 import signals


import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

# correctly identified transitions
from signal_dict_10_NOV_11 import signals

s = Shot(27444, LHt=[(0.259,0.2545,0.2595)], HLt=[(0.324,0.323,0.325)])
s1 = Shot(27446, LHt=[(0.276,0.274,0.2765)], HLt=[(0.3074,0.307,0.308)])
s2 = Shot(27448, LHt=[(0.110,0.105,0.118)], HLt=[(0.2894,0.2893,0.2895)])
s3 = Shot(27449, LHt=[(0.115,0.110,0.120)], HLt=[(0.301,0.300,0.306)])
s4 = Shot(27450, LHt=[(0.116,0.110,0.118)], HLt=[(0.305,0.303,0.306)])
s5 = Shot(27451, LHt=[(0.2665,0.266,0.267),(0.2847,0.284,0.2855)], HLt=[(0.273,0.2725,0.2735),(0.287,0.287,0.289)])
s6 = Shot(27453, LHt=[(0.295,0.2945,0.2955)], HLt=[(0.3105,0.3099,0.311)])
s7 = Shot(27454, LHt=[(0.277,0.276,0.278)], HLt=[(0.2893,0.289,0.290)])


from signal_dict_06_OCT_11 import signals

s8 = Shot(27035, LHt=[(0.2868,0.2865,0.287)], HLt = [(0.3096,0.3096,0.3098)])
s9 = Shot(27036, LHt = [(0.2565, 0.2545,0.258)], HLt = [(0.3261,0.3261,0.327)])
s10 = Shot(27037, LHt=[(0.2607,0.260,0.261)], HLt = [(0.3247, 0.3246, 0.3252)])



# old transitions identification
"""
from signal_dict_10_NOV_11 import signals

s = Shot(27444, LHt=[(0.111,0.105,0.116)], HLt=[(0.324,0.323,0.325)])

s1 = Shot(27446, LHt=[(0.115,0.110,0.120)], HLt=[(0.3074,0.307,0.308)])

s2 = Shot(27448, LHt=[(0.110,0.105,0.118)], HLt=[(0.2894,0.2893,0.2895)])

s3 = Shot(27449, LHt=[(0.115,0.110,0.120)], HLt=[(0.301,0.300,0.306)])

s4 = Shot(27450, LHt=[(0.116,0.110,0.118)], HLt=[(0.305,0.303,0.306)])

s5 = Shot(27451, LHt=[(0.2665,0.266,0.267),(0.2847,0.284,0.2855)], HLt=[(0.273,0.2725,0.2735),(0.287,0.287,0.289)])

s6 = Shot(27451, LHt=[(0.2665,0.266,0.267),(0.2847,0.284,0.2855)], HLt=[(0.273,0.2725,0.2735),(0.287,0.287,0.289)])

s7 = Shot(27454, LHt=[(0.277,0.276,0.278)], HLt=[(0.2893,0.289,0.290)])


from signal_dict_06_OCT_11 import signals

s8 = Shot(27035, LHt=[(0.1150,0.1281,0.1017)], HLt = [(0.3096,0.3098,0.3096)])

s9 = Shot(27036, LHt = [(0.1111,0.1212, 0.1014)], HLt = [(0.3261,0.327,0.3261)])

s10 = Shot(27037, LHt=[(0.1089,0.1210,0.1014)], HLt = [(0.3247, 0.3252, 0.3246)])
"""

s.transition_params()
df = pd.DataFrame(s._pandas)

for a in [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10]:
    a.transition_params()
    df = df.append(pd.DataFrame(a._pandas))
    

#%%
df.set_index('shot',inplace = True)
#%%

dflh_AYC_NE = df[(df['LH/HL']=='LH')&(df['param']=='AYC_NE')]
dflh_AYC_NE_shots = list(dflh_AYC_NE.index)
dflh_AYC_NE_ploss = df[(df['LH/HL']=='LH')&( df['param']=='Ploss')]
dflh_AYC_NE_ploss  = dflh_AYC_NE_ploss[(dflh_AYC_NE_ploss.index.isin(dflh_AYC_NE_shots))]


dflh_ANE_NE = df[(df['LH/HL']=='LH')&(df['param']=='ANE_DENSITY')]
dflh_ANE_NE.loc[:,'p_value'] = dflh_ANE_NE['p_value']/4 # 5.3
dflh_ANE_NE.loc[:,'p_value_err'] = dflh_ANE_NE['p_value_err'] /4
dflh_ANE_NE_shots = list(dflh_ANE_NE.index)
dflh_ANE_NE_ploss = df[(df['LH/HL']=='LH')&( df['param']=='Ploss')]
dflh_ANE_NE_ploss  = dflh_ANE_NE_ploss[(dflh_ANE_NE_ploss.index.isin(dflh_ANE_NE_shots))]



plt.figure(figsize=(13,9))
plt.errorbar(x = dflh_AYC_NE['p_value'], markersize=10, y = dflh_AYC_NE_ploss['p_value'], xerr=dflh_AYC_NE['p_value_err'],yerr =  dflh_AYC_NE_ploss['range_err'],fmt='o', label = 'LH AYC_NE',color = 'red')

#for i, txt in enumerate(dflh_AYC_NE_shots):
#    plt.annotate(txt, (list(dflh_AYC_NE['p_value'])[i], list(dflh_AYC_NE_ploss['p_value'])[i]))

#plt.errorbar(x = dflh_ANE_NE['p_value'], markersize=10, y = dflh_ANE_NE_ploss['p_value'], xerr=dflh_ANE_NE['range_err'], yerr = dflh_ANE_NE_ploss['range_err'],fmt='o', label = 'LH ANE_NE',color = 'r')

#for i, txt in enumerate(dflh_ANE_NE_shots):
#    plt.annotate(txt, (list(dflh_ANE_NE['p_value'])[i], list(dflh_ANE_NE_ploss['p_value'])[i]))



#%%
# log log fit



x_raw = list(dflh_AYC_NE['p_value'])
x_raw.extend(list(dflh_ANE_NE['p_value'] ))
x_data = np.log(x_raw)

y_raw = list(dflh_AYC_NE_ploss['p_value'])
y_raw.extend(dflh_ANE_NE_ploss['p_value'])
y_data = np.log(y_raw)

c_err = list(dflh_AYC_NE['p_value_err'])
c_err.extend(list(dflh_ANE_NE['p_value_err'] ))
x_err = np.log(c_err)

d_err = list(dflh_AYC_NE_ploss['range_err'])
d_err.extend(dflh_ANE_NE_ploss['range_err'])
y_err = np.log(d_err)


# here I will swap AYC for ANE
"""
x_raw = list(dflh_ANE_NE['p_value'])
#x_raw.extend(list(dflh_ANE_NE['p_value'] ))
x_data = np.log(x_raw)

y_raw = list(dflh_ANE_NE_ploss['p_value'])
#y_raw.extend(dflh_ANE_NE_ploss['p_value'])
y_data = np.log(y_raw)

c_err = list(dflh_ANE_NE['p_value_err'])
#c_err.extend(list(dflh_ANE_NE['p_value_err'] ))
#x_err = np.log(c_err)
x_err = np.zeros(len(c_err))

d_err = list(dflh_ANE_NE_ploss['range_err'])
#d_err.extend(dflh_ANE_NE_ploss['range_err'])
y_err = np.log(d_err)
"""

[a,b], [[a_v,ab_v],[_,b_v]] = \
    np.polyfit(x_data,y_data,1,w=1/np.sqrt(y_err**2 + x_err**2),full=False,cov=True)

print(r'the LH $\alpha$ proportanility coeficient is {0} \pm {1}'.format(a,a_v))



#plt.figure()
#plt.scatter(np.power(x_raw,a),y_raw)

xnew =np.linspace(min(x_data),max(x_data), 30)
plt.plot(np.exp(xnew), np.exp(a*xnew+b),linestyle='dashed',color='orange',label = r'$L \to H$ loglog fit $\alpha=${0} $\pm$ {1}'.format(np.round(a,2), np.round(a_v,2)))

#%%
# Here do HL analysis and plot

s.transition_params()
df = pd.DataFrame(s._pandas)

for a in [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10]:
    a.transition_params()
    df = df.append(pd.DataFrame(a._pandas))
    
df.set_index('shot',inplace = True)

dflh_AYC_NE = df[(df['LH/HL']=='HL')&(df['param']=='AYC_NE')]
dflh_AYC_NE_shots = list(dflh_AYC_NE.index)
dflh_AYC_NE_ploss = df[(df['LH/HL']=='HL')&( df['param']=='Ploss')]
dflh_AYC_NE_ploss  = dflh_AYC_NE_ploss[(dflh_AYC_NE_ploss.index.isin(dflh_AYC_NE_shots))]

# Here ANE

dflh_ANE_NE = df[(df['LH/HL']=='HL')&(df['param']=='ANE_DENSITY')]
dflh_ANE_NE['p_value'] = dflh_ANE_NE['p_value']/4 # 5.3
dflh_ANE_NE['p_value_err'] = dflh_ANE_NE['p_value_err'] /4
dflh_ANE_NE_shots = list(dflh_ANE_NE.index)
dflh_ANE_NE_ploss = df[(df['LH/HL']=='HL')&( df['param']=='Ploss')]
dflh_ANE_NE_ploss  = dflh_ANE_NE_ploss[(dflh_ANE_NE_ploss.index.isin(dflh_ANE_NE_shots))]



plt.errorbar(x = dflh_AYC_NE['p_value'], markersize=10, y = dflh_AYC_NE_ploss['p_value'], xerr=dflh_AYC_NE['p_value_err'],yerr =  dflh_AYC_NE_ploss['range_err'],fmt='x', label = 'HL AYC_NE',color = 'blue')

#for i, txt in enumerate(dflh_AYC_NE_shots):
#    plt.annotate(txt, (list(dflh_AYC_NE['p_value'])[i], list(dflh_AYC_NE_ploss['p_value'])[i]))

#plt.errorbar(x = dflh_ANE_NE['p_value'], markersize=10, y = dflh_ANE_NE_ploss['p_value'], xerr=dflh_ANE_NE['range_err'], yerr = dflh_ANE_NE_ploss['range_err'],fmt='x', label = 'HL ANE_NE',color = 'lime')

#for i, txt in enumerate(dflh_ANE_NE_shots):
#    plt.annotate(txt, (list(dflh_ANE_NE['p_value'])[i], list(dflh_ANE_NE_ploss['p_value'])[i]))


# log log fit


x_raw = list(dflh_AYC_NE['p_value'])
#x_raw.extend(list(dflh_ANE_NE['p_value'] ))
x_data = np.log(x_raw)

y_raw = list(dflh_AYC_NE_ploss['p_value'])
#y_raw.extend(dflh_ANE_NE_ploss['p_value'])
y_data = np.log(y_raw)

c_err = list(dflh_AYC_NE['p_value_err'])
#c_err.extend(list(dflh_ANE_NE['p_value_err'] ))
x_err = np.log(c_err)

d_err = list(dflh_AYC_NE_ploss['range_err'])
#d_err.extend(dflh_ANE_NE_ploss['range_err'])
y_err = np.log(d_err)


[a,b], [[a_v,ab_v],[_,b_v]] = \
    np.polyfit(x_data,y_data,1,w=1/np.sqrt(y_err**2 + x_err**2),full=False,cov=True)

print(r'the HL $\alpha$ proportanility coeficient is {0} \pm {1}'.format(a,a_v))



#plt.figure()
#plt.scatter(np.power(x_raw,a),y_raw)

xnew =np.linspace(min(x_data),np.log(4e19), 30)
plt.plot(np.exp(xnew), np.exp(a*xnew+b),linestyle='dashed', color = 'green',label = r'$H \to L$ loglog fit $\alpha=${0} $\pm$ {1}'.format(np.round(a,2), np.round(a_v,2)))



#%%
#plt.plot(np.linspace(min(x_raw),max(x_raw),100),e*np.linspace(min(x_raw),max(x_raw),100) + f,label='loglog lin fit',alpha=0.7)
plt.legend(loc=2)
#plt.xscale('log')
#plt.yscale('log')
plt.xlim([0,7e19])
textstr = r'$I_p=700$kA $B_t=-0.425$T'
plt.text(3.6e19, 8e6, textstr, fontsize=14)
plt.xlim([9e18,4.5e19])
plt.ylim([0,7.8e6])
plt.title(r'$P_{th}$ scaling $L \to H$ and $H \to L$')
plt.xlabel(r'$n_e$ (AYC_NE, ANE_DENSITY) [$n^{-3}$]')
plt.ylabel('Ploss [W]')
plt.ticklabel_format(axis='y',scilimits=(0,0))
#plt.show()






