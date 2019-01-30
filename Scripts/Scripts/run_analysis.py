# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 17:02:00 2018

@author: Tomas
"""



import matplotlib.pyplot as plt
from signal_dict_10_NOV_11 import signals

# run shot calss

# This is analysis for session 10_NOV_11
plt.close('all')


shot = Shot(24124


)

#shot = Shot(20381, LHt=[(0.2342,0.2341,0.2343)], HLt=[(0.3108,0.31079,0.31081)])


shot.plot_JP()


#shot.plot_compare(['IP','WMHD','AYC_TE0','ANE_DENSITY','AIT_PTOT_OSP','AIM_DA_TO','Ploss','PINJ' ])

#shot.plot_compare(['IP','WMHD','TE0','NE','Dalphstrp','Dalphint','ngrad','Ploss','PINJ' ])


#%%

shot = Shot(27444, LHt=[(0.254,0.251,0.259)], HLt=[(0.324,0.323,0.325)])





plt.figure()
plt.title(r'I_p vs B_t')

b_t = np.interp(np.linspace(min(shot.data['BT']['time']),max(shot.data['BT']['time']),1000), shot.data['BT']['time'], shot.data['BT']['data'])
i_p = np.interp(np.linspace(min(shot.data['BT']['time']),max(shot.data['BT']['time']),1000), shot.data['IP']['time'], shot.data['IP']['data'])

plt.plot(np.linspace(min(shot.data['BT']['time']),max(shot.data['BT']['time']),1000), i_p/b_t)
plt.show()










"""
test = Shot_Class.Shot(27772)

print( test.signals_present())

test.plot_JP(tlim = (0,1), ip = 'IP', wmhd = 'WMHD', coreTe = 'AYC_TE0', 
                ne = 'ANE_DENSITY', Dalpha = 'AIM_DA_HM', Bt = 'AIM_DA_TO',
                Ploss = 'Ploss', PINJ = 'PINJ', POHM = 'POHM'
                )



# Test of D_ALPHA ISNGALS AVAIALBEL

fig, ax = plt.subplots(5, sharex=True, figsize=(11,7))
fig.subplots_adjust(top=0.935,bottom=0.09,left=0.08,right=0.975,hspace=0.0,wspace=0.2)
fig.suptitle('Shot %s' % (test.ShotNumber))

panel=0
for sig in ['AIM_DA_HM','AIM_DA_TO','ASB_CII','ASB_OII','ASB_SVN_REVISION' ]:
        
    time = test.data[sig]['time']
    data = test.data[sig]['data']
    errors = test.data[sig]['errors'] # may be None, deal with later
    ax[panel].plot(time,data,label=sig)
    ax[panel].legend()
    panel+=1





# add figure title, labels, set time range
fig.suptitle('Shot %s' % (test.ShotNumber))


        

sig = 'AYE_TE'

test.data[sig]['errors']





import matplotlib.pyplot as plt
plt.figure()
plt.errorbar(test.data[sig]['time'],test.data[sig]['data'],yerr=test.data[sig]['errors'])
plt.show()

"""