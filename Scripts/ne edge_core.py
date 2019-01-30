# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 11:25:30 2019

@author: rbatt

NE edge v core comparison and calibration
"""

#from Shot_Class import Shot
import numpy as np
import matplotlib.pyplot as plt
global signals
from signal_dict_13_DEC_PULL import signals
#all_shots = [Shot(24130, LHt=[(0.285,0,0)]), Shot(24129), Shot(24128, LHt=[(0.258,0,0)])]
all_shots = [Shot(24129)]    
plt.figure(11)
ees=[]
ccs=[]
for shot in all_shots:
    print(shot)
    for i, j in enumerate(shot.data['AYE_R']['time']):
        r_edge = shot.data['AYE_R']['data'][i]
        ne_edge = shot.data['AYE_NE']['data'][i]
        ne_er_edge = shot.data['AYE_NE']['errors'][i]
        
        good_e = np.isfinite(r_edge) & np.isfinite(ne_edge)
        r_edge,ne_edge = r_edge[good_e], ne_edge[good_e]
        
        #get core r,ne data
        # on average, r_core is in r_edge range for index>110
        r_core = shot.data['AYC_R']['data'][i][110:]
        ne_core = shot.data['AYC_NE']['data'][i][110:]
        ne_er_core = shot.data['AYC_NE']['errors'][i][110:]
        
        good_c = np.isfinite(r_core) & np.isfinite(ne_core)
        r_core,ne_core = r_core[good_c], ne_core[good_c]
        
        try:
            e_poly = np.poly1d(np.polyfit(r_edge,ne_edge,15))
            c_poly = np.poly1d(np.polyfit(r_core,ne_core,15))
        
            min_r = max(min(r_core), min(r_edge))
            max_r = min(max(r_core), max(r_edge))
            for r in np.linspace(min_r, max_r, 20):
                if r<np.max(r_core):
                    if r>np.min(r_core):
                        print('yes')
                        plt.figure(1)
                        ee = e_poly(r)
                        cc = c_poly(r)
                        plt.scatter(cc,ee, marker='x', c='k')
                        ees.append(ee)
                        ccs.append(cc)

                
        except:
            pass
        


#%%
# Generating figure from above
plt.figure()
#plt.ylim(0,4e19)
#plt.xlim(0,4e19)

x = np.linspace(0,5e19)
plt.plot(x,x, ls='--', c='k', label='1:1')
plt.xlabel('ne_core')
plt.ylabel('ne_edge')

# remove impossible values <0 (results of poor polyfits)
ees, ccs = np.asarray(ees), np.asarray(ccs)
condition = np.where((ees>0)&(ccs>0)&(ccs<0.4e20))
ees = ees[condition]
ccs = ccs[condition]

plt.scatter(ccs,ees,marker='x',c='b', alpha=0.5)

st_poly = np.poly1d(np.polyfit(ccs,ees,1)) # fit line to data points

x = np.linspace(0,4e19)
plt.plot(x,st_poly(x), c='red', label='fit={}'.format(str(st_poly)))

plt.legend()


#%%
# load more data

from signal_dict_13_DEC_PULL import signals
o1=Shot(24130, LHt=[(0.285,0.2845,0.2855)], HLt=[(0.3325,0.332,0.333)])
o2=Shot(24129, LHt=[(0.2922,0.290,0.295)], HLt=[(0.3174,0.317,0.318)])
o3=Shot(24128, LHt=[(0.2572,0.257,0.258)], HLt=[(0.3435,0.343,0.344)])

n1 = Shot(24215, LHt=[(0.2515,0.2513,0.252)],HLt=[(0.284,0.2839,0.2841)])
n2=Shot(24216, LHt=[(0.2537,0.25369,0.254), (0.3174,0.31739,0.3176)],HLt=[(0.2845,0.28449,0.2847), (0.3585,0.3579, 0.3586)])

n3=Shot(24324, LHt=[(0.2535,0.2533,0.2536), (0.3181,0.3175,0.3189)],HLt=[(0.2823,0.2821,0.2824), (0.3431,0.3423,0.34311)])
n4=Shot(24325, LHt=[(0.2515,0.2512,0.2518), (0.319, 0.317,0.321)],HLt=[(0.2845,0.2843,0.2847), (0.345,0.344,0.346)])
n5=Shot(24326, LHt=[(0.2515, 0.251, 0.252)],HLt=[(0.284,0.2839, 0.2845)])
n6=Shot(24327, LHt=[(0.2511,0.2508,0.2513)],HLt=[(0.2875, 0.2874, 0.2876)])
n7=Shot(24328, LHt=[(0.251, 0.2506, 0.2514)],HLt=[(0.2895, 0.2894, 0.2896)])
n8=Shot(24329, LHt=[(0.2625, 0.2624, 0.263), (0.318, 0.317, 0.319)],HLt=[(0.281, 0.2808, 0.2812), (0.3365, 0.3364, 0.3366)])
n9=Shot(24330, LHt=[(0.252, 0.2517, 0.2521)],HLt=[(0.2842, 0.2841, 0.2843)])
nall = [n1,n2,n3,n4,n5,n6,n7,n8,n9, o1,o2,o3]

for n in nall:
    n.plot_JP(plot_thomson=4)

#%%
# density scan of knee value, gradient
# by hand, shot by shot
    

#n1 24215
# interseting around 0.25, first 8 capture LH, second 8 capture HL

# want knee at 



#%%
# Te, Tec plots
plt.figure('Te/c')
plt.xlabel('Tec')
plt.ylabel('Te')

#n6
# l mode points
for i in np.arange(48,56):
    Te,Tec = n6.Te_Tec(i,prev=False)
    plt.scatter(Tec,Te, c='r', marker='x')
# h mode points
for i in np.arange(64,72):
    Te,Tec = n6.Te_Tec(i, prev=False)
    plt.scatter(Tec,Te, c='g', marker='x')

    



    