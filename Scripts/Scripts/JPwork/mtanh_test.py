# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 15:07:32 2018

@author: jb4317, Jan-Peter Baehner

Programme to test a new modified tanh fcn as a fit to the pedestal in Helium shots of experiment 10JUN09
Shots loaded (including H-mode phases):
    22650
    22652
"""

import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import math
from data_access_funcs import load_signal_data,signals
from power_fit import odr_complete#,curve_complete
#from helium10JUN09 import LHdata,HLdata

shotnos=[22650,22652] # 22647,22649,,22653,22656  numbers of shots 
data=[{} for shot in shotnos]
# =============================================================================
# data is a list of shots
# each shot contains a dictionary, where the names of the signals are the keys
# and the keyvalues are again a dictionary of data, errors, time and units
# =============================================================================
notloaded=[] #list of signals that could not be loaded, because the corresponding file does not exist.

#%% load data and write to 'data'
for i,shot in enumerate(shotnos):
    for sig in signals:
        try:
            filename=str(shot)+'_'+sig+'.p'
            data[i][sig]=load_signal_data(filename) #set data of sig to key sig
        except FileNotFoundError:
            if sig not in notloaded:
                notloaded.append(sig)
# print out confirmation on loaded signals
if not notloaded:
    print('All signals could be loaded.')
else:
    print('Signals that could not be loaded: ',*notloaded)


#%% define modified tanh function for fit on pedestal:
# as proposed by Groebner R.J. et al 1998 Plasma Phys. Control. Fusion 40 673

def ped_tanh_odr(p,x):
    a=p[0]
    b=p[1]
    x_sym=p[2]
    width=p[3]
    slope=p[4]
    x_knee=x_sym-width/2
    y=a*np.tanh(2*(x_sym-x)/width) + b
    try:
        if x<x_knee:
            y+= slope*(x_knee-x)
    except ValueError:
        for i in range(len(x)):
            if x[i]<x_knee:
                y[i]+= slope*(x_knee-x[i])
    return y

def diff_ped_tanh_odr(p,x):
    a=p[0]
    #b=p[1] # not needed in derivative
    x_sym=p[2]
    width=p[3]
    slope=p[4]
    x_knee=x_sym-width/2
    y=-2*a/width/np.cosh(2*(x_sym-x)/width)**2
    try:
        if x<x_knee:
            y-= slope
    except ValueError:
        for i in range(len(x)):
            if x[i]<x_knee:
                y[i]-= slope
    return y

# own definition (including an additional quadratic term):
# with additional quadratic term to account for more complex profiles
# with location specification 'loc' for determining whether an inboard or an outboard pedestal is to be fitted

def ped_tanh_odr2(p,x,loc='out'):
    '''Modified tanh for fitting pedestal structures in 
    density/temperature/pressure profiles in tokamak plasmas.
    p - list of parameters (len=7)
    x - xdata (usually major radius or normalized flux )
    loc = 'out'/'in' - defines whether outboard or inboard pedestal is to be fitted'''
    # extract function parameters from p
    a=p[0]
    b=p[1]
    x_sym=p[2]
    width=p[3]
    slope=p[4]
    dwell=p[5]
    x_well=p[6]
    if loc=='out': # fit outboard pedestal 
        x_knee=x_sym-width/2
        c=dwell/(x_knee-x_well)**2
        # calculate function value:
        y=a*np.tanh(2*(x_sym-x)/width) + b
        try: # handle single value for x
            if x<x_knee:
                y+= slope*(x-x_knee) + c*(x-x_well)**2 - dwell
        except ValueError: # handle list or array for x
            for i in range(len(x)):
                if x[i]<x_knee:
                    y[i]+= slope*(x[i]-x_knee) + c*(x[i]-x_well)**2 - dwell
    elif loc=='in': # fit inboard pedestal 
        x_knee=x_sym+width/2
        c=dwell/(x_knee-x_well)**2
        # calculate function value:
        y=a*np.tanh(2*(x-x_sym)/width) + b
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

#%% fit modified tanh to pedestal in ne, Te and pe measured by the Ruby TS for all shots using odr

# set limits for fitting with both functions individually
xlims=[dict(NE=[1.2,1.45],
            TE=[1.2,1.41],
            PE=[1.2,1.41]) for shot in shotnos]
xlims2=[dict(NE=[0.85,1.45],
            TE=[1.2,1.41],
            PE=[1.2,1.41]) for shot in shotnos]
#xlims=[dict(NE=[1,1.45],
#            TE=[1.2,1.45],
#            PE=[1.2,1.45]) for shot in shotnos]
#xlims2=xlims


# empty lists for saving fit-results:
ne_R_p=[]
Te_R_p=[]
pe_R_p=[]

for i,shot in enumerate(shotnos):
    #density fit:
    ne_data=[data[i]['R12_R']['data'][0],data[i]['R12_R']['errors'][0],data[i]['NE12_R']['data'][0],data[i]['NE12_R']['errors'][0]] # create data for fitting tool
    ne_fit=odr_complete(ne_data,ped_tanh_odr,diff_ped_tanh_odr,[2.5e19,2.5e19,1.387,0.05,1e19], xlimit=xlims2[i]['NE'],title='Helium experiment shot #%d ne edge pedestal odr fit' %shot,xname='major radius [m]',yname='$n_e$ [$10^{19} m^{-3}$]')
    ne_fit=odr_complete(ne_data,ped_tanh_odr2,diff_ped_tanh_odr2,[2.5e19,2.5e19,1.387,0.05,-1e19,1e19,1.1], xlimit=xlims2[i]['NE'],title='Helium experiment shot #%d ne edge pedestal odr fit' %shot,xname='major radius [m]',yname='$n_e$ [$10^{19} m^{-3}$]')
    ne_R_p.append(ne_fit)
    #temperature fit:
    Te_data=[data[i]['R12_R']['data'][0],data[i]['R12_R']['errors'][0],data[i]['TE12_R']['data'][0],data[i]['TE12_R']['errors'][0]] # create data for fitting tool
    Te_fit=odr_complete(Te_data,ped_tanh_odr,diff_ped_tanh_odr,[100,100,1.44,0.05,1000], xlimit=xlims2[i]['TE'],title='Helium experiment shot #%d Te edge pedestal odr fit' %shot,xname='major radius [m]',yname='$T_e$ [eV]')
    Te_fit=odr_complete(Te_data,ped_tanh_odr2,diff_ped_tanh_odr2,[100,100,1.44,0.05,-2.5e3,2.5e2,1.25], xlimit=xlims2[i]['TE'],title='Helium experiment shot #%d Te edge pedestal odr fit' %shot,xname='major radius [m]',yname='$T_e$ [eV]')
    Te_R_p.append(Te_fit)
    #pressure fit:
    pe_data=[data[i]['R12_R']['data'][0],data[i]['R12_R']['errors'][0],data[i]['PE12_R']['data'][0],data[i]['PE12_R']['errors'][0]] # create data for fitting tool
    pe_fit=odr_complete(pe_data,ped_tanh_odr,diff_ped_tanh_odr,[1000,1000,1.38,0.01,10000], xlimit=xlims2[i]['PE'],title='Helium experiment shot #%d pe edge pedestal odr fit' %shot,xname='major radius [m]',yname='$p_e$ [Pa]')
    pe_fit=odr_complete(pe_data,ped_tanh_odr2,diff_ped_tanh_odr2,[1000,1000,1.38,0.01,-1e4,1e3,1.25], xlimit=xlims2[i]['PE'],title='Helium experiment shot #%d pe edge pedestal odr fit' %shot,xname='major radius [m]',yname='$p_e$ [Pa]')
    pe_R_p.append(pe_fit)

#%% time evolution of pedestal for each shot
#short versions of L-H and H-L transition times only for selected shots:
tLH=[0.236,0.233]
txHL=[0.2715,0.284]

# time intervals for each shot
tlims=[[tLH[i]-0.01,txHL[i]+0.01] for i in range(len(shotnos))] # choose time interval around L-H transition
tHmode=[[tLH[i],txHL[i]] for i in range(len(shotnos))] #exact time interval of H-mode
# index intervals for each shot
ind=[np.where((data[i]['NE']['time'] > tlims[i][0]) &  (data[i]['NE']['time'] < tlims[i][1]) )[0] for i in range(len(shotnos))] 
indHmode=[np.where((data[i]['NE']['time'] > tHmode[i][0]) &  (data[i]['NE']['time'] < tHmode[i][1]) )[0] for i in range(len(shotnos))] 

# create new pedestal data with deleting 'nan' values from arrays, since they cannot be handled by fitting routines
pedestal_data=[{} for shot in shotnos]
ped_sigs=['NE','TE','PE']
for i in range(len(shotnos)):
    for sig in ped_sigs:
        sig_data=[] # list for data
        sig_data_err=[] # list for errors on data
        sig_radii=[] # list for corresponding radii
        sig_radii_err=[] # list of errors on radii
        for j in range(len(ind[i])): # loop through time slots of L-H transition
            sigj=list(data[i][sig]['data'][ind[i][j]]) # density profile for time j
            sigj_err=list(data[i][sig]['errors'][ind[i][j]]) # errors of density profile for time j
            Rj=list(data[i]['R2_CTS']['data'][ind[i][j]]) # radii for time j
            Rj_err=list(data[i]['R2_CTS']['errors'][ind[i][j]]) # errors of radii for time j
            nan_indices=[]
            for n in range(len(sigj)): # find 'nan' values
                if math.isnan(sigj[n]):
                    nan_indices.append(n)
            for k in range(len(nan_indices)): # delete 'nan' entries and corresponding positions in R
                del sigj[nan_indices[k]-k]
                del sigj_err[nan_indices[k]-k]
                del Rj[nan_indices[k]-k]
                del Rj_err[nan_indices[k]-k]
            sig_data.append(sigj)
            sig_data_err.append(sigj_err)
            sig_radii.append(Rj)
            sig_radii_err.append(Rj_err)
        #create dictionary for data, radii, errors and time for this sig in this shot:
        sig_dict=dict(data=sig_data,data_errors=sig_data_err,radii=sig_radii,radii_errors=sig_radii_err,time=data[i][sig]['time'][ind[i]])
        pedestal_data[i][sig]=sig_dict
    #add plasma current I_p and toroidal magnetic field B_t:
    Ip_=np.mean(data[i]['IP']['data'][np.where((data[i]['IP']['time'] > tHmode[i][0]) &  (data[i]['IP']['time'] < tHmode[i][1]) )[0]])
    Bt_=np.mean(data[i]['BT']['data'][np.where((data[i]['BT']['time'] > tHmode[i][0]) &  (data[i]['BT']['time'] < tHmode[i][1]) )[0]])
    pedestal_data[i]['IP']=Ip_
    pedestal_data[i]['BT']=Bt_

#%% combine timbases of EFIT LCFS_R_out with timebase of TS
# create new signal in 'data' called 'LCFS_R_out_TStb' which is EFIT info projected on TS timebase
for i in range(len(shotnos)):
    LCFS_R_out_i=[]
    for j in range(len(data[i]['NE']['time'])): #loop through TS timebase
        for k in range(len(data[i]['LCFS_R_out']['time'])): #loop through EFIT timebase and break when time gets larger than current timeslot in TS timebase
            if k!=0 and data[i]['LCFS_R_out']['time'][k]>=data[i]['NE']['time'][j]:
                break 
        # weighted average of values around current TS time:
        LCFS_R_out_ij=(data[i]['LCFS_R_out']['data'][k]*(data[i]['LCFS_R_out']['time'][k]-data[i]['NE']['time'][j]) + data[i]['LCFS_R_out']['data'][k-1]*(data[i]['NE']['time'][j]-data[i]['LCFS_R_out']['time'][k-1])) / (data[i]['LCFS_R_out']['time'][k]-data[i]['LCFS_R_out']['time'][k-1])
        LCFS_R_out_i.append(LCFS_R_out_ij) 
    #add new signal in TS timebase to data
    data[i]['LCFS_R_out_TStb']=dict(data=LCFS_R_out_i,time=data[i]['NE']['time'],errors=None,units=data[i]['LCFS_R_out']['units'])

#%% fit modified tanh to profiles of time interval:

# create initial guess with position of LCFS as guess for x_sym+width
p0=[[dict(NE=[2.5e19,2.5e19,data[i]['LCFS_R_out_TStb']['data'][j]-0.02,0.05,1e19],TE=[1e2,1e2,data[i]['LCFS_R_out_TStb']['data'][j]-0.02,0.05,2.5e3],PE=[1e3,1e3,data[i]['LCFS_R_out_TStb']['data'][j]-0.02,0.05,1e4]) for j in ind[i]] for i in range(len(shotnos))]
p02=[[dict(NE=[2.5e19,2.5e19,data[i]['LCFS_R_out_TStb']['data'][j]-0.02,0.05,-1e19,1e19,1.1],TE=[1e2,1e2,data[i]['LCFS_R_out_TStb']['data'][j]-0.02,0.05,-2.5e3,2.5e2,1.25],PE=[1e3,1e3,data[i]['LCFS_R_out_TStb']['data'][j]-0.02,0.05,-1e4,1e3,1.25]) for j in ind[i]] for i in range(len(shotnos))]

pedestal_fits=[{} for shot in shotnos]
pedestal_fits2=[{} for shot in shotnos]

# fit for all shots, signals and data sets in the time interval respectively with old and new fit function
for i,shot in enumerate(shotnos):
    for sig in ped_sigs:
        # original tanh
        sig_fits=[]
        for j in range(len(ind[i])):
            sig_fit_data=[pedestal_data[i][sig]['radii'][j],pedestal_data[i][sig]['radii_errors'][j],pedestal_data[i][sig]['data'][j],pedestal_data[i][sig]['data_errors'][j]] # create data for fitting tool
            sig_fits.append(odr_complete(sig_fit_data,ped_tanh_odr,diff_ped_tanh_odr,p0[i][j][sig], xlimit=xlims[i][sig],plot=False))#,title='Helium experiment shot #%d \n ne edge pedestal odr fit, t=%.3f s' %(shot,pedestal_data[i][sig]['time'][j]),xname='major radius [m]',yname='$n_e$ [$10^{19} m^{-3}$]'))
        pedestal_fits[i][sig]=sig_fits
        # new tanh
        sig_fits2=[]
        for j in range(len(ind[i])):
            sig_fit_data2=[pedestal_data[i][sig]['radii'][j],pedestal_data[i][sig]['radii_errors'][j],pedestal_data[i][sig]['data'][j],pedestal_data[i][sig]['data_errors'][j]] # create data for fitting tool
            sig_fits2.append(odr_complete(sig_fit_data2,ped_tanh_odr2,diff_ped_tanh_odr2,p02[i][j][sig], xlimit=xlims2[i][sig],plot=False))#,title='Helium experiment shot #%d \n %s edge pedestal odr fit, t=%.3f s' %(shot,sig,pedestal_data[i][sig]['time'][j]),xname='major radius [m]',yname='$n_e$ [$10^{19} m^{-3}$]'))
        pedestal_fits2[i][sig]=sig_fits2
        
#%% Analyse pedestal fits

# plot pedestal fits around L-H transition for each shot
for i,shot in enumerate(shotnos):
    for sig in ped_sigs:
        fig_i=plt.figure()
        for j in range(len(ind[i])):
            x=np.linspace(*xlims2[i][sig],200) # x values evenly distributed over major radius
            plt.plot(x,ped_tanh_odr2(pedestal_fits2[i][sig][j][0],x),label='t=%.3f'%pedestal_data[i][sig]['time'][j])
            plt.xlim(0.8,1.5)
        plt.legend(loc='upper left')
        plt.xlabel('major radius [m]')
        plt.ylabel('%s [%s]'%(sig,data[i][sig]['units']))
        plt.title('Helium experiment shot #%d \n %s edge pedestal profile fits' %(shot,sig))
        plt.annotate('$I_p$= %.1fMA \n$B_t$= %.1fT'%(pedestal_data[i]['IP']/1e3,abs(pedestal_data[i]['BT'])), xy=(0.86,1.03),xycoords='axes fraction',fontsize=10)
        plt.show()

        
#%% animation of time evolution of edge pedestal, partly with example code taken from:
"""
Matplotlib Animation Example

