# -*- coding: utf-8 -*-
"""

Created on Mo Aug 06 2018

@author: jb4317, Jan-Peter Baehner

Programme to analyse the pedestal of shots of X-point height variation studies.
Shots loaded (including H-mode phases):
         13042, 13043, 13044, 13045, 13046, 13047,                     26MAY05 (6)
         13704, 13705, 13706, 13707, 13708, 13709, 13710, 13711,       10AUG05 (8)
         14545, 14546, 14547, 14548, 14552, 14554, 14555,              08NOV05 (7)
         (23822, 23824, 23825, 23826, 23827, 23832, 
         23835, 23837, 23841, 23842, 23843, 23844                      09DEC09 (12))
Shots from 09DEC09 have separate Core TS and Edge TS data - had to be combined in special programme.
All other shots are missing the R2_CTS signal, i.e. the time resolved radial positions - use static R_CTS instead.

With new pedestal fitfunction
"""

import pickle
import numpy as np
import math
from power_fit import odr_complete
#import matplotlib.pyplot as plt
# import data from sessions
from Xpoint_shots import shotnos,data,tLH,tHL,LHdata,HLdata

# select only one session
#shotnos=shotnos[14:]
#data=data[14:]
#tLH=tLH[14:]
#tHL=tHL[14:]
#LHdata=LHdata[14:]
#HLdata=HLdata[14:]
#%% define modified tanh function for fit on pedestal:
# new tanh definition:
# based on definition proposed by Groebner R.J. et al 1998 Plasma Phys. Control. Fusion 40 673
# with additional quadratic term to account for more complex profiles
# with location specification 'loc' for determining whether an inboard or an outboard pedestal is to be fitted

def ped_tanh_odr2(p,x,loc='out'):
    '''Modified tanh for fitting pedestal structures in 
    density/temperature/pressure profiles in tokamak plasmas.
    p - list of parameters (len=7)
    x - xdata (usually major radius or normalized flux )
    loc = 'out'/'in' - defines whether outboard or inboard pedestal is to be fitted'''
    # extract function parameters from p
    a=p[0] # >0
    b=p[1] # a+b>0
    x_sym=p[2] # in [0.2,0.8] for inboard or in [0.8,1.5] for outboard in m (range of major radius in plasma)
    width=p[3] # in [0.001,0.5] in m
    slope=p[4] # no constraint
    dwell=p[5] # no constraint
    x_well=p[6] # same as x_sym
    
    # handle constraints 
    if width<1e-3 or width>0.5 or a<0 or a+b<0:
        try:
            return np.ones(len(x))*1e200
        except TypeError:
            return 1e200
    
    if loc=='out': # fit outboard pedestal 
        # handle constraints 
        if x_sym<0.8 or x_sym>1.5 or x_well<0.8 or x_well>1.5:
            try:
                return np.ones(len(x))*1e200
            except TypeError:
                return 1e200
        #calculate parameters specific to outboard pedestal
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
        # handle constraints 
        if x_sym<0.2 or x_sym>0.8 or x_well<0.2 or x_well>0.8:
            try:
                return np.ones(len(x))*1e200
            except TypeError:
                return 1e200
        #calculate parameters specific to inboard pedestal
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

