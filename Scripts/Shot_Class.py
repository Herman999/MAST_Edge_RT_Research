"""
MSci Project: PLAS-Andrew-1
Title: L-H Transitions and Pedestal Characterisation Studies on MAST

This code is the core of analysis. Produced with project partner.
Separate scripts have been written for particular purposes calling methods in Shot Class.
In total 8000 lines of code were produced with Shot Class being over 1000. Lot of data issues/inconsistency had to be dealt with automatically in Shot Class
Requirements: Python 3 and standard packages. Signals definitions. Previous work (JP) scripts,such as "do_odr, ped_tanh_odr2, tanh", are required.
Example of Signals definition is appended below this Shot Class.
All scripts are available at Github repository, https://github.com/Herman999/

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import bisect


# Import this using below to set working path:
#import sys
#sys.path.append(r'C:\Users\Tomas\Imperial College London\Battle, Ronan - Shared MSci project\Scripts') # "/Users/Tomas/Imperial\ College London/Battle,\ Ronan\ -\ Shared\ MSci\ project/Scripts")
#sys.path.append(r'C:\Users\rbatt\OneDrive - Imperial College London\Shared MSci project\Scripts')
#from Shot_Class import Shot

# import pickle loading function
from data_access_funcs import load_signal_data
# import fiting functions built by JP (prvious work)
from fit_funcs import do_odr, ped_tanh_odr2, tanh

# =============================================================================
# import your own signal dictionary when running code
# eg from signal_dict_06_OCT_11 import signals, shotnos
#    from signal_dict_10_NOV_11 import signals
#    from signal_dict_13_DEC_PULL import signals
# =============================================================================
#global signals
#from signal_dict_13_DEC_PULL import signals

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
        self.__id = '{s}_{t}'.format(s=self.shot, t=self.t0)

    def add_param(self, parameter, value):
        self.parameters[parameter] = value

    def update_database(self):
        """
        store record in central database
        if record exists in database, do nothing
        """
        

class Shot():
    def __init__(self, ShotNumber, LHt = None, HLt = None):
        """
        Initiate Shot object
        transition times needed in format: LHt, HLt = [(time, +error, -error), (time, +error, -error)]
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
        """
        Returns all present signals in Shot
        """
        keys = self.data.keys()
        return len(keys), keys
    
    def signal_has_errors(self, SignalName):
        """
        Return whether signal has errors
        """
        if self.data[SignalName]['errors'] is None:
            return False
        else:
            return True
    
    def Te_Tec_L(self, index, A=1, prev=False):
        time = self.data['AYE_R']['time'][index]
        psi_t,psi_95 = self.data['EFM_R_PSI95_OUT']['time'],self.data['EFM_R_PSI95_OUT']['data'] 
        R_95 = np.interp(time, psi_t, psi_95)
        
        r_edge, Te_edge = self.data['AYE_R']['data'][index], self.data['AYE_TE']['data'][index]
        Te_edge_smooth = np.convolve(Te_edge, np.ones((5,))/5, mode='same')
        T_e = np.interp(R_95, r_edge, Te_edge_smooth)
        
        ne_edge = self.data['AYE_NE']['data'][index]
        ne_edge_smooth = np.convolve(ne_edge, np.ones((5,))/5, mode='same')
        
        ci = np.where(r_edge>R_95)[0][0]
        ne_select , ne_r_select = ne_edge_smooth[ci-2:ci+1], r_edge[ci-2:ci+1]
        try:
            ne_grad = np.polyfit(ne_r_select,ne_select,1)[0]
        except:
            ne_grad = 1e40
        ne_at_95 = np.interp(R_95, r_edge, ne_edge_smooth)
    
        Bts, B_times = self.data['BT']['data'], self.data['BT']['time']
        B_t = np.interp(time, B_times, Bts)
        
        T_ec = np.sqrt(-ne_grad/ne_at_95) * np.power(np.abs(B_t), 2./3) * A
        
        return(T_e, T_ec)
        
    def _Ln_Te(self, index, previewTe = False):
        """ Find L_n, T_e at index of Thomson burst
        """
        # Ln = 1/n dn/dr|(max slope)
        edge_ne_fit, time, (radii, ne) = self.fit_edge_tanh_pedestal(index, preview = False) # caution this is put in one variable in some other methods
        knee, width, max_slope, ne_max_slope, ne_knee = self._tanh_params(edge_ne_fit) # caution this is done differently in Te_Tec for eg.
        R_max_slope = knee + width /2. # slope = dn/dr
        
        Ln = - ne_max_slope / max_slope # gradient scale length = -n/grad(n)
        print('Density gradient scale length:', Ln)

        # Psi data
        PsiTime, Psi100, Psi95, Psi90 = [self.data['EFM_R_PSI100_OUT']['time'], 
                                         self.data['EFM_R_PSI100_OUT']['data'],
                                         self.data['EFM_R_PSI95_OUT']['data'],
                                         self.data['EFM_R_PSI90_OUT']['data'] ] 
        P100, P95, P90 = [np.interp(time, PsiTime, Psi100),
                          np.interp(time, PsiTime, Psi95),
                          np.interp(time, PsiTime, Psi90) ] # now in form R = ... m
        
        if previewTe == True:
            fig, ax = self._plot_edge_pedestal(index, sig='TE') # Te data
            # draw lines
            ax.axvline(P100, ls='-.', c='lightgray', label='P 100')
            ax.axvline(P95, ls='-.', c='darkgray', label='P 95')
            ax.axvline(P90, ls='-.', c='dimgray', label='P 90')
            ax.axvline(knee, ls='--', c='b', label='NE knee')
            ax.axvline(R_max_slope, ls='--', c='r', label='NE max slope')        
            ax.axvline(knee+width, ls='--', c='b', label='NE knee+width')
            ax.legend()
        
        # Te profile data. Radiis already known from above 
        Tes = self.data['AYC_TE']['data'][index]
        Te_ers = self.data['AYC_TE']['errors'][index]
        radii = self.data['AYC_R']['data'][index]

        # calculate a Te
        Te = np.interp(R_max_slope, radii, Tes) # from R of max dn/dr
        Te_er = np.interp(R_max_slope, radii, Te_ers)
        
        P98 = np.interp(98, [95,100], [P95, P100]) # radii of Psi98
        Te_P98 = np.interp(P98, radii, Tes)
        Te_P95 = np.interp(P95, radii, Tes)
        
        return  Ln, Te, Te_P98, Te_P95
    
    def Te_after_time(self, t0, slices):
        """Playing around with Te profile. Where can it be cut off?"""
        times = self.data['AYC_NE']['time']
        ind_0 = np.where(times>t0)[0][0]
        inds = np.arange(ind_0, ind_0+ slices)
        
        results = []
        
        for i in inds:
            Ln, Te, Te_P98, Te_P95 = self._Ln_Te(i)
            t = times[i]
            results.append((t,Ln, Te, Te_P98, Te_P95))
        
        return results
            
    
    def _plot_edge_pedestal(self, index, sig='NE'):
        """ plot with errors the edge data (pedestal) of sig at index given
        """
        y = self.data['AYE_{}'.format(sig)]['data'][index]
        y_er = self.data['AYE_{}'.format(sig)]['errors'][index]
        x = self.data['AYE_R']['data'][index]
        x_er = self.data['AYE_R']['errors'][index]
        time = self.data['AYE_R']['time'][index]
        
        # remove nans
        condition = np.where(~np.isnan(y))
        y, y_er, x, x_er = y[condition], y_er[condition], x[condition], x_er[condition]
        
        fig, ax = plt.subplots(1)
        fig.canvas.set_window_title('{0} {1} edge data at {2:3f} s'.format(self.ShotNumber,sig,time))
        ax.errorbar(x,y,yerr=y_er,xerr=x_er, elinewidth=0.5, label='data')
        ax.set_xlabel('R [m]')
        ax.set_ylabel(sig)
        ax.set_ylim(0,)
        ax.legend()
        return fig, ax
        
        
    def Te_Tec(self, index, A=1., prev=False): #THIS WILL BE Te_Tec_H (mode)
        """
        Generate (T_e,T_ec) for given index of Thomson data (using edge)
        A = multiplicative Tec constant 
        A ~ 0.45 * Z^1/3 / (R(m)A_i)^1/6
        
        Only really works in H mode when tanh fit works. But pedestal fits in L still not horrendous.
        """
        edge_ne_fit = self.fit_tanh_pedestal(index, preview = prev) # result, time, (R's, ne's)
        knee, width, max_slope, ne_max_slope, ne_knee = self._tanh_params(edge_ne_fit[0])
        R_max_slope = knee + width /2.
        
        # fitting TE pedestal is probably useless but we do it anyway
        res,t,xys,Te_name = self.fit_tanh_pedestal(index, sig='TE', preview = False) # result, time, (x,y,x_er,y_er), canvas_name
        # clean up data from SOL
        cond = np.where(xys[0] < knee+ width) # only want R's inside the NE pedestal
        # apply condition to TE data (returned from self.fit_tanh_pedestal)
        x,y,xer,yer = xys[0][cond],xys[1][cond],xys[2][cond],xys[3][cond]
        
