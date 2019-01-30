# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 20:26:41 2018

@author: jb4317, Jan-Peter Baehner

Programme to visualise the analysed pedestal-data of Helium experiment
(from helium_pedestals.py)
Shots loaded (including H-mode phases):
Deuterium18SEP08
    20377
    20378
    20379
    20380
    20381 
Deuterium25SEP08
    (20474 - 2 H-modes) TS times are off
    (20475) TS times are off
    20476
    20479 - 2 H-modes
    20480 - 2 H-modes    
Helium06NOV08:
    (20832 - ref shot) - only Ip, Ne0 and ne0 signal, not inlcuded here
    20841
    20842
    20843
    20848
    20849
    20850
Helium11NOV08:
    20856
    20859
    20861 - no Ruby TS data!
    20862
    20863
Helium10JUN09:
    22647 - ref shot
    22649
    22650
    22652
    22653
    22656
"""

import pickle
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
#import scaling functions
from Pth_scalings import Martin08_scaling2,McDonald04_scaling2,McDonald04_scaling3,Takizuka04_scaling,Takizuka04_scalingZeff
#from helium_pedestals import data,rubyshots,ne_R_p,Te_R_p,pe_R_p,pedestal_data,pedestal_fits,LHdata,HLdata,xlims_fine

file=open( 'helium_pedestal.p', "rb" )
results=pickle.load(file) # set loaded data as initial guess file
file.close()

shotnos,tLH,tHL,data,rubyshots,ne_R_p,Te_R_p,pe_R_p,pedestal_data,pedestal_fits,LHdata,HLdata,xlims_fine=results

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

#%% time intervals of and around H-mode

# time intervals for each shot   
tlims=[[tLH[i]-0.01,tHL[i]+0.01] for i in range(len(shotnos))] # choose time interval around L-H/H-L transition - the TS time resolution is 4 ms, so this will produce 2 additional indices in ind before and after the L-H and H-L transition respectively 
tHmode=[[tLH[i],tHL[i]] for i in range(len(shotnos))] #exact time interval of H-mode
# index intervals for each shot
ind=[np.where((data[i]['NE']['time'] > tlims[i][0]) &  (data[i]['NE']['time'] < tlims[i][1]) )[0] for i in range(len(shotnos))] 
indHmode=[np.where((data[i]['NE']['time'] > tHmode[i][0]) &  (data[i]['NE']['time'] < tHmode[i][1]) )[0] for i in range(len(shotnos))]  # indices of data points INSIDE of H-mode


#%% Plot pedestal fits

## plot pedestal fits around L-H/H-L transition for each shot
#for i,shot in enumerate(shotnos):
#    for sig in ['NE','TE','PE']:
#        fig_i=plt.figure()
##        for j in range(len(ind[i])): # loop through all time slots in ind
##        for j in [0,1,2,3,-4,-3,-2,-1]: # plot 4 profiles around L-H and H-L transition respectively
#        for j in [1,2,-3,-2]: # plot 2 profiles around L-H and H-L transition respectively
#            x=np.linspace(*xlims_fine[i][j][sig],200) # x values evenly distributed over major radius
#            plt.plot(x,ped_tanh_odr2(pedestal_fits[i][sig][j][0],x),label='t=%.3f'%pedestal_data[i][sig]['time'][j])
#            plt.xlim(0.8,1.5)
#        plt.legend(loc='upper left')
#        plt.xlabel('major radius [m]')
#        plt.ylabel('%s [%s]'%(sig,data[i][sig]['units']))
#        plt.title('Helium experiment shot #%d \n %s edge pedestal profile fits' %(shot,sig))
#        plt.annotate('$I_p$= %.1fMA \n$B_t$= %.1fT'%(pedestal_data[i]['IP']/1e3,abs(pedestal_data[i]['BT'])), xy=(0.86,1.03),xycoords='axes fraction',fontsize=10)
#        plt.annotate('$t_{L-H}$= %.3fs \n$t_{H-L}$= %.3fs'%(tLH[i],tHL[i]), xy=(0.02,0.06),xycoords='axes fraction',fontsize=10)
#        plt.show()

# plot 22650 pedestal fits throughout H-mode transition for report
shot=22650
i=shotnos.index(shot)

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']
colors.append('k')#add black to have 11 colors, since len(ind[i][1:-1])=11

fig,axs = plt.subplots(3,sharex=True)
fig.subplots_adjust(hspace=0)
fig.set_size_inches(9, 10, True)
axs[0].set(title='Helium experiment shot #%d \n edge pedestal profile evolution' %shot,xlim=(1.225, 1.475), ylim=(0, 7.5))
axs[0].annotate('$I_p$= %.1fMA \n$B_t$= %.1fT'%(pedestal_data[i]['IP']/1e3,abs(pedestal_data[i]['BT'])), xy=(0.86,0.8),xycoords='axes fraction',fontsize=12)
axs[0].annotate('$n_{e}$ [$10^{19}$m$^{-3}$]', xy=(0.02,0.85),xycoords='axes fraction',fontsize=11)
axs[1].annotate('$T_{e}$ [k%s]'%data[i]['TE']['units'], xy=(0.02,0.85),xycoords='axes fraction',fontsize=11)
axs[1].set(ylim=(0, 0.85))
axs[2].annotate('$p_{e}$ [kPa]', xy=(0.02,0.85),xycoords='axes fraction',fontsize=11)
axs[2].set(xlabel='major radius [m]', ylim=(0, 7.5))
axs[2].annotate('$t_{LH}$= %.3fs \n$t_{HL}$= %.3fs'%(tLH[i],tHL[i]), xy=(0.85,0.8),xycoords='axes fraction',fontsize=11)
norms=[1e19,1e3,1e3]
for k,sig in enumerate(['NE','TE','PE']):
    for t in range(len(ind[i][1:-1])): # loop through all time slots in ind
        j=t+1
        x=np.linspace(*xlims_fine[i][j][sig],200) # x values evenly distributed over major radius
        axs[k].plot(x,ped_tanh_odr2(pedestal_fits[i][sig][j][0],x)/norms[k],label='t=%.3f'%pedestal_data[i][sig]['time'][j],color=colors[t],lw=1)
        axs[k].plot(pedestal_data[i][sig]['radii'][j],np.array(pedestal_data[i][sig]['data'][j])/norms[k],'x',color=colors[t])
axs[1].legend(loc='lower right')

#figname='../Plots_and_graphics/pedestal_evolustion_shot%d.png'%shot
#plt.savefig(figname,format='png',dpi=100)

#%% plot L-H and H-L data (Pth and pedestal height and width) for several shots
#only ante transitus (at)  ###################### and post transitus (pt)
        
#mean values of shots for plasma current and toroidal magnetic field etc.:
#this may need some changing if IP and BT values differ too much
Ip_=np.mean([pedestal_data[i]['IP'] for i in range(len(shotnos))]) # averaged plasma current
Bt_=np.mean([pedestal_data[i]['BT'] for i in range(len(shotnos))]) # averaged toroidal magnetic field

#average other values only over transition time slices:
# index intervals for each shot over H-mode (+- 10ms)
indEFIT=[np.where((data[i]['RGEO']['time'] > tlims[i][0]) &  (data[i]['RGEO']['time'] < tlims[i][1]) )[0] for i in range(len(shotnos))] 

R_=np.mean([np.mean(data[i]['RGEO']['data'][list(indEFIT[i][:4])+list(indEFIT[i][-4:])]) for i in range(len(shotnos))]) # averaged major radius
a_=np.mean([np.mean(data[i]['AMIN']['data'][list(indEFIT[i][:4])+list(indEFIT[i][-4:])]) for i in range(len(shotnos))]) # averaged minor radius
S_=np.mean([np.mean(data[i]['SAREA']['data'][list(indEFIT[i][:4])+list(indEFIT[i][-4:])]) for i in range(len(shotnos))]) # averaged plasma surface area
Scross_=np.mean([np.mean(data[i]['AREA']['data'][list(indEFIT[i][:4])+list(indEFIT[i][-4:])]) for i in range(len(shotnos))]) # averaged plasma cross-sectional area
k_=np.mean([np.mean(data[i]['KAPPA']['data'][list(indEFIT[i][:4])+list(indEFIT[i][-4:])]) for i in range(len(shotnos))]) # averaged elongation
Vloop_=np.mean([np.mean(data[i]['Vloop']['data'][list(indEFIT[i][:4])+list(indEFIT[i][-4:])]) for i in range(len(shotnos))])  # averaged plasma surface loop voltage
W_=np.mean([np.mean(data[i]['WMHD']['data'][list(indEFIT[i][:4])+list(indEFIT[i][-4:])]) for i in range(len(shotnos))]) # averaged stored plasma energy
V_=np.mean([np.mean(data[i]['VOL']['data'][list(indEFIT[i][:4])+list(indEFIT[i][-4:])]) for i in range(len(shotnos))]) # averaged plasma volume
   
###############################################################################
        
fig=plt.figure()
plt.title('L-H/H-L transition power threshold \n in He and D')
plt.annotate('$I_p$= %.1fMA \n$B_t$= %.1fT'%(Ip_/1e3,Bt_), xy=(0.83,0.87),xycoords='axes fraction',fontsize=10)
plt.annotate('L-H', xy=(0.02,0.9),xycoords='axes fraction',fontsize=10,color='g')
plt.annotate('H-L', xy=(0.02,0.85),xycoords='axes fraction',fontsize=10,color='r')
#plt.annotate('o L-H p.t.', xy=(0.02,0.8),xycoords='axes fraction',fontsize=10,color='g')
plt.annotate('x Helium \n$\diamond$ Deuterium', xy=(0.02,0.75),xycoords='axes fraction',fontsize=10)
plt.ylabel('$P_{loss}$ [M%s]'%LHdata[0]['Plossat']['units'])
plt.xlabel(r'$\bar{n}_{e}$ [$10^{20} m^{-3}$ ]')#%s%LHdata[0]['NE_at']['units']
#plt.yscale('log')
for i,shot in enumerate(shotnos):
    # loop through shots and only plot the transition data, if the error is not larger than twice the value itself
    # i.e. only plot reasonable values
    if abs(LHdata[i]['Plossat']['data'])>LHdata[i]['Plossat']['errors']:
        if i<8:
            plt.errorbar(LHdata[i]['NE_at']['data']/1e20, LHdata[i]['Plossat']['data']/1e6,xerr=LHdata[i]['NE_at']['errors']/1e20,yerr=LHdata[i]['Plossat']['errors']/1e6, fmt='d',color='g',ecolor='g')#
        else:
            plt.errorbar(LHdata[i]['NE_at']['data']/1e20, LHdata[i]['Plossat']['data']/1e6,xerr=LHdata[i]['NE_at']['errors']/1e20,yerr=LHdata[i]['Plossat']['errors']/1e6, fmt='x',color='g',ecolor='g')#
#    if abs(LHdata[i]['Plosspt']['data'])>LHdata[i]['Plosspt']['errors']:
#        plt.errorbar(LHdata[i]['NE_pt']['data']/1e20, LHdata[i]['Plosspt']['data']/1e6,xerr=LHdata[i]['NE_pt']['errors']/1e20,yerr=LHdata[i]['Plosspt']['errors']/1e6, fmt='o',color='g',ecolor='g')#
    if abs(HLdata[i]['Plossat']['data'])>HLdata[i]['Plossat']['errors']:
        if i<8:
            plt.errorbar(HLdata[i]['NE_at']['data']/1e20, HLdata[i]['Plossat']['data']/1e6,xerr=HLdata[i]['NE_at']['errors']/1e20,yerr=HLdata[i]['Plossat']['errors']/1e6, fmt='d',color='r',ecolor='r') #
        else:
            plt.errorbar(HLdata[i]['NE_at']['data']/1e20, HLdata[i]['Plossat']['data']/1e6,xerr=HLdata[i]['NE_at']['errors']/1e20,yerr=HLdata[i]['Plossat']['errors']/1e6, fmt='x',color='r',ecolor='r') #

# add Pth scalings:
xlims=[plt.gca().get_xlim()[0],0.6]
ne_=np.linspace(*xlims)

#Martin08 scaling
#axs[1].plot(ne_,Martin08_scaling1(ne_,Bt_,a_,R_),'--',c='b')
plt.plot(ne_,Martin08_scaling2(ne_,Bt_,S_),'--',c='0.5') # this does not differ much from plot above
plt.annotate('$P_{th,Martin08}^D$', xy=(xlims[1]*0.85,Martin08_scaling2(ne_[-1],Bt_,S_)*0.3),fontsize=9, color='0.2', rotation=2)#,xycoords='axes fraction'/plt.gca().get_ylim()[1]

#McDonald04 scaling for He
plt.plot(ne_,McDonald04_scaling2(ne_,Bt_,S_),'-.',c='0.5') # this does not differ much from plot above
plt.annotate('$P_{th,McDonald04}^{He}$', xy=(xlims[1]*0.85,McDonald04_scaling2(ne_[-1],Bt_,S_)*1.3),fontsize=9, color='0.2', rotation=2)#,xycoords='axes fraction'/plt.gca().get_ylim()[1]

#Takizuka04 scaling with A, scaled for He with McDonald04
plt.plot(ne_,McDonald04_scaling3(Takizuka04_scaling(ne_,Bt_,S_,a_,R_,Ip_*1e3,0,0,0,0,0,0)[0]),'-',c='0.5') # this does not differ much from plot above
plt.annotate('$P_{th,Takizuka04}^{He}$', xy=(xlims[1]*0.85,McDonald04_scaling3(Takizuka04_scaling(ne_[-1],Bt_,S_,a_,R_,Ip_*1e3,0,0,0,0,0,0)[0])*0.8),fontsize=9, color='0.2', rotation=8)#,xycoords='axes fraction'/plt.gca().get_ylim()[1]

#Takizuka04 scaling with A, scaled for He with McDonald04, including Zeff effect
Z_eff=2.5 #assume Zeff=2.5, no measurement available. Typically Z_eff=1.5 in D plasmas
plt.plot(ne_,McDonald04_scaling3(Takizuka04_scalingZeff(ne_,Bt_,S_,a_,R_,Ip_*1e3,Scross_,k_,Vloop_,W_,V_,Z_eff)),':',c='0.5')
plt.annotate('$P_{th,Takizuka04,Z_{eff}}^{He}$', xy=(xlims[1]*0.85,McDonald04_scaling3(Takizuka04_scalingZeff(ne_[-1],Bt_,S_,a_,R_,Ip_*1e3,Scross_,k_,Vloop_,W_,V_,2.5))*1.1),fontsize=9, color='0.2', rotation=10)#,xycoords='axes fraction'/plt.gca().get_ylim()[1]

# set lower limit of y axis of both subplots to zero and xlimits from before:
#plt.ylim([0.1,10])
plt.xlim(xlims)
plt.ylim(0,10)
plt.show()

#%% Ploss vs Pth,scaling      
fig=plt.figure()
plt.title('L-H/H-L transition power threshold \n in He and D')
plt.annotate('$I_p$= %.1fMA \n$B_t$= %.1fT'%(Ip_/1e3,Bt_), xy=(0.83,0.87),xycoords='axes fraction',fontsize=10)
plt.annotate('L-H', xy=(0.02,0.9),xycoords='axes fraction',fontsize=10,color='g')
plt.annotate('H-L', xy=(0.02,0.85),xycoords='axes fraction',fontsize=10,color='r')
plt.annotate('x Helium \n$\diamond$ Deuterium', xy=(0.02,0.75),xycoords='axes fraction',fontsize=10)
plt.ylabel('$P_{loss}$ [M%s]'%LHdata[0]['Plossat']['units'])
plt.xlabel('$P_{th,Takizuka04}^{He}$ [MW]')

for i,shot in enumerate(shotnos):
    # loop through shots and only plot the transition data, if the error is not larger than twice the value itself
    # i.e. only plot reasonable values
    Pth_sc_D_LH=Takizuka04_scaling(LHdata[i]['NE_at']['data']/1e20,
                                   LHdata[i]['BTat']['data'],#Bt_
                                   LHdata[i]['SAREAat']['data'],#S_
                                   LHdata[i]['AMINat']['data'],#a_
                                   LHdata[i]['RGEOat']['data'],#R_
                                   LHdata[i]['IPat']['data']*1e3,#,#Ip_ in A
                                   LHdata[i]['NE_at']['errors']/1e20,
                                   0,#LHdata[i]['BTat']['errors'],#Bt_
                                   0,#LHdata[i]['SAREAat']['errors'],#S_
                                   0,#LHdata[i]['AMINat']['errors'],#a_
                                   0,#LHdata[i]['RGEOat']['errors'],#R_
                                   0)#LHdata[i]['IPat']['errors']*1e3)#,#Ip_ in A
    Pth_sc_LH=McDonald04_scaling3(Pth_sc_D_LH[0])
    Pth_sc_LH_err=McDonald04_scaling3(Pth_sc_D_LH[1])
    if i<8:
        plt.errorbar(Pth_sc_LH, LHdata[i]['Plossat']['data']/1e6,xerr=Pth_sc_LH_err,yerr=LHdata[i]['Plossat']['errors']/1e6,color='g',ecolor='g', fmt='d')#
    else:
        plt.errorbar(Pth_sc_LH, LHdata[i]['Plossat']['data']/1e6,xerr=Pth_sc_LH_err,yerr=LHdata[i]['Plossat']['errors']/1e6,color='g',ecolor='g', fmt='x')#
    try:
        Pth_sc_D_HL=Takizuka04_scaling(HLdata[i]['NE_at']['data']/1e20,
                                       HLdata[i]['BTat']['data'],#Bt_
                                       HLdata[i]['SAREAat']['data'],#S_
                                       HLdata[i]['AMINat']['data'],#a_
                                       HLdata[i]['RGEOat']['data'],#R_
                                       HLdata[i]['IPat']['data']*1e3,#Ip_ in A
                                       HLdata[i]['NE_at']['errors']/1e20,
                                       0,#HLdata[i]['BTat']['errors'],#Bt_
                                       0,#HLdata[i]['SAREAat']['errors'],#S_
                                       0,#HLdata[i]['AMINat']['errors'],#a_
                                       0,#HLdata[i]['RGEOat']['errors'],#R_
                                       0)#HLdata[i]['IPat']['errors']*1e3)#Ip_ in A
        Pth_sc_HL=McDonald04_scaling3(Pth_sc_D_HL[0])
        Pth_sc_HL_err=McDonald04_scaling3(Pth_sc_D_HL[1])
        if i<8:
            plt.errorbar(Pth_sc_HL, HLdata[i]['Plossat']['data']/1e6,xerr=Pth_sc_HL_err,yerr=HLdata[i]['Plossat']['errors']/1e6,color='r',ecolor='r', fmt='d') #
        else:
            plt.errorbar(Pth_sc_HL, HLdata[i]['Plossat']['data']/1e6,xerr=Pth_sc_HL_err,yerr=HLdata[i]['Plossat']['errors']/1e6,color='r',ecolor='r', fmt='x') #
    except TypeError:
        pass
#predicted value for ITER as comparison:
#plt.scatter(McDonald04_scaling3(45),McDonald04_scaling3(45))
#plt.annotate('ITER', xy=(45,55),fontsize=10,color='#1f77b4', weight='bold')
# add diagonal:
#lims=[min(plt.gca().get_xlim()[0],plt.gca().get_ylim()[0]),max(plt.gca().get_xlim()[1],plt.gca().get_ylim()[1])]
lims=[1,10]#max(plt.gca().get_xlim()[1],plt.gca().get_ylim()[1])+5]#
plt.plot(lims,lims,'--',c='0.5',lw=0.5)
plt.xlim(lims)
plt.ylim(lims)
plt.xscale('log')
plt.yscale('log')
plt.show()

#%% magnetic configuration of shots
fig=plt.figure()
plt.title('Magnetic configuration parameter \n at transition times in He and D shots')
#plt.annotate('$I_p$= %.1fMA \n$B_t$= %.1fT'%(Ip_/1e3,Bt_), xy=(0.86,1.03),xycoords='axes fraction',fontsize=10)
plt.annotate('x L-H', xy=(0.86,0.52),xycoords='axes fraction',fontsize=10)
plt.annotate('o H-L', xy=(0.86,0.48),xycoords='axes fraction',fontsize=10)
kappas=[LHdata[i]['KAPPAat']['data'] for i in range(len(shotnos))]+[HLdata[i]['KAPPAat']['data'] for i in range(len(shotnos))]
plt.annotate(r'Elongation $\langle\kappa\rangle$=%.3f; std=%.3f'%(np.mean(kappas),np.std(kappas)), xy=(0.02,0.55),xycoords='axes fraction',fontsize=10,color='g')
x1zs=[LHdata[i]['X1Zat']['data'] for i in range(len(shotnos))]+[HLdata[i]['X1Zat']['data'] for i in range(len(shotnos))]
plt.annotate(r'$\langle|Z_{X-point}^{lower}|\rangle$=%.3f m; std=%.3f m'%(abs(np.mean(x1zs)),np.std(x1zs)), xy=(0.02,0.5),xycoords='axes fraction',fontsize=10,color='r')
x2zs=[LHdata[i]['X2Zat']['data'] for i in range(len(shotnos))]+[HLdata[i]['X2Zat']['data'] for i in range(len(shotnos)) if HLdata[i]['X2Zat']['data']>0]
plt.annotate(r'$\langle Z_{X-point}^{upper}\rangle$=%.3f m; std=%.3f m'%(np.mean(x2zs),np.std(x2zs)), xy=(0.02,0.45),xycoords='axes fraction',fontsize=10,color='b')
plt.xlabel('Number of shot')
#plt.yscale('log')
for i,shot in enumerate(shotnos):
    # loop through shots and only plot the transition data, if the error is not larger than twice the value itself
    # i.e. only plot reasonable values
    plt.errorbar(i,LHdata[i]['KAPPAat']['data'],xerr=None,yerr=LHdata[i]['KAPPAat']['errors'],color='g',ecolor='g', fmt='x')#
    plt.errorbar(i,abs(LHdata[i]['X1Zat']['data']),xerr=None,yerr=LHdata[i]['X1Zat']['errors'],color='r',ecolor='r', fmt='x')#
    plt.errorbar(i,LHdata[i]['X2Zat']['data'],xerr=None,yerr=LHdata[i]['X2Zat']['errors'],color='b',ecolor='b', fmt='x')#
    try:
        plt.errorbar(i,HLdata[i]['KAPPAat']['data'],xerr=None,yerr=HLdata[i]['KAPPAat']['errors'],color='g',ecolor='g', fmt='o') #
        plt.errorbar(i,abs(HLdata[i]['X1Zat']['data']),xerr=None,yerr=HLdata[i]['X1Zat']['errors'],color='r',ecolor='r', fmt='o') #
        if HLdata[i]['X2Zat']['data']>0:
            plt.errorbar(i,HLdata[i]['X2Zat']['data'],xerr=None,yerr=HLdata[i]['X2Zat']['errors'],color='b',ecolor='b', fmt='o') #
    except TypeError:
        pass
plt.xticks(np.arange(len(shotnos)), [str(shot) for shot in shotnos], rotation=-60)
plt.show()

#%%pedestal value plot   
## only ante transitus (at) values
plotsigs=['NE_ped','TE_ped','PE_ped']

# pedestal heights ############################################################
plotsiglabels=['$n_e$ pedestal height [$10^{19}$','$T_{e}$ pedestal height [k','$p_{e}$ pedestal height [kPa]']
norm=[1e19,1e3,1e3]

fig,axs=plt.subplots(3,sharex=True)
fig.subplots_adjust(hspace=0)
axs[0].set(title='L-H/H-L transition pedestal heights \n in He and D')
axs[0].annotate('$I_p$= %.1fMA \n$B_t$= %.1fT'%(Ip_/1e3,Bt_), xy=(0.86,1.03),xycoords='axes fraction',fontsize=10)
axs[0].annotate('L-H', xy=(0.01,0.65),xycoords='axes fraction',fontsize=10,color='g')
axs[0].annotate('H-L', xy=(0.01,0.5),xycoords='axes fraction',fontsize=10,color='r')
axs[0].annotate(r'$\diamond$ D', xy=(0.01,0.35),xycoords='axes fraction',fontsize=10)
axs[2].set_xlabel(r'$\bar{n}_{e}$ [$10^{20} m^{-3}$ ]')#%s%LHdata[0]['NE_at']['units']

for j,sig in enumerate(plotsigs):
    for i,shot in enumerate(shotnos):
    # loop through shots and only plot the transition data, if the error is not larger than twice the value itself
    # i.e. only plot reasonable values
        #if LHdata[i][sig+'_heightat']['data']>0 and LHdata[i][sig+'_heightat']['data']/norm[j]<10:
        if abs(LHdata[i][sig+'_heightat']['resvar'])<10 and abs(LHdata[i][sig+'_heightat']['data'])>LHdata[i][sig+'_heightat']['errors']:
            if i<8:
                axs[j].errorbar(LHdata[i]['NE_at']['data']/1e19, LHdata[i][sig+'_heightat']['data']/norm[j], xerr=LHdata[i]['NE_at']['errors']/1e19, yerr=LHdata[i][sig+'_heightat']['errors']/norm[j],color='g',ecolor='g', fmt='d')#
            else:
                axs[j].errorbar(LHdata[i]['NE_at']['data']/1e19, LHdata[i][sig+'_heightat']['data']/norm[j], xerr=LHdata[i]['NE_at']['errors']/1e19, yerr=LHdata[i][sig+'_heightat']['errors']/norm[j],color='g',ecolor='g')#, fmt='x'
        #if HLdata[i][sig+'_heightat']['data']>0 and HLdata[i][sig+'_height']['data']/norm[j]<10:
        if abs(HLdata[i][sig+'_heightat']['resvar'])<10 and abs(HLdata[i][sig+'_heightat']['data'])>HLdata[i][sig+'_heightat']['errors']:
            if i<8:
                axs[j].errorbar(HLdata[i]['NE_at']['data']/1e19, HLdata[i][sig+'_heightat']['data']/norm[j], xerr=HLdata[i]['NE_at']['errors']/1e19, yerr=HLdata[i][sig+'_heightat']['errors']/norm[j],color='r',ecolor='r', fmt='d') #
            else:
                axs[j].errorbar(HLdata[i]['NE_at']['data']/1e19, HLdata[i][sig+'_heightat']['data']/norm[j], xerr=HLdata[i]['NE_at']['errors']/1e19, yerr=HLdata[i][sig+'_heightat']['errors']/norm[j],color='r',ecolor='r') #, fmt='x'
    if j<len(plotsigs)-1:
        axs[j].annotate(plotsiglabels[j]+'%s]'%LHdata[i][sig+'_heightat']['units'], xy=(0.01,0.8),xycoords='axes fraction',fontsize=9)
    else:
        axs[j].annotate(plotsiglabels[j], xy=(0.01,0.8),xycoords='axes fraction',fontsize=9)    
    axs[j].set(ylim=0)

# pedestal widths #############################################################
## only ante transitus (at) ###################################################
plotsiglabels=['$\Delta n_e$ pedestal width [','$\Delta T_{e}$ pedestal width [','$\Delta p_{e}$ pedestal width [']

fig2,axs=plt.subplots(3,sharex=True)
fig2.subplots_adjust(hspace=0)
axs[0].set(title='L-H/H-L transition pedestal widths \n in He and D')
axs[0].annotate('$I_p$= %.1fMA \n$B_t$= %.1fT'%(Ip_/1e3,Bt_), xy=(0.86,1.03),xycoords='axes fraction',fontsize=10)
axs[0].annotate('L-H', xy=(0.85,0.85),xycoords='axes fraction',fontsize=10,color='g')
axs[0].annotate('H-L', xy=(0.85,0.7),xycoords='axes fraction',fontsize=10,color='r')
axs[0].annotate(r'$\diamond$ D', xy=(0.85,0.55),xycoords='axes fraction',fontsize=10)
axs[2].set_xlabel(r'$\bar{n}_{e}$ [$10^{20} m^{-3}$ ]')#%s%LHdata[0]['NE_at']['units']

ylims=[(0, 10),(-0.5, 1),(-5, 10)]
for j,sig in enumerate(plotsigs):
    for i,shot in enumerate(shotnos):
    # loop through shots and only plot the transition data, if the error is not larger than twice the value itself
    # i.e. only plot reasonable values
        #if LHdata[i][sig+'_widthat']['data']<1:
        if abs(LHdata[i][sig+'_widthat']['resvar'])<10 and abs(LHdata[i][sig+'_widthat']['data'])>LHdata[i][sig+'_widthat']['errors']:
            if i<8:
                axs[j].errorbar(LHdata[i]['NE_at']['data']/1e19, LHdata[i][sig+'_widthat']['data'], xerr=LHdata[i]['NE_at']['errors']/1e19, yerr=LHdata[i][sig+'_widthat']['errors'],color='g',ecolor='g', fmt='d')#
            else:
                axs[j].errorbar(LHdata[i]['NE_at']['data']/1e19, LHdata[i][sig+'_widthat']['data'], xerr=LHdata[i]['NE_at']['errors']/1e19, yerr=LHdata[i][sig+'_widthat']['errors'],color='g',ecolor='g')#, fmt='x'
        #if HLdata[i][sig+'_widthat']['data']<1:
        if abs(HLdata[i][sig+'_widthat']['resvar'])<10 and abs(HLdata[i][sig+'_widthat']['data'])>HLdata[i][sig+'_widthat']['errors']:
            if i<8:
                axs[j].errorbar(HLdata[i]['NE_at']['data']/1e19, HLdata[i][sig+'_widthat']['data'], xerr=HLdata[i]['NE_at']['errors']/1e19, yerr=HLdata[i][sig+'_widthat']['errors'],color='r',ecolor='r', fmt='d')#
            else:
                axs[j].errorbar(HLdata[i]['NE_at']['data']/1e19, HLdata[i][sig+'_widthat']['data'], xerr=HLdata[i]['NE_at']['errors']/1e19, yerr=HLdata[i][sig+'_widthat']['errors'],color='r',ecolor='r')#, fmt='x'
    
    axs[j].annotate(plotsiglabels[j]+'%s]'%LHdata[i][sig+'_widthat']['units'], xy=(0.01,0.8),xycoords='axes fraction',fontsize=9)  
    axs[j].set(ylim=0)


#%% inboard vs outboard pedestal plots from Ruby TS fits
    
fig5,axs=plt.subplots(3,2)
axs[0,0].set(title='Inboard and outboard pedestal heights \n in He and D H-modes')
axs[0,1].set(title='Inboard and outboard pedestal widths \n in He and D H-modes')
axs[0,1].annotate('$I_p$= %.1fMA \n$B_t$= %.1fT'%(Ip_/1e3,Bt_), xy=(0.75,0.8),xycoords='axes fraction',fontsize=10)
          
## pedestal heights ############################################################
#ne_p_lims=[1,5.1]
#axs[0,0].plot(ne_p_lims,ne_p_lims,'--',c='0.5',lw=0.5)
#axs[0,0].set(xlim=ne_p_lims,ylim=ne_p_lims,xlabel='inboard $n_{e,ped}$ [$10^{19} m^{-3}$]',ylabel='outboard $n_{e,ped}$ [$10^{19} m^{-3}$]')
#
#Te_p_lims=[0.13,0.35]
#axs[1,0].plot(Te_p_lims,Te_p_lims,'--',c='0.5',lw=0.5)
#axs[1,0].set(xlim=Te_p_lims,ylim=Te_p_lims,xlabel='inboard $T_{e,ped}$ [keV]',ylabel='outboard $T_{e,ped}$ [keV]')
#
#pe_p_lims=[0,4]
#axs[2,0].plot(pe_p_lims,pe_p_lims,'--',c='0.5',lw=0.5)
#axs[2,0].set(xlim=pe_p_lims,ylim=pe_p_lims,xlabel='inboard $p_{e,ped}$ [kPa]',ylabel='outboard $p_{e,ped}$ [kPa]')
#
## pedestal widths #############################################################
#ne_pw_lims=[0,0.05]
#axs[0,1].plot(ne_pw_lims,ne_pw_lims,'--',c='0.5',lw=0.5)
#axs[0,1].set(xlim=ne_pw_lims,ylim=ne_pw_lims,xlabel='inboard $\Delta n_e$ [m]',ylabel='outboard $\Delta n_e$ [m]')
#
#Te_pw_lims=[0.005,0.06]
#axs[1,1].plot(Te_pw_lims,Te_pw_lims,'--',c='0.5',lw=0.5)
#axs[1,1].set(xlim=Te_pw_lims,ylim=Te_pw_lims,xlabel='inboard $\Delta T_{e}$ [m]',ylabel='outboard $\Delta T_{e}$ [m]')
#
#pe_pw_lims=[0,0.1]
#axs[2,1].plot(pe_pw_lims,pe_pw_lims,'--',c='0.5',lw=0.5)
#axs[2,1].set(xlim=pe_pw_lims,ylim=pe_pw_lims,xlabel='inboard $\Delta p_{e}$ [m]',ylabel='outboard $\Delta p_{e}$ [m]')

# plot data from selected shots with Ruby TS fit:
for i,shot in enumerate(rubyshots):#
    # pedestal heights ############################################################
    if abs(ne_R_p[i]['inboard'][0][0])>ne_R_p[i]['inboard'][1][0] and abs(ne_R_p[i]['outboard'][0][0])>ne_R_p[i]['outboard'][1][0] and abs(ne_R_p[i]['inboard'][0][1])>ne_R_p[i]['inboard'][1][1] and abs(ne_R_p[i]['outboard'][0][1])>ne_R_p[i]['outboard'][1][1]:#abs(ne_R_p[i]['inboard'][2])<10 and abs(ne_R_p[i]['outboard'][2])<10 and 
        axs[0,0].errorbar((ne_R_p[i]['inboard'][0][0]+ne_R_p[i]['inboard'][0][1])/1e19, (ne_R_p[i]['outboard'][0][0]+ne_R_p[i]['outboard'][0][1])/1e19, xerr=np.sqrt(ne_R_p[i]['inboard'][1][0]**2+ne_R_p[i]['inboard'][1][1]**2)/1e19, yerr=np.sqrt(ne_R_p[i]['outboard'][1][0]**2+ne_R_p[i]['outboard'][1][1]**2)/1e19,label='#%s'%shot)
    if abs(Te_R_p[i]['inboard'][0][0])>Te_R_p[i]['inboard'][1][0] and abs(Te_R_p[i]['outboard'][0][0])>Te_R_p[i]['outboard'][1][0] and abs(Te_R_p[i]['inboard'][0][1])>Te_R_p[i]['inboard'][1][1] and abs(Te_R_p[i]['outboard'][0][1])>Te_R_p[i]['outboard'][1][1]:#abs(Te_R_p[i]['inboard'][2])<10 and abs(Te_R_p[i]['outboard'][2])<10 and 
        axs[1,0].errorbar((Te_R_p[i]['inboard'][0][0]+Te_R_p[i]['inboard'][0][1])/1e3, (Te_R_p[i]['outboard'][0][0]+Te_R_p[i]['outboard'][0][1])/1e3, xerr=np.sqrt(Te_R_p[i]['inboard'][1][0]**2+Te_R_p[i]['inboard'][1][1]**2)/1e3, yerr=np.sqrt(Te_R_p[i]['outboard'][1][0]**2+Te_R_p[i]['outboard'][1][1]**2)/1e3,label='#%s'%shot)
    if abs(pe_R_p[i]['inboard'][0][0])>pe_R_p[i]['inboard'][1][0] and abs(pe_R_p[i]['outboard'][0][0])>pe_R_p[i]['outboard'][1][0] and abs(pe_R_p[i]['inboard'][0][1])>pe_R_p[i]['inboard'][1][1] and abs(pe_R_p[i]['outboard'][0][1])>pe_R_p[i]['outboard'][1][1]:#abs(pe_R_p[i]['inboard'][2])<10 and abs(pe_R_p[i]['outboard'][2])<10 and 
        axs[2,0].errorbar((pe_R_p[i]['inboard'][0][0]+pe_R_p[i]['inboard'][0][1])/1e3, (pe_R_p[i]['outboard'][0][0]+pe_R_p[i]['outboard'][0][1])/1e3, xerr=np.sqrt(pe_R_p[i]['inboard'][1][0]**2+pe_R_p[i]['inboard'][1][1]**2)/1e3, yerr=np.sqrt(pe_R_p[i]['outboard'][1][0]**2+pe_R_p[i]['outboard'][1][1]**2)/1e3,label='#%s'%shot)
    # pedestal widths #############################################################
    if abs(ne_R_p[i]['inboard'][0][3])>ne_R_p[i]['inboard'][1][3] and abs(ne_R_p[i]['outboard'][0][3])>ne_R_p[i]['outboard'][1][3]: #abs(ne_R_p[i]['inboard'][2])<10 and abs(ne_R_p[i]['outboard'][2])<10 and 
        axs[0,1].errorbar(ne_R_p[i]['inboard'][0][3], ne_R_p[i]['outboard'][0][3], xerr=ne_R_p[i]['inboard'][1][3], yerr=ne_R_p[i]['outboard'][1][3],label='#%s'%shot)#, fmt=shotmarker[i]
    if abs(Te_R_p[i]['inboard'][0][3])>Te_R_p[i]['inboard'][1][3] and abs(Te_R_p[i]['outboard'][0][3])>Te_R_p[i]['outboard'][1][3]: #abs(Te_R_p[i]['inboard'][2])<10 and abs(Te_R_p[i]['outboard'][2])<10 and 
        axs[1,1].errorbar(Te_R_p[i]['inboard'][0][3], Te_R_p[i]['outboard'][0][3], xerr=Te_R_p[i]['inboard'][1][3], yerr=Te_R_p[i]['outboard'][1][3],label='#%s'%shot)#, fmt=shotmarker[i]
    if abs(pe_R_p[i]['inboard'][0][3])>pe_R_p[i]['inboard'][1][3] and abs(pe_R_p[i]['outboard'][0][3])>pe_R_p[i]['outboard'][1][3]: #abs(pe_R_p[i]['inboard'][2])<10 and abs(pe_R_p[i]['outboard'][2])<10 and 
        axs[2,1].errorbar(pe_R_p[i]['inboard'][0][3], pe_R_p[i]['outboard'][0][3], xerr=pe_R_p[i]['inboard'][1][3], yerr=pe_R_p[i]['outboard'][1][3],label='#%s'%shot)#, fmt=shotmarker[i]

# pedestal heights ############################################################
ne_p_lims=[min(axs[0,0].get_xlim()[0],axs[0,0].get_ylim()[0]),max(axs[0,0].get_xlim()[1],axs[0,0].get_ylim()[1])]#[1,5.1]
axs[0,0].plot(ne_p_lims,ne_p_lims,'--',c='0.5',lw=0.5)
axs[0,0].set(xlim=ne_p_lims,ylim=ne_p_lims,xlabel='inboard $n_{e,ped}$ [$10^{19} m^{-3}$]',ylabel='outboard $n_{e,ped}$ [$10^{19} m^{-3}$]')

Te_p_lims=[min(axs[1,0].get_xlim()[0],axs[1,0].get_ylim()[0]),max(axs[1,0].get_xlim()[1],axs[1,0].get_ylim()[1])]#[0.13,0.35]
axs[1,0].plot(Te_p_lims,Te_p_lims,'--',c='0.5',lw=0.5)
axs[1,0].set(xlim=Te_p_lims,ylim=Te_p_lims,xlabel='inboard $T_{e,ped}$ [keV]',ylabel='outboard $T_{e,ped}$ [keV]')

pe_p_lims=[min(axs[2,0].get_xlim()[0],axs[2,0].get_ylim()[0]),max(axs[2,0].get_xlim()[1],axs[2,0].get_ylim()[1])]#[0,4]
axs[2,0].plot(pe_p_lims,pe_p_lims,'--',c='0.5',lw=0.5)
axs[2,0].set(xlim=pe_p_lims,ylim=pe_p_lims,xlabel='inboard $p_{e,ped}$ [kPa]',ylabel='outboard $p_{e,ped}$ [kPa]')

# pedestal widths #############################################################
ne_pw_lims=[min(axs[0,1].get_xlim()[0],axs[0,1].get_ylim()[0]),max(axs[0,1].get_xlim()[1],axs[0,1].get_ylim()[1])]#[0,0.05]
axs[0,1].plot(ne_pw_lims,ne_pw_lims,'--',c='0.5',lw=0.5)
axs[0,1].set(xlim=ne_pw_lims,ylim=ne_pw_lims,xlabel='inboard $\Delta n_e$ [m]',ylabel='outboard $\Delta n_e$ [m]')

Te_pw_lims=[min(axs[1,1].get_xlim()[0],axs[1,1].get_ylim()[0]),max(axs[1,1].get_xlim()[1],axs[1,1].get_ylim()[1])]#[0.005,0.06]
axs[1,1].plot(Te_pw_lims,Te_pw_lims,'--',c='0.5',lw=0.5)
axs[1,1].set(xlim=Te_pw_lims,ylim=Te_pw_lims,xlabel='inboard $\Delta T_{e}$ [m]',ylabel='outboard $\Delta T_{e}$ [m]')

pe_pw_lims=[min(axs[2,1].get_xlim()[0],axs[2,1].get_ylim()[0]),max(axs[2,1].get_xlim()[1],axs[2,1].get_ylim()[1])]#[0,0.1]
axs[2,1].plot(pe_pw_lims,pe_pw_lims,'--',c='0.5',lw=0.5)
axs[2,1].set(xlim=pe_pw_lims,ylim=pe_pw_lims,xlabel='inboard $\Delta p_{e}$ [m]',ylabel='outboard $\Delta p_{e}$ [m]')

# add legend to lower right subplot 
axs[2,0].legend(loc='lower right',fontsize=8.5)

#%% animation of time evolution of edge pedestal, partly with example code taken from:
#"""
#Matplotlib Animation Example
#
#author: Jake Vanderplas
#email: vanderplas@astro.washington.edu
#website: http://jakevdp.github.com
#license: BSD
#Please feel free to use and modify this, but keep the above information. Thanks!
#"""
#for i,shot in enumerate(shotnos):#[7,shotnos[7]],[8,shotnos[8]]:#
#    # First set up the figure, the axis, and the plot element we want to animate
#    fig4,ax4 = plt.subplots(3,sharex=True)
#    fig4.subplots_adjust(hspace=0)
#    fig4.set_size_inches(10, 10, True)
#    ax4[0].set(title='Helium experiment shot #%d \n edge pedestal profile evolution' %shot,xlim=(0.3, 1.5), ylim=(0, 6.5))
#    ax4[0].annotate('$I_p$= %.1fMA \n$B_t$= %.1fT'%(pedestal_data[i]['IP']/1e3,abs(pedestal_data[i]['BT'])), xy=(0.86,1.04),xycoords='axes fraction',fontsize=10)
#    ax4[0].annotate('$n_{e}$ [$10^{19}$m$^{-3}$]', xy=(0.02,0.85),xycoords='axes fraction',fontsize=9)
#    ax4[1].annotate('$T_{e}$ [k%s]'%data[i]['TE']['units'], xy=(0.02,0.85),xycoords='axes fraction',fontsize=9)
#    ax4[1].set(ylim=(0, 1.7))
#    ax4[2].annotate('$p_{e}$ [kPa]', xy=(0.02,0.85),xycoords='axes fraction',fontsize=9)
#    ax4[2].set(xlabel='major radius [m]', ylim=(0, 14))
#    # pedestal data
#    ne_pedestal, = ax4[0].plot([], [], 'x-', lw=0.5)
#    Te_pedestal, = ax4[1].plot([], [], 'x-', lw=0.5)
#    pe_pedestal, = ax4[2].plot([], [], 'x-', lw=0.5)
#    # pedestal fits
#    ne_pedestal_fit, = ax4[0].plot([], [], lw=1)
#    Te_pedestal_fit, = ax4[1].plot([], [], lw=1)
#    pe_pedestal_fit, = ax4[2].plot([], [], lw=1)
#    # vline for LCFS
#    lcfs0 = ax4[0].axvline(c='0.5', lw=1, ls='--')
#    lcfs1 = ax4[1].axvline(c='0.5', lw=1, ls='--')
#    lcfs2 = ax4[2].axvline(c='0.5', lw=1, ls='--')
#    # texts in plot
#    time_text = ax4[1].text(0.4, 0.1, '', transform=ax4[1].transAxes)
#    Hmode_text = ax4[1].text(0.62, 0.1, '', transform=ax4[1].transAxes)
#    ne_resvar_text = ax4[0].text(0.75, 0.8, '', transform=ax4[0].transAxes)
#    Te_resvar_text = ax4[1].text(0.75, 0.8, '', transform=ax4[1].transAxes)
#    pe_resvar_text = ax4[2].text(0.75, 0.8, '', transform=ax4[2].transAxes)
#    LCFS_text = ax4[2].text(0.6, 11, 'LCFS', color='0.5',rotation=90)
#    # initialization function: plot the background of each frame
#    def init():
#        # pedestal data
#        ne_pedestal.set_data([], [])
#        Te_pedestal.set_data([], [])
#        pe_pedestal.set_data([], [])
#        # pedestal fits
#        ne_pedestal_fit.set_data([],[])
#        Te_pedestal_fit.set_data([],[])
#        pe_pedestal_fit.set_data([],[])
#        # vline for LCFS
#        lcfs0.set_xdata(0)
#        lcfs1.set_xdata(0)
#        lcfs2.set_xdata(0)
#        # texts in plot
#        time_text.set_text('')
#        Hmode_text.set_text('')
#        ne_resvar_text.set_text('')
#        Te_resvar_text.set_text('')
#        pe_resvar_text.set_text('')
#        LCFS_text.set_x(0)
#        
#        return ne_pedestal, Te_pedestal, pe_pedestal, ne_pedestal_fit, Te_pedestal_fit, pe_pedestal_fit, lcfs0, lcfs1, lcfs2, time_text, Hmode_text, ne_resvar_text, Te_resvar_text, pe_resvar_text, LCFS_text,
#    
#    # animation function.  This is called sequentially
#    def animate(j):
#        # pedestal data
#        R = data[i]['R2_CTS']['data'][j]
#        ne_pedestal.set_data(R, data[i]['NE']['data'][j]/1e19)
#        Te_pedestal.set_data(R, data[i]['TE']['data'][j]/1e3)
#        pe_pedestal.set_data(R, data[i]['PE']['data'][j]/1e3)
#        # pedestal fits
#        if j in ind[i]:
#            ne_x_fit=np.linspace(*xlims_fine[i][j-ind[i][0]]['NE'],200)
#            ne_pedestal_fit.set_data(ne_x_fit, ped_tanh_odr2(pedestal_fits[i]['NE'][j-ind[i][0]][0],ne_x_fit)/1e19)
#            ne_resvar_text.set_text('resvar=%.2E'%pedestal_fits[i]['NE'][j-ind[i][0]][2])
#            Te_x_fit=np.linspace(*xlims_fine[i][j-ind[i][0]]['TE'],200)
#            Te_pedestal_fit.set_data(Te_x_fit, ped_tanh_odr2(pedestal_fits[i]['TE'][j-ind[i][0]][0],Te_x_fit)/1e3)
#            Te_resvar_text.set_text('resvar=%.2E'%pedestal_fits[i]['TE'][j-ind[i][0]][2])
#            pe_x_fit=np.linspace(*xlims_fine[i][j-ind[i][0]]['PE'],200)
#            pe_pedestal_fit.set_data(pe_x_fit, ped_tanh_odr2(pedestal_fits[i]['PE'][j-ind[i][0]][0],pe_x_fit)/1e3)
#            pe_resvar_text.set_text('resvar=%.2E'%pedestal_fits[i]['PE'][j-ind[i][0]][2])
#        else:
#            ne_pedestal_fit.set_data([],[])
#            Te_pedestal_fit.set_data([],[])
#            pe_pedestal_fit.set_data([],[])
#            ne_resvar_text.set_text('')
#            Te_resvar_text.set_text('')
#            pe_resvar_text.set_text('')
#        # vline for LCFS
#        lcfs0.set_xdata(data[i]['LCFS_R_out_TStb']['data'][j])
#        lcfs1.set_xdata(data[i]['LCFS_R_out_TStb']['data'][j])
#        lcfs2.set_xdata(data[i]['LCFS_R_out_TStb']['data'][j])
#        # texts in plot
#        time_text.set_text('time = %.3fs' %data[i]['NE']['time'][j])
#        if j in indHmode[i]:
#            Hmode_text.set(text='H-mode',color='red')
#        else:
#            Hmode_text.set_text('')
#        LCFS_text.set_x(data[i]['LCFS_R_out_TStb']['data'][j]-0.04)
#        
#        return ne_pedestal, Te_pedestal, pe_pedestal, ne_pedestal_fit, Te_pedestal_fit, pe_pedestal_fit, lcfs0, lcfs1, lcfs2, time_text, Hmode_text, ne_resvar_text, Te_resvar_text, pe_resvar_text, LCFS_text,
#    
#    # call the animator.  blit=True means only re-draw the parts that have changed.
#    anim = animation.FuncAnimation(fig4, animate, init_func=init,frames=len(data[i]['R2_CTS']['time']), interval=100, blit=True)
#    
#    # save the animation as an mp4.  This requires ffmpeg or mencoder to be
#    # installed.  The extra_args ensure that the x264 codec is used, so that
#    # the video can be embedded in html5.  You may need to adjust this for
#    # your system: for more information, see
#    # http://matplotlib.sourceforge.net/api/animation_api.html
#    #anim.save('../Plots_and_graphics/ped_evolution_videos/%dpedestal_evolution.mp4'%shot, fps=5, dpi=100, extra_args=['-vcodec', 'libx264'])
#    plt.show()
