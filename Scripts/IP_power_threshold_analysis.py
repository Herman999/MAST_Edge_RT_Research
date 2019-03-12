# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 14:49:54 2019

@author: Tomas
"""

from signal_dict_2019_IP import signals
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#plt.rcParams.update({'font.size': 14})




# power thresold IP analysis

# load selected shots

# load IP, Ploss, ne
# normalize Pth by ne






alpha = 0.8 

shots = [30351,
24514,
24514,
24524,
24524,
29486,
29486,
29487,
29487,
29493,
29493,

14554,
13704,
24134,
14545,
14546,
13043,
13044,



]




df = pd.read_excel('ML_data_new.xlsx')

df = df[~(df['AYC_NE']=='')]
df = df[~(df['Ploss']<1)]


# shot filter
df = df[df['shot'].isin(shots)]


# Ploss / ne**alpha
# IP

# PLoss
Ploss_LH = np.array( df[(df['transition']=='LH')]['Ploss'])
Ploss_HL = np.array( df[(df['transition']=='HL')]['Ploss'])

Ploss_LH_e = np.array( df[(df['transition']=='LH')]['Ploss_e'])
Ploss_HL_e = np.array( df[(df['transition']=='HL')]['Ploss_e'])

# ne
ne_LH = np.array( df[(df['transition']=='LH')]['AYC_NE'])
ne_HL = np.array( df[(df['transition']=='HL')]['AYC_NE'])

ne_LH_e = np.array( df[(df['transition']=='LH')]['AYC_NE_e'])
ne_HL_e = np.array( df[(df['transition']=='HL')]['AYC_NE_e'])

# ip

ip_LH = np.array( df[(df['transition']=='LH')]['IP'])
ip_HL = np.array( df[(df['transition']=='HL')]['IP'])

ip_LH_e = np.array( df[(df['transition']=='LH')]['IP_e'])
ip_HL_e = np.array( df[(df['transition']=='HL')]['IP_e'])

# shot
shot_LH = np.array( df[(df['transition']=='LH')]['shot'])
shot_HL = np.array( df[(df['transition']=='HL')]['shot'])

plt.figure(figsize=(11.5,8))
plt.title('Normailized Pth dependance on IP')


# LH
plt.errorbar(fmt='o',x = ip_LH, xerr=ip_LH_e, y =Ploss_LH/(ne_LH**alpha), yerr=Ploss_LH_e/(ne_LH**alpha), label='Selected LH',color = 'red'
        )
#for i, txt in enumerate(shot_LH):
#    plt.annotate(txt, (ip_LH[i], (Ploss_LH/(ne_LH**alpha))[i]))
    

# HL
plt.errorbar(fmt='o',x = ip_HL, xerr=ip_HL_e, y =Ploss_HL/(ne_HL**alpha), yerr=Ploss_HL_e/(ne_HL**alpha), label='Selected HL',color = 'blue'
        )
#for i, txt in enumerate(shot_HL):
#    plt.annotate(txt, (ip_HL[i], (Ploss_HL/(ne_HL**alpha))[i]))

#plt.xscale('log')
#plt.yscale('log')
plt.xlabel('IP [kA]')
plt.ylabel(r'$ Ploss   \div \overline{ne}^{0.8} $ $[a.u.]$')

plt.legend()



#%%

# YASMIN SUPER CUSTOMIZED PLOT

# load pedestal data

alpha = 0.8 

db_ped = pd.read_excel('ML_data_PED_new.xlsx')

db_all = pd.read_excel('ML_data_new.xlsx')

X ='X1Z' 
X_e = 'X1Z_e'


# I want to add X point height for each
xs = []
xs_e = []
ploss = []
ploss_e = []
ne = []

for row in range(len(db_ped)-1):
    
    # filter a fucked up shot
    db_ped = db_ped[~((db_ped['transition']=='HL')&(db_ped['shot']==27572))] 
    
    shot = db_ped.iloc[row]['shot']
    transition  = db_ped.iloc[row]['transition']
    
    try:
        xs.append(
            db_all[(db_all['shot']==shot) & (db_all['transition']==transition)][X].iloc[0]
            )
    except: xs.append(np.nan)
    
    try:
        xs_e.append(
            db_all[(db_all['shot']==shot) & (db_all['transition']==transition)][X_e].iloc[0]
            )
    except: xs_e.append(np.nan)

    try:
        ploss.append(
            db_all[(db_all['shot']==shot) & (db_all['transition']==transition)]['Ploss'].iloc[0]
            )
    except: ploss.append(np.nan)
    try:
        ploss_e.append(
            db_all[(db_all['shot']==shot) & (db_all['transition']==transition)]['Ploss_e'].iloc[0]
            )
    except: ploss_e.append(np.nan)
    try:
        ne.append(
            db_all[(db_all['shot']==shot) & (db_all['transition']==transition)]['AYC_NE'].iloc[0]
            )
    except: ne.append(np.nan)




db_ped[X] = pd.Series(xs)
db_ped[X_e] = pd.Series(xs_e)
db_ped['Ploss'] = pd.Series(ploss)
db_ped['Ploss_e'] = pd.Series(ploss_e)
db_ped['AYC_NE'] = pd.Series(ne)

db_ped = db_ped.dropna()



# Ploss/ ne **alpha
# Te ped
# Ne ped

# agains X1 point height

#%%



LH_shot_list = list(db_ped[(db_ped['transition']=='LH')]['shot'])
HL_shot_list = list(db_ped[(db_ped['transition']=='HL')]['shot'])

x_LH = list(db_ped[(db_ped['transition']=='LH')][X])
x_HL = list(db_ped[(db_ped['transition']=='HL')][X])

x_LH_e = list(db_ped[(db_ped['transition']=='LH')][X_e])
x_HL_e = list(db_ped[(db_ped['transition']=='HL')][X_e])

ne_LH = list(db_ped[(db_ped['transition']=='LH')]['ne_at_ped'])
ne_HL = list(db_ped[(db_ped['transition']=='HL')]['ne_at_ped'])

ne_LH_e = list(db_ped[(db_ped['transition']=='LH')]['ne_at_ped_e'])
ne_HL_e = list(db_ped[(db_ped['transition']=='HL')]['ne_at_ped_e'])

te_LH = list(db_ped[(db_ped['transition']=='LH')]['te_at_ped'])
te_HL = list(db_ped[(db_ped['transition']=='HL')]['te_at_ped'])

te_LH_e = list(db_ped[(db_ped['transition']=='LH')]['te_at_ped_e'])
te_HL_e = list(db_ped[(db_ped['transition']=='HL')]['te_at_ped_e'])

pe_LH = list(
        np.array(db_ped[(db_ped['transition']=='LH')]['Ploss']) / 
        (
        np.array(db_ped[(db_ped['transition']=='LH')]['AYC_NE']) ** alpha
        )
        
        )
        
pe_HL = list(
        np.array(db_ped[(db_ped['transition']=='HL')]['Ploss']) / 
        (
        np.array(db_ped[(db_ped['transition']=='HL')]['AYC_NE']) ** alpha
        )
        
        )
        
pe_LH_e = list(
        db_ped[(db_ped['transition']=='LH')]['Ploss_e']/ 
        (
        np.array(db_ped[(db_ped['transition']=='LH')]['AYC_NE']) ** alpha
        )
        
        )
pe_HL_e = list(db_ped[(db_ped['transition']=='HL')]['Ploss_e']/ 
        (
        np.array(db_ped[(db_ped['transition']=='HL')]['AYC_NE']) ** alpha
        )
        )


# NE            
fig, ax = plt.subplots(3,sharex=True,figsize=(11.5,8))


textstr = r'$I_p=500-700$kA $B_t=-0.425$T'
#ax[0].text(1.08, 4.5e19, textstr, fontsize=14)
ax[0].text(-1.045, 4.5e19, textstr, fontsize=14)

ax[0].set_title(r'Customized Pedestal Characteristics on {} point height'.format(X))
ax[2].errorbar(fmt='o',x=x_LH,y=ne_LH,xerr=x_LH_e,yerr=ne_LH_e,c='red',label='LH')
ax[2].errorbar(fmt='o',x=x_HL,y=ne_HL,xerr=x_HL_e,yerr=ne_HL_e,c='blue',label='HL')
#ax[0].scatter(LH_ne_average,LH_ne_at_ped,c='orange',label='LH')
#ax[0].scatter(HL_ne_average,HL_ne_at_ped,c='blue',label='HL')


#for i, txt in enumerate(LH_shot_list):
#    ax[2].annotate(txt, (x_LH[i], ne_LH[i]))
    
#for i, txt in enumerate(HL_shot_list):
#    ax[2].annotate(txt, (x_HL[i], ne_HL[i]))


# lin fit
#(res,cov) = np.polyfit(ne_average,ne_at_ped,deg=1,cov=True)
#neav = np.linspace(min(ne_average),max(ne_average))
#nefit = res[1] + res[0] * neav
#ax[0].plot(neav,nefit,'--',label=r'fit k={0}$\pm${1} c={2}'.format("{:.2E}".format(res[0]),"{:.2E}".format(cov[0,0]),"{:.2E}".format(res[1])))

    
ax[2].set_xlabel('X point height')
ax[2].set_ylabel(r'$Ne_{ped}$ $ [m^{-3}]$')
ax[2].legend()
#ax[0].set_ylim([0,0.05e21])

# TE
#ax[1].scatter(LH_ne_average,LH_te_at_ped,c='orange',label='LH')
#ax[1].scatter(HL_ne_average,HL_te_at_ped,c='blue',label='HL')
#ax[1].errorbar(fmt='o',x=LH_ne_average,y=LH_te_at_ped,xerr=LH_ne_average_e,yerr=LH_te_at_ped_e,c='orange',label='LH')
#ax[1].errorbar(fmt='o',x=HL_ne_average,y=HL_te_at_ped,xerr=HL_ne_average_e,yerr=HL_te_at_ped_e,c='blue',label='HL')
ax[1].errorbar(fmt='o',x=x_LH,y=te_LH,xerr=x_LH_e,yerr=te_LH_e,c='red',label='LH')
ax[1].errorbar(fmt='o',x=x_HL,y=te_HL,xerr=x_HL_e,yerr=te_HL_e,c='blue',label='HL')


#for i, txt in enumerate(LH_shot_list):
#    ax[1].annotate(txt, (x_LH[i], te_LH[i]))
    
#for i, txt in enumerate(HL_shot_list):
#    ax[1].annotate(txt, (x_HL[i], te_HL[i]))

#(res,cov) = np.polyfit(ne_average,te_at_ped,w=1/np.sqrt(np.array(ne_average_e)**2+np.array(te_at_ped)**2),deg=1,cov=True)
#neav = np.linspace(min(ne_average),max(ne_average))
#nefit = res[1] + res[0] * neav
#ax[1].plot(neav,nefit,'--',label=r'fit k={0}$\pm${1} c={2}'.format("{:.2E}".format(res[0]),"{:.2E}".format(cov[0,1]),"{:.2E}".format(res[1])))

#attempt for error calculation
#nefitm = res[1] + (res[0] ) * neav - cov[0,0]
#nefitp = res[1] + (res[0] ) * neav + cov[0,0]
#ax[1].plot(neav,nefitm,color = 'orange',linestyle = 'dashed', alpha = 0.5)
#ax[1].plot(neav,nefitp,color = 'orange',linestyle = 'dashed', alpha = 0.5)
#ax[1].set_ylim([0,455])
#ax[1].set_xlim([0,4e19])
ax[1].set_ylim([0,250])
ax[1].set_xlim([0.27,0.535])

#ax[1].set_xlim([0.438,0.535])
ax[1].set_xlabel('X point height')
ax[1].set_ylabel(r'$Te_{ped}$ $ [eV]$')
ax[1].legend()

# PE
#ax[2].scatter(LH_ne_average,LH_pe_at_ped,c='orange',label='LH')
#ax[2].scatter(HL_ne_average,HL_pe_at_ped,c='blue',label='HL')
#ax[2].errorbar(fmt='o',x=LH_ne_average,y=LH_pe_at_ped,xerr=LH_ne_average_e,yerr=LH_pe_at_ped_e,c='orange',label='LH')
#ax[2].errorbar(fmt='o',x=HL_ne_average,y=HL_pe_at_ped,xerr=HL_ne_average_e,yerr=HL_pe_at_ped_e,c='blue',label='HL')

ax[0].errorbar(fmt='o',x=x_LH,y=pe_LH,xerr=x_LH_e,yerr=pe_LH_e,c='red',label='LH')
ax[0].errorbar(fmt='o',x=x_HL,y=pe_HL,xerr=x_HL_e,yerr=pe_HL_e,c='blue',label='HL')

#for i, txt in enumerate(LH_shot_list):
#    ax[0].annotate(txt, (x_LH[i], pe_LH[i]))
    
#for i, txt in enumerate(HL_shot_list):
#    ax[0].annotate(txt, (x_HL[i], pe_HL[i]))
    

#(res,cov) = np.polyfit(ne_average,pe_at_ped,deg=1,cov=True)
#(res,cov) = np.polyfit(ne_average,pe_at_ped,w=1/np.sqrt(np.array(ne_average_e)**2+np.array(pe_at_ped)**2),deg=1,cov=True)
#neav = np.linspace(min(ne_average),max(ne_average))
#nefit = res[1] + res[0] * neav
#ax[2].plot(neav,nefit,'--',label=r'fit k={0}$\pm${1} c={2}'.format("{:.2E}".format(res[0]),"{:.2E}".format(cov[0,0]),"{:.2E}".format(res[1])))

ax[0].set_xlabel('X point height')
ax[0].set_ylabel(r'$ Ploss   \div \overline{ne}^{0.8} $ $[a.u.]$')
ax[0].legend()


#%%


# JP data

from signal_dict_26_MAY_05 import signals


alpha = 0.8 

shots = [
        
13042,
13043,
13044,
13045,
13047,

14545,
14546,
14547,
14548,
14552,
14554,
14555,

]

shot_com = [
'Shot(13042, LHt=[(0.302,0.300,0.303)], HLt=[(0.393,0.392,0.396)])',
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
'Shot(14555, LHt=[(0.2915,0.291,0.292)], HLt=[(0.3060,0.305,0.3065)])',

]


df = pd.read_excel('ML_data_new.xlsx')

#df = df[~(df['AYC_NE']=='')]
#df = df[~(df['Ploss']<1)]


# shot filter
df = df[df['shot'].isin(shots)]


# Ploss / ne**alpha
# IP

# PLoss
Ploss_LH = np.array( df[(df['transition']=='LH')]['Ploss'])
Ploss_HL = np.array( df[(df['transition']=='HL')]['Ploss'])

Ploss_LH_e = np.array( df[(df['transition']=='LH')]['Ploss_e'])
Ploss_HL_e = np.array( df[(df['transition']=='HL')]['Ploss_e'])


# x1

x1_LH = np.array( df[(df['transition']=='LH')]['X1Z'])
x1_HL = np.array( df[(df['transition']=='HL')]['X1Z'])

x1_LH_e = np.array( df[(df['transition']=='LH')]['X1Z_e'])
x1_HL_e = np.array( df[(df['transition']=='HL')]['X1Z_e'])

# x2

x2_LH = np.array( df[(df['transition']=='LH')]['X2Z'])
x2_HL = np.array( df[(df['transition']=='HL')]['X2Z'])

x2_LH_e = np.array( df[(df['transition']=='LH')]['X2Z_e'])
x2_HL_e = np.array( df[(df['transition']=='HL')]['X2Z_e'])

# shot
shot_LH = np.array( df[(df['transition']=='LH')]['shot'])
shot_HL = np.array( df[(df['transition']=='HL')]['shot'])



db = pd.DataFrame(columns=['shot', 'shot_time', 'time', 'time_em', 'time_ep', 'transition', 'BTOut','BTOut_e','AYC_NE', 'AYC_NE_e'])



for shot_c in shot_com:
    
    
    s=eval(shot_c)

    
    parameters = ['AYC_NE']
    
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
        
        #dic['session'] = session
        #dic['geometry'] = geometry
        
        # Add BTout
        A = 1.3 # mast aspect ratio
        dic['BTOut'] = A/(A+1) * np.interp(t1, s.data['BT']['time'] , s.data['BT']['data'])
        singal_t_err_range =  A/(A+1)*np.interp(np.linspace(t_err1,t_err2,30), s.data['BT']['time'] , s.data['BT']['data'])
        singal_t_err_error_range = np.zeros(30)
        dic['BTOut_e'] = max(singal_t_err_range) - min(singal_t_err_range) + np.mean(np.abs(singal_t_err_error_range))
        
            
        # now load up parameteres
        for parameter in parameters:
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

# ne
ne_LH = np.array( db[(db['transition']=='LH')]['AYC_NE'])
ne_HL = np.array( db[(db['transition']=='HL')]['AYC_NE'])

ne_LH_e = np.array( db[(db['transition']=='LH')]['AYC_NE_e'])
ne_HL_e = np.array( db[(db['transition']=='HL')]['AYC_NE_e'])




ax[0].errorbar(fmt='o',x=x1_LH,y=Ploss_LH/(ne_LH**alpha),xerr=x1_LH_e,yerr=Ploss_LH_e/(ne_LH**alpha),c='black',label='JP SN LH')
ax[0].errorbar(fmt='o',x=x1_HL,y=Ploss_HL/(ne_HL**alpha),xerr=x1_HL_e,yerr=Ploss_HL_e/(ne_HL**alpha),c='green',label='JP SN HL')

#for i, txt in enumerate(LH_shot_list):
#    ax[3].annotate(txt, (x1_LH[i], (Ploss_LH/(ne_LH**alpha))[i]))
    
#for i, txt in enumerate(HL_shot_list):
#    ax[3].annotate(txt, (x1_HL[i], (Ploss_HL/(ne_HL**alpha))[i]))
    

#(res,cov) = np.polyfit(ne_average,pe_at_ped,deg=1,cov=True)
#(res,cov) = np.polyfit(ne_average,pe_at_ped,w=1/np.sqrt(np.array(ne_average_e)**2+np.array(pe_at_ped)**2),deg=1,cov=True)
#neav = np.linspace(min(ne_average),max(ne_average))
#nefit = res[1] + res[0] * neav
#ax[2].plot(neav,nefit,'--',label=r'fit k={0}$\pm${1} c={2}'.format("{:.2E}".format(res[0]),"{:.2E}".format(cov[0,0]),"{:.2E}".format(res[1])))


#textstr = r'JP LH Shots SN'
#ax[3].text(0.45, 1.6e-9, textstr, fontsize=18)

#ax[3].set_title('JP SHOTS PLOSS')
#ax[3].set_xlabel('X point height')
#ax[3].set_ylim([6e-12,2.01e-9])
ax[0].set_ylim([6e-12,2.01e-9])
#ax[3].set_ylabel(r'$JP Ploss   \div \overline{ne}^{0.8} $ $[a.u.]$')
ax[0].legend()




#%%




