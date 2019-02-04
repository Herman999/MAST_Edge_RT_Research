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
test = Shot(27039, HLt = [(0.3307, 0, 0)])

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

data= test.data['AYE_NE']['data']
time = test.data['AYE_NE']['time']
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
#comparison of edge and core data

data_core= test.data['AYC_NE']['data']
rad_core = test.data['AYC_R']['data']
data_edge = test.data['AYE_NE']['data']
rad_edge = test.data['AYE_R']['data']
#plt.figure()
i = 12
plt.plot(rad_core[i], data_core[i], 'x-')
plt.plot(rad_edge[i], data_edge[i], 'o-')

#%%

test = Shot(27035, HLt = [(0.3307, 0, 0)])
test = Shot(27037)

# creating fancy plot which will later be animated for time series of [ne, pe, te] and value at (3) radii.

from matplotlib.gridspec import GridSpec
from matplotlib import animation

# =============================================================================
# animator below for data:
data= test.data['AYC_NE']['data']
time = test.data['AYC_NE']['time']
radii = test.data['AYC_R']['data']
#data= test.data['ATS_N_E']['data']
#time = test.data['ATS_TIME']['time']
#radii = test.data['ATS_R']['data']
# =============================================================================

# data for 3 time traces
# define radii for interpolation
phi1 = np.mean(radii.T[6])
phi2 = np.mean(radii.T[9])
phi3 = np.mean(radii.T[12])

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

#%%
    
# mark two
    
test = Shot(27037)

from matplotlib.gridspec import GridSpec
from matplotlib import animation

#core data
data_core= test.data['AYC_NE']['data']
err_core = test.data['AYC_NE']['errors'] # currently unused
rad_core = test.data['AYC_R']['data']
t_core = test.data['AYC_NE']['time']
#edge data
data_edge = test.data['AYE_NE']['data']
err_edge = test.data['AYE_NE']['errors']
rad_edge = test.data['AYE_R']['data']
t_edge = test.data['AYE_NE']['time']

# times should be the same, check here:
print('Times are the same: ', np.array_equal(t_core, t_edge))

# LCFS data
lcfs_r = test.data['LCFS_R_out']['data']
lcfs_t = test.data['LCFS_R_out']['time']

# =============================================================================
# Unused combined into one data set for easier animation (though they still exist independently)
data = np.concatenate((data_core, data_edge), axis=1)
radii = np.concatenate((rad_core, rad_edge), axis=1)
time = t_core
# doing this breaks np.interp so use interp only for one data set
# =============================================================================

# define radii for interpolation
phi1 = np.mean(rad_edge.T[6])
phi2 = np.mean(rad_edge.T[9])
phi3 = np.mean(rad_edge.T[12])
# data for 3 time traces:
phi1_data = [np.interp(phi1, rads, prof) for prof, rads in zip(data_edge, rad_edge)]
phi2_data = [np.interp(phi2, rads, prof) for prof, rads in zip(data_edge, rad_edge)]
phi3_data = [np.interp(phi3, rads, prof) for prof, rads in zip(data_edge, rad_edge)]
# interpolated LCFS position sanity check
data_lcfs = [np.interp(t, lcfs_t, lcfs_r) for t in time] # now lcfs data has same times as ne data


# Set up the figure, the axis, and the plot element we want to animate
fig = plt.figure() #constrained_layout = True)
#create grid space with 3 rows (upper, middle, lower) and 2 columns (left, right)
gs = GridSpec(3, 3, figure=fig)

ax0 = fig.add_subplot(gs[:,:2]) # left column (spans all rows)
ax3 = fig.add_subplot(gs[2,-1]) # lower right 
ax2 = fig.add_subplot(gs[1,-1], sharex = ax3) # middle right
ax1 = fig.add_subplot(gs[0,-1], sharex = ax3) # upper right
# remove x tick labels from upper two subplots
plt.setp(ax2.get_xticklabels(), visible = False)
plt.setp(ax1.get_xticklabels(), visible = False)
# remove space between right column subplots (which share their x axis)
fig.subplots_adjust(hspace = 0)

