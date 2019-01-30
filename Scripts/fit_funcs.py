# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 14:11:35 2019

@author: rbatt

Functions for fitting data
"""
import numpy as np
import scipy.odr as odr
 
#%%
# functions defined

# _odr2 functions taken from work of JP, in particular
def ped_tanh_odr2(p,x,loc='out'):
    '''Modified tanh for fitting pedestal structures in 
    density/temperature/pressure profiles in tokamak plasmas.
    p - list of parameters (len=7)
    x - xdata (usually major radius or normalized flux )
    loc = 'out'/'in' - defines whether outboard or inboard pedestal is to be fitted'''
    # extract function parameters from p
    a, b, x_sym, width, slope, dwell, x_well = p
    
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
    a, b, x_sym, width, slope, dwell, x_well = p #b not needed as derivative
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
#fit routines
    
tanh = odr.Model(ped_tanh_odr2) # this is the way .ODR needs models 

def do_odr(data,tanh_model = tanh, p=[2.5e19,2.5e19,1.38,0.05,1e19,1.,1.]):
    """data = [x, y, xerr, yerr]
    model = odr.Model(fn)
    p = model initial parameer guesses
    
    returns fitted parameters ~p
    """
    x,y,xe,ye = data[0],data[1],data[2],data[3]
    data = odr.RealData(x,y,sx=xe,sy=ye)
    myodr = odr.ODR(data,tanh_model, beta0=p)
    output = myodr.run()
    return output.beta


