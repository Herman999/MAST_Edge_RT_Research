# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 21:36:16 2018

@author: jb4317, Jan-Peter Baehner

Programme to create plots especially for the poster presentation / report.
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
import numpy as np
from Pth_scalings import Martin08_scaling2,McDonald04_scaling2,McDonald04_scaling3,Takizuka04_scaling,Takizuka04_scalingZeff

#%% He evaluation:
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

#%% plot of typical pedestal fits incl. marking of height and width
#radial limits for out- and inboard pedestal 
xlims_out=dict(NE=[1,1.45],TE=[1.2,1.45],PE=[1.2,1.45])
xlims_in=dict(NE=[0.2,0.6],TE=[0.2,0.6],PE=[0.2,0.6])
#major radii corresponding to limits
Rne=dict(inboard=np.linspace(*xlims_in['NE']),outboard=np.linspace(*xlims_out['NE']))
RTe=dict(inboard=np.linspace(*xlims_in['TE']),outboard=np.linspace(*xlims_out['TE']))
RPe=dict(inboard=np.linspace(*xlims_in['PE']),outboard=np.linspace(*xlims_out['PE']))

#generate setup of figure      
fig,ax=plt.subplots(3,2,figsize=(8, 7))
fig.suptitle('Typical H-mode pedestals in He and D')
fig.subplots_adjust(top=0.925,bottom=0.1,left=0.075,right=0.93,hspace=0.0,wspace=0.13)
ax[0][0].set(ylim=(0,5.5),xlim=(0.24,0.4))
ax[0][1].set(ylim=(0,5.5),xlim=(1.3,1.44))
ax[0][0].annotate('$n_{e}$ [$10^{19}$m$^{-3}$]', xy=(0.02,0.8),xycoords='axes fraction',fontsize=10)
ax[1][0].annotate('$T_{e}$ [k%s]'%data[0]['TE']['units'], xy=(0.02,0.8),xycoords='axes fraction',fontsize=10)
ax[1][0].set(ylim=(0, 0.6),xlim=(0.24,0.4))
ax[1][1].set(ylim=(0, 0.6),xlim=(1.3,1.44))
ax[2][0].annotate('$p_{e}$ [kPa]', xy=(0.02,0.8),xycoords='axes fraction',fontsize=10)
ax[2][0].set(ylim=(0, 5),xlim=(0.24,0.4))#
ax[2][1].set(ylim=(0, 5),xlim=(1.3,1.44))#
# plot data of Helium and Deuterium shot in two different colours
colors=dict(D20476='xkcd:cerulean',He22653='xkcd:olive green')
ax[0][1].annotate('#20476 (D)', xy=(0.7,1.12),xycoords='axes fraction',fontsize=10,color=colors['D20476'])
ax[0][1].annotate('#22653 (He)', xy=(0.7,1.03),xycoords='axes fraction',fontsize=10,color=colors['He22653'])

