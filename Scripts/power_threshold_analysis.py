# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 12:02:30 2018

@author: Tomas

# TO USE
# 1. Initiate
2. LOAD SESSION 1
3. RUN DATA ANALYSSIS
4. RETURN AND LOAD SESION 2
5. RUN PLTTING for old method
6. RUN REST IN SECTIONS NORMALY 
7. ENJOY
"""

from signal_dict_10_NOV_11 import signals


import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

db = pd.DataFrame(columns=['shot', 'shot_time', 'time', 'time_em', 'time_ep', 'transition', 'session', 'geometry', 'Ploss', 'Ploss_e', 'BT', 'BT_e','BTOut','BTOut_e','IP', 'IP_e', 'KAPPA', 'KAPPA_e', 'AYC_NE', 'AYC_NE_e', 'AYE_NE', 'AYE_NE_e', 'ANE_DENSITY', 'ANE_DENSITY_e', 'AYC_TE', 'AYC_TE_e', 'AYE_TE', 'AYE_TE_e', 'AYC_PE', 'AYC_PE_e', 'AYE_PE', 'AYE_PE_e', 'NE', 'NE_e', 'TE', 'TE_e', 'PE', 'PE_e', 'X1Z', 'X1Z_e', 'X2Z', 'X2Z_e','SAREA','SAREA_e','AIM_DA_TO','AIM_DA_TO_e'])

# %%
# NEW ANALYSIS

session = 'Pth Ne Scaling'
geometry ='Not interested'

from signal_dict_10_NOV_11 import signals
shots = [
'Shot(27444, LHt=[(0.259,0.2545,0.2595)], HLt=[(0.324,0.323,0.325)])',
'Shot(27446, LHt=[(0.276,0.274,0.2765)], HLt=[(0.3074,0.307,0.308)])',
'Shot(27448, LHt=[(0.110,0.105,0.118)], HLt=[(0.2894,0.2893,0.2895)])',
'Shot(27449, LHt=[(0.115,0.110,0.120)], HLt=[(0.306,0.301,0.3061)])',
'Shot(27450, LHt=[(0.116,0.110,0.118)], HLt=[(0.3055,0.303,0.306)])',
#'Shot(27451, LHt=[(0.2665,0.266,0.267),(0.2847,0.284,0.2855)], HLt=[(0.273,0.2725,0.2735),(0.287,0.287,0.289)])',
'Shot(27453, LHt=[(0.295,0.2945,0.2955)], HLt=[(0.3105,0.3099,0.311)])',
'Shot(27454, LHt=[(0.277,0.276,0.278)], HLt=[(0.2893,0.289,0.290)])',
]

#%%

from signal_dict_06_OCT_11 import signals
shots=[
'Shot(27035, LHt=[(0.2868,0.2865,0.287)], HLt = [(0.3096,0.3096,0.3098)])',
'Shot(27036, LHt = [(0.2565, 0.2545,0.258)], HLt = [(0.3261,0.3261,0.327)])',
'Shot(27037, LHt=[(0.2607,0.260,0.261)], HLt = [(0.3247, 0.3246, 0.3252)])',
]

#%%


for shot_str in shots:

    s=eval(shot_str)

    
    parameters = ['Ploss','BT','IP','KAPPA',
                               'AYC_NE','AYE_NE','ANE_DENSITY',
                               'AYC_TE','AYE_TE',
                               'AYC_PE','AYE_PE',
                               'NE', 'TE', 'PE',
                               'X1Z','X2Z','SAREA','AIM_DA_TO']
    
    # here iterate shots
    
    # compbine LHt and HLt 
    list_of_transitions = []
    list_of_transitions.extend(s._LHt)
    list_of_transitions.extend(s._HLt)
    
    for t in list_of_transitions:
        dic = {}
        t1 = t[0]   #time of tranision
        t_err1 = t[1] # lower bound time error
        t_err2 = t[2] # upper bound time error
        
        # update dic separately for LH and HL
        dic['shot']=s.ShotNumber
        dic['shot_time']=str(s.ShotNumber) + '_' + str(int(round(t1*1000)))
        dic['time']=t1
        dic['time_em']=t[1] - t[0]
        dic['time_ep']= t[2] - t[0]
        
        
        if t in s._LHt:
            dic['transition'] = 'LH'
        elif t in s._HLt:
            dic['transition'] = 'HL'
        else:
            dic['transition'] = 'error'
        
        dic['session'] = session
        dic['geometry'] = geometry
        
        # Add BTout
        A = 1.3 # mast aspect ratio
        dic['BTOut'] = A/(A+1) * np.interp(t1, s.data['BT']['time'] , s.data['BT']['data'])
        singal_t_err_range =  A/(A+1)*np.interp(np.linspace(t_err1,t_err2,30), s.data['BT']['time'] , s.data['BT']['data'])
        singal_t_err_error_range = np.zeros(30)
        dic['BTOut_e'] = max(singal_t_err_range) - min(singal_t_err_range) + np.mean(np.abs(singal_t_err_error_range))
        
            
        # now load up parameteres
        for parameter in parameters:
            if parameter == 'Ploss' and dic['transition'] == 'HL':
                # define all the stuff again for special case 
                # DO NOT INTERPOLATE
                
                try: units = s.data[parameter]['units']
                except: 
                    dic[parameter] = None
                    dic[parameter+'_e'] = None
                    continue
                
                import bisect
                signal_ind = bisect.bisect(s.data['Ploss']['time'], t1) #get index of value we will use
                print('################', s.data['Ploss']['time'][signal_ind-1])
                signal_at_t1 = s.data['Ploss']['data'][signal_ind-1]        #bisect
                signal_at_t1_err = s.data['Ploss']['errors'][signal_ind-1]         #bisect the previous value
                
                signal_t_err_range = 0.
                signal_t_err_error_range = 0.
                signal_t_err_spread = 0.
            
                dic[parameter] = signal_at_t1
                dic[parameter+'_e'] = signal_at_t1_err
                
                continue # return to next parameter in parameters
            
                
            # skip if not in data
            if parameter not in s.signals_present()[1]: 
                print(parameter,' Not in signals of shot {}, Skipping.'.format(s.ShotNumber))
                
                dic[parameter] = None
                dic[parameter+'_e'] = None
                continue # if singal doesnt exist, continue
            
            print('loading : {0} for shot {1}'.format(parameter,s.ShotNumber))
            # for problematic data
            try:
                s.data['AYC_NE']['data']=np.nanmean(s.data['AYC_NE']['data'],axis=1)
                s.data['AYC_NE']['errors']=np.nanmean(s.data['AYC_NE']['errors'],axis=1)
                
                s.data['AYC_TE']['data']=np.nanmean(s.data['AYC_TE']['data'],axis=1)
                s.data['AYC_TE']['errors']=np.nanmean(s.data['AYC_TE']['errors'],axis=1)
                
                s.data['AYC_PE']['data']=np.nanmean(s.data['AYC_PE']['data'],axis=1)
                s.data['AYC_PE']['errors']=np.nanmean(s.data['AYC_PE']['errors'],axis=1)
            except:
                pass
            
            try:            
                s.data['AYE_NE']['data']=np.nanmean(s.data['AYE_NE']['data'],axis=1)
                s.data['AYE_NE']['errors']=np.nanmean(s.data['AYE_NE']['errors'],axis=1)
                
                s.data['AYE_TE']['data']=np.nanmean(s.data['AYE_TE']['data'],axis=1)
                s.data['AYE_TE']['errors']=np.nanmean(s.data['AYE_TE']['errors'],axis=1)
                
                s.data['AYE_PE']['data']=np.nanmean(s.data['AYE_PE']['data'],axis=1)
                s.data['AYE_PE']['errors']=np.nanmean(s.data['AYE_PE']['errors'],axis=1)
                
            except:
                pass
            
            try:         
                # for NE for 08 JP shots
                s.data['NE']['data']=np.nanmean(s.data['NE']['data'],axis=1)
                s.data['NE']['errors']=np.nanmean(s.data['NE']['errors'],axis=1)
                s.data['TE']['data']=np.nanmean(s.data['TE']['data'],axis=1)
                s.data['TE']['errors']=np.nanmean(s.data['TE']['errors'],axis=1)
                s.data['PE']['data']=np.nanmean(s.data['PE']['data'],axis=1)
                s.data['PE']['errors']=np.nanmean(s.data['PE']['errors'],axis=1)
                #print(s.data['NE'])
            except: 
                pass
            
            
            
            # get  units
            units = s.data[parameter]['units']
            
            # get parameter at transition
            singal_at_t1 = np.interp(t1, s.data[parameter]['time'] , s.data[parameter]['data'])
            
            # get erro in parameter at transition
            try: # this is None case
                if s.data[parameter]['errors'] == None:
                    singal_at_t1_err = 0
            except:
                if s.data[parameter]['errors'].shape == 2:
                    singal_at_t1_err = np.interp(t1, s.data[parameter]['time'] , np.nanmean(s.data[parameter]['errors'],axis=1))
                else:
                    singal_at_t1_err = np.interp(t1, s.data[parameter]['time'] , s.data[parameter]['errors'])
        
        
            # get parameter range during the time error
            singal_t_err_range = np.interp(np.linspace(t_err1,t_err2,30), s.data[parameter]['time'] , s.data[parameter]['data'])
            #print(singal_t_err_range)
            
            # get errors in the range of time error
            try: 
                if s.data[parameter]['errors'] == None:
                    singal_t_err_error_range = np.zeros(30)
            except: 
                if s.data[parameter]['errors'].shape == 2:
                    singal_t_err_error_range = np.interp(np.linspace(t_err1,t_err2,30), s.data[parameter]['time'] , np.nanmean(s.data[parameter]['errors'],axis=1))
                else:
                    singal_t_err_error_range  = np.interp(np.linspace(t_err1,t_err2,30), s.data[parameter]['time'] , s.data[parameter]['errors'])
            
            #print(singal_t_err_error_range)
            
            # calculate spread in singal during t range and add mean error
            singal_t_err_spread = max(singal_t_err_range) - min(singal_t_err_range) + np.mean(np.abs(singal_t_err_error_range))
            
            
            if parameter not in ['X1Z','X2Z']:
                # add parameter to dic
                dic[parameter] = singal_at_t1
                dic[parameter+'_e'] = singal_t_err_spread
            else:
                if parameter=='X1Z':
                    dic[parameter] = abs(singal_at_t1 + 1.55 )# 1.55m below
                    dic[parameter+'_e'] = abs(singal_t_err_spread)
                elif parameter=='X2Z':
                    dic[parameter] =abs( singal_at_t1 - 1.55 )# 1.55m above
                    dic[parameter+'_e'] = abs(singal_t_err_spread)
        #save db before next transition in same shot
        print(dic)
        db.loc[len(db)]=dic
        del dic

#%%

        
X = 'Ploss'
X_e = 'Ploss_e'

# plot the stuff
LH_shot_list = list(db[(db['transition']=='LH')]['shot'])
HL_shot_list = list(db[(db['transition']=='HL')]['shot'])

ploss_LH = list(db[(db['transition']=='LH')][X])
ploss_HL = list(db[(db['transition']=='HL')][X])

ploss_LH_e = list(db[(db['transition']=='LH')][X_e])
ploss_HL_e = list(db[(db['transition']=='HL')][X_e])

ne_LH = list(db[(db['transition']=='LH')]['AYC_NE'])
ne_HL = list(db[(db['transition']=='HL')]['AYC_NE'])

ne_LH_e = list(db[(db['transition']=='LH')]['AYC_NE_e'])
ne_HL_e = list(db[(db['transition']=='HL')]['AYC_NE_e'])



# PLOTTING



# ------------------------- LH

plt.figure(figsize=(11.5,8))
plt.rcParams.update({'font.size': 14})
plt.errorbar(x = ne_LH, markersize=10, y = ploss_LH , xerr=ne_LH_e,yerr = ploss_LH_e,fmt='o', label = 'LH AYC_NE',color = 'red')


for i, txt in enumerate(LH_shot_list):
    plt.annotate(txt, (list(ne_LH)[i], list(ploss_LH)[i]))

#plt.errorbar(x = dflh_ANE_NE['p_value'], markersize=10, y = dflh_ANE_NE_ploss['p_value'], xerr=dflh_ANE_NE['range_err'], yerr = dflh_ANE_NE_ploss['range_err'],fmt='o', label = 'LH ANE_NE',color = 'r')

#for i, txt in enumerate(dflh_ANE_NE_shots):
#    plt.annotate(txt, (list(dflh_ANE_NE['p_value'])[i], list(dflh_ANE_NE_ploss['p_value'])[i]))


x_data = np.log(ne_LH)

y_data = np.log(ploss_LH)

c_err = list(ne_LH_e)
#c_err.extend(list(dflh_ANE_NE['p_value_err'] ))
x_err = np.log(c_err)

d_err = list(ploss_LH_e)

y_err = np.log(d_err)


[a,b], [[a_v,ab_v],[_,b_v]] = \
    np.polyfit(x_data,y_data,1,w=1/np.sqrt(y_err**2 + x_err**2),full=False,cov=True)

print(r'the LH $\alpha$ proportanility coeficient is {0} \pm {1}'.format(a,a_v))


xnew =np.linspace(min(x_data),max(x_data), 30)
plt.plot(np.exp(xnew), np.exp(a*xnew+b),linestyle='dashed',color='orange',label = r'$L \to H$ loglog fit $\alpha=${0} $\pm$ {1}'.format(np.round(a,2), np.round(a_v,2)))

# --------------------- HL
plt.errorbar(x = ne_HL, markersize=10, y = ploss_HL , xerr=ne_HL_e,yerr = ploss_HL_e,fmt='o', label = 'HL AYC_NE',color = 'blue')


for i, txt in enumerate(HL_shot_list):
    plt.annotate(txt, (list(ne_HL)[i], list(ploss_HL)[i]))


x_data = np.log(ne_HL)

y_data = np.log(ploss_HL)

c_err = list(ne_HL_e)
#c_err.extend(list(dflh_ANE_NE['p_value_err'] ))
x_err = np.log(c_err)

d_err = list(ploss_HL_e)

y_err = np.log(d_err)


[a,b], [[a_v,ab_v],[_,b_v]] = \
    np.polyfit(x_data,y_data,1,w=1/np.sqrt(y_err**2 + x_err**2),full=False,cov=True)

print(r'the HL $\alpha$ proportanility coeficient is {0} \pm {1}'.format(a,a_v))


xnew =np.linspace(min(x_data),max(x_data), 30)
plt.plot(np.exp(xnew), np.exp(a*xnew+b),linestyle='dashed',color='green',label = r'$H \to L$ loglog fit $\alpha=${0} $\pm$ {1}'.format(np.round(a,2), np.round(a_v,2)))



#plt.plot(np.linspace(min(x_raw),max(x_raw),100),e*np.linspace(min(x_raw),max(x_raw),100) + f,label='loglog lin fit',alpha=0.7)
plt.legend(loc=2)
#plt.xscale('log')
#plt.yscale('log')
plt.xlim([0,7e19])
textstr = r'$I_p=700$kA $B_t=-0.425$T'
plt.text(3.6e19, 8e6, textstr, fontsize=14)
plt.xlim([9e18,4.5e19])
plt.ylim([0,7.8e6])
plt.title(r'$P_{th}$ dependance $L \to H$ and $H \to L$')
plt.xlabel(r'$n_e$ [$n^{-3}$]')
plt.ylabel('Ploss [W]')
plt.ticklabel_format(axis='y',scilimits=(0,0))
#plt.show()


#%%
        
# EVERYTHING BELOW IS RUBBISH

# correctly identified transitions
from signal_dict_10_NOV_11 import signals

s = Shot(27444, LHt=[(0.259,0.2545,0.2595)], HLt=[(0.324,0.323,0.325)])
s1 = Shot(27446, LHt=[(0.276,0.274,0.2765)], HLt=[(0.3074,0.307,0.308)])
s2 = Shot(27448, LHt=[(0.110,0.105,0.118)], HLt=[(0.2894,0.2893,0.2895)])
s3 = Shot(27449, LHt=[(0.115,0.110,0.120)], HLt=[(0.306,0.301,0.3061)])
s4 = Shot(27450, LHt=[(0.116,0.110,0.118)], HLt=[(0.3055,0.303,0.306)])
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



plt.figure(figsize=(11.5,8))
plt.errorbar(x = dflh_AYC_NE['p_value'], markersize=10, y = dflh_AYC_NE_ploss['p_value'], xerr=dflh_AYC_NE['p_value_err'],yerr =  dflh_AYC_NE_ploss['range_err'],fmt='o', label = 'LH AYC_NE',color = 'red')


for i, txt in enumerate(dflh_AYC_NE_shots):
    plt.annotate(txt, (list(dflh_AYC_NE['p_value'])[i], list(dflh_AYC_NE_ploss['p_value'])[i]))

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

for i, txt in enumerate(dflh_AYC_NE_shots):
    plt.annotate(txt, (list(dflh_AYC_NE['p_value'])[i], list(dflh_AYC_NE_ploss['p_value'])[i]))

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
plt.title(r'$P_{th}$ dependance $L \to H$ and $H \to L$')
plt.xlabel(r'$n_e$ [$n^{-3}$]')
plt.ylabel('Ploss [W]')
plt.ticklabel_format(axis='y',scilimits=(0,0))
#plt.show()

#%%