#%% combine timbases of EFIT LCFS_R_out with timebase of TS - only used for animation
# create new signal in 'data' called 'LCFS_R_out_TStb' which is EFIT info projected on TS timebase
# similar for ruby TS but with inboard LCFS
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
    
    # Ruby TS time
    t_RTS=data[i]['NE12_R']['time'][0]
    for k in range(len(data[i]['LCFS_R_out']['time'])): #loop through EFIT timebase and break when time gets larger than current timeslot in TS timebase
        #assuming timebase of LCFS_R_out and LCFS_R_in is the same
        if k!=0 and data[i]['LCFS_R_out']['time'][k]>=t_RTS:
            break 
    # weighted average of values around current TS time:
    LCFS_R_out_RTS=(data[i]['LCFS_R_out']['data'][k]*(data[i]['LCFS_R_out']['time'][k]-t_RTS) + data[i]['LCFS_R_out']['data'][k-1]*(t_RTS-data[i]['LCFS_R_out']['time'][k-1])) / (data[i]['LCFS_R_out']['time'][k]-data[i]['LCFS_R_out']['time'][k-1])
    LCFS_R_in_RTS=(data[i]['LCFS_R_in']['data'][k]*(data[i]['LCFS_R_in']['time'][k]-t_RTS) + data[i]['LCFS_R_in']['data'][k-1]*(t_RTS-data[i]['LCFS_R_in']['time'][k-1])) / (data[i]['LCFS_R_in']['time'][k]-data[i]['LCFS_R_in']['time'][k-1])
    #add new signals to data
    data[i]['LCFS_R_out_RTS']=dict(data=LCFS_R_out_RTS,time=data[i]['NE']['time'],errors=None,units=data[i]['LCFS_R_out']['units'])
    data[i]['LCFS_R_in_RTS']=dict(data=LCFS_R_in_RTS,time=data[i]['NE']['time'],errors=None,units=data[i]['LCFS_R_in']['units'])
    

#%% fit modified tanh to pedestal in ne, Te and pe measured by the Ruby TS for all shots using odr

# set limits for fitting in- and outboard
xlims_out=[dict(NE=[1,1.45],
            TE=[1.2,1.45],
            PE=[1.2,1.45]) for shot in shotnos]
xlims_in=[dict(NE=[0.2,0.6],
            TE=[0.2,0.6],
            PE=[0.2,0.6]) for shot in shotnos]

#set initial guess of form p=[ a, b, x_sym, width, slope, dwell, x_well]
#outboard pedestal
p0out=[dict(NE=[2.5e19,2.5e19,data[i]['LCFS_R_out_RTS']['data'],0.05,-1e19,1e19,1.1],
        TE=[1e2,1e2,data[i]['LCFS_R_out_RTS']['data'],0.05,-1e4,2.5e2,1.25],
        PE=[1e3,1e3,data[i]['LCFS_R_out_RTS']['data'],0.05,-1e5,1e3,1.25]) for i in range(len(shotnos))]
#inboard pedestal
p0in=[dict(NE=[2e19,2e19,data[i]['LCFS_R_in_RTS']['data'],0.05,1e19,1e19,0.5],
        TE=[1e2,1e2,data[i]['LCFS_R_in_RTS']['data'],0.05,1e4,2.5e2,0.5],
        PE=[5e2,5e2,data[i]['LCFS_R_in_RTS']['data'],0.05,1e5,1e3,0.5]) for i in range(len(shotnos))]
# empty lists for saving fit-results:
ne_R_p=[]
Te_R_p=[]
pe_R_p=[]
rubyshots=[]