rightleft=['right','left']
for k in [0,1]:
    for i,iR,shot in [shotnos.index(20476),rubyshots.index(20476),'D20476'],[shotnos.index(22653),rubyshots.index(22653),'He22653']:
        # plot data from Ruby TS
        R = data[i]['R12_R']['data'][0]
        Rerr = data[i]['R12_R']['errors'][0]
        ax[0][k].errorbar(R, data[i]['NE12_R']['data'][0]/1e19,xerr=Rerr,yerr=data[i]['NE12_R']['errors'][0]/1e19,fmt='.',color=colors[shot],ecolor='r',zorder=0)
        ax[1][k].errorbar(R, data[i]['TE12_R']['data'][0]/1e3,xerr=Rerr,yerr=data[i]['TE12_R']['errors'][0]/1e3,fmt='.',color=colors[shot],ecolor='r',zorder=0)
        ax[2][k].errorbar(R, data[i]['PE12_R']['data'][0]/1e3,xerr=Rerr,yerr=data[i]['PE12_R']['errors'][0]/1e3,fmt='.',color=colors[shot],ecolor='r',zorder=0)
        # plot fit from ne_R_p etc.
        #outboard
        ax[0][k].plot(Rne['outboard'], ped_tanh_odr2(ne_R_p[iR]['outboard'][0],Rne['outboard'])/1e19,color='k',lw='1',zorder=10)
        ax[1][k].plot(RTe['outboard'], ped_tanh_odr2(Te_R_p[iR]['outboard'][0],RTe['outboard'])/1e3,color='k',lw='1',zorder=10)
        ax[2][k].plot(RPe['outboard'], ped_tanh_odr2(pe_R_p[iR]['outboard'][0],RPe['outboard'])/1e3,color='k',lw='1',zorder=10)
        # mark height and width
        ax[0][k].axvline(ne_R_p[iR]['outboard'][0][2]-ne_R_p[iR]['outboard'][0][3]/2,ymax=ped_tanh_odr2(ne_R_p[iR]['outboard'][0],ne_R_p[iR]['outboard'][0][2]-ne_R_p[iR]['outboard'][0][3]/2)/1e19/ax[0][k].get_ylim()[1],ls=':',color='0.7')#x_knee=x_sym-width/2
        ax[0][k].axvline(ne_R_p[iR]['outboard'][0][2],ymax=ped_tanh_odr2(ne_R_p[iR]['outboard'][0],ne_R_p[iR]['outboard'][0][2])/1e19/ax[0][k].get_ylim()[1],ls='--',color='0.5')#x_knee=x_sym-width/2
        ax[0][k].axvline(ne_R_p[iR]['outboard'][0][2]+ne_R_p[iR]['outboard'][0][3]/2,ymax=ped_tanh_odr2(ne_R_p[iR]['outboard'][0],ne_R_p[iR]['outboard'][0][2]+ne_R_p[iR]['outboard'][0][3]/2)/1e19/ax[0][k].get_ylim()[1],ls=':',color='0.7')#x_knee=x_sym-width/2
        ax[0][k].axhline((ne_R_p[iR]['outboard'][0][0]+ne_R_p[iR]['outboard'][0][1])/1e19,xmin=(0.5-ax[0][k].get_xlim()[0])/(ax[0][k].get_xlim()[1]-ax[0][k].get_xlim()[0]),xmax=(ne_R_p[iR]['outboard'][0][2]-ne_R_p[iR]['outboard'][0][3]/2-ax[0][k].get_xlim()[0])/(ax[0][k].get_xlim()[1]-ax[0][k].get_xlim()[0]),ls='--',color='0.5')#x_knee=x_sym-width/2
        
        ax[1][k].axvline(Te_R_p[iR]['outboard'][0][2]-Te_R_p[iR]['outboard'][0][3]/2,ymax=ped_tanh_odr2(Te_R_p[iR]['outboard'][0],Te_R_p[iR]['outboard'][0][2]-Te_R_p[iR]['outboard'][0][3]/2)/1e3/ax[1][k].get_ylim()[1],ls=':',color='0.7')#x_knee=x_sym-width/2
        ax[1][k].axvline(Te_R_p[iR]['outboard'][0][2],ymax=ped_tanh_odr2(Te_R_p[iR]['outboard'][0],Te_R_p[iR]['outboard'][0][2])/1e3/ax[1][k].get_ylim()[1],ls='--',color='0.5')#x_knee=x_sym-width/2
        ax[1][k].axvline(Te_R_p[iR]['outboard'][0][2]+Te_R_p[iR]['outboard'][0][3]/2,ymax=ped_tanh_odr2(Te_R_p[iR]['outboard'][0],Te_R_p[iR]['outboard'][0][2]+Te_R_p[iR]['outboard'][0][3]/2)/1e3/ax[1][k].get_ylim()[1],ls=':',color='0.7')#x_knee=x_sym-width/2
        ax[1][k].axhline((Te_R_p[iR]['outboard'][0][0]+Te_R_p[iR]['outboard'][0][1])/1e3,xmin=(0.5-ax[1][k].get_xlim()[0])/(ax[1][k].get_xlim()[1]-ax[1][k].get_xlim()[0]),xmax=(Te_R_p[iR]['outboard'][0][2]-Te_R_p[iR]['outboard'][0][3]/2-ax[1][k].get_xlim()[0])/(ax[1][k].get_xlim()[1]-ax[1][k].get_xlim()[0]),ls='--',color='0.5')#x_knee=x_sym-width/2
        
        ax[2][k].axvline(pe_R_p[iR]['outboard'][0][2]-pe_R_p[iR]['outboard'][0][3]/2,ymax=ped_tanh_odr2(pe_R_p[iR]['outboard'][0],pe_R_p[iR]['outboard'][0][2]-pe_R_p[iR]['outboard'][0][3]/2)/1e3/ax[2][k].get_ylim()[1],ls=':',color='0.7')#x_knee=x_sym-width/2
        ax[2][k].axvline(pe_R_p[iR]['outboard'][0][2],ymax=ped_tanh_odr2(pe_R_p[iR]['outboard'][0],pe_R_p[iR]['outboard'][0][2])/1e3/ax[2][k].get_ylim()[1],ls='--',color='0.5')#x_knee=x_sym-width/2
        ax[2][k].axvline(pe_R_p[iR]['outboard'][0][2]+pe_R_p[iR]['outboard'][0][3]/2,ymax=ped_tanh_odr2(pe_R_p[iR]['outboard'][0],pe_R_p[iR]['outboard'][0][2]+pe_R_p[iR]['outboard'][0][3]/2)/1e3/ax[2][k].get_ylim()[1],ls=':',color='0.7')#x_knee=x_sym-width/2
        ax[2][k].axhline((pe_R_p[iR]['outboard'][0][0]+pe_R_p[iR]['outboard'][0][1])/1e3,xmin=(0.5-ax[2][k].get_xlim()[0])/(ax[2][k].get_xlim()[1]-ax[2][k].get_xlim()[0]),xmax=(pe_R_p[iR]['outboard'][0][2]-pe_R_p[iR]['outboard'][0][3]/2-ax[2][k].get_xlim()[0])/(ax[2][k].get_xlim()[1]-ax[2][k].get_xlim()[0]),ls='--',color='0.5')#x_knee=x_sym-width/2
        
        #inboard
        ax[0][k].plot(Rne['inboard'], ped_tanh_odr2(ne_R_p[iR]['inboard'][0],Rne['inboard'],'in')/1e19,color='k',lw='1',zorder=10)#colors[shot]
        ax[1][k].plot(RTe['inboard'], ped_tanh_odr2(Te_R_p[iR]['inboard'][0],RTe['inboard'],'in')/1e3,color='k',lw='1',zorder=10)
        ax[2][k].plot(RPe['inboard'], ped_tanh_odr2(pe_R_p[iR]['inboard'][0],RPe['inboard'],'in')/1e3,color='k',lw='1',zorder=10)
        # mark height and width
        ax[0][k].axvline(ne_R_p[iR]['inboard'][0][2]+ne_R_p[iR]['inboard'][0][3]/2,ymax=ped_tanh_odr2(ne_R_p[iR]['inboard'][0],ne_R_p[iR]['inboard'][0][2]-ne_R_p[iR]['inboard'][0][3]/2)/1e19/ax[0][k].get_ylim()[1],ls=':',color='0.7')#x_knee=x_sym-width/2
        ax[0][k].axvline(ne_R_p[iR]['inboard'][0][2],ymax=ped_tanh_odr2(ne_R_p[iR]['inboard'][0],ne_R_p[iR]['inboard'][0][2])/1e19/ax[0][k].get_ylim()[1],ls='--',color='0.5')#x_knee=x_sym-width/2
        ax[0][k].axvline(ne_R_p[iR]['inboard'][0][2]+ne_R_p[iR]['inboard'][0][3]/2,ymax=ped_tanh_odr2(ne_R_p[iR]['inboard'][0],ne_R_p[iR]['inboard'][0][2]+ne_R_p[iR]['inboard'][0][3]/2)/1e19/ax[0][k].get_ylim()[1],ls=':',color='0.7')#x_knee=x_sym-width/2
        ax[0][k].axhline((ne_R_p[iR]['inboard'][0][0]+ne_R_p[iR]['inboard'][0][1])/1e19,xmin=(ne_R_p[iR]['inboard'][0][2]+ne_R_p[iR]['inboard'][0][3]/2-ax[0][k].get_xlim()[0])/(ax[0][k].get_xlim()[1]-ax[0][k].get_xlim()[0]),xmax=(0.8-ax[0][k].get_xlim()[0])/(ax[0][k].get_xlim()[1]-ax[0][k].get_xlim()[0]),ls='--',color='0.5')#x_knee=x_sym-width/2
        
        ax[1][k].axvline(Te_R_p[iR]['inboard'][0][2]+Te_R_p[iR]['inboard'][0][3]/2,ymax=ped_tanh_odr2(Te_R_p[iR]['inboard'][0],Te_R_p[iR]['inboard'][0][2]-Te_R_p[iR]['inboard'][0][3]/2)/1e3/ax[1][k].get_ylim()[1],ls=':',color='0.7')#x_knee=x_sym-width/2
        ax[1][k].axvline(Te_R_p[iR]['inboard'][0][2],ymax=ped_tanh_odr2(Te_R_p[iR]['inboard'][0],Te_R_p[iR]['inboard'][0][2])/1e3/ax[1][k].get_ylim()[1],ls='--',color='0.5')#x_knee=x_sym-width/2
        ax[1][k].axvline(Te_R_p[iR]['inboard'][0][2]+Te_R_p[iR]['inboard'][0][3]/2,ymax=ped_tanh_odr2(Te_R_p[iR]['inboard'][0],Te_R_p[iR]['inboard'][0][2]+Te_R_p[iR]['inboard'][0][3]/2)/1e3/ax[1][k].get_ylim()[1],ls=':',color='0.7')#x_knee=x_sym-width/2
        ax[1][k].axhline((Te_R_p[iR]['inboard'][0][0]+Te_R_p[iR]['inboard'][0][1])/1e3,xmin=(Te_R_p[iR]['inboard'][0][2]+Te_R_p[iR]['inboard'][0][3]/2-ax[1][k].get_xlim()[0])/(ax[1][k].get_xlim()[1]-ax[1][k].get_xlim()[0]),xmax=(0.8-ax[1][k].get_xlim()[0])/(ax[1][k].get_xlim()[1]-ax[1][k].get_xlim()[0]),ls='--',color='0.5')#x_knee=x_sym-width/2
        
        ax[2][k].axvline(pe_R_p[iR]['inboard'][0][2]+pe_R_p[iR]['inboard'][0][3]/2,ymax=ped_tanh_odr2(pe_R_p[iR]['inboard'][0],pe_R_p[iR]['inboard'][0][2]-pe_R_p[iR]['inboard'][0][3]/2)/1e3/ax[2][k].get_ylim()[1],ls=':',color='0.7')#x_knee=x_sym-width/2
        ax[2][k].axvline(pe_R_p[iR]['inboard'][0][2],ymax=ped_tanh_odr2(pe_R_p[iR]['inboard'][0],pe_R_p[iR]['inboard'][0][2])/1e3/ax[2][k].get_ylim()[1],ls='--',color='0.5')#x_knee=x_sym-width/2
        ax[2][k].axvline(pe_R_p[iR]['inboard'][0][2]+pe_R_p[iR]['inboard'][0][3]/2,ymax=ped_tanh_odr2(pe_R_p[iR]['inboard'][0],pe_R_p[iR]['inboard'][0][2]+pe_R_p[iR]['inboard'][0][3]/2)/1e3/ax[2][k].get_ylim()[1],ls=':',color='0.7')#x_knee=x_sym-width/2
        ax[2][k].axhline((pe_R_p[iR]['inboard'][0][0]+pe_R_p[iR]['inboard'][0][1])/1e3,xmin=(pe_R_p[iR]['inboard'][0][2]+pe_R_p[iR]['inboard'][0][3]/2-ax[2][k].get_xlim()[0])/(ax[2][k].get_xlim()[1]-ax[2][k].get_xlim()[0]),xmax=(0.8-ax[2][k].get_xlim()[0])/(ax[2][k].get_xlim()[1]-ax[2][k].get_xlim()[0]),ls='--',color='0.5')#x_knee=x_sym-width/2
    
    # remove spines in middle of plot
    ax[0][k].spines[rightleft[k]].set_visible(False)
    ax[1][k].spines[rightleft[k]].set_visible(False)
    ax[2][k].spines[rightleft[k]].set_visible(False)
   
