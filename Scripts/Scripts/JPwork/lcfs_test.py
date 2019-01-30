# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 14:43:53 2018

@author: jb4317
Test programme to figure out LCFS data
"""

import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
from data_access_funcs import load_signal_data,signals
#from helium10JUN09 import tLH,tHL

shotnos=[22650,22653] # 22647,22649,,22653,22656  numbers of shots 
data=[{} for shot in shotnos]
# =============================================================================
# data is a list of shots
# each shot contains a dictionary, where the names of the signals are the keys
# and the keyvalues are again a dictionary of data, errors, time and units
# =============================================================================
notloaded=[] #list of signals that could not be loaded, because the corresponding file does not exist.

#%% load data and write to 'data' (same as in other files)
for i,shot in enumerate(shotnos):
    for sig in signals:
        try:
            filename=str(shot)+'_'+sig+'.p'
            data[i][sig]=load_signal_data(filename) #set data of sig to key sig
        except FileNotFoundError:                   #add sig to notloaded if file can not be loaded (i.e. it does not exist)
            if sig not in notloaded:
                notloaded.append(sig)
# print out confirmation on loaded signals
if not notloaded:
    print('All signals could be loaded.')
else:
    print('Signals that could not be loaded: ',*notloaded)

 
# =============================================================================
# look for LCFS position with signals:
# LCFS_N='EFM_LCFS(N)_(C)', #No. of coords on LCFS (61x1)
# LCFS_R='EFM_LCFS(R)_(C)', #r-coords of seperatrix in m (61x2600)
# LCFS_Z='EFM_LCFS(Z)_(C)', #z-coords of seperatrix in m (61x2600)
# LCFS_L='EFM_LCFS_LENGTH', #length of LCFS in m (61x1)
#
# after some tries:
# LCFS_N gives the number of coordinates of 2600 used for describing the LCFS in LCFS_R and LCFS_Z
# All entries in LCFS_R and LCFS_Z after that are ~1e9, therefore just plotting any of them lookes like a step function.
# Plotting LCFS_R over LCFS_Z (or the other way around) only using the entries up to LCFS_N for each timeslot reproduces the contour of the LCFS
# This has been done in the following cell.
# =============================================================================

#%% plot of LCFS for each timeslot
# (only for first shot, which was chosen arbitrarily as an example):
plt.figure()
for t in range(len(data[0]['LCFS_R']['time'])): 
    plt.plot(data[0]['LCFS_R']['data'][t][:data[0]['LCFS_N']['data'][t]],data[0]['LCFS_Z']['data'][t][:data[0]['LCFS_N']['data'][t]],'x') #plot LCFS_R/Z data up to index given by LCFS_N 
    plt.xlabel('$R$ [m]')
    plt.ylabel('$Z$ [m]')
    plt.title('Time evolution of LCFS of shot %d'%shotnos[0])
plt.axis('equal')
#mark boundary of wall and 5 cm off
plt.axvline(x=0.19625,color='0.5')
plt.axvline(x=0.19625+0.05,linestyle=':',color='0.5')
    
#%% animation of time evolution LCFS

'''Does not work, file missing'''    

tHmode=[[tLH[2],tHL[2]],[tLH[3],tHL[3]]] #exact time interval of H-mode
indHmode=[np.where((data[i]['LCFS_R']['time'] > tHmode[i][0]) &  (data[i]['LCFS_R']['time'] < tHmode[i][1]) )[0] for i in range(len(shotnos))]  #index interval of H-mode

for i,shot in enumerate(shotnos):
    # First set up the figure, the axis, and the plot element we want to animate
    fig=plt.figure()
    ax = plt.axes()
    ax.set_title('Helium experiment shot #%d \n LCFS time evolution' %shot)
    ax.set_xlabel('major radius R [m]')
    ax.set_ylabel('z [m]')
    ax.axis('equal')
    ax.set(xlim=(0.15, 1.5), ylim=(-1.5, 1.5))#
    #mark boundary of wall and 5 cm off
    ax.axvline(x=0.19625,color='0.5')
    ax.axvline(x=0.19625+0.05,linestyle=':',color='0.5')
    lcfs, = ax.plot([], [], 'x-', lw=1)

    
    # set up time stamp (and H-mode stamp)
    time_text = ax.text(0.4, 0.1, '', transform=ax.transAxes)
    Hmode_text = ax.text(0.6, 0.1, '', transform=ax.transAxes)
    # initialization function: plot the background of each frame
    def init():
        lcfs.set_data([], [])
        time_text.set_text('')
        Hmode_text.set_text('')
        return lcfs, time_text, Hmode_text,
    
    # animation function.  This is called sequentially
    def animate(j):
        R = data[i]['LCFS_R']['data'][j][:data[i]['LCFS_N']['data'][j]]
        z = data[i]['LCFS_Z']['data'][j][:data[i]['LCFS_N']['data'][j]]
        lcfs.set_data(R, z)
        time_text.set_text('time = %.3f' %data[i]['LCFS_R']['time'][j])
        if j in indHmode[i]:
            Hmode_text.set(text='H-mode',color='red')
        else:
            Hmode_text.set_text('')
        return lcfs, time_text, Hmode_text,
    
    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=len(data[i]['LCFS_R']['time']), interval=100, blit=True)
    
    # save the animation as an mp4.  This requires ffmpeg or mencoder to be
    # installed.  The extra_args ensure that the x264 codec is used, so that
    # the video can be embedded in html5.  You may need to adjust this for
    # your system: for more information, see
    # http://matplotlib.sourceforge.net/api/animation_api.html
    #anim.save('%dLCFS_evolution.mp4'%shot, fps=5, extra_args=['-vcodec', 'libx264'])
    plt.show()

#%% get LCFS - outboard radius at mid-plane (z=0)
#   compare calculated value to signal given by LCFS_R_out

LCFS_midplane_R=[[] for i in range(len(shotnos))]

for i,shot in enumerate(shotnos):
    for t in range(len(data[i]['LCFS_N']['time'])):
        for j in range(data[i]['LCFS_N']['data'][t]):
            if j!=0 and j!=(data[i]['LCFS_N']['data'][t]-1):
                if data[i]['LCFS_Z']['data'][t][j]==0:
                    #print(j,data[i]['LCFS_R']['data'][t][j])
                    LCFS_midplane_R[i].append(data[i]['LCFS_R']['data'][t][j])

# compare to data from  LCFS_R_out='EFM_R(PSI100)_OUT'
for i,shot in enumerate(shotnos):
    plt.figure()
    plt.title('Outboard radial position of LCFS in midplane, shot #%d'%shot)
    plt.plot(data[i]['LCFS_N']['time'],LCFS_midplane_R[i],'|-')
    plt.plot(data[i]['LCFS_R_out']['time'],data[i]['LCFS_R_out']['data'],'x')
    plt.xlabel('time [s]')
    plt.ylabel('$R_{LCFS,out}$ [m]')
    plt.show()

# =============================================================================
# The outboard radial position of the LCFS in the midplane calculated with the 
# information of the LCFS_N/R/Z data is exactly the same as the signal EFM_R(PSI100)_OUT.
# Therefore for simplicity the signal will be used in any further analysis.
# =============================================================================