for i,shot in enumerate(shotnos):
    if data[i]['NE12_R']['time'][0]>tLH[i] and data[i]['NE12_R']['time'][0]<tHL[i]:
        rubyshots.append(shot)
        #density fit:
        ne_data=[data[i]['R12_R']['data'][0],data[i]['R12_R']['errors'][0],data[i]['NE12_R']['data'][0],data[i]['NE12_R']['errors'][0]] # create data for fitting tool
        ne_fit_out=odr_complete(ne_data,ped_tanh_odr2,diff_ped_tanh_odr2,p0out[i]['NE'], xlimit=xlims_out[i]['NE'],plot=False)#,title='Helium experiment shot #%d ne edge pedestal odr fit' %shot,xname='major radius [m]',yname='$n_e$ [$10^{19} m^{-3}$]')#
        ne_fit_in=odr_complete(ne_data,lambda p,x: ped_tanh_odr2(p,x,'in'),lambda p,x: diff_ped_tanh_odr2(p,x,'in'),p0in[i]['NE'], xlimit=xlims_in[i]['NE'],plot=False)#,title='Helium experiment shot #%d ne edge pedestal odr fit' %shot,xname='major radius [m]',yname='$n_e$ [$10^{19} m^{-3}$]')#
        ne_R_p.append(dict(outboard=ne_fit_out,inboard=ne_fit_in))
        #temperature fit:
        Te_data=[data[i]['R12_R']['data'][0],data[i]['R12_R']['errors'][0],data[i]['TE12_R']['data'][0],data[i]['TE12_R']['errors'][0]] # create data for fitting tool
        Te_fit_out=odr_complete(Te_data,ped_tanh_odr2,diff_ped_tanh_odr2,p0out[i]['TE'], xlimit=xlims_out[i]['TE'],plot=False)#,title='Helium experiment shot #%d Te edge pedestal odr fit' %shot,xname='major radius [m]',yname='$T_e$ [eV]')#
        Te_fit_in=odr_complete(Te_data,lambda p,x: ped_tanh_odr2(p,x,'in'),lambda p,x: diff_ped_tanh_odr2(p,x,'in'),p0in[i]['TE'], xlimit=xlims_in[i]['TE'],plot=False)#,title='Helium experiment shot #%d Te edge pedestal odr fit' %shot,xname='major radius [m]',yname='$T_e$ [eV]')#
        Te_R_p.append(dict(outboard=Te_fit_out,inboard=Te_fit_in))
        #pressure fit:
        pe_data=[data[i]['R12_R']['data'][0],data[i]['R12_R']['errors'][0],data[i]['PE12_R']['data'][0],data[i]['PE12_R']['errors'][0]] # create data for fitting tool
        pe_fit_out=odr_complete(pe_data,ped_tanh_odr2,diff_ped_tanh_odr2,p0out[i]['PE'], xlimit=xlims_out[i]['PE'],plot=False)#,title='Helium experiment shot #%d pe edge pedestal odr fit' %shot,xname='major radius [m]',yname='$p_e$ [Pa]')#
        pe_fit_in=odr_complete(pe_data,lambda p,x: ped_tanh_odr2(p,x,'in'),lambda p,x: diff_ped_tanh_odr2(p,x,'in'),p0in[i]['PE'], xlimit=xlims_in[i]['PE'],plot=False)#,title='Helium experiment shot #%d pe edge pedestal odr fit' %shot,xname='major radius [m]',yname='$p_e$ [Pa]')#
        pe_R_p.append(dict(outboard=pe_fit_out,inboard=pe_fit_in))


#%% time evolution of pedestal for each shot

# time intervals for each shot   
tlims=[[tLH[i]-0.01,tHL[i]+0.01] for i in range(len(shotnos))] # choose time interval around L-H transition - the TS time resolution is 4 ms, so this will produce 2 additional indices in ind before and after the L-H and H-L transition respectively 
tHmode=[[tLH[i],tHL[i]] for i in range(len(shotnos))] #exact time interval of H-mode
# index intervals for each shot
ind=[np.where((data[i]['NE']['time'] > tlims[i][0]) &  (data[i]['NE']['time'] < tlims[i][1]) )[0] for i in range(len(shotnos))] 
indHmode=[np.where((data[i]['NE']['time'] > tHmode[i][0]) &  (data[i]['NE']['time'] < tHmode[i][1]) )[0] for i in range(len(shotnos))]  # indices of data points INSIDE of H-mode