#remobe/handle ticks of axes     
ax[0][0].yaxis.tick_left()
ax[0][0].tick_params(bottom=False,labelbottom=False)
ax[1][0].yaxis.tick_left()
ax[1][0].tick_params(bottom=False,labelbottom=False)
ax[2][0].yaxis.tick_left()
ax[0][1].yaxis.tick_right()
ax[0][1].tick_params(bottom=False,labelbottom=False)
ax[1][1].yaxis.tick_right()
ax[1][1].tick_params(bottom=False,labelbottom=False)
ax[2][1].yaxis.tick_right()

#plot diagnols that indicate cut of axes
d = .03 # how big to make the diagonal lines in axes coordinates
kwargs = dict(color='k', clip_on=False, lw=1)
#left
ax[0][0].plot((1-d,1+d), (1-d,1+d), transform=ax[0][0].transAxes, **kwargs) #top
ax[1][0].plot((1-d,1+d), (1-d,1+d), transform=ax[1][0].transAxes, **kwargs) #top
ax[2][0].plot((1-d,1+d), (1-d,1+d), transform=ax[2][0].transAxes, **kwargs) #top
ax[2][0].plot((1-d,1+d), (-d,+d), transform=ax[2][0].transAxes, **kwargs) #bootom
#right
ax[0][1].plot((-d,+d), (1-d,1+d), transform=ax[0][1].transAxes, **kwargs) #top
ax[1][1].plot((-d,+d), (1-d,1+d), transform=ax[1][1].transAxes, **kwargs) #top
ax[2][1].plot((-d,+d), (1-d,1+d), transform=ax[2][1].transAxes, **kwargs) #top
ax[2][1].plot((-d,+d), (-d,+d), transform=ax[2][1].transAxes, **kwargs) #bootom

