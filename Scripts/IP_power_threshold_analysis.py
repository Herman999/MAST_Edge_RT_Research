# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 14:49:54 2019

@author: Tomas
"""

from pull_data_2019_IP_new_shots import signals
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


plt.rcParams.update({'font.size': 14})




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

plt.figure(figsize=(13,9))
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

X ='X2Z' 
X_e = 'X2Z_e'


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
fig, ax = plt.subplots(3,sharex=True,figsize=(13,9))


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
ax[1].set_xlim([0.438,0.535])
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