# create new pedestal data with deleting 'nan' values from arrays, since they cannot be handled by fitting routines
pedestal_data=[{} for shot in shotnos]
ped_sigs=['NE','TE','PE']
for i in [14,15,16,17,18,19,20]: #only for 08NOV05 #range(len(shotnos)):
    for sig in ped_sigs:
        sig_data=[] # list for data
        sig_data_err=[] # list for errors on data
        sig_radii=[] # list for corresponding radii
        sig_radii_err=[] # list of errors on radii
        for j in range(len(ind[i])): # loop through time slots of L-H transition
            sigj=list(data[i][sig]['data'][ind[i][j]]) # density profile for time j
            sigj_err=list(data[i][sig]['errors'][ind[i][j]]) # errors of density profile for time j
            # only R_CTS is availabe for these shots (see comment in file description)
            Rj=list(data[i]['R_CTS']['data'][0]) # radii for time j
            Rj_err=list(data[i]['R_CTS']['errors'][0]) # error of radii for time j
            nan_indices=[]
            for n in range(len(sigj)): # find 'nan' values
                if math.isnan(sigj[n]):
                    nan_indices.append(n)
            for k in range(len(nan_indices)): # delete 'nan' entries and corresponding positions in R
                del sigj[nan_indices[k]-k]
                del sigj_err[nan_indices[k]-k]
                del Rj[nan_indices[k]-k]
                del Rj_err[nan_indices[k]-k]
            
            if len(sigj)==0: # for the case that sigj is empty because all value were 'nan', create artificial dataset
                sigj=np.zeros(50) # set data to zero
                sigj_err=np.ones(50)*1e-3 # set error to 1e-3 (ODR cannot handle error 0) 
                Rj=np.linspace(0.3,1.4) # linspace for typicall radii
                Rj_err=np.ones(50)*1e-3 # set error to 1e-3 (ODR cannot handle error 0)
                
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

#%% fit modified tanh to profiles of time interval:

# set initial guess with position of LCFS from EFIT minus about half a width as gues for x_sym
p0=[[dict(NE=[1e19,1e19,data[i]['LCFS_R_out_TStb']['data'][j]-0.01,0.02,-1e19,5e18,1.2],TE=[1e2,1e2,data[i]['LCFS_R_out_TStb']['data'][j]-0.03,0.03,-2.5e3,1e2,1.25],PE=[5e2,5e2,data[i]['LCFS_R_out_TStb']['data'][j]-0.02,0.02,-1e4,50,1.25]) for j in ind[i]] for i in range(len(shotnos))]

#first coarse fit of most of profile to find initial guess for pedestal
profile_fits=[{} for shot in shotnos] # for storing fit results
for i in [14,15,16,17,18,19,20]: #only for 08NOV05 #[10]: #range(len(shotnos)):#
    for sig in ped_sigs:#['NE']:#
        sig_fits=[] # fit data for the current signal
        for j in range(len(ind[i])):
            sig_fit_data=[pedestal_data[i][sig]['radii'][j],pedestal_data[i][sig]['radii_errors'][j],pedestal_data[i][sig]['data'][j],pedestal_data[i][sig]['data_errors'][j]] # create data for fitting tool
            sig_fits.append(odr_complete(sig_fit_data,ped_tanh_odr2,diff_ped_tanh_odr2,p0[i][j][sig], xlimit=xlims_out[i][sig]
                            ,plot=False))#,title='Helium experiment shot #%d \n %s coarse profile odr fit, t=%.5f s' %(shotnos[i],sig,pedestal_data[i][sig]['time'][j]),xname='major radius [m]',yname='$n_e$ [$10^{19} m^{-3}$]'))
            #plt.axvline(data[i]['LCFS_R_out_TStb']['data'][j],c='0.5', lw=1, ls='--')
        profile_fits[i][sig]=sig_fits#

#%% now fine fit with only pedestal region (selected with result from coarse fit)
# select region to be fitted by [x_sym-2.5*width,x_sym+1.5*width]

xlims_fine=[[dict(NE=[profile_fits[i]['NE'][j][0][2]-0.1,profile_fits[i]['NE'][j][0][2]+0.1],
                  TE=[profile_fits[i]['TE'][j][0][2]-0.1,profile_fits[i]['TE'][j][0][2]+0.1],
                  PE=[profile_fits[i]['PE'][j][0][2]-0.1,profile_fits[i]['PE'][j][0][2]+0.1]) 
            for j in range(len(ind[i]))] for i in [14,15,16,17,18,19,20]] #only for 08NOV05 #]