# annotate label of x-axis
ax[2][0].annotate('major radius [m]', xy=(0.9,-0.3),xycoords='axes fraction',fontsize=10)
# annotate fit function
#ax[2][1].text(-0.8,0.78,r'$y=a\; \tanh (2\frac{R_{sym}-R}{width}) + b\; [ + slope\; (R-R_{knee}) + c\; (R-R_{well})^2 - d_{well}$; if $R </> R_{knee}]$', transform=ax[2][1].transAxes,fontsize=9, clip_on=False, bbox=dict(boxstyle='square', fc="w", ec="k"))

#figname='../Plots_and_graphics/typical_ped_inout.png'
#plt.savefig(figname,format='png',dpi=100)

#%% plot L-H and H-L data (Pth and pedestal height and width) for several shots
#only ante transitus (at)  ###################### and post transitus (pt)

# time intervals for each shot   
tlims=[[tLH[i]-0.01,tHL[i]+0.01] for i in range(len(shotnos))] # choose time interval around L-H/H-L transition - the TS time resolution is 4 ms, so this will produce 2 additional indices in ind before and after the L-H and H-L transition respectively 
        
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
plt.plot(ne_,McDonald04_scaling3(Takizuka04_scalingZeff(ne_,Bt_,S_,a_,R_,Ip_*1e3,Scross_,k_,Vloop_,W_,V_,2.5)),':',c='0.5')#,2.5 #assume Zeff=2.5  this does not differ much from plot above
plt.annotate('$P_{th,Takizuka04,Z_{eff}}^{He}$', xy=(xlims[1]*0.85,McDonald04_scaling3(Takizuka04_scalingZeff(ne_[-1],Bt_,S_,a_,R_,Ip_*1e3,Scross_,k_,Vloop_,W_,V_,2.5))*1.1),fontsize=9, color='0.2', rotation=10)#,xycoords='axes fraction'/plt.gca().get_ylim()[1]

