# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 12:28:08 2018

@author: Tomas
"""
import matplotlib.pyplot as plt
import numpy as np

# Import this using below:
#import sys
#sys.path.append(r'C:\Users\Tomas\Imperial College London\Battle, Ronan - Shared MSci project\Scripts') # "/Users/Tomas/Imperial\ College London/Battle,\ Ronan\ -\ Shared\ MSci\ project/Scripts")
#sys.path.append(r'C:\Users\rbatt\OneDrive - Imperial College London\Shared MSci project\Scripts')
#from Shot_Class import Shot

# import signals dictionaries
from signal_dict_10_NOV_11 import signals
# import pickle loading function
from data_access_funcs import load_signal_data
    
class Shot():
    def __init__(self, ShotNumber, transitions = None):
#       must define signals dictionary here based on shot number/session series
        self.data = {} # initialise data dictionary
        self.ShotNumber = ShotNumber
        self._transitions = transitions
        
        self.unloaded = []
        for sig in signals:
            try:
                fn = str(ShotNumber) + '_' + sig + '.p'
                self.data[sig] = load_signal_data(fn)
            except FileNotFoundError:
                self.unloaded.append(sig)
    
    def signals_present(self):
        keys = self.data.keys()
        return len(keys), keys
    
    def signal_has_errors(self, SignalName):
        if self.data[SignalName]['errors'] is None:
            return False
        else:
            return True

    def plot_signal(self, SignalName):
        # this should go into another file anyway with plotting stuff
        x,y = self.data[SignalName]['time'], self.data[SignalName]['data']
        units = self.data[SignalName]['units']
        try:
            plt.plot(x,y)
            
            plt.ylabel('%s %s' % (SignalName, units))
            plt.annotate(self.ShotNumber, (0.9,0.9), xycoords = 'axes fraction')
            plt.xlim(-0.1)
        except:
            print('Can\'t deal with this signal yet')
   
    
    def plot_compare(self, signalslist):
        n = len(signalslist)
        fig, ax = plt.subplots(n, sharex=True, figsize=(11,7))
        ax[-1].set_xlim([0,1])
        fig.suptitle('Shot %s' % (self. ShotNumber))
        
        for i, signal in enumerate(signalslist):
            self._plot_ax_sig(ax, signal, i, signame= signal)
        
        
    def plot_JP(self, tlim = (0,1), ip = 'IP', wmhd = 'WMHD', coreTe = 'AYC_TE0', 
                ne = 'ANE_DENSITY', Dalpha = 'AIM_DA_TO', Bt = 'BT',
                Ploss = 'Ploss', PINJ = 'PINJ', POHM = 'POHM'
                ):
        """
        Plot some signals together on single figure
        """
        n_signals = 7 # number of signals to be plotted
        
        # make figure and adjust boundaries
        fig, ax = plt.subplots(n_signals, sharex=True, figsize=(11,7))
        fig.subplots_adjust(top=0.935,bottom=0.09,left=0.08,right=0.975,hspace=0.0,wspace=0.2)
        
        # add figure title, labels, set time range
        fig.suptitle('Shot %s' % (self. ShotNumber))
        ax[-1].set_xlabel('$time \ [s]$')
        ax[-1].set_xlim(tlim)
        
        # mark LH, HL transition points
        if self._transitions:
            pass
        else:
            print('No transitions known')
            
        # plot plasma current, ax = 0
        self._plot_ax_sig(ax, ip, 0, signame = 'I_{p}')
        # plot n_e
        self._plot_ax_sig(ax, ne, 1, signame = 'n_{e}', plot_errors='fill') # , units='m^{-2}')
        # plot WMHD
        self._plot_ax_sig(ax, wmhd,2 , signame = 'W_{MHD}')
        # plot core T_e
        self._plot_ax_sig(ax, coreTe, 3 , signame = 'T_{e}^{core}',plot_errors='fill')
        # plot Dalpha of some kind
        self._plot_ax_sig(ax, Dalpha, 4, signame = 'D_{\\alpha}')
        # plot B_T
        self._plot_ax_sig(ax, Bt, 5, signame = 'B_{T}')
        # plot powers
        #self._plot_ax_sig(ax, POHM, panel = 6, signame = 'Pohm', label='POHM', errors=True) #Ploss = 'Ploss', PINJ = 'PINJ', POHM = 'POHM'
        self._plot_ax_sig(ax, Ploss, panel = 6, signame = 'Ploss', label='Ploss', plot_errors='fill')
        self._plot_ax_sig(ax, PINJ, panel = 6, signame = 'PINJ', label='PINJ', plot_errors='fill')
        
        

    
    def _plot_ax_sig(self, ax, sig, panel, signame='', plot_errors=False, units=None, label=None):
        """ for use in plot_JP
        plots signal (sig) on subplot axes (ax[panel]) and labels with signame (and sig units)
        need to add error handeling
        Note: use units with care, as not longer automatic, maybe just use for presentation plots
        """
        # type(ax[panel]) might want to make sure its correct
        shape = self.data[sig]['data'].shape
        if len(shape) == 2 and shape[0] != 1:
            print('Data format of {} has another dimension -> taking mean'.format(sig))
            time = self.data[sig]['time']
            data = np.nanmean(self.data[sig]['data'],axis=1)
            try:
                errors = np.nanmean(self.data[sig]['errors'],axis=1)
            except:
                print('No errors found in {}'.format(sig))
                errors = self.data[sig]['errors']
        #elif len(shape) == 2 and shape[0] == 1:
        #    time = self.data[sig]['time']
         #   data = self.data[sig]['data'][0]
         #   errors = self.data[sig]['errors'][0]
            
    
        else:    
            time = self.data[sig]['time']
            data = self.data[sig]['data']
            errors = self.data[sig]['errors'] # may be None, deal with later
            
        if not units:
            units = self.data[sig]['units']
        else:
            pass
        if units == 'MW': 
            data=data*10e6/5 #what?
        
        if signame!='': 
            label=signame
        
        # Decide how to plot depending on plot_error call
        if plot_errors == True:
            #linestyle = '.'
            ax[panel].errorbar(time,data, yerr=errors,ecolor="red",label=label)
        elif plot_errors == 'fill':
            #print(sig)
            #print(data)                                        # why not just 
            # fix if errors is nothing then make it zero        # if errors != None: ax[panel].fill_between(...)
            try:                                                # else: pass      #just goes on to plot instead
                if errors ==None: errors = np.zeros(len(data))
            except: 
                pass
            #print(errors)
            
            ax[panel].plot(time,data,label=label)
            ax[panel].fill_between(time, data-np.nan_to_num(errors), data + np.nan_to_num(errors), alpha=0.3)
            
        else: 
            ax[panel].plot(time,data,label=label)
        
        ax[panel].annotate(r'$%s \ [%s]$' %(signame, units), xy=(0.01,0.7), xycoords='axes fraction', fontsize=11)
        ax[panel].legend()
    
    
    
    
    
    
    
    