author: Jake Vanderplas
email: vanderplas@astro.washington.edu
website: http://jakevdp.github.com
license: BSD
Please feel free to use and modify this, but keep the above information. Thanks!
"""
for i,shot in enumerate(shotnos):
    # First set up the figure, the axis, and the plot element we want to animate
    fig2,ax2 = plt.subplots(3,sharex=True)
    fig2.subplots_adjust(hspace=0)
    ax2[0].set(title='Helium experiment shot #%d \n edge pedestal profile evolution' %shot,xlim=(0.3, 1.5), ylim=(0, 6.5))
    ax2[0].annotate('$I_p$= %.1fMA \n$B_t$= %.1fT'%(pedestal_data[i]['IP']/1e3,abs(pedestal_data[i]['BT'])), xy=(0.86,1.04),xycoords='axes fraction',fontsize=10)
    ax2[0].annotate('$n_{e}$ [$10^{19}$m$^{-3}$]', xy=(0.02,0.85),xycoords='axes fraction',fontsize=9)
    ax2[1].annotate('$T_{e}$ [k%s]'%data[i]['TE']['units'], xy=(0.02,0.85),xycoords='axes fraction',fontsize=9)
    ax2[1].set(ylim=(0, 1.5))
    ax2[2].annotate('$p_{e}$ [k%s]'%data[i]['PE']['units'], xy=(0.02,0.85),xycoords='axes fraction',fontsize=9)
    ax2[2].set(xlabel='major radius [m]', ylim=(0, 15))
    #old tanh
    ne_pedestal, = ax2[0].plot([], [], 'x', lw=1)
    ne_pedestal_fit, = ax2[0].plot([], [], lw=1)
    Te_pedestal, = ax2[1].plot([], [], 'x', lw=1)
    Te_pedestal_fit, = ax2[1].plot([], [], lw=1)
    pe_pedestal, = ax2[2].plot([], [], 'x', lw=1)
    pe_pedestal_fit, = ax2[2].plot([], [], lw=1)
    #new tanh
    ne_pedestal_fit2, = ax2[0].plot([], [], lw=1)
    Te_pedestal_fit2, = ax2[1].plot([], [], lw=1)
    pe_pedestal_fit2, = ax2[2].plot([], [], lw=1)
    # vline for LCFS
    lcfs0 = ax2[0].axvline(c='0.5', lw=1, ls='--')
    lcfs1 = ax2[1].axvline(c='0.5', lw=1, ls='--')
    lcfs2 = ax2[2].axvline(c='0.5', lw=1, ls='--')
    # set up time stamp, H-mode stamp and LCFS annotation
    time_text = ax2[1].text(0.4, 0.1, '', transform=ax2[1].transAxes)
    Hmode_text = ax2[1].text(0.6, 0.1, '', transform=ax2[1].transAxes)
    LCFS_text = ax2[2].text(0.6, 11, 'LCFS', color='0.5',rotation=90)#, transform=ax2[2].transAxes)
    
    # initialization function: plot the background of each frame
    def init():
        ne_pedestal.set_data([], [])
        ne_pedestal_fit.set_data([],[])
        Te_pedestal.set_data([], [])
        Te_pedestal_fit.set_data([],[])
        pe_pedestal.set_data([], [])
        pe_pedestal_fit.set_data([],[])
        #new tanh
        ne_pedestal_fit2.set_data([],[])
        Te_pedestal_fit2.set_data([],[])
        pe_pedestal_fit2.set_data([],[])
        # vline for LCFS
        lcfs0.set_xdata(0)
        lcfs1.set_xdata(0)
        lcfs2.set_xdata(0)
        # texts in plot
        time_text.set_text('')
        Hmode_text.set_text('')
        LCFS_text.set_x(0)
        return ne_pedestal, Te_pedestal, pe_pedestal, ne_pedestal_fit, Te_pedestal_fit, pe_pedestal_fit, ne_pedestal_fit2, Te_pedestal_fit2, pe_pedestal_fit2, lcfs0, lcfs1, lcfs2, time_text, Hmode_text, LCFS_text,
    
    # animation function.  This is called sequentially
    def animate(j):
        # set pedestal data plots
        x = data[i]['R2_CTS']['data'][j]
        ne_pedestal.set_data(x, data[i]['NE']['data'][j]/1e19)
        Te_pedestal.set_data(x, data[i]['TE']['data'][j]/1e3)
        pe_pedestal.set_data(x, data[i]['PE']['data'][j]/1e3)
        # time stamp and H-mode stamp
        time_text.set_text('time = %.3f' %data[i]['NE']['time'][j])
        if j in indHmode[i]:
            Hmode_text.set(text='H-mode',color='red')
        else:
            Hmode_text.set_text('')
        # set pedestal fit plots
        if j in ind[i]:
            ne_x_fit=np.linspace(*xlims[i]['NE'],200)
            ne_pedestal_fit.set_data(ne_x_fit, ped_tanh_odr(pedestal_fits[i]['NE'][j-ind[i][0]][0],ne_x_fit)/1e19)
            Te_x_fit=np.linspace(*xlims[i]['TE'],200)
            Te_pedestal_fit.set_data(Te_x_fit, ped_tanh_odr(pedestal_fits[i]['TE'][j-ind[i][0]][0],Te_x_fit)/1e3)
            pe_x_fit=np.linspace(*xlims[i]['PE'],200)
            pe_pedestal_fit.set_data(pe_x_fit, ped_tanh_odr(pedestal_fits[i]['PE'][j-ind[i][0]][0],pe_x_fit)/1e3)
            #new tanh
            ne_x_fit=np.linspace(*xlims2[i]['NE'],200)
            ne_pedestal_fit2.set_data(ne_x_fit, ped_tanh_odr2(pedestal_fits2[i]['NE'][j-ind[i][0]][0],ne_x_fit)/1e19)
            Te_x_fit=np.linspace(*xlims2[i]['TE'],200)
            Te_pedestal_fit2.set_data(Te_x_fit, ped_tanh_odr2(pedestal_fits2[i]['TE'][j-ind[i][0]][0],Te_x_fit)/1e3)
            pe_x_fit=np.linspace(*xlims2[i]['PE'],200)
            pe_pedestal_fit2.set_data(pe_x_fit, ped_tanh_odr2(pedestal_fits2[i]['PE'][j-ind[i][0]][0],pe_x_fit)/1e3)
        else:
            ne_pedestal_fit.set_data([],[])
            Te_pedestal_fit.set_data([],[])
            pe_pedestal_fit.set_data([],[])
            ne_pedestal_fit2.set_data([],[])
            Te_pedestal_fit2.set_data([],[])
            pe_pedestal_fit2.set_data([],[])
        # set vline for LCFS and text
        lcfs0.set_xdata(data[i]['LCFS_R_out_TStb']['data'][j])
        lcfs1.set_xdata(data[i]['LCFS_R_out_TStb']['data'][j])
        lcfs2.set_xdata(data[i]['LCFS_R_out_TStb']['data'][j])
        LCFS_text.set_x(data[i]['LCFS_R_out_TStb']['data'][j]-0.04)
        return ne_pedestal, Te_pedestal, pe_pedestal, ne_pedestal_fit, Te_pedestal_fit, pe_pedestal_fit, ne_pedestal_fit2, Te_pedestal_fit2, pe_pedestal_fit2, lcfs0, lcfs1, lcfs2, time_text, Hmode_text, LCFS_text,
    
    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig2, animate, init_func=init,
                                   frames=len(data[i]['R2_CTS']['time']), interval=100, blit=True)
    
    # save the animation as an mp4.  This requires ffmpeg or mencoder to be
    # installed.  The extra_args ensure that the x264 codec is used, so that
    # the video can be embedded in html5.  You may need to adjust this for
    # your system: for more information, see
    # http://matplotlib.sourceforge.net/api/animation_api.html
    #anim.save('%dpedestal_evolution_test.mp4'%shot, fps=5, extra_args=['-vcodec', 'libx264'])
    plt.show()