#for upper y (NE) limits:
ymax = np.nanmax(data_edge)*1.1

# big subplot labels
ax0.set_title('AYC + AYE NE')
ax0.set_ylabel('NE [m^-3]')
ax0.set_ylim(0, ymax)
ax0.set_xlabel('Radius [m]')
ax0.set_xlim(np.nanmin(radii), np.nanmax(radii))

# time series colours
c1, c2, c3 = 'g', 'm', 'b'

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
    #ne_core, = ax0.errorbar([],[],yerr=[], marker='x', lw=0.5, c= 'r')
    ne_core, = ax0.plot([],[], marker='x', lw=0.5, c='r')
    ne_edge, = ax0.plot([],[], 'x', lw=0.5, c= 'k')
    lcfs = ax0.axvline(ls='-.', c='0.5', lw=0.5)
    ne_phi1, = ax1.plot([],[], 'x-', lw=0.5, c=c1)
    ne_phi2, = ax2.plot([],[], 'x-', lw=0.5, c=c2)
    ne_phi3, = ax3.plot([],[], 'x-', lw=0.5, c=c3)
    
    #tanh fits
    tanh_core, = ax0.plot([],[], c='r')
    tanh_edge, = ax0.plot([],[], c='k')
    
    # texts in plot
    time_text = ax0.text(0.75, 0.9, '', transform=ax0.transAxes)
    
    # initialization function: plot the background of each frame
    def init():
        #ne_core.set_data([], [], yerr=[]) # Dalpha data
        ne_core.set_data([],[])
        ne_edge.set_data([],[])
        lcfs.set_xdata(0)
        ne_phi1.set_data([], [])
        ne_phi2.set_data([], [])
        ne_phi3.set_data([], [])
        time_text.set_text('') # texts in plot
        return ne_core, ne_edge, lcfs, ne_phi1, ne_phi2, ne_phi3, time_text
    
    # animation function.  This is called sequentially
    def animate(j):  
        # = radii[j] # pedestal data
        #ne_core.set_data(rad_core[j], data_core[j], yerr=err_core[j]) # pedestal data
        ne_core.set_data(rad_core[j], data_core[j])
        ne_edge.set_data(rad_edge[j], data_edge[j])
        lcfs.set_xdata(data_lcfs[j])
        ne_phi1.set_data(time[:j+1], phi1_data[:j+1])
        ne_phi2.set_data(time[:j+1], phi2_data[:j+1])
        ne_phi3.set_data(time[:j+1], phi3_data[:j+1])
        
        time_text.set_text('time = %.3fs' %time[j])  # texts in plot
        return ne_core, ne_edge, lcfs, ne_phi1, ne_phi2, ne_phi3, time_text
    # These two functions can be moved outside the for profile, t: animate call but for readability, left in
    
    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, init_func=init,frames=len(data), interval=150, blit=True)
 
#%%
# tanh fit. 
# based on work of JP, in particular, his ped_tanh_odr2 function, 
def ped_tanh_odr2(p,x,loc='out'):
    '''Modified tanh for fitting pedestal structures in 
    density/temperature/pressure profiles in tokamak plasmas.
    p - list of parameters (len=7)
    x - xdata (usually major radius or normalized flux )
    loc = 'out'/'in' - defines whether outboard or inboard pedestal is to be fitted'''
    # extract function parameters from p
    a, b, x_sym, width, slope, dwell, x_well = p
