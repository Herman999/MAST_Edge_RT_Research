# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 10:42:29 2019

@author: rbatt
"""


# session 26MAY05:
#       shots = [13042 - 13047]
# below lists signals currently in our data set, many more exist
signals=dict(
            Dalphstrp='AIM_DA/HU10/U', #Dalpha View of upper strike point region under the top plate
            NE0='ATM_NE_CORE', #core electron density from core Thomson
            TE0='ATM_TE_CORE', #core temperature from core Thomson
            PE0='ATM_PE_CORE', #core electron pressure from core TS
            R_CTS='ATM_R', #major radius for core Thomson measurement
            R0_CTS='ATM_R_CORE', #magnetic centre (peak Te) for core Thomson
            NE12_R='ATS_NE/12', #from ruby Thomson
            TE12_R='ATS_TE/12', #from ruby Thomson
            PE12_R='ATS_PE/12', #from ruby TS
            Zeff_C='AZE_CENTRAL_ZEFF_ND-YAG',
            Zeff_NDY='AZE_ZEFF_ND-YAG',

            EFM_R_PSI100_OUT = 'EFM_R(PSI100)_OUT', # Outboard radius of 100% normalised magnetic flux; f(B)
            EFM_R_PSI90_OUT = 'EFM_R(PSI90)_OUT', # Outboard radius of 90% normalised magnetic flux; f(B)
            EFM_R_PSI95_OUT = 'EFM_R(PSI95)_OUT', # Outboard radius of 95% normalised magnetic flux; f(B)
            
            # ADA Dalpha signals
            ADA_DALPHA_INVERTED = 'ADA_DALPHA_INVERTED',
            ADA_DALPHA_RAW = 'ADA_DALPHA_RAW',
            
            # AIM Dalpha signals
            AIM_DA_HM = 'AIM_DA/HM10/T', # tangential mid plane plasma view
            AIM_DA_TO = 'AIM_DA/TO10', # view of lower coil shield and centre column region
            Dalphint = 'ADA_DALPHA INTEGRATED',
            
            # ANE CO2 interferometry
            ANE_CO2 = 'ANE_CO2',
            ANE_DENSITY = 'ANE_DENSITY',
            
            # ASB Dalpha like signals (??)
            ASB_CII = 'ASB_CII',
            ASB_OII = 'ASB_OII',
            ASB_SVN_REVISION = 'ASB_SVN_REVISION',
            
            # ASM H-mode indicators
            ASM_HM = 'ASM_HM',
            ASM_HM_PER = 'ASM_HM_PER', 
            
            # AYC core thomson scattering
            AYC_NE ='AYC_NE',
            AYC_NE0 = 'AYC_NE0',
            AYC_PE = 'AYC_PE',
            AYC_R0_CTS = 'AYC_R0_CTS',
            AYC_R_CTS = 'AYC_R_CTS',
            AYC_TE = 'AYC_TE',
            AYC_TE0 = 'AYC_TE0',
            
            # AYE edge thomson scattering
            AYE_NE = 'AYE_NE',
            AYE_PE = 'AYE_PE',
            AYE_R = 'AYE_R',
            AYE_TE = 'AYE_TE',
            AYE_TIME = 'AYE_TIME',
            
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