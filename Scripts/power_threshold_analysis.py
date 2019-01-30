# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 12:02:30 2018

@author: Tomas
"""

from signal_dict_10_NOV_11 import signals


import pandas as pd

s = Shot(27444, LHt=[(0.254,0.251,0.259)], HLt=[(0.324,0.323,0.325)])
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

s.transition_params()
df = pd.DataFrame(s._pandas)

for a in [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10]:
    a.transition_params()
    df = df.append(pd.DataFrame(a._pandas))
    

#%%
    
dflh = df[df['LH/HL'] == 'LH'].set_index('shot')

ne = dflh[dflh['param'].isin(['AYC_NE'])]
#ne = dflh[dflh['param'].isin(['ANE_DENSITY'])]
#ne = ne.append(dflh[dflh['param']=='AYC_NE'])
ploss = dflh[dflh['param'] == 'Ploss']

#dflh.loc[ind][dflh['param'] == 'Ploss']

#ploss = ploss.append(dflh[dflh['param'] == 'Ploss'])

plt.figure()
plt.errorbar(ne['p_value'], ploss['p_value'], yerr = ploss['range_err'], xerr = ne['p_value_err'], fmt=None)

#%%

dflh = df.loc[df['LH/HL']=='LH']
ploss = dflh[dflh['param']=='Ploss']
ne = dflh[dflh['param'] == 'AYC_NE']


plt.figure()
plt.errorbar(x=ne['p_value'],xerr=ne['p_value_err'],y = ploss['p_value'],yerr=ploss['p_value_err'])

plt.xlabel(r'n_e')
plt.ylabel(r'P_{loss}')
plt.title('test Pth plot')













