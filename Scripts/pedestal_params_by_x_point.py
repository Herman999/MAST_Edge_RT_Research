# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 11:03:10 2019

@author: Tomas
"""

# Pedesal params by X point height

import pandas as pd
import numpy as np
#clen
db_ped = pd.read_excel('shot_peddb_only_good_shots.xlsx')
#nasty
#db_ped = pd.read_excel('shot_peddb.xlsx')

db_all = pd.read_excel('ML_data.xlsx')

# I want to add X point height for each
xs = []
xs_e = []
for row in range(len(db_ped)):
    shot = db_ped.iloc[row]['shot']
    transition  = db_ped.iloc[row]['transition']
    
    try:
        xs.append(
            db_all[(db_all['shot']==shot) & (db_all['transition']==transition)]['X1Z'].iloc[0]
            )
    except: xs.append(np.nan)
    
    try:
        xs_e.append(
            db_all[(db_all['shot']==shot) & (db_all['transition']==transition)]['X1Z_e'].iloc[0]
            )
    except: xs_e.append(np.nan)
    
db_ped['X1Z'] = pd.Series(xs)
db_ped['X1Z_e'] = pd.Series(xs_e)
db_ped = db_ped.dropna()

#%%
# plot the stuff

x_LH = list(db_ped[(db_ped['transition']=='LH')]['X1Z'])
x_HL = list(db_ped[(db_ped['transition']=='HL')]['X1Z'])

x_LH_e = list(db_ped[(db_ped['transition']=='LH')]['X1Z_e'])
x_HL_e = list(db_ped[(db_ped['transition']=='HL')]['X1Z_e'])

ne_LH = list(db_ped[(db_ped['transition']=='LH')]['ne_at_ped'])
ne_HL = list(db_ped[(db_ped['transition']=='HL')]['ne_at_ped'])

ne_LH_e = list(db_ped[(db_ped['transition']=='LH')]['ne_at_ped_e'])
ne_HL_e = list(db_ped[(db_ped['transition']=='HL')]['ne_at_ped_e'])

te_LH = list(db_ped[(db_ped['transition']=='LH')]['te_at_ped'])
te_HL = list(db_ped[(db_ped['transition']=='HL')]['te_at_ped'])

te_LH_e = list(db_ped[(db_ped['transition']=='LH')]['te_at_ped_e'])
te_HL_e = list(db_ped[(db_ped['transition']=='HL')]['te_at_ped_e'])

pe_LH = list(db_ped[(db_ped['transition']=='LH')]['pe_at_ped'])
pe_HL = list(db_ped[(db_ped['transition']=='HL')]['pe_at_ped'])

pe_LH_e = list(db_ped[(db_ped['transition']=='LH')]['pe_at_ped_e'])
pe_HL_e = list(db_ped[(db_ped['transition']=='HL')]['pe_at_ped_e'])


# NE            
fig, ax = plt.subplots(3,sharex=True,figsize=(13,9))


textstr = r'$I_p=700$kA $B_t=-0.425$T'
ax[0].text(1.08, 4.5e19, textstr, fontsize=14)
ax[0].text(-1.045, 4.5e19, textstr, fontsize=14)

ax[0].set_title(r'Pedestal Characteristics on X1 point height')
ax[0].errorbar(fmt='o',x=x_LH,y=ne_LH,xerr=x_LH_e,yerr=ne_LH_e,c='red',label='LH')
ax[0].errorbar(fmt='o',x=x_HL,y=ne_HL,xerr=x_HL_e,yerr=ne_HL_e,c='blue',label='HL')
#ax[0].scatter(LH_ne_average,LH_ne_at_ped,c='orange',label='LH')
#ax[0].scatter(HL_ne_average,HL_ne_at_ped,c='blue',label='HL')

"""
for i, txt in enumerate(LH_shot_list):
    ax[0].annotate(txt, (LH_ne_average[i], LH_ne_at_ped[i]))
    
for i, txt in enumerate(HL_shot_list):
    ax[0].annotate(txt, (HL_ne_average[i], HL_ne_at_ped[i]))