# can this be done better, taking account of xer,yer?
        
        
        sol_cut = knee+width
        
        
        # T_e via 3 point average.
        ptavg = 3 # how many points to average over
        y_smooth = pd.DataFrame(y).rolling(ptavg, center=True).mean().values.squeeze()
        T_e = np.interp(R_max_slope, x,y_smooth)
        #error calculation
        
        # 2 options. only use second
        # 1: take range of y's that have been smoothed
        cind = bisect.bisect_right(x,R_max_slope)
        T_e_err = np.ptp(y[cind-1:cind+2])
        
        # 2: Te signal error only 
        T_e_err = np.interp(R_max_slope, x,yer)
        
        
        ####################OLD T_e line###########################
        #T_e = ped_tanh_odr2(edge_te_fit[0], R_max_slope) # this fit is bad
        
        Bts, B_times = self.data['BT']['data'], self.data['BT']['time']
        B_t = np.interp(edge_ne_fit[1], B_times, Bts) # find B_T at time of NE fit
        
        Ln = -ne_max_slope/max_slope
        Theta = T_e / np.sqrt(Ln)
        Theta_err = T_e_err/np.sqrt(Ln)
        Theta_c = A * np.power(np.abs(B_t), 2./3.)
        T_ec = Theta_c * np.sqrt(Ln)
        
                
    #    print('max slope: {0:.3e}. ne at max slope: {1:.3e}. Bt = {2}'.format(max_slope, ne_max_slope, B_t))
        return (T_e, T_e_err, T_ec, (Theta,Theta_c,Theta_err))
    
    def Te_Tec_all(self, good_indexes, A=1., label=False, bigerrs=True, Tec_err = None, theta_transition_times=False):
        
        cols = {'LH':'orange', 
                'L':'red', 
                'H':'green', 
                'HL':'blue'
                }
        
        lookup = [(self._LHt[0][1], 'L'),
                  (self._LHt[0][2], 'LH'),
                  (self._HLt[0][1], 'H'),
                  (self._HLt[0][2], 'HL'),
                  (0.8, 'L')
                  ]
        if len(self._LHt)>1:
            if len(self._LHt)>2:
                print('more than two h mode periods! You must be kidding. Shot {}'.format(self.ShotNumber))
            lookup = [(self._LHt[0][1], 'L'),
                  (self._LHt[0][2], 'LH'),
                  (self._HLt[0][1], 'H'),
                  (self._HLt[0][2], 'HL'), # end of first H-mode
                  (self._LHt[1][1], 'L'),
                  (self._LHt[1][2], 'LH'),
                  (self._HLt[1][1], 'H'),
                  (self._HLt[1][2], 'HL'), # end of second H-mode
                  (0.8, 'L')
                  ] 
        
        plt.figure('Te/c')
        plt.xlabel('Tec')
        plt.ylabel('Te')
        plt.title('Shot {}'.format(self.ShotNumber))
        
        for ind, time in enumerate(self.data['AYE_R']['time']):
            if ind not in good_indexes:
                pass
            else:
                label= lookup[bisect.bisect(lookup,(time,))][1] #'L', 'LH', 'H' etc
                if label in ['L','LH']:
        # here the calls to self.Te_Tec are made for given index
                    Te,Te_err,Tec,(theta,theta_c,theta_err) = self.Te_Tec(ind)
                else: # its 'H' or 'HL'
                    Te,Te_err,Tec,(theta,theta_c,theta_err) = self.Te_Tec(ind)
                
                if Te_err/Te > 1:
                    print('Error Warning: index {}'.format(ind))
                    if bigerrs == False: 
                        continue # if 'include big errs = False' exit loop, don't plot point
                
                plt.figure('Te/c')
                plt.errorbar(Tec*A, Te, yerr=Te_err,xerr=Tec_err, marker='x', c=cols[label])
                if label == True:
                    plt.annotate(str(ind), [Tec*A, Te])
                plt.figure('simple Te')
                plt.errorbar(time,Te, yerr=Te_err, marker='x', c=cols[label])
                plt.figure('Theta')
                plt.errorbar(time,theta,yerr=theta_err, c=cols[label])
                plt.scatter(time,A*theta_c, c='k')
        if theta_transition_times == True:
            plt.figure('Theta')
            if self._LHt:
                for tset in self._LHt:  # tset = (time, -tlim_err, =tlim_err)
                    plt.axvline(tset[0], c='g', lw=1, ls='--', clip_on=False) #draw vertical line for transition
                    if tset[1] != 0:
                        plt.axvline(tset[1], c='g', lw=1, ls=':', clip_on=False, alpha= 0.6) # draw error line
                    if tset[2] != 0:
                        plt.axvline(tset[2], c='g', lw=1, ls=':', clip_on=False, alpha= 0.6) # draw error line
            if self._HLt:
                for tset in self._HLt:  # tset = (time, -tlim_err, +tlim_err)
                    plt.axvline(tset[0], c='r', lw=1, ls='--', clip_on=False)   
                    if tset[1] != 0:
                        plt.axvline(tset[1], c='r', lw=1, ls=':', clip_on=False, alpha= 0.6)
                    if tset[2] != 0:
                        plt.axvline(tset[1], c='r', lw=1, ls=':', clip_on=False, alpha= 0.6) 
                    
        plt.figure('simple Te')
        plt.xlabel('time')
        plt.ylabel('Te')
        plt.title('Shot {}'.format(self.ShotNumber))
        if self._LHt:
            for tset in self._LHt:  # tset = (time, -tlim_err, =tlim_err)
                plt.axvline(tset[0], c='g', lw=1, ls='--', clip_on=False) #draw vertical line for transition
                if tset[1] != 0:
                    plt.axvline(tset[1], c='g', lw=1, ls=':', clip_on=False, alpha= 0.6) # draw error line
                if tset[2] != 0:
                    plt.axvline(tset[2], c='g', lw=1, ls=':', clip_on=False, alpha= 0.6) # draw error line
        if self._HLt:
            for tset in self._HLt:  # tset = (time, -tlim_err, +tlim_err)
                plt.axvline(tset[0], c='r', lw=1, ls='--', clip_on=False)   
                if tset[1] != 0:
                    plt.axvline(tset[1], c='r', lw=1, ls=':', clip_on=False, alpha= 0.6)
                if tset[2] != 0:
                    plt.axvline(tset[1], c='r', lw=1, ls=':', clip_on=False, alpha= 0.6)
        
        # additional plot points for legend generation (FAKE POINTS OUTSIDE OF PLOT)
