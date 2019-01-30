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
# import pickle loading function
from data_access_funcs import load_signal_data

# =============================================================================
# import your own signal dictionary when running code
# eg from signal_dict_06_OCT_11 import signals, shotnos
#    from signal_dict_10_NOV_11 import signals
# =============================================================================
#from signal_dict_10_NOV_11 import signals

class Transition():
    def __init__(self, LHorHL, t0, tplus, tminus, shot):
        """
        transition class
        """
        self.flavour = LHorHL
        self.t0 = t0
        self.tplus = tplus
        self.tminus = tminus
        self.shot = shot
        self.parameters = {}
    
    def add_param(self, parameter, value):
        self.parameters[parameter] = value
        


class Shot():
    def __init__(self, ShotNumber, LHt = None, HLt = None):
        """
        LHt, HLt = [(time, +error, -error), (time, +error, -error)]
        """
#       must define signals dictionary here based on shot number/session series
        self.data = {} # initialise data dictionary
        self.ShotNumber = ShotNumber
        self._LHt = LHt
        self._HLt = HLt
        self._transitions = []
        
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

    def plot_signal(self, SignalName, figname = None):
        # this could go into another file anyway with plotting stuff
        if len(self.data[SignalName]['data'].shape) >1:
            x, y = self.data[SignalName]['time'] , np.nanmean(self.data[SignalName]['data'], axis=1) 
        else:
            x,y = self.data[SignalName]['time'], self.data[SignalName]['data']
            
        units = self.data[SignalName]['units']
        
        if figname != None:
            plt.figure(figname)
        try:
            plt.plot(x,y)
            
            plt.ylabel('%s %s' % (SignalName, units))
            plt.annotate(self.ShotNumber, (0.9,0.9), xycoords = 'axes fraction')
            plt.xlim(-0.1)
        except:
            print('Can\'t deal with this signal yet')
   
    
    def plot_compare(self, signalslist):
        """ Plot arbitrary number of self.signals in subplots of a single figure
        
        signalslist = ['npos', 'ngrad']
        """
        n = len(signalslist)
        fig, ax = plt.subplots(n, sharex=True, figsize=(11,7))
        
        
        for i, signal in enumerate(signalslist):
            self._plot_ax_sig(ax, signal, i, signame= signal)
            
    def transitions_generator(self, additional_params = None):
        if self._LHt == None and self._HLt == None:
            print('no transitions')
            return
        
        parameters = ['IP','BT','Ploss','KAPPA','ANE_DENSITY','AYC_NE' ] # AYC_NE, AYE_NE doesnt work
        if additional_params != None:
            parameters.extend(additional_params)
            
        list_of_transitions = []
        for t  in self._LHt:
            list_of_transitions.append((t,'LH'))
        for t in self._HLt:
            list_of_transitions.append((t,'HL'))
        print(list_of_transitions)
        
        for tran,name in list_of_transitions:
            tclass = Transition(name, tran[0], tran[1], tran[2], self.ShotNumber)
            
            for param in parameters:
                print(param)
                if param not in self.signals_present()[1]:
                    print('signal not present')
                    continue
                units = self.data[param]['units']
                
                if len(self.data[param]['data'].shape) >1:
                    print('Signal {} has been squashed into one dimension'.format(param))
                    p_0 = np.interp(tclass.t0, self.data[param]['time'] , np.nanmean(self.data[param]['data'], axis=1))
                    p_0_err = np.interp(tclass.t0, self.data[param]['time'] , np.nanmean(self.data[param]['errors'], axis=1))
                    t_err_range = np.interp(np.linspace(tclass.tminus,tclass.tplus,30), self.data[param]['time'] , np.nanmean(self.data[param]['data'], axis=1))

                else:
                    p_0 = np.interp(tclass.t0, self.data[param]['time'] , self.data[param]['data'])
                    try:
                        p_0_err = np.interp(tclass.t0, self.data[param]['time'] , self.data[param]['errors'])
                    except:
                        p_0_err = 0
                    t_err_range = np.interp(np.linspace(tclass.tminus,tclass.tplus,30), self.data[param]['time'] , self.data[param]['data'])
                
                t_err_err = np.ptp(t_err_range) # numpy range function, max-min
                error = np.sqrt(t_err_err**2 + p_0_err**2) # some math/logic to do overall error
                
                dictionary = {'p_0': p_0,
                              'p_0_err': p_0_err,
                              't_err': t_err_err,
                              'error': error,
                              'units': units }
                tclass.add_param(param, dictionary)
            
            self._transitions.append(tclass)
            
            
    def transition_params(self, additional_params = None):
        if self._LHt == None or self._HLt == None:
            """ parameters at transition times including errors
            outputs to excel and self._pandas
            """
            print('ABORT: No LH or HL in shot {}'.format(self.ShotNumber))
            return
        
        parameters = ['IP','BT','Ploss','KAPPA','ANE_DENSITY','NE', 'AYE_NE','AYC_NE','X1Z','X2Z'] # AYC_NE, AYE_NE doesnt work
        if additional_params != None: parameters.extend(additional_params)
        
        # prepare dict for pandas
        self._pandas = {
                'shot':[],
                'LH/HL':[],
                'time':[],
                'units':[],
                'param':[],
                'p_value':[],
                'p_value_err':[],
                'perc_range_err':[],
                'range_err':[]
                }
        
        # why?
        parameter = 'IP'
        
        # compbine LHt and HLt 
        list_of_transitions = []
        list_of_transitions.extend(self._LHt)
        list_of_transitions.extend(self._HLt)
        
        for parameter in parameters:
            if parameter not in self.signals_present()[1]: 
                # WHAT DOES THIS DO PRACTICALLY?
                continue # if singal doesnt exist, continue
            
            
            # for problematic data
            # WHY DOES THIS ONLY WORK FOR SPECIFIED 'AYCE_NE'?
            try:
                self.data['AYC_NE']['data']=np.nanmean(self.data['AYC_NE']['data'],axis=1)
                self.data['AYC_NE']['errors']=np.nanmean(self.data['AYC_NE']['errors'],axis=1)
                self.data['AYE_NE']['data']=np.nanmean(self.data['AYE_NE']['data'],axis=1)
                self.data['AYE_NE']['errors']=np.nanmean(self.data['AYE_NE']['errors'],axis=1)
            except:
                pass
            try:         
                # for NE for 08 JP shots
                self.data['NE']['data']=np.nanmean(self.data['NE']['data'],axis=1)
                self.data['NE']['errors']=np.nanmean(self.data['NE']['errors'],axis=1)
                self.data['NE']['data']=np.nanmean(self.data['NE']['data'],axis=1)
                self.data['NE']['errors']=np.nanmean(self.data['NE']['errors'],axis=1)
                print(self.data['NE'])
            except: 
                pass
            
            print(parameter)
            for t in list_of_transitions:
                print('truing: {}'.format(parameter))
                t1 = t[0]   #time of tranision
                t_err1 = t[1] # lower bound time error
                t_err2 = t[2] # upper bound time error
                
                # get  units
                units = self.data[parameter]['units']
                
                # get parameter at transition
                singal_at_t1 = np.interp(t1, self.data[parameter]['time'] , self.data[parameter]['data'])
                
                # get erro in parameter at transition
                try: # this is None case
                    if self.data[parameter]['errors'] == None:
                        singal_at_t1_err = 0
                except:
                    if self.data[parameter]['errors'].shape == 2:
                        singal_at_t1_err = np.interp(t1, self.data[parameter]['time'] , np.nanmean(self.data[parameter]['errors'],axis=1))
                    else:
                        singal_at_t1_err = np.interp(t1, self.data[parameter]['time'] , self.data[parameter]['errors'])

    
                # get parameter range during the time error
                singal_t_err_range = np.interp(np.linspace(t_err1,t_err2,30), self.data[parameter]['time'] , self.data[parameter]['data'])
                print(singal_t_err_range)
                
                # get errors in the range of time error
                try: 
                    if self.data[parameter]['errors'] == None:
                        singal_t_err_error_range = np.zeros(30)
                except: 
                    if self.data[parameter]['errors'].shape == 2:
                        singal_t_err_error_range = np.interp(np.linspace(t_err1,t_err2,30), self.data[parameter]['time'] , np.nanmean(self.data[parameter]['errors'],axis=1))
                    else:
                        singal_t_err_error_range  = np.interp(np.linspace(t_err1,t_err2,30), self.data[parameter]['time'] , self.data[parameter]['errors'])
                
                print(singal_t_err_error_range)
                
                # calculate spread in singal during t range and add mean error
                singal_t_err_spread = max(singal_t_err_range) - min(singal_t_err_range) + np.mean(np.abs(singal_t_err_error_range))
                
                # add to dict
                self._pandas['shot'].append(self.ShotNumber)
                if t in self._LHt:
                    self._pandas['LH/HL'].append('LH')
                elif t in self._HLt:
                    self._pandas['LH/HL'].append('HL')
                else: 
                    self._pandas['LH/HL'].append('WTF?') #:)
                self._pandas['time'].append(t1)
                self._pandas['units'].append(units)
                self._pandas['param'].append(parameter)
                self._pandas['p_value'].append(singal_at_t1)
                self._pandas['p_value_err'].append(singal_at_t1_err)
                self._pandas['perc_range_err'].append(np.round(singal_t_err_spread/singal_at_t1*100,2))
                self._pandas['range_err'].append(singal_t_err_spread)
            
      
        # transform to pandas and save to excel
        import pandas as pd
        parameters_results = pd.DataFrame(self._pandas)
        writer = pd.ExcelWriter('parameters_output_{}.xlsx'.format(self.ShotNumber))
        parameters_results.to_excel(writer,'Sheet1')
        writer.save()
       
        
    def plot_JP(self, tlim = (0,0.5), ip = 'IP', wmhd = 'WMHD', coreTe = 'AYC_TE0', 
                ne = 'ANE_DENSITY', Dalpha = 'AIM_DA_TO', Bt = 'BT',
                Ploss = 'Ploss', PINJ = 'PINJ', POHM = 'POHM'
                ):
        """
        Plot some signals together on single figure
        """
        
        # if ANE Density not avilable try to switch to AYC_NE
        if ne not in self.data.keys():
            if 'AYC_NE' in self.data.keys():
                ne = 'AYC_NE'
        
        n_signals = 7 # number of signals to be plotted
        
        # make figure and adjust boundaries
        fig, ax = plt.subplots(n_signals, sharex=True, figsize=(11,7))
        fig.canvas.set_window_title('Shot {}'.format(self.ShotNumber))
        fig.subplots_adjust(top=0.935,bottom=0.09,left=0.08,right=0.975,hspace=0.0,wspace=0.2)
        
        # add figure title, labels, set time range
        fig.suptitle('Shot %s' % (self. ShotNumber))
        ax[-1].set_xlabel('$time \ [s]$')
        ax[-1].set_xlim(tlim)
        
        # mark LH, HL transition points
        if self._LHt:
            for tset in self._LHt:  # tset = (time, -tlim_err, =tlim_err)
                for axes in ax:
                    axes.axvline(tset[0], c='g', lw=1, ls='--', clip_on=False) #draw vertical line for transition
                    if tset[1] != 0:
                        axes.axvline(tset[1], c='g', lw=1, ls=':', clip_on=False, alpha= 0.6) # draw error line
                    if tset[2] != 0:
                        axes.axvline(tset[2], c='g', lw=1, ls=':', clip_on=False, alpha= 0.6) # draw error line
        if self._HLt:
            for tset in self._HLt:  # tset = (time, -tlim_err, +tlim_err)
                for axes in ax:
                    axes.axvline(tset[0], c='r', lw=1, ls='--', clip_on=False)   
                    if tset[1] != 0:
                        axes.axvline(tset[1], c='r', lw=1, ls=':', clip_on=False, alpha= 0.6)
                    if tset[2] != 0:
                        axes.axvline(tset[1], c='r', lw=1, ls=':', clip_on=False, alpha= 0.6)
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
        
        TOMAS, COULD YOU CLEAN UP/COMMENT?
        """
        # type(ax[panel]) might want to make sure its correct
        shape = self.data[sig]['data'].shape
        if len(shape) == 2:
            print('Data format of {} has another dimension -> taking mean'.format(sig))
            time = self.data[sig]['time']
            data = np.nanmean(self.data[sig]['data'],axis=1)
            try:
                errors = np.nanmean(self.data[sig]['errors'],axis=1)
            except:
                print('No errors found in {}'.format(sig))
                errors = self.data[sig]['errors']
    
        else:    
            time = self.data[sig]['time']
            data = self.data[sig]['data']
            errors = self.data[sig]['errors'] # may be None, deal with later
            
        if not units:
            units = self.data[sig]['units']
        else:
            pass
        if units == 'MW': 
            data=data*10e6/5 # what?
        
        if signame!='': 
            label=signame
        
        # Decide how to plot depending on plot_error call
        if plot_errors == True:
            #linestyle = '.'
            ax[panel].errorbar(time,data, yerr=errors,ecolor="red",label=label)
        elif plot_errors == 'fill':
            try:
                if errors == None:        
                    ax[panel].plot(time,data,label=label)
            except:
                ax[panel].plot(time,data,label=label)
                ax[panel].fill_between(time, data-np.nan_to_num(errors), data + np.nan_to_num(errors), alpha=0.3)
        else: 
            ax[panel].plot(time,data,label=label)
        
        ax[panel].annotate(r'$%s \ [%s]$' %(signame, units), xy=(0.01,0.7), xycoords='axes fraction', fontsize=11)
        ax[panel].legend()
        
    # EXPERIMENTAL #
    def add_ir_signal(self, signals= ['AIT_PTOT_ISP', 'AIT_PTOT_OSP']):
        #signals must be same type, ie just use the default
        times = self.data[signals[0]]['time']
        unit = self.data[signals[0]]['units']
#        errors = None  #for this case
        power = self.data[signals[0]]['data']
        for p in signals[1:]:
            power = + self.data[p]['data']
        
        di = {'time': times,
              'data': power,
              'errors': None,
              'units': unit}
        self.data['Ploss_IR'] = di
    

def plot_shot_comparison(shots, tlim = (0,1), ip = 'IP', wmhd = 'WMHD', coreTe = 'AYC_TE0', ne = 'ANE_DENSITY', Dalpha = 'AIM_DA_TO', Bt = 'BT', Ploss = 'Ploss', PINJ = 'PINJ', POHM = 'POHM'):
    """
    """
    n_signals = 4
    fig, ax = plt.subplots(n_signals, sharex=True, figsize=(11,7))
    fig.suptitle('Multiple shots')
    ax[-1].set_xlabel('$time \ [s]$')
    ax[-1].set_xlim(tlim)
    
    shotlist = []
    for s in shots:
        shotlist.append(Shot(s))
    
    for sc in shotlist:
        sc._plot_ax_sig(ax, ip, 0)
        sc._plot_ax_sig(ax, wmhd, 1)
        sc._plot_ax_sig(ax, Dalpha, 2)
        sc._plot_ax_sig(ax, Bt, 3)
    
    for axes in ax:
        axes.legend()
        
    
        
    
    
    
    
    
    