# lin fit
(res,cov) = np.polyfit(ne_average,ne_at_ped,deg=1,cov=True)
neav = np.linspace(min(ne_average),max(ne_average))
nefit = res[1] + res[0] * neav
ax[0].plot(neav,nefit,'--',label=r'fit k={0}$\pm${1} c={2}'.format("{:.2E}".format(res[0]),"{:.2E}".format(cov[0,0]),"{:.2E}".format(res[1])))
"""
    
ax[0].set_xlabel('X point height')
ax[0].set_ylabel(r'$Ne_{ped} [m^{-3}]$')
ax[0].legend()
#ax[0].set_ylim([0,0.05e21])

# TE
#ax[1].scatter(LH_ne_average,LH_te_at_ped,c='orange',label='LH')
#ax[1].scatter(HL_ne_average,HL_te_at_ped,c='blue',label='HL')
#ax[1].errorbar(fmt='o',x=LH_ne_average,y=LH_te_at_ped,xerr=LH_ne_average_e,yerr=LH_te_at_ped_e,c='orange',label='LH')
#ax[1].errorbar(fmt='o',x=HL_ne_average,y=HL_te_at_ped,xerr=HL_ne_average_e,yerr=HL_te_at_ped_e,c='blue',label='HL')
ax[1].errorbar(fmt='o',x=x_LH,y=te_LH,xerr=x_LH_e,yerr=te_LH_e,c='red',label='LH')
ax[1].errorbar(fmt='o',x=x_HL,y=te_HL,xerr=x_HL_e,yerr=te_HL_e,c='blue',label='HL')

"""
for i, txt in enumerate(LH_shot_list):
    ax[1].annotate(txt, (LH_ne_average[i], LH_te_at_ped[i]))
    
for i, txt in enumerate(HL_shot_list):
    ax[1].annotate(txt, (HL_ne_average[i], HL_te_at_ped[i]))

(res,cov) = np.polyfit(ne_average,te_at_ped,w=1/np.sqrt(np.array(ne_average_e)**2+np.array(te_at_ped)**2),deg=1,cov=True)
neav = np.linspace(min(ne_average),max(ne_average))
nefit = res[1] + res[0] * neav
ax[1].plot(neav,nefit,'--',label=r'fit k={0}$\pm${1} c={2}'.format("{:.2E}".format(res[0]),"{:.2E}".format(cov[0,1]),"{:.2E}".format(res[1])))

#attempt for error calculation
#nefitm = res[1] + (res[0] ) * neav - cov[0,0]
#nefitp = res[1] + (res[0] ) * neav + cov[0,0]
#ax[1].plot(neav,nefitm,color = 'orange',linestyle = 'dashed', alpha = 0.5)
#ax[1].plot(neav,nefitp,color = 'orange',linestyle = 'dashed', alpha = 0.5)
#ax[1].set_ylim([0,455])
#ax[1].set_xlim([0,4e19])
"""
ax[1].set_xlabel('X point height')
ax[1].set_ylabel(r'$Te_{ped} [eV]$')
ax[1].legend()

# PE
#ax[2].scatter(LH_ne_average,LH_pe_at_ped,c='orange',label='LH')
#ax[2].scatter(HL_ne_average,HL_pe_at_ped,c='blue',label='HL')
#ax[2].errorbar(fmt='o',x=LH_ne_average,y=LH_pe_at_ped,xerr=LH_ne_average_e,yerr=LH_pe_at_ped_e,c='orange',label='LH')
#ax[2].errorbar(fmt='o',x=HL_ne_average,y=HL_pe_at_ped,xerr=HL_ne_average_e,yerr=HL_pe_at_ped_e,c='blue',label='HL')

ax[2].errorbar(fmt='o',x=x_LH,y=pe_LH,xerr=x_LH_e,yerr=pe_LH_e,c='red',label='LH')
ax[2].errorbar(fmt='o',x=x_HL,y=pe_HL,xerr=x_HL_e,yerr=pe_HL_e,c='blue',label='HL')
"""
for i, txt in enumerate(LH_shot_list):
    ax[2].annotate(txt, (LH_ne_average[i], LH_pe_at_ped[i]))
    
for i, txt in enumerate(HL_shot_list):
    ax[2].annotate(txt, (HL_ne_average[i], HL_pe_at_ped[i]))
    

#(res,cov) = np.polyfit(ne_average,pe_at_ped,deg=1,cov=True)
(res,cov) = np.polyfit(ne_average,pe_at_ped,w=1/np.sqrt(np.array(ne_average_e)**2+np.array(pe_at_ped)**2),deg=1,cov=True)
neav = np.linspace(min(ne_average),max(ne_average))
nefit = res[1] + res[0] * neav
ax[2].plot(neav,nefit,'--',label=r'fit k={0}$\pm${1} c={2}'.format("{:.2E}".format(res[0]),"{:.2E}".format(cov[0,0]),"{:.2E}".format(res[1])))
"""
ax[2].set_xlabel('X point height')
ax[2].set_ylabel(r'$Pe_{ped} [a.u.]$')
ax[2].legend()