# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 11:08:38 2019

@author: Tomas

"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create db

"""
dic = (['shot','shot_time','time','time_em','time_ep','transition',
                            'Ploss','Ploss_e',
                           'BT','IP','KAPPA',
                           'Ne_AYC','Ne_AYC_e', 'Ne_AYE','Ne_AYE_e','Ne_ANE','Ne_ANE_e',
                           'Te_AYC','Te_AYC_e', 'Te_AYE','Te_AYE_e',
                           'Pe_AYC','Pe_AYC_e', 'Pe_AYE','Pe_AYE_e',
                           'X1Z','X2Z','session','geometry'
                           ])
"""


db = pd.DataFrame(columns=['shot', 'shot_time', 'time', 'time_em', 'time_ep', 'transition', 'session', 'geometry', 'Ploss', 'Ploss_e', 'BT', 'BT_e','BTOut','BTOut_e','IP', 'IP_e', 'KAPPA', 'KAPPA_e', 'AYC_NE', 'AYC_NE_e', 'AYE_NE', 'AYE_NE_e', 'ANE_DENSITY', 'ANE_DENSITY_e', 'AYC_TE', 'AYC_TE_e', 'AYE_TE', 'AYE_TE_e', 'AYC_PE', 'AYC_PE_e', 'AYE_PE', 'AYE_PE_e', 'NE', 'NE_e', 'TE', 'TE_e', 'PE', 'PE_e', 'X1Z', 'X1Z_e', 'X2Z', 'X2Z_e','SAREA','SAREA_e','AIM_DA_TO','AIM_DA_TO_e'])

#db.loc[len(db)]=dic




#%%
# session 18Sep08
# NO AYC_NE, AYE_NE
session = '18Sep08'
geometry = 'CND'

#from signal_dict_SEP_08 import signals
from signal_dict_10_NOV_11 import signals

shots = [
'Shot(20377, LHt=[(0.2339,0.2338,0.2340)], HLt=[(0.335,0.3349,0.3351)])',

'Shot(20378, LHt=[(0.2332,0.23309,0.23321)], HLt=[(0.2987,0.29869,0.29871)])',

'Shot(20379, LHt=[(0.2805,0.28049,0.28051)], HLt=[(0.314,0.308,0.3141)])',

'Shot(20380, LHt=[(0.2496,0.24959,0.24961)], HLt=[(0.2954,0.29539,0.29541)])',

'Shot(20381, LHt=[(0.2342,0.2341,0.2343)], HLt=[(0.3108,0.31079,0.31081)])',

'Shot(20476, LHt=[(0.2196,0.2195,0.2197)], HLt=[(0.3038,0.3037,0.3039)])',

'Shot(20479, LHt=[(0.1909,0.1908,0.1910)], HLt=[(0.3116,0.3115,0.3117)])',

'Shot(20480, LHt=[(0.1975,0.1974,0.1976)], HLt=[(0.267,0.2669,0.2671)])',

'Shot(27030, LHt=[(0.1928, 0.193, 0.1927)], HLt=[(0.1963, 0.1963,0.19637)])',
'Shot(27035, LHt=[(0.2868,0.2865,0.287)], HLt = [(0.3096,0.3096,0.3098)])',
'Shot(27036, LHt = [(0.2565, 0.2545,0.258)], HLt = [(0.3261,0.3261,0.327)])',
'Shot(27037, LHt=[(0.2607,0.260,0.261)], HLt = [(0.3247, 0.3246, 0.3252)])',

'Shot(27444, LHt=[(0.259,0.2545,0.2595)], HLt=[(0.324,0.323,0.325)])',
'Shot(27446, LHt=[(0.276,0.274,0.2765)], HLt=[(0.3074,0.307,0.308)])',
'Shot(27448, LHt=[(0.110,0.105,0.118)], HLt=[(0.2894,0.2893,0.2895)])',
'Shot(27449, LHt=[(0.115,0.110,0.120)], HLt=[(0.301,0.300,0.306)])',
'Shot(27450, LHt=[(0.116,0.110,0.118)], HLt=[(0.305,0.303,0.306)])',
#'Shot(27451, LHt=[(0.2665,0.266,0.267),(0.2847,0.284,0.2855)], HLt=[(0.273,0.2725,0.2735),(0.287,0.287,0.289)])',
'Shot(27453, LHt=[(0.295,0.2945,0.2955)], HLt=[(0.3105,0.3099,0.311)])',
'Shot(27454, LHt=[(0.277,0.276,0.278)], HLt=[(0.2893,0.289,0.290)])'

         ]