# plt.scatter(-1,-1, marker='x', c='r', label='L')   
# plt.scatter(-1,-1, marker='x', c='g', label='H')
# plt.scatter(-1,-1, marker='x', c='orange', label='LH')
# plt.scatter(-1,-1, marker='x', c='blue', label='HL')
# plt.legend()
    
    def _tanh_params(self, result):
        """return useful values from tanh fit parameters
        """
        knee = result[2]-result[3]/2
        width = result[3]
        max_slope = -2* result[0]/result[3]
        ne_max_slope = ped_tanh_odr2(result, knee+width/2.) # ne at max slope
        ne_at_knee = ped_tanh_odr2(result, knee) # ne at max slope
        return(knee, width, max_slope, ne_max_slope, ne_at_knee)
    
    def fit_after_time(self, t0, slices, sig='NE', scaling=1., prev=True):
        """
        selects slices number of times after t0 in thomson data to tanh fit
        and shows which in a JP plot
        
        results = {t0: (knee, width, max_slope, ne|max slope, ne at knee)
                   t1: ...
                   }
        """
        # maybe check times are the safe for core and edge. I think it's always true
        times = self.data['AYC_NE']['time']
    
        ind_0 = np.where(times>t0)[0][0]
        inds = np.arange(ind_0, ind_0+ slices)
        results = {}
                
        for i in inds:
            fit, time, xy = self.fit_tanh_pedestal(i, sig=sig, scaling=scaling, preview=prev)
            results[time] = self._tanh_params(fit)
                
        if prev == True:
            fig, ax = self.plot_JP(plot_thomson=4)
            fig.canvas.set_window_title('Where {} fitted (red lines)'.format(self.ShotNumber))
            for i in inds:
                ax[4].axvline(times[i], c='r')
            
        return results        
    
    def fit_edge_tanh_pedestal(self, index, sig='NE', preview = True):
        """
        Fit the modified 'ped_tanh_odr2' fn to the AYE tomson data for specified signal, index. Like:
        x = self.data['AYE_sig']['data'][index]
        y = self.data['AYE_R']['data'][index]
    
        Returns fitted parameters
        """
        y = self.data['AYE_{}'.format(sig)]['data'][index]
        y_er = self.data['AYE_{}'.format(sig)]['errors'][index]
        x = self.data['AYE_R']['data'][index]
        x_er = self.data['AYE_R']['errors'][index]
        time = self.data['AYE_R']['time'][index]
        
        # remove nans
        condition = np.where(~np.isnan(y))
        y, y_er, x, x_er = y[condition], y_er[condition], x[condition], x_er[condition]
        
        #do fitting
        result = do_odr([x,y,x_er,y_er]) # a,b,x_sym, width, slope, dwell, x_well
        
        if preview:
            self._pedestal_preview(x,y,x_er,y_er, time, result, sig)
            
        return result, time, (x,y)
        
    def fit_core_tanh_pedestal(self, index, sig='NE', preview=True):
        """ as above
        """
        # all core data
        y = self.data['AYC_{}'.format(sig)]['data'][index]
        y_er = self.data['AYC_{}'.format(sig)]['errors'][index]

        x = self.data['AYC_R']['data'][index]
        x_er = self.data['AYC_R']['errors'][index]
        time = self.data['AYC_R']['time'][index]
        
        #cutoff radius for fitting. defined as lowest R present in edge data
        r_cutoff= self.data['AYE_R']['data'][index][0]
        condition = np.where((x > r_cutoff)&(~np.isnan(y)))
           
        y, y_er, x, x_er = y[condition], y_er[condition], x[condition], x_er[condition]
        
        # may need to pad core values outside LCFS
        
        #do fitting on reduced data
        result = do_odr([x,y,x_er,y_er]) # a,b,x_sym, width, slope, dwell, x_well
                
        if preview:
            self._pedestal_preview(x,y,x_er,y_er, time,result,sig)