# add annotation of scaling:
plt.annotate(r'$P_{th,Martin08}^D = 0.0488 \times n_{e20}^{0.717} B_T^{0.803} S^{0.941}$, [1]', xy=(0.4,0.7),xycoords='axes fraction',fontsize=10)
plt.annotate(r'$P_{th,McDonald04}^{He} = M^{-1.1} Z^{1.6} \times P_{th}^D$,  [2]', xy=(0.4,0.6),xycoords='axes fraction',fontsize=10)
plt.annotate('with M, Z mass and charge normalised to that of D', xy=(0.4,0.53),xycoords='axes fraction',fontsize=8)
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

# add annotation of scaling:
plt.annotate(r'$P_{th,Takizuka04}^D = 0.072 \times |B|_{out}^{0.7} \, n_{e20}^{0.7} \, S^{0.9} \, F(A)^{0.5}$', xy=(0.45,0.2),xycoords='axes fraction',fontsize=10)
plt.annotate(r'$F = \frac{A}{1-\sqrt{2/(1+A)}}$,  [3]', xy=(0.583,0.11),xycoords='axes fraction',fontsize=10)

plt.show()

###############################################################################
###############################################################################
###############################################################################
#%% switch to X-point evaluation:
file=open( 'Xpoint_pedestal.p', "rb" )
results=pickle.load(file) # set loaded data as initial guess file
file.close()