# take result from coarse fit as initial gues for fine fit
pedestal_fits=[{} for shot in shotnos] # for storing fit results
for i in [14,15,16,17,18,19,20]: #only for 08NOV05 #range(len(shotnos)):#[10]: #
    for sig in ped_sigs:#['NE']:#
        sig_fits=[] # fit data for the current signal
        for j in range(len(ind[i])):
            sig_fit_data=[pedestal_data[i][sig]['radii'][j],pedestal_data[i][sig]['radii_errors'][j],pedestal_data[i][sig]['data'][j],pedestal_data[i][sig]['data_errors'][j]] # create data for fitting tool
            sig_fits.append(odr_complete(sig_fit_data,ped_tanh_odr2,diff_ped_tanh_odr2,profile_fits[i][sig][j][0], xlimit=xlims_fine[i-14][j][sig]
                            ,plot=False)) #,title='Helium experiment shot #%d \n %s edge pedestal odr fit, t=%.3f s' %(shotnos[i],sig,pedestal_data[i][sig]['time'][j]),xname='major radius [m]',yname='$n_e$ [$10^{19} m^{-3}$]'))
        pedestal_fits[i][sig]=sig_fits#

#%% Analyse pedestal fits
    
# get pedestal L-H and H-L data (height and width)
# seperate ante transitus (at) and post transitus (pt) #################### 
for i in [14,15,16,17,18,19,20]: #only for 08NOV05 #range(len(shotnos)):
    for sig in ped_sigs:
        # find index rigth before transitions
        t=0
        # L-H transition:
        while pedestal_data[i][sig]['time'][t] < tLH[i]:
            indLHat = t
            t+=1
        #goodness of fit (residual variance)
        sig_LH_resvarat=pedestal_fits[i][sig][indLHat][2]
        sig_LH_resvarpt=pedestal_fits[i][sig][indLHat+1][2]
        # pedestal height (a(p[0]) + b(p[1]) in ped_tanh_odr2)
        sig_LH_phat=pedestal_fits[i][sig][indLHat][0][0]  +  pedestal_fits[i][sig][indLHat][0][1]
        sig_LH_ph_errat=np.sqrt(pedestal_fits[i][sig][indLHat][1][0]**2  +  pedestal_fits[i][sig][indLHat][1][1]**2)
        sig_LH_phpt=pedestal_fits[i][sig][indLHat+1][0][0]  +  pedestal_fits[i][sig][indLHat+1][0][1]
        sig_LH_ph_errpt=np.sqrt(pedestal_fits[i][sig][indLHat+1][1][0]**2  +  pedestal_fits[i][sig][indLHat+1][1][1]**2)
        # pedestal width (p[3] in ped_tanh_odr2)
        sig_LH_pwat=pedestal_fits[i][sig][indLHat][0][3]
        sig_LH_pw_errat=pedestal_fits[i][sig][indLHat][1][3]
        sig_LH_pwpt=pedestal_fits[i][sig][indLHat+1][0][3]
        sig_LH_pw_errpt=pedestal_fits[i][sig][indLHat+1][1][3]
        # write to LHdata / HLdata
        LHdata[i][sig+'_ped_heightat']=dict(data=sig_LH_phat,errors=sig_LH_ph_errat,units=data[i][sig]['units'],time=tLH[i],resvar=sig_LH_resvarat)
        LHdata[i][sig+'_ped_heightpt']=dict(data=sig_LH_phpt,errors=sig_LH_ph_errpt,units=data[i][sig]['units'],time=tLH[i],resvar=sig_LH_resvarpt)
        LHdata[i][sig+'_ped_widthat']=dict(data=sig_LH_pwat,errors=sig_LH_pw_errat,units=data[i]['R_CTS']['units'],time=tLH[i],resvar=sig_LH_resvarat)
        LHdata[i][sig+'_ped_widthpt']=dict(data=sig_LH_pwpt,errors=sig_LH_pw_errpt,units=data[i]['R_CTS']['units'],time=tLH[i],resvar=sig_LH_resvarpt)
        
        # H-L transition
           
        try:
            while pedestal_data[i][sig]['time'][t] < tHL[i]:
                indHLat = t
                t+=1
            #goodness of fit (residual variance)
            sig_HL_resvarat=pedestal_fits[i][sig][indHLat][2]
            sig_HL_resvarpt=pedestal_fits[i][sig][indHLat+1][2]
            # pedestal height (a(p[0]) + b(p[1]) in ped_tanh_odr2)
            sig_HL_phat=pedestal_fits[i][sig][indHLat][0][0]  +  pedestal_fits[i][sig][indHLat][0][1]
            sig_HL_ph_errat=np.sqrt(pedestal_fits[i][sig][indHLat][1][0]**2  +  pedestal_fits[i][sig][indHLat][1][1]**2)
            sig_HL_phpt=pedestal_fits[i][sig][indHLat+1][0][0]  +  pedestal_fits[i][sig][indHLat+1][0][1]
            sig_HL_ph_errpt=np.sqrt(pedestal_fits[i][sig][indHLat+1][1][0]**2  +  pedestal_fits[i][sig][indHLat+1][1][1]**2)
            # pedestal width (p[3] in ped_tanh_odr2)
            sig_HL_pwat=pedestal_fits[i][sig][indHLat][0][3]
            sig_HL_pw_errat=pedestal_fits[i][sig][indHLat][1][3]
            sig_HL_pwpt=pedestal_fits[i][sig][indHLat+1][0][3]
            sig_HL_pw_errpt=pedestal_fits[i][sig][indHLat+1][1][3]
            # write to LHdata / HLdata
            HLdata[i][sig+'_ped_heightat']=dict(data=sig_HL_phat,errors=sig_HL_ph_errat,units=data[i][sig]['units'],time=tHL[i],resvar=sig_HL_resvarat)
            HLdata[i][sig+'_ped_heightpt']=dict(data=sig_HL_phpt,errors=sig_HL_ph_errpt,units=data[i][sig]['units'],time=tHL[i],resvar=sig_HL_resvarpt)
            HLdata[i][sig+'_ped_widthat']=dict(data=sig_HL_pwat,errors=sig_HL_pw_errat,units=data[i]['R_CTS']['units'],time=tHL[i],resvar=sig_HL_resvarat)
            HLdata[i][sig+'_ped_widthpt']=dict(data=sig_HL_pwpt,errors=sig_HL_pw_errpt,units=data[i]['R_CTS']['units'],time=tHL[i],resvar=sig_HL_resvarpt)
        except IndexError:# when H-L transition is too late and there is no data anymore at that point
            # set data and errors to 'None' value
            HLdata[i][sig+'_ped_heightat']=dict(data=None,errors=None,units=data[i][sig]['units'],time=tHL[i],resvar=None)
            HLdata[i][sig+'_ped_heightpt']=dict(data=None,errors=None,units=data[i][sig]['units'],time=tHL[i],resvar=None)
            HLdata[i][sig+'_ped_widthat']=dict(data=None,errors=None,units=data[i]['R_CTS']['units'],time=tHL[i],resvar=None)
            HLdata[i][sig+'_ped_widthpt']=dict(data=None,errors=None,units=data[i]['R_CTS']['units'],time=tHL[i],resvar=None)

#%% write data to file
results=[shotnos,tLH,tHL,data,rubyshots,ne_R_p,Te_R_p,pe_R_p,pedestal_data,pedestal_fits,LHdata,HLdata,xlims_fine]

filename='Xpoint_pedestal.p'
file=open(filename,"wb") # generate file
pickle.dump(results,file,pickle.HIGHEST_PROTOCOL) # pickle data and write to file
file.close()