#%%

session = '26-May-05'
geometry = 'SN'

from signal_dict_26_MAY_05 import signals

shots = ['Shot(13042, LHt=[(0.302,0.300,0.303)], HLt=[(0.393,0.392,0.396)])',
         'Shot(13043, LHt=[(0.314,0.310,0.315)], HLt=[(0.326,0.325,0.327)])',
         'Shot(13044, LHt=[(0.336,0.334,0.337)], HLt=[(0.346,0.345,0.347)])',
         'Shot(13045, LHt=[(0.348,0.346,0.349)], HLt=[(0.363,0.362,0.364)])',
         'Shot(13047, LHt=[(0.297,0.2965,0.298)], HLt=[(0.3835,0.383,0.384)])',
         'Shot(14545, LHt=[(0.272,0.2715,0.273)], HLt=[(0.424,0.423,0.425)])',
         'Shot(14546, LHt=[(0.313,0.312,0.314)], HLt=[(0.417,0.416,0.419)])',
         'Shot(14547, LHt=[(0.283,0.2825,0.289)], HLt=[(0.343,0.342,0.344)])',
         'Shot(14548, LHt=[(0.292,0.265,0.293)], HLt=[(0.359,0.358,0.360)])',
         'Shot(14552, LHt=[(0.3083,0.308,0.309)], HLt=[(0.3263,0.326,0.327)])',
         'Shot(14554, LHt=[(0.3016,0.301,0.302)], HLt=[(0.31175,0.3117,0.3118)])',
         'Shot(14555, LHt=[(0.2915,0.291,0.292)], HLt=[(0.3060,0.305,0.3065)])'

         ]

#%%
session = '10-Aug-05'
geometry = 'CDN'

from signal_dict_26_MAY_05 import signals

shots = ['Shot(13704, LHt=[(0.337,0.334,0.360)], HLt=[(0.384,0.383,0.387)])'
         ]

#%%


session = '22-Jan-10'
geometry = 'maybe CND'

from signal_dict_13_DEC_PULL import signals

shots = [
'Shot(24134, LHt=[(0.3018,0.3016,0.302)], HLt=[(0.3448,0.344,0.345)])',
'Shot(24133, LHt=[(0.2818,0.2815,0.282),(0.3286,0.3275,0.329)], HLt=[(0.3255,0.325,0.326),(0.3315,0.331,0.332)])',
'Shot(24132, LHt=[(0.2637,0.262,0.264),(0.2945,0.294,0.295)], HLt=[(0.283,0.282,0.2835),(0.340,0.339,0.341)])',
'Shot(24131, LHt=[(0.2905,0.290,0.291)], HLt=[(0.3366,0.3365,0.344)])',
'Shot(24130, LHt=[(0.285,0.2845,0.2855)], HLt=[(0.3325,0.332,0.333)])',
'Shot(24129, LHt=[(0.2922,0.290,0.295)], HLt=[(0.3174,0.317,0.318)])',
'Shot(24128, LHt=[(0.2572,0.257,0.258)], HLt=[(0.3435,0.343,0.344)])',
'Shot(24127, LHt=[(0.2738,0.273,0.274)], HLt=[(0.311,0.3105,0.3115)])',
'Shot(24126, LHt=[(0.2781,0.278,0.2815)], HLt=[(0.3435,0.343,0.344)])',
'Shot(24125, LHt=[(0.2856,0.285,0.286)], HLt=[(0.3232,0.323,0.3235)])',

'Shot(24124, LHt=[(0.246,0.242,0.260)], HLt=[(0.2896,0.288,0.2897)])', # I had to cut on the lower end of uncertainty here in HL


'Shot(24215, LHt=[(0.2515,0.2513,0.252)],HLt=[(0.284,0.2839,0.2841)])',
'Shot(24216, LHt=[(0.2537,0.25369,0.254), (0.3174,0.31739,0.3176)],HLt=[(0.2845,0.28449,0.2847), (0.3585,0.3579, 0.3586)])',
'Shot(24324, LHt=[(0.2535,0.2533,0.2536), (0.3181,0.3175,0.3189)],HLt=[(0.2823,0.2821,0.2824), (0.3431,0.3423,0.34311)])',
'Shot(24325, LHt=[(0.2515,0.2512,0.2518), (0.319, 0.317,0.321)],HLt=[(0.2845,0.2843,0.2847), (0.345,0.344,0.346)])',
'Shot(24326, LHt=[(0.2515, 0.251, 0.252)],HLt=[(0.284,0.2839, 0.2845)])',
'Shot(24327, LHt=[(0.2511,0.2508,0.2513)],HLt=[(0.2875, 0.2874, 0.2876)])',
'Shot(24328, LHt=[(0.251, 0.2506, 0.2514)],HLt=[(0.2895, 0.2894, 0.2896)])',
'Shot(24329, LHt=[(0.2625, 0.2624, 0.263), (0.318, 0.317, 0.319)],HLt=[(0.281, 0.2808, 0.2812), (0.3365, 0.3364, 0.3366)])',
'Shot(24330, LHt=[(0.252, 0.2517, 0.2521)],HLt=[(0.2842, 0.2841, 0.2843)])'
]