#    a=p[0]
#    b=p[1]
#    x_sym=p[2]
#    width=p[3]
#    slope=p[4]
#    dwell=p[5]
#    x_well=p[6]
    if loc == 'out': # fit outboard pedestal 
        x_knee = x_sym - width / 2
        c = dwell / (x_knee - x_well)**2
        # calculate function value:
        y = a*np.tanh(2*(x_sym - x) / width) + b
        try: # handle single value for x
            if x < x_knee:
                y += slope*(x-x_knee) + c*(x-x_well)**2 - dwell
        except ValueError: # handle list or array for x
            for i in range(len(x)):
                if x[i]<x_knee:
                    y[i]+= slope*(x[i]-x_knee) + c*(x[i]-x_well)**2 - dwell
    elif loc == 'in': # fit inboard pedestal 
        x_knee = x_sym + width/2
        c = dwell / (x_knee - x_well)**2
        # calculate function value:
        y = a*np.tanh(2*(x-x_sym)/width) + b
        try: # handle single value for x
            if x>x_knee:
                y+= slope*(x-x_knee) + c*(x-x_well)**2 - dwell
        except ValueError: # handle list or array for x
            for i in range(len(x)): 
                if x[i]>x_knee:
                    y[i]+= slope*(x[i]-x_knee) + c*(x[i]-x_well)**2 - dwell
    else:
        raise ValueError('loc must be "in" for inboard pedestal fit or "out" (default) for outboard pedestal fit.')
    return y

def diff_ped_tanh_odr2(p,x,loc='out'):
    '''Derivative of a modified tanh for fitting pedestal structures in 
    density/temperature/pressure profiles in tokamak plasmas.
    p - list of parameters (len=7)
    x - xdata (usually major radius or normalized flux )
    loc = 'out'/'in' - defines whether outboard or inboard pedestal is to be fitted'''
    # extract function parameter from p
    a=p[0]
    #b=p[1] # not needed in derivative
    x_sym=p[2]
    width=p[3]
    slope=p[4]
    dwell=p[5]
    x_well=p[6]
    if loc=='out': # fit outboard pedestal 
        x_knee=x_sym-width/2
        c=dwell/(x_knee-x_well)**2
        # calculate function value:
        y=-2*a/width/np.cosh(2*(x_sym-x)/width)**2
        try: # handle single value for x
            if x<x_knee:
                y+= 2*c*(x-x_well) + slope
        except ValueError: # handle list or array for x
            for i in range(len(x)):
                if x[i]<x_knee:
                    y[i]+= 2*c*(x[i]-x_well) + slope
    elif loc=='in': # fit inboard pedestal 
        x_knee=x_sym+width/2
        c=dwell/(x_knee-x_well)**2
        # calculate function value:
        y=2*a/width/np.cosh(2*(x-x_sym)/width)**2
        try: # handle single value for x
            if x>x_knee:
                y+= 2*c*(x-x_well) + slope
        except ValueError: # handle list or array for x
            for i in range(len(x)):
                if x[i]>x_knee:
                    y[i]+= 2*c*(x[i]-x_well) + slope
    else:
        raise ValueError('loc must be "in" for inboard pedestal fit or "out" (default) for outboard pedestal fit.')
    return y


#%%
import scipy.odr as odr

# =============================================================================
tanh = odr.Model(ped_tanh_odr2)
# =============================================================================
endi = 30
x,y,yr,xr = [rad_core[50][endi:],data_core[50][endi:],err_core[50][endi:],0.01]
p=[2.5e19,2.5e19,1.38,0.05,1e19,1,1]
mydata = odr.RealData(x,y,sx=xr,sy=yr)
myodr = odr.ODR(mydata,tanh,beta0=p)
myoutput = myodr.run()
plt.figure(44)
plt.plot(x,ped_tanh_odr2(myoutput.beta,x))
plt.errorbar(x,y,yerr=yr,xerr=xr)

def do_odr(data,tanh_model, p=[2.5e19,2.5e19,1.38,0.05,1e19,1.,1.]):
    x,y,ye,xe = data[0],data[1],data[2],data[3]
    data = odr.RealData(x,y,sx=xe,sy=ye)
    myodr = odr.ODR(data,tanh_model, beta0=p)
    output = myodr.run()
    return output.beta

#%%
# a good shot with known LHt
new = Shot(24130, LHt=[(0.285,0,0)])
new2 = Shot(24129)
new3 = Shot(24128, LHt=[(0.258,0,0)])

#%%
# analysis of 24129 where thomson just captures a LHt at 0.292

