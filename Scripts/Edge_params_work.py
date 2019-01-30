# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 12:26:47 2018

@author: rbatt

Edge parameter Analysis
"""

#%%
from Shot_Class import Shot, Transition
from signal_dict_10_NOV_11 import signals
import matplotlib.pyplot as plt
import numpy as np

# test shot
#test = Shot(27450, LHt=[(0.116,0.110,0.118)], HLt=[(0.305,0.303,0.306)])
#test = Shot(27039, HLt = [(0.3307, 0, 0)])
#test = Shot(20379, LHt=[(0.2805,0.28049,0.28051)], HLt=[(0.314,0.308,0.3141)])
test = Shot(27787)

test.plot_JP(tlim=(0,0.4))

#%%

# Edge parameters that are relevant

edge_param = ['AYE_NE', 'AYE_PE', 'AYE_TE', 'AYE_R', 'AYE_TIME']

# data is of form (80, 16) except for _TIME which is (80,). Check with next two lines

#for param in edge_param:
#    print(test.data[param]['data'].shape)

#%%

#check AYE_R format

times = test.data['AYE_TIME']['data']
first_r = test.data['AYE_R']['data'].T[0]

#plt.scatter(times, first_r)
plt.figure()
plt.plot(times, first_r, 'x-')

plt.figure()
plt.plot(range(len(times)), times, 'x-')
plt.xlabel('index')
plt.ylabel('time')
# step function looking -> short bursts of measurements (eg shot 27450)

#%%

#annimate edge params

from matplotlib import animation

# for NE only below

data= test.data['AYE_PE']['data']
time = test.data['AYE_PE']['time']
radii = test.data['AYE_R']['data']

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('AYC_NE')
ax.set_ylabel('NE [m^-3]')
ax.set_ylim(0, np.nanmax(data)*1.1)
ax.set_xlabel('Radius [m]')
ax.set_xlim(1.29,1.5)

for profile, t in zip(data, time):
    # Dalpha data
    ne_profile, = ax.plot([],[], 'x-', lw=0.5)
    # texts in plot
    time_text = ax.text(0.75, 0.9, '', transform=ax.transAxes)

    # initialization function: plot the background of each frame
    def init():
        # Dalpha data
        ne_profile.set_data([], [])
        # texts in plot
        time_text.set_text('')
        
        return ne_profile, time_text
    
    # animation function.  This is called sequentially
    def animate(j):
        # pedestal data
        rad = radii[j]
        ne_profile.set_data(rad, data[j])
        # texts in plot
        time_text.set_text('time = %.3fs' %time[j])
        
        return ne_profile, time_text
    
    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, init_func=init,frames=len(data), interval=100, blit=True)
    
    # save the animation as an mp4.  This requires ffmpeg or mencoder to be
    # installed.  The extra_args ensure that the x264 codec is used, so that
    # the video can be embedded in html5.  You may need to adjust this for
    # your system: for more information, see
    # http://matplotlib.sourceforge.net/api/animation_api.html
    #anim.save('../Plots_and_graphics/ped_evolution_videos/%dpedestal_evolution.mp4'%shot, fps=5, extra_args=['-vcodec', 'libx264'])

#%%
    
data_ne = test.data['AYE_NE']['data']
data_pe = test.data['AYE_PE']['data']
data_te = test.data['AYE_TE']['data']
time = test.data['AYE_TIME']['data']
radii = test.data['AYE_R']['data']

fig, axs = plt.subplots(3, 2, sharex = True)
fig.subplots_adjust(hspace = 0)

axs[0][0].plot(np.ones(15))
axs[0][1].plot(np.ones(15)*2)
axs[2][1].plot(np.ones(15)*3)

#%%

test = Shot(27035, HLt = [(0.3307, 0, 0)])
test = Shot(27037)

# creating fancy plot which will later be animated for time series of [ne, pe, te] and value at (3) radii.

from matplotlib.gridspec import GridSpec

# =============================================================================
# animator below for data:
data= test.data['AYE_NE']['data']
time = test.data['AYE_NE']['time']
radii = test.data['AYE_R']['data']
# =============================================================================

# data for 3 time traces
# define radii for interpolation
phi1 = np.mean(radii.T[8])
phi2 = np.mean(radii.T[9])
phi3 = np.mean(radii.T[10])

phi1_data = [np.interp(phi1, rads, prof) for prof, rads in zip(data, radii)]
phi2_data = [np.interp(phi2, rads, prof) for prof, rads in zip(data, radii)]
phi3_data = [np.interp(phi3, rads, prof) for prof, rads in zip(data, radii)]
 
   # old test data. Works but just takes data at given index, so at varying r
    #phi1_data = data.T[8]
    #phi2_data = data.T[9]
    #phi3_data = data.T[10]

# Set up the figure, the axis, and the plot element we want to animate
fig = plt.figure() #constrained_layout = True)
#create grid space with 3 rows (upper, middle, lower) and 2 columns (left, right)
gs = GridSpec(3, 2, figure=fig)

ax0 = fig.add_subplot(gs[:,0]) # left column (spans all rows)
ax3 = fig.add_subplot(gs[2,-1]) # lower right 
ax2 = fig.add_subplot(gs[1,-1], sharex = ax3) # middle right
ax1 = fig.add_subplot(gs[0,-1], sharex = ax3) # upper right
# remove x tick labels from upper two subplots
plt.setp(ax2.get_xticklabels(), visible = False)
plt.setp(ax1.get_xticklabels(), visible = False)
# remove space between right column subplots (which share their x axis)
fig.subplots_adjust(hspace = 0)

#for upper y limits:
ymax = np.nanmax(data)*1.1

# big subplot labels
ax0.set_title('AYC_NE')
ax0.set_ylabel('NE [m^-3]')
ax0.set_ylim(0, ymax)
ax0.set_xlabel('Radius [m]')
ax0.set_xlim(np.nanmin(radii), np.nanmax(radii))

# time series colours
c1 = 'g'
c2 = 'm'
c3 = 'b'
# time series labels
ax2.set_ylabel('NE [m^-3]')
ax3.set_xlabel('time [s]')
ax3.set_xlim(0, max(time))
ax3.set_ylim(0, ymax)
ax2.set_ylim(0, ymax)
ax1.set_ylim(0, ymax)
ax0.axvline(phi1, ls='--', lw=0.5, c=c1)
ax0.axvline(phi2, ls='--', lw=0.5, c=c2)
ax0.axvline(phi3, ls='--', lw=0.5, c=c3)
ax1.text(0.1,0.9, '{}'.format(phi1), transform = ax1.transAxes)
ax2.text(0.1,0.9, '{}'.format(phi2), transform = ax2.transAxes)
ax3.text(0.1,0.9, '{}'.format(phi3), transform = ax3.transAxes)
# time series plot lightly
ax1.plot(time, phi1_data, lw=0.2, c=c1)
ax2.plot(time, phi2_data, lw=0.2, c=c2)
ax3.plot(time, phi3_data, lw=0.2, c=c3)

for profile, t, radius in zip(data, time, radii):
    # Dalpha data
    ne_profile, = ax0.plot([],[], 'x-', lw=0.5, c='k')
    ne_phi1, = ax1.plot([],[], 'x-', lw=0.5, c=c1)
    ne_phi2, = ax2.plot([],[], 'x-', lw=0.5, c=c2)
    ne_phi3, = ax3.plot([],[], 'x-', lw=0.5, c=c3)
    # texts in plot
    time_text = ax0.text(0.75, 0.9, '', transform=ax0.transAxes)
    
    # initialization function: plot the background of each frame
    def init():
        ne_profile.set_data([], []) # Dalpha data
        ne_phi1.set_data([], [])
        ne_phi2.set_data([], [])
        ne_phi3.set_data([], [])
        time_text.set_text('') # texts in plot
        return ne_profile, ne_phi1, ne_phi2, ne_phi3, time_text
    
    # animation function.  This is called sequentially
    def animate(j):  
        rad = radii[j] # pedestal data
        ne_profile.set_data(rad, data[j]) # pedestal data
        ne_phi1.set_data(time[:j+1], phi1_data[:j+1])
        ne_phi2.set_data(time[:j+1], phi2_data[:j+1])
        ne_phi3.set_data(time[:j+1], phi3_data[:j+1])
        
        time_text.set_text('time = %.3fs' %time[j])  # texts in plot
        return ne_profile, ne_phi1, ne_phi2, ne_phi3, time_text
    # These two functions can be moved outside the for profile, t: animate call but for readability, left in
    
    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, init_func=init,frames=len(data), interval=100, blit=True)