######### add title for core or edge ########
        return result, time (x,y)
    

    
    def fit_tanh_pedestal(self, index, scaling = 1./0.9, sig='NE', preview=True, guess=[2.5e19,2.5e19,1.38,0.05,1e19,1.,1.]):
        """ Fits modified 'ped_tanh_odr2' fn to AYE thomson for signal=sig at index
        x = self.data['AYE_sig']['data'][index] + self.data['AYC_sig']['data'][index]
        y = self.data['AYE_R']['data'][index]   (+ iff in valid R range)
        
        scaling = applied to edge data to bring in line with core values
        """
        # EDGE data
        y = self.data['AYE_{}'.format(sig)]['data'][index] *scaling
        y_er = self.data['AYE_{}'.format(sig)]['errors'][index] *scaling
        x = self.data['AYE_R']['data'][index]
        x_er = self.data['AYE_R']['errors'][index]
        time = self.data['AYE_R']['time'][index]    
        # remove nans
        condition = np.where(~np.isnan(y))
        y, y_er, x, x_er = y[condition], y_er[condition], x[condition], x_er[condition]
    
        # CORE data
        c_y = self.data['AYC_{}'.format(sig)]['data'][index]
        c_y_er = self.data['AYC_{}'.format(sig)]['errors'][index]
        c_x = self.data['AYC_R']['data'][index]
        c_x_er = self.data['AYC_R']['errors'][index]
        
        #cutoff radius for fitting. defined as lowest R present in edge data
        r_cutoff= x[0]
        condition = np.where((c_x > r_cutoff)&(~np.isnan(c_y)))
        c_y, c_y_er, c_x, c_x_er = c_y[condition], c_y_er[condition], c_x[condition], c_x_er[condition]

        # combine data into pandas DataFrame        
        edge = pd.DataFrame({'x':x,'y':y,'x_er': x_er,'y_er': y_er})
        core = pd.DataFrame({'x':c_x,'y':c_y,'x_er':c_x_er,'y_er':c_y_er})
        data = edge.append(core).sort_values('x')
        # split combined data back up
        x,y,x_er,y_er = data['x'].values, data['y'].values, data['x_er'].values, data['y_er'].values
        
        #do fitting on combined data
