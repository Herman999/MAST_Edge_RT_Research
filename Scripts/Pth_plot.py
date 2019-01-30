# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 12:42:56 2018

@author: rbatt
"""


t1= Shot(27035, LHt=[(0.1150,0.1281,0.1017)], HLt = [(0.3096,0.3098,0)])
t2= Shot(27036, LHt = [(0.1111,0.1212, 0.1014)], HLt = [(0.3261,0.327,0)])
t3= Shot(27037, LHt=[(0.1089,0.1210,0.1014)], HLt = [(0.3247, 0.3252, 0.3246)])

testshots = [t1,t2,t3]
for shot in testshots:
    shot.transition_params()
    
df = pd.DataFrame(t1._pandas)
df = df.append(pd.DataFrame(t2._pandas))
df = df.append(pd.DataFrame(t3._pandas))

dflh = df.loc[df['LH/HL']=='LH']
ploss = dflh[dflh['param']=='Ploss']
ne = dflh[dflh['param'] == 'AYC_NE']


plt.figure()
plt.errorbar(x=ne['p_value'],xerr=ne['p_value_err'],y = ploss['p_value'],yerr=ploss['p_value_err'])

plt.xlabel(r'n_e')
plt.ylabel(r'P_{loss}')
plt.title('test Pth plot')