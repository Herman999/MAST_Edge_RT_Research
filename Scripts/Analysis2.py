# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 11:30:27 2018

@author: rbatt
"""
from signal_dict_10_NOV_11 import signals
from Shot_Class import Shot, Transition
import matplotlib.pyplot as plt

import pandas as pd
print(len(signals))
s = Shot(27444, LHt=[(0.254,0.251,0.259)], HLt=[(0.324,0.323,0.325)])
s1 = Shot(27446, LHt=[(0.115,0.110,0.120)], HLt=[(0.3074,0.307,0.308)])
s2 = Shot(27448, LHt=[(0.110,0.105,0.118)], HLt=[(0.2894,0.2893,0.2895)])
s3 = Shot(27449, LHt=[(0.115,0.110,0.120)], HLt=[(0.301,0.300,0.306)])
s4 = Shot(27450, LHt=[(0.116,0.110,0.118)], HLt=[(0.305,0.303,0.306)])
s5 = Shot(27451, LHt=[(0.2665,0.266,0.267),(0.2847,0.284,0.2855)], HLt=[(0.273,0.2725,0.2735),(0.287,0.287,0.289)])
s6 = Shot(27453, LHt=[(0.295,0.2945,0.2955)], HLt=[(0.3105,0.3099,0.311)])
s7 = Shot(27454, LHt=[(0.277,0.276,0.278)], HLt=[(0.2893,0.289,0.290)])

from signal_dict_06_OCT_11 import signals
s8 = Shot(27035, LHt=[(0.1150,0.1281,0.1017)], HLt = [(0.3096,0.3098,0.3095)])
s9 = Shot(27036, LHt = [(0.1111,0.1212, 0.1014)], HLt = [(0.3261,0.327,0.3260)])
s10 = Shot(27037, LHt=[(0.1089,0.1210,0.1014)], HLt = [(0.3247, 0.3252, 0.3246)])

all_trans = []

for a in [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10]:
    a.transitions_generator()
    all_trans.extend(a._transitions)
    
#%%

plt.figure()
y_mag = 1e6

for t in all_trans:
    xparam = 'AYC_NE'

    try:
        x = t.parameters[xparam]['p_0']
        xerr = t.parameters[xparam]['error']
        y = t.parameters['Ploss']['p_0'] / y_mag
        yerr = t.parameters['Ploss']['error'] / y_mag
        if t.flavour == 'LH':
            c = 'g'
        else: # t.flavour == 'HL'
            c = 'r'
        plt.errorbar(x, y, yerr = yerr, xerr=xerr, color = c)
        plt.annotate(str(t.shot), (x,y))
    except:
        pass
plt.title('AYC_NE Thomson scattering')
plt.xlim(0,)
plt.ylim(0,)
plt.xlabel(r'$n_e \ [m^{-3}]$')
plt.ylabel(r'$P_{loss} \ [MW]$')


plt.figure()
plt.title('ANE_DENSITY interferometry')
for t in all_trans:
    xparam = 'ANE_DENSITY'
    length_factor = 4.0
    try:
        x = t.parameters[xparam]['p_0'] / length_factor
        xerr = t.parameters[xparam]['error'] / length_factor
        y = t.parameters['Ploss']['p_0'] / y_mag
        yerr = t.parameters['Ploss']['error'] / y_mag
        if t.flavour == 'LH':
            c = 'b'
        else: # t.flavour == 'HL'
            c = 'pink'
        plt.errorbar(x, y, yerr = yerr, xerr=xerr, color = c)
        plt.annotate(str(t.shot), (x,y))
    except:
        pass    

plt.xlim(0,)
plt.ylim(0,)
plt.xlabel(r'$n_e \ [m^{-3}]$')
plt.ylabel(r'$P_{loss} \ [MW]$')

#%%
import numpy as np

def convolve_past(sig, time, N):
    sig2 = []
    for i, t in enumerate(time):
        if i < N:
            sig2.append(np.average(sig[:i+1])) # average of signal up to time=t
        else:
            sig2.append(sum(sig[i-N+1:i+1])/N) # average over previous N points
    print('N time steps = ', np.ptp(time[:N]), 's equivalent')
    return np.asarray(sig2)

test = Shot(27039, LHt=[(0.3, 0.25, 0.35)], HLt=[(0.4,0,0)])
test = Shot(27039, HLt = [(0.3307, 0, 0)])


useful = ['AIT_PTOT_ISP', 'AIT_PTOT_OSP']

# Ploss data
time_p, ploss = test.data['Ploss']['time'], test.data['Ploss']['data']/1e6 #now in MW

# Power to the divertor outer/inner strike point (MW)
time_o, osp = test.data['AIT_PTOT_ISP']['time'], test.data['AIT_PTOT_ISP']['data']
time_i, isp = test.data['AIT_PTOT_OSP']['time'], test.data['AIT_PTOT_OSP']['data']

# sum of power to divertor inner and outer strike points
ptot = osp + isp
delayed = convolve_past(ptot, time_o, 51)

fig, ax = plt.subplots(1, figsize = (11,7))

ax.plot(time_p, ploss, label=r'$P_{loss}$')
ax.scatter(time_p, ploss)
ax.plot(time_i, ptot, alpha=0.3, label = r'$P to strike pts$')
N = 100
#ax.plot(time_i, np.convolve(ptot, np.ones((N,))/N, mode='full')[50:-49], label=r'$convolved$')
ax.plot(time_i, delayed, label = r'$my \ convolve$')


ax.set_xlabel(r'$time [s]$')
ax.set_ylabel(r'$Power [MW]$')
ax.legend()

#%%

test = Shot(27039, LHt = [(0.1,0,0)], HLt = [(0.3307, 0, 0)])
test.plot_JP()
test.transitions_generator(additional_params=useful)


#%%

#%% animation of time evolution of d alpha wide angle, partly with example code taken from:
#"""
#Matplotlib Animation Example
#
#author: Jake Vanderplas
#email: vanderplas@astro.washington.edu
#website: http://jakevdp.github.com
#license: BSD
#Please feel free to use and modify this, but keep the above information. Thanks!
#"""
from matplotlib import animation