# if not NE signal, want to change the p guess.
        result = do_odr([x,y,x_er,y_er], p=guess) # a,b,x_sym, width, slope, dwell, x_well
        
        knee, width, max_slope, ne_max_slope, ne_at_knee = self._tanh_params(result) # parameters to check if fit is decent
        palt =[3.0e19,2.0e19,1.47,0.05,1.0e19,1,1] # alternative pguess to check if it works
        if knee + width > 1.55 or width <0 or width < 0.005: # bad fit criteria
            result = do_odr([x,y,x_er,y_er], p=palt) # re do fit with alternative
        
        canvas_name = None
        if preview:
            canvas_name = self._pedestal_preview(x,y,x_er,y_er, time,result,sig)
####### may want to add appropriate labels to this plot #####
            
        return result, time, (x,y,x_er,y_er), canvas_name
    
    
    def _pedestal_preview(self, x,y,xr,yr, time,result,sig):
        """
        For 'preview' of result from fit_core/edge_tanh_pedestal only.
        """
        plt.rcParams.update({'font.size': 15})
        fig = plt.figure(figsize=(10,7.2))
        
        canvas_name= '{0} {1} pedestal at {2:3f} s'.format(self.ShotNumber,sig,time)
        fig.canvas.set_window_title(canvas_name)
        
        #show data and fit
        plt.errorbar(x,y, yerr=yr, xerr=xr,fmt='x',mfc='blue',elinewidth=2,markersize=15)

        fitx = np.arange(np.min(x),np.max(x),step=0.001)
        plt.plot(fitx, ped_tanh_odr2(result,fitx), c='r',lw=3, label='mtanh fit')
        
        plt.xlabel('R [m]')
        plt.ylabel(r'$N_e$ [$\times 10^{19}$m$^{-3}$]')
        
        plt.ylim(0,)

        # mark useful labels
        knee = result[2]-result[3]/2
        width = result[3]
        midpt = knee + width/2
        max_slope = -2* result[0]/result[3]
        y_knee = ped_tanh_odr2(result, knee)
        plt.axvline(knee, ls='--', c='k',lw = 3,label='Pedestal') #, label='knee= {0:.3g}'.format(y_knee))
        plt.axvline(knee + width,ls='--', c='k',lw=3)#, label='knee+width')
    
        # show max slope 
        slope_xs = x
        y_mid = ped_tanh_odr2(result, midpt)
        slope_ys = (y_mid-max_slope*midpt) + max_slope* slope_xs
        plt.plot(slope_xs, slope_ys, c='g',lw=3,label='Max gradient')#label='grad= {0:.2g}'.format(max_slope))
        plt.legend(loc=1) 
        
        return canvas_name
    
    def plot_signal(self, SignalName, figname = None):
        """
        Plots specified signal for general inspection
        """
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
        
        parameters = ['IP','BT','Ploss','KAPPA','ANE_DENSITY','AYC_NE', 'AYE_NE'] # AYC_NE, AYE_NE doesnt work
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
        
            for t in list_of_transitions:
                print('truing: {}'.format(parameter))
                t1 = t[0]   #time of tranision
                t_err1 = t[1] # lower bound time error
                t_err2 = t[2] # upper bound time error
                
                                # get  units
                units = self.data[parameter]['units']
                                # add to dict
                self._pandas['shot'].append(self.ShotNumber)
                if t in self._LHt:
                    self._pandas['LH/HL'].append('LH')
                elif t in self._HLt:
                    self._pandas['LH/HL'].append('HL')
                else: 
                    self._pandas['LH/HL'].append('WTF?') #:)   
                
                if parameter == 'Ploss' and t in self._HLt:
                        
                    #                # define all the stuff again for special case 
                    # DO NOT INTERPOLATE
                    
                    #try: units = s.data[parameter]['units']
                    #except: 
                    #    dic[parameter] = None
                    #    dic[parameter+'_e'] = None
                    #    continue
                    
                    import bisect
                    signal_ind = bisect.bisect(self.data['Ploss']['time'], t1) #get index of value we will use
                    print('################', self.data['Ploss']['time'][signal_ind-1])
                    signal_at_t1 = self.data['Ploss']['data'][signal_ind-1]        #bisect
                    signal_at_t1_err = self.data['Ploss']['errors'][signal_ind-1]         #bisect the previous value
                    
                    signal_t_err_range = 0.
                    signal_t_err_error_range = 0.
                    signal_t_err_spread = 0.
                
                    self._pandas['time'].append(t1)
                    self._pandas['units'].append(units)
                    self._pandas['param'].append(parameter)
                    self._pandas['p_value'].append(singal_at_t1)
                    self._pandas['p_value_err'].append(singal_at_t1_err)
                    self._pandas['perc_range_err'].append(np.round(singal_t_err_spread/singal_at_t1*100,2))
                    self._pandas['range_err'].append(singal_t_err_spread)
                    
                    continue # return to next parameter in parameters
                                    
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
                

                self._pandas['time'].append(t1)
                self._pandas['units'].append(units)
                self._pandas['param'].append(parameter)
                self._pandas['p_value'].append(singal_at_t1)
                self._pandas['p_value_err'].append(singal_at_t1_err)
                self._pandas['perc_range_err'].append(np.round(singal_t_err_spread/singal_at_t1*100,2))
                self._pandas['range_err'].append(singal_t_err_spread)
            
      
        # transform to pandas and save to excel
        print(self._pandas)
        for key in self._pandas.keys():
            print(key , len(self._pandas[key]))
        parameters_results = pd.DataFrame(self._pandas)
        writer = pd.ExcelWriter('parameters_output_{}.xlsx'.format(self.ShotNumber))
        parameters_results.to_excel(writer,'Sheet1')
        writer.save()
       
        
    def plot_JP(self, tlim = (0,0.5), ip = 'IP', wmhd = 'WMHD', coreTe = 'AYC_TE0', 
                ne = 'ANE_DENSITY', Dalpha = 'AIM_DA_TO', Bt = 'BT',
                PINJ = 'PINJ',Ploss = 'Ploss', POHM = 'POHM',
                plot_thomson = False, label_thomson = False):
        """
        Plot some signals together on single figure
        """
        
        # if ANE Density not avilable try to switch to AYC_NE
        if ne not in self.data.keys():
            if 'AYC_NE' in self.data.keys():
                ne = 'AYC_NE'
            else:
                ne='NE' #dumb data fix
        
        
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
        
        if plot_thomson:
            for i in self.data['AYC_NE']['time']:
                ax[plot_thomson].axvline(i,color='orange',linestyle='dashed')
            if label_thomson == True:
                for index, t in enumerate(self.data['AYE_NE']['time']):
                    ax[plot_thomson].text(t,0.,str(index))
        
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
        
        return fig, ax

    
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
            data=data*10e6/7 # what?
        
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
        
        if signame == 'WMHD':
            ax[panel].ticklabel_format(axis='y', style='sci', scilimits=(4,6))
        if signame == 'Ploss':
            ax[panel].ticklabel_format(axis='y', style='sci', scilimits=(0,0))
        if signame!='PINJ':
            ax[panel].annotate(r'$%s \ [%s]$' %(signame, units), xy=(0.01,0.7), xycoords='axes fraction', fontsize=11)
        #ax[panel].legend()
        
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
    
    def plot_JP_report(self, tlim = (0,0.5), ip = 'IP', wmhd = 'WMHD', coreTe = 'AYC_TE0', 
                ne = 'ANE_DENSITY', Dalpha = 'AIM_DA_TO', Bt = 'BT',
                Ploss = 'Ploss', PINJ = 'PINJ', POHM = 'POHM',
                plot_thomson = False, label_thomson = False,figsize=(12,8),fontsize=16,width=1):
        """
        Plot some signals together on single figure FOR REPORT
        """         
        n_signals = 7 # number of signals to be plotted
        # make figure and adjust boundaries
        plt.rcParams.update({'font.size': fontsize})
        fig, ax = plt.subplots(n_signals, sharex=True, figsize=figsize)
        
        fig.canvas.set_window_title('Shot {} FOR REPORT'.format(self.ShotNumber))
        fig.subplots_adjust(top=0.935,bottom=0.12,left=0.1,right=0.975,hspace=0.0,wspace=0.2)    
        # add figure title, labels, set time range