new3.plot_compare(['WMHD','Ploss','AIM_DA_TO','ANE_DENSITY'])
for x in new3.data['AYE_NE']['time']:
    plt.axvline(x, c='b')
plt.axvline(0.292, c='r')
plt.xlim(0.2,0.4)

#thomson_range is index 64 to 72
i1=64
i2=72
# get edge, core data for ne
core = new2.data['AYC_NE']
core_rad = new2.data['AYC_R']
edge = new2.data['AYE_NE']
edge_rad = new2.data['AYE_R']

rad_e, time_e, ne_e, ne_er_e = edge_rad['data'][i1:i2],edge['time'][i1:i2],edge['data'][i1:i2],edge['errors'][i1:i2]
rad_c, time_c, ne_c, ne_er_c = core_rad['data'][i1:i2],core['time'][i1:i2],core['data'][i1:i2],core['errors'][i1:i2]

tanh = odr.Model(ped_tanh_odr2)
#%%

co = 40
plt.figure()
for i,time in enumerate(time_e[:2]):
    plt.title('time = {}'.format(time))
    
    #must remove nans
    filt = ~np.isnan(ne_c[i][co:])

    fit_c = do_odr([rad_c[i][co:][filt],ne_c[i][co:][filt],ne_er_c[i][co:][filt],0.01], tanh)
    fit_e = do_odr([rad_e[i],ne_e[i],ne_er_e[i],0.01], tanh)
    
    x = rad_c[i][co:]
    plt.plot(x, ped_tanh_odr2(fit_c,x), ls='--')
    x = rad_e[i]
    plt.plot(x, ped_tanh_odr2(fit_e,x), ls='--')
    
    plt.plot(rad_e[i],ne_e[i])
    plt.plot(rad_c[i],ne_c[i])
    
    print(fit_c)

#%%
# work on 31/1/19
# point 2.4: where is tanh fit reliable?
    
def fit_params(result, shot):
    fig,ax = plt.subplots(4, sharex=True)
    fig.canvas.set_window_title('{} tanh fit params'.format(shot.ShotNumber))
    for res in result:
        ax[0].scatter(res, result[res][0], c='k') #scatter knee value
        ax[1].scatter(res, result[res][1], c='r') #plot width
        ax[2].scatter(res, result[res][2], c='b') #plot max slope
        ax[3].scatter(res, result[res][3], c='orange') #plot ne at max slope
    
    plt.title('Tanh fit parameters')
    ax[0].set_title('knee position')
    ax[1].set_title('width')
    ax[2].set_title('max slope')
    ax[3].set_title('ne at max slope')
    
    for axes in ax:
        axes.axvline(ts._LHt[0][0], c='green')
        axes.axvline(ts._HLt[0][0], C='red')
    
    return fig,ax    


# to define signals...
from signal_dict_13_DEC_PULL import signals, shotnos
# a test shot
ts = Shot(24130, LHt=[(0.285,0,0)], HLt=[(0.324,0,0)])
ts2= Shot(27035, LHt=[(0.1150,0.1017,0.1281)], HLt = [(0.3096,0.3096,0.3098)])

#generate shot tanh fit results
result = ts.fit_after_time(0,80, prev=False)
result2= ts2.fit_after_time(0.0,80, prev=False)
#plot results
fig,ax = fit_params(result, ts)
fig2,ax2 = fit_params(result2, ts2)

# =============================================================================
# No easy parameter to use to defin ewhether fit good
# =============================================================================

#%%
# point 2.5

ts = Shot(24130, LHt=[(0.285,0,0)], HLt=[(0.324,0,0)])
ts2= Shot(27035, LHt=[(0.1150,0.1017,0.1281)], HLt = [(0.3096,0.3096,0.3098)])

res_t = ts2.fit_after_time(0.01,129, sig='TE', prev=True)
res_n = ts2.fit_after_time(0.01,129, sig='NE', prev=False)
plt.figure()
plt.title('blue=Te, red=ne')
for i, j in zip(res_t, res_n):
    plt.scatter(i, res_t[i][0], c='b')
    plt.scatter(j, res_n[j][0], c='r')







