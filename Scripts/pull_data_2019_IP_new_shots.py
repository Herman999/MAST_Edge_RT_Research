# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21  2018

@author: jb4317, Jan-Peter Baehner

version2

New routine to pull data from MAST data base via pyuda and transfere to files
"""
#import pyuda
#client=pyuda.Client()   #set up pyuda

#from data_access_funcs import save_signal_data

# all new
shotnos = [
# Pedestal Scaling in IP not that releacnt
30340,
30341,
30342,
30344,
30348,
30351,
30352,
30353,
30355,
30356,
30358,
30359,
30361,
30362,

#Influence of IP to E_R
24426,
24428,
24430,
24431,

# 17FEB10  BETA SCAN, BT
24514,
24517,
24518,
24522,
24524,
24525,

# Transition access LH dependance on IP
29482,
29485,
29486,
29487,
29488,
29489,
29493,
29494,
29495,
29496,

# 17NOV11 LH transition programme
27571,
27572,
27573,
27574,
27586,
27587,
27588,
27589,



]

# session ended early due to inadequate progress. h-mode weaker. suggestion its time to boronise.


# below lists signals currently in our data set, many more exist

signals=dict(# NEW AT TOP
            EFM_R_PSI100_OUT = 'EFM_R(PSI100)_OUT', # Outboard radius of 100% normalised magnetic flux; f(B)
            EFM_R_PSI90_OUT = 'EFM_R(PSI90)_OUT', # Outboard radius of 90% normalised magnetic flux; f(B)
            EFM_R_PSI95_OUT = 'EFM_R(PSI95)_OUT', # Outboard radius of 95% normalised magnetic flux; f(B)
        
            AIT_ETOT_ISP = 'AIT_ETOT_ISP', #Instantaneous energy to divertor inner
            AIT_ETOT_OSP = 'AIT_ETOT_OSP', #Instantaneous energy to divertor outer
            AIT_ETOT_OSP_ELM = 'AIT_ETOT_OSP_ELM', #Instantaneous energy to divertor outer for ELM (equiv exists for inner)
            AIT_PTOT_ISP = 'AIT_PTOT_ISP', # Power to the divertor inner strike point
            AIT_PTOT_ISP_ELM = 'AIT_PTOT_ISP_ELM', # Power to the divertor inner strike point for ELM
            AIT_PTOT_OSP = 'AIT_PTOT_OSP', # Power to the divertor outer strike point
            AIT_PTOT_OSP_ELM = 'AIT_PTOT_OSP_ELM', # Power to the divertor outer strike point for ELM
        
            # ADA Dalpha signals
            ADA_DALPHA_INVERTED = 'ADA_DALPHA INVERTED',
            ADA_DALPHA_RAW = 'ADA_DALPHA RAW_FULL',
            ADA_GEO = 'ADA_GEO_FULL',
            
            # AIM Dalpha signals
            AIM_DA_HM = 'AIM_DA/HM10/T', # tangential mid plane plasma view
            AIM_DA_TO = 'AIM_DA/TO10', # view of lower coil shield and centre column region
            Dalphint = 'ADA_DALPHA INTEGRATED',
            
            # ANE CO2 interferometry
            ANE_CO2 = 'ANE_CO2', # integrated electron density determined from co2 laser interference fringes
            ANE_DENSITY = 'ANE_DENSITY', # integrated electron density including vibration correction
            
            # ASB Dalpha like signals (??)
            ASB_CII = 'ASB_CII_DGA', # CII emission - view of lower centre column
            ASB_OII = 'ASB_OII_DGA', # View of upper coil shield and centre column region
            ASB_SVN_REVISION = 'ASB_SVN_REVISION',
            
            # ASM H-mode indicators
            ASM_HM = 'ASM_HM/RATING', # an H-Mode rating from 0 to 1 throughout the shot
            ASM_HM_PER = 'ASM_HM/PERIODS', # a trace of the interesting and probable H-Mode periods. The height of each period (again between 0 and 1) gives an indication of how likely it is to be H-Mode.
            
            # AYC core thomson scattering
            AYC_NE ='AYC_NE',
            AYC_PE = 'AYC_PE',
            AYC_TE = 'AYC_TE',
            AYC_R = 'AYC_R', # radial basis (x,t)
            AYC_R_CORE = 'AYC_R_CORE', # peak position (t)
      #      AYC_R_CTS = 'AYC_R_CTS',
      #      AYC_R0_CTS = 'AYC_R0_CTS',
            AYC_NE0 = 'AYC_NE_CORE',       
            AYC_TE0 = 'AYC_TE_CORE',
            AYC_TIME = 'AYC_TIME',
            
            # AYE edge thomson scattering
            AYE_NE = 'AYE_NE',
            AYE_PE = 'AYE_PE',
            AYE_R = 'AYE_R',
            AYE_TE = 'AYE_TE',
            AYE_TIME = 'AYE_TIME',
            
            # ATS Analysed Ruby THOMSON scattering data
            ATS_N_E = 'ATS_N_E', 
            ATS_P_E = 'ATS_P_E',  
            ATS_T_E = 'ATS_T_E',
            ATS_R = 'ATS_R', # radial coordinates
            ATS_TIME = 'ATS_TIME', # time of measurement
            ATS_WAVELENGTH = 'ATS_WAVELENGTH', # wavelength of spectra
            
            
            WMHD = 'EFM_PLASMA_ENERGY',
            DWMHD = 'ESM_W_DOT',
            IP = 'AMC_PLASMA CURRENT',
            ngrad = 'ADG_DENSITY_GRADIENT', # from Dalpha signals for H-mode identifying
            npos = 'ADG_GRADIENT_POSITION', # from Dalpha signals

            # energies
            Paux = 'ESM_P_AUX',
            Ploss = 'ESM_P_LOSS',
            PRAD = 'ABM_PRAD_POL',    
            PINJ='ANB_TOT_SUM_POWER', #NBI power
            POHM='ESM_PPHIX', # ohmic power, ESM_P_PHI - ESM_X.

            # ESM: height [m] (inner/outer lower/upper strike points)
            ILSPZ = 'ESM_ILSPZ', # IL SP
            IUSPZ = 'ESM_ILSPZ', # IU SP
            OLSPR = 'ESM_OLSPR', # OL SP
            OUSPR = 'ESM_OUSPR', # OU SP
            
            # EFM magnetic configuration 
            RGEO='EFM_GEOM_AXIS_R(C)', # major radius
            AMIN='EFM_MINOR_RADIUS', # minor radius
            VOL='EFM_PLASMA_VOLUME', # plasma volume
            SAREA = 'ESM_SURFACE_AREA',
            AREA='EFM_PLASMA_AREA', # Area of poloidal cross-section of plasma; f(B)

            LCFS_N='EFM_LCFS(N)_(C)', #No. of coords on LCFS (61x1)
            LCFS_R='EFM_LCFS(R)_(C)', #r-coords of seperatrix in m (61x2600)
            LCFS_Z='EFM_LCFS(Z)_(C)', #z-coords of seperatrix in m (61x2600)
            LCFS_L='EFM_LCFS_LENGTH', #length of LCFS in m (61x1)
            LCFS_R_out='EFM_R(PSI100)_OUT', # Outboard radius of 100% normalised magnetic flux (seperatrix); f(B)
            LCFS_R_in='EFM_R(PSI100)_IN', # Inboard radius of 100% normalised magnetic flux (seperatrix); f(B)

            X1R='EFM_XPOINT1_R(C)', # Radius of first X-point; f(B)
            X1Z='EFM_XPOINT1_Z(C)', # Height of first X-point; f(B)
            X2R='EFM_XPOINT2_R(C)', # Radius of second X-point; f(B)
            X2Z='EFM_XPOINT2_Z(C)', # Height of second X-point; f(B)

            KAPPA='EFM_ELONGATION',
            Q95='EFM_Q_95',	

            TAUTOT = 'ESM_TAU_E_GUESS',
            Vloop = 'ESM_V_LOOP_DYNAMIC', #plasma surface Vloop, calculated allowing for the movement of the LCFS; i.e. in the observer's frame of reference.
            BT='EFM_BVAC_RMAG',
            )      

"""
for shot in shotnos:
    loaded=[]
    notloaded=[]
    for sig in signals:
        try:
            temp_obj=client.get(signals[sig],shot) #create temporary object pulled form MAST database
            filename=str(shot)+'_'+sig+'.p' #create filename
            save_signal_data(temp_obj,filename) #save data of parameter in pickle file
            loaded.append(sig)
        except pyuda.UDAException as err: #exception for param not in database
            notloaded.append(sig)
    
    # print out info on loaded signals:
    if not loaded:
        print('%d: No signal could be loaded!'%shot)
    elif not notloaded:
        print('%d: All signals could be loaded and saved!'%shot)#: ',*loaded)
    else:
        #print('Signals loaded and saved: ',*loaded)
        print('%d: Signals that could not be loaded: '%shot,*notloaded)
"""
#dsd