shotnos,tLH,tHL,data,rubyshots,ne_R_p,Te_R_p,pe_R_p,pedestal_data,pedestal_fits,LHdata,HLdata,xlims_fine=results

#%% change of x-point height variation

LHxpoint_heights=[]
#xpoint_mins=[]
#xpoint_maxs=[]

for i in range(len(shotnos)):
    if LHdata[i]['X1Zat']['data']==-999.0:
        LHxpoint_heights.append(-1.2)
    else:
        LHxpoint_heights.append(LHdata[i]['X1Zat']['data'])
    x1z=[data[i]['X1Z']['data'][j] for j in range(len(data[i]['X1Z']['time'])) if data[i]['X1Z']['data'][j]!=-999.0]
#    xpoint_mins.append(min(x1z))
#    xpoint_maxs.append(max(x1z))
    
LHimin=LHxpoint_heights.index(min(LHxpoint_heights))
LHimax=LHxpoint_heights.index(max(LHxpoint_heights))
#imin=xpoint_mins.index(min(xpoint_mins))
#imax=xpoint_maxs.index(max(xpoint_maxs))
#HLxpoint_heights=[HLdata[i]['X1Zat']['data'] for i in range(len(shotnos)) if HLdata[i]['X1Zat']['data']]
#HLimax=HLxpoint_heights.index(max(HLxpoint_heights))
#HLimin=HLxpoint_heights.index(min(HLxpoint_heights))
t=0
while data[LHimin]['LCFS_R']['time'][t]<LHdata[LHimin]['X1Zat']['time']:
    LHtmin=t
    t+=1
t=0
while data[LHimax]['LCFS_R']['time'][t]<LHdata[LHimax]['X1Zat']['time']:
    LHtmax=t
    t+=1

plt.figure()
plt.plot(data[LHimin]['LCFS_R']['data'][LHtmin][:data[LHimin]['LCFS_N']['data'][LHtmin]],data[LHimin]['LCFS_Z']['data'][LHtmin][:data[LHimin]['LCFS_N']['data'][LHtmin]],'-',label='min #%s, t=%d ms'%(shotnos[LHimin],data[LHimin]['LCFS_R']['time'][LHtmin]*1e3)) #plot LCFS_R/Z data up to index given by LCFS_N 
plt.plot(data[LHimax]['LCFS_R']['data'][LHtmax][:data[LHimax]['LCFS_N']['data'][LHtmax]],data[LHimax]['LCFS_Z']['data'][LHtmax][:data[LHimax]['LCFS_N']['data'][LHtmax]],':',label='max #%s, t=%d ms'%(shotnos[LHimax],data[LHimax]['LCFS_R']['time'][LHtmax]*1e3)) #plot LCFS_R/Z data up to index given by LCFS_N 
plt.legend(loc='upper right')
plt.xlabel('$R$ [m]')
plt.ylabel('$Z$ [m]')
plt.title('Range of configuration')
plt.axis('equal')