#%%
# new data shots
from signal_dict_2019_IP import signals
session = 'IP_scan+IP on E_R'
geometry = 'CND'

shots = [
'Shot(30351, LHt=[(0.300, 0.295, 0.334)],HLt=[(0.620, 0.615, 0.622)])',
'Shot(30356, LHt=[(0.273, 0.270, 0.275)],HLt=[(0.2791, 0.2790, 0.2794)])',
'Shot(30358, LHt=[(0.1975, 0.19745, 0.1976)],HLt=[(0.3425, 0.342, 0.343)])',

'Shot(30358, LHt=[(0.2665, 0.266, 0.267),(0.385,0.384,0.3865)],HLt=[(0.3629, 0.3625, 0.363),(0.401,0.400,0.404)])',
'Shot(24431, LHt=[(0.2615, 0.261, 0.262)],HLt=[(0.3823, 0.382, 0.3877)])',

	
'Shot(24514, LHt=[(0.336, 0.335, 0.337)],HLt=[(0.3574, 0.357, 0.3575)])',
'Shot(24517, LHt=[(0.2794, 0.280, 0.285)],HLt=[(0.3086, 0.300, 0.301)])',
'Shot(24518, LHt=[(0.2907, 0.290, 0.292)],HLt=[(0.3535, 0.353, 0.3536)])',
'Shot(24522, LHt=[(0.2535, 0.253, 0.254)],HLt=[(0.3555, 0.355, 0.3558)])',
'Shot(24524, LHt=[(0.201, 0.197, 0.202)],HLt=[(0.355, 0.354, 0.3558)])',
'Shot(24524, LHt=[(0.201, 0.197, 0.202)],HLt=[(0.355, 0.354, 0.3558)])',
		
#H-mode Access and rotating RMP		
'Shot(29486, LHt=[(0.2681, 0.268, 0.2682)],HLt=[(0.3378, 0.3375, 0.3379)])',
'Shot(29487, LHt=[(0.2725, 0.2724, 0.2726)],HLt=[(0.378, 0.372, 0.385)])',
'Shot(29493, LHt=[(0.419, 0.418, 0.4195)],HLt=[(0.4395, 0.439, 0.4399)])',
'Shot(29496, LHt=[(0.279, 0.278, 0.280)],HLt=[(0.661, 0.660, 0.662)])',
		
		
#L-H transition at low Ip vs Divertor Detachment		
'Shot(27571, LHt=[(0.258, 0.257, 0.259)],HLt=[(0.3065, 0.306, 0.307)])',
'Shot(27572, LHt=[(0.260, 0.255, 0.261)],HLt=[(0.2735, 0.273, 0.279)])',
'Shot(27573, LHt=[(0.268, 0.262, 0.2681)],HLt=[(0.2751, 0.275, 0.2755)])',
'Shot(27587, LHt=[(0.222, 0.221, 0.223)],HLt=[(0.268, 0.267, 0.269)])',
'Shot(27588, LHt=[(0.2222, 0.222, 0.2223)],HLt=[(0.2667, 0.265, 0.267)])',
'Shot(27589, LHt=[(0.2001, 0.200, 0.201)],HLt=[(0.329, 0.328, 0.3293)])'

]


#%%



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
                units = s.data[parameter]['units']
                
                import bisect
                signal_ind = bisect.bisect(t1, s.data['Ploss']['time']) #get index of value we will use
                signal_at_t1 = s.data['Ploss']['data'][signal_ind]        #bisect
                signal_at_t1_err = s.data['Ploss']['errors'][signal_ind]         #bisect the previous value
                
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
        
writer = pd.ExcelWriter('shot_database_ALL_SHOTS_NewX1X2_.xlsx')
db.to_excel(writer,'Sheet1')
writer.save()


#%%
writer = pd.ExcelWriter('test2.xlsx')
combined.to_excel(writer,'Sheet1')
writer.save()
