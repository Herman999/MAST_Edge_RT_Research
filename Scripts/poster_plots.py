# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 23:40:29 2019

@author: Tomas
"""
import matplotlib.pyplot as plt

# Make JP plot

s = Shot(27454, LHt=[(0.277,0.276,0.278)], HLt=[(0.2893,0.289,0.290)])
s = Shot(27446, LHt=[(0.276,0.274,0.2765)], HLt=[(0.3074,0.307,0.308)])











f = s.plot_JP_report(plot_thomson=4,label_thomson=False)

f[1][0].set_xlim([0,0.328])
f[1][0].set_title('Example LH Transitions #27446')


index = 56
result, time, (x,y) = s.fit_edge_tanh_pedestal(index, sig='NE', preview = True)

index = 71
result, time_, (x_,y_) = s.fit_edge_tanh_pedestal(index, sig='NE', preview = True)

plt.figure()
plt.title(r'27446 L and H Pedestal $N_e$')
plt.plot(x,y,label='L mode')
plt.plot(x_,y_,label='H mode')
plt.legend(loc=1)
plt.xlabel('R [m]')
plt.ylabel(r'$N_e$ [$m^{-3}$]')
plt.ylim(0,)


plt.show()