data = s1.data['ADA_DALPHA_RAW']['data']
time = s1.data['ADA_DALPHA_RAW']['time']
fig = plt.figure()

for profile, t in zip(data, time):
    # First set up the figure, the axis, and the plot element we want to animate
    ax = fig.add_subplot(111)
    ax.set_title('ADA_DALPHA_RAW')
    ax.set_ylabel('D_alpha')
    ax.set_ylim(0,0.8)
    ax.set_xlabel('Radius [a.u.]')
    ax.set_xlim(0,1000)

    # Dalpha data
    d_alpha, = ax.plot([],[], 'x-', lw=0.5)

    # texts in plot
    time_text = ax.text(0.75, 0.9, '', transform=ax.transAxes)
    Hmode_text = ax.text(0.62, 0.1, '', transform=ax.transAxes)

    # initialization function: plot the background of each frame
    def init():
        # Dalpha data
        d_alpha.set_data([], [])
        # texts in plot
        time_text.set_text('')
        Hmode_text.set_text('')
        
        return d_alpha, time_text, Hmode_text # ne_pedestal, Te_pedestal, pe_pedestal, ne_pedestal_fit, Te_pedestal_fit, pe_pedestal_fit, lcfs0, lcfs1, lcfs2, time_text, Hmode_text, ne_resvar_text, Te_resvar_text, pe_resvar_text, LCFS_text,
    
    # animation function.  This is called sequentially
    def animate(j):
        # pedestal data
        R = range(len(data[0]))
        d_alpha.set_data(R, data[j])
  
      # texts in plot
        time_text.set_text('time = %.3fs' %time[j])
        
        return d_alpha, time_text #ne_pedestal, Te_pedestal, pe_pedestal, ne_pedestal_fit, Te_pedestal_fit, pe_pedestal_fit, lcfs0, lcfs1, lcfs2, time_text, Hmode_text, ne_resvar_text, Te_resvar_text, pe_resvar_text, LCFS_text,
    
    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, init_func=init,frames=len(data), interval=100, blit=True)
    
    # save the animation as an mp4.  This requires ffmpeg or mencoder to be
    # installed.  The extra_args ensure that the x264 codec is used, so that
    # the video can be embedded in html5.  You may need to adjust this for
    # your system: for more information, see
    # http://matplotlib.sourceforge.net/api/animation_api.html
    #anim.save('../Plots_and_graphics/ped_evolution_videos/%dpedestal_evolution.mp4'%shot, fps=5, extra_args=['-vcodec', 'libx264'])
#    plt.show()

#%%
    