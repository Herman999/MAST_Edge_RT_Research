# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 17:02:00 2018

@author: Tomas
"""

import Shot_Class
import matplotlib.pyplot as plt

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