#        fig.suptitle('Shot %s' % (self. ShotNumber))
        ax[-1].set_xlabel('$time \ [s]$')
        ax[-1].set_xlim(tlim)
        
        if plot_thomson:
            for i in self.data['AYC_NE']['time']:
                ax[plot_thomson].axvline(i,color='orange',linestyle='dashed')
            if label_thomson == True:
                for index, t in enumerate(self.data['AYE_NE']['time']):
                    ax[plot_thomson].text(t,0.,str(index))
        
        # mark LH, HL transition points
        if self._LHt:
            for tset in self._LHt:  # tset = (time, -tlim_err, =tlim_err)
                for axes in ax:
                    axes.axvline(tset[0], c='g', lw=width, ls='--', clip_on=False,linewidth=width) #draw vertical line for transition
                    if tset[1] != 0:
                        axes.axvline(tset[1], c='g', lw=width, ls=':', clip_on=False, alpha= 0.6,linewidth=width) # draw error line
                    if tset[2] != 0:
                        axes.axvline(tset[2], c='g', lw=width, ls=':', clip_on=False, alpha= 0.6,linewidth=width) # draw error line
        if self._HLt:
            for tset in self._HLt:  # tset = (time, -tlim_err, +tlim_err)
                for axes in ax:
                    axes.axvline(tset[0], c='r', lw=width, ls='--', clip_on=False,linewidth=width)   
                    if tset[1] != 0:
                        axes.axvline(tset[1], c='r', lw=width, ls=':', clip_on=False, alpha= 0.6,linewidth=width)
                    if tset[2] != 0:
                        axes.axvline(tset[1], c='r', lw=width, ls=':', clip_on=False, alpha= 0.6,linewidth=width)
        
        for axes in ax: axes.axvline(0.248, c='gray', lw=width, ls='--', clip_on=False,linewidth=width)
        
        
        # plot plasma current, ax = 0
        self._plot_ax_sig2(ax, ip, 0, signame = 'I_{p}')
        # plot n_e
        self._plot_ax_sig2(ax, ne, 1, signame = 'n_{e}', plot_errors='fill', units=r'$x10^{20} m^{2}$', annot=False) # , units='m^{-2}')
        ax[1].annotate(r'$n_{e} \ [x10^{20} \ m^{-3}]$', xy=(0.01,0.65), xycoords='axes fraction', fontsize=11)
        # plot WMHD
        self._plot_ax_sig2(ax, wmhd,2 , signame = 'W_{MHD}')
        # plot core T_e
        self._plot_ax_sig2(ax, coreTe, 3 , signame = 'T_{e}^{core}',plot_errors='fill')
        # plot Dalpha of some kind
        self._plot_ax_sig2(ax, Dalpha, 4, signame = 'D_{\\alpha}', annot=False)
        ax[4].annotate(r'$D_{\alpha} \ [x10^{19} \ photons/sr. m^{2}. s]$', xy=(0.01,0.65), xycoords='axes fraction', fontsize=11)
        
        # plot B_T
        self._plot_ax_sig2(ax, Bt, 5, signame = 'B_{T}')
        # plot powers
        
        #self._plot_ax_sig2(ax, POHM, panel = 6, plot_errors='fill', annot=False) #Ploss = 'Ploss', PINJ = 'PINJ', POHM = 'POHM'
        self._plot_ax_sig2(ax, Ploss, panel = 6, signame = 'P_{loss}', plot_errors='fill')
        self._plot_ax_sig2(ax, PINJ, panel = 6, plot_errors='fill', annot=False)
        
        #ax[6].annotate(r'$P_{ohm}$ \ [MW]$', xy = (0.01,0.3), xycoords='axes fraction', fontsize=11, color='#8B0000')
        ax[6].annotate(r'$P_{inj} \ [MW]$', xy = (0.01,0.3), xycoords='axes fraction', fontsize=11, color='#8B0000')
        
        ax[2].set_ylim([0,0.12])
        ax[3].set_ylim([0,1.5])
        ax[4].set_ylim([0,4.5])
        ax[5].set_ylim([-0.8,-0.35])
        
        return fig, ax

    
    def _plot_ax_sig2(self, ax, sig, panel, signame='', plot_errors=False, units=None, label=None, annot=True):
        """ for use in plot_JP
        plots signal (sig) on subplot axes (ax[panel]) and labels with signame (and sig units)
        need to add error handeling
        Note: use units with care, as not longer automatic, maybe just use for presentation plots
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
        
        # correct other units
        if sig == 'ANE_DENSITY':
            data = data/1e20
        if sig == 'WMHD':
            data = data/1e6
            units = r'$MW$'
        if sig == 'AYC_TE0':
            data = data/1e3
            units = r'$keV$'
        if sig == 'Ploss':
            data = data/1e6
            units = r'$MW$'
            errors = errors/1e6
        if sig == 'AIM_DA_TO':
            data = data/1e19
        
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
        
        if annot:
            ax[panel].annotate(r'$%s \ [%s]$' %(signame, units), xy=(0.01,0.65), xycoords='axes fraction', fontsize=11)

        #ax[panel].legend()
    

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
        
    
        
    
    
    
    
    
    