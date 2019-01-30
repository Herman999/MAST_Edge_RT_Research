# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 11:10:33 2018

@author: rbatt
"""
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 11:41:24 2018

@author: rbatt

Signal dictionaries for different sessions
"""

# session 10Nov11:
shotnos = [27443, # no h-mode: few signals
         27444, # good h-mode, killed by breakdown at 320 ms
         27445, # puffing through LHt, h-mode lost at 315 ms
         27446, # h mode delayed by 10 ms 
         27447, # h-mode lost. Success because reduced SS NBI power
         27448, # low density: missing ANE
         27449, # h mode reestablished, interferometer back ***
         27450, # thomson data just before transition         
         27451, # brief h mode periods: missing ANE
         27452, # extended dithering at transition
         27453, # brief sawtooth induced h mode: missing ANE
         27454, # brief h mode still
         ]
# below lists signals currently in our data set, many more exist
# notice different asm (h-mode) and ayc signal names
signals=dict(# NEW AT TOP
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
     

# orginial dictionary inherited from JP + some additions up to 8/11/18       
originalsignals = dict(Dalphint='ADA_DALPHA INTEGRATED',
            ngrad='ADG_DENSITY_GRADIENT', #from Dalpha signal for identification of H-mode
            npos='ADG_GRADIENT_POSITION', #from Dalpha signal
#            Dalphtan='AIM_DA/HM10/T', #Dalpha Tangential mid plane plasma view
#            Dalphcentre='AIM_DA/HU10/R', #Daplpa View of upper centre column region
            Dalphstrp='AIM_DA/HU10/U', #Dalpha View of upper strike point region under the top plate
#            Daplhshield='AIM_DA/TO10', #Dalpha View of lower coil shield and centre column region
            IP='AMC_PLASMA CURRENT',
            
            #electron density and temperatures from Thomson scattering:
            NE='ATM_NE', #electron density from core Thomson
            NE0='ATM_NE_CORE', #core electron density from core Thomson
            #NE_RC='ATM_N_E_RC', #density from core TS but ruby calibrated
            TE='ATM_TE', #electron temperature from core Thomson
            TE0='ATM_TE_CORE', #core temperature from core Thomson
            PE='ATM_PE', #electron pressure from core TS
            PE0='ATM_PE_CORE', #core electron pressure from core TS
            R_CTS='ATM_R', #major radius for core Thomson measurement
            R2_CTS='ATM_R2', #major radius for core Thomson measurement for each timeslot
            R0_CTS='ATM_R_CORE', #magnetic centre (peak Te) for core Thomson
            #NE_R='ATS_NE', #from ruby Thomson
            NE12_R='ATS_NE/12', #from ruby Thomson
            #TE_R='ATS_TE', #from ruby Thomson
            TE12_R='ATS_TE/12', #from ruby Thomson
            #PE_R='ATS_PE', #from ruby TS
            PE12_R='ATS_PE/12', #from ruby TS
            #R_R='ATS_R', #major radius in ruby Thomson
            R12_R='ATS_R/12', #major radius in ruby Thomson
            
            # new AYC data: added Ronan 4/11/18
            AYC_NE = 'AYC_NE',
            AYC_NE0 = 'AYC_NE0',
            AYC_TE = 'AYC_TE',
            AYC_TE0 = 'AYC_TE0',
            AYC_PE = 'AYC_PE',
            AYC_R_CTS = 'AYC_R_CTS',
            AYC_R0_CTS = 'AYC_R0_CTS',
                
            # new added Ronan 8/11/18
            ADA_DALPHA_RAW = 'ADA_DALPHA RAW_FULL',
            ADA_DALPHA_INVERTED = 'ADA_DALPHA INVERTED',
            AIM_DA_HM = 'AIM_DA/HM10/T',
            AIM_DA_TO = 'AIM_DA/TO10',
            ASB_CII = 'ASB_CII_DGA',
            ASB_OII = 'ASB_OII_DGA',
            ASB_SVN_REVISION = 'ASB_SVN_REVISION',
        
            AYE_NE = 'AYE_NE',
            AYE_PE = 'AYE_PE',
            AYE_TE = 'AYE_TE',
            AYE_R = 'AYE_R',
            AYE_TIME = 'AYE_TIME',
        
            ASM_HM = 'ASM_HM/RATING',
            ASM_HM_PER = 'ASM_HM/PERIODS',
            
            ANE_DENSITY = 'ANE_DENSITY', #
            ANE_CO2 = 'ANE_CO2',

            # possible Zeff data
            # 'Z-Effective from ZEBRA 2D visible bremsstrahlung camera and Thomson scattering'
            Zeff_C='AZE_CENTRAL_ZEFF_ND-YAG',
            #Zeff='AZE_ZEFF', # this is available in none of the investigated shots
            Zeff_NDY='AZE_ZEFF_ND-YAG',
            Zeff_R='AZE_ZEFF_RUBY',
        
            # CO2-interferometry
#            N_CO2='ANE_DENSITY',
#            CO2='ANE_CO2',
            
            # 'time resolved' CXRS
#            Tpla='ACT_C_PLA_TEMPERATURE',
#            Ti='ACT_C_SS_TEMPERATURE', # ion temp. from CXRS with Carbon in SS beam (?)
#            vi='ACT_C_SS_VELOCITY', # ion velocity from CXRS with Carbon in SS beam (?)
            
            #H-mode detector:
#            HMper='ASM_HM/PERIODS', #a trace of the interesting and probable H-Mode periods. The height of each period (again between 0 and 1) gives an indication of how likely it is to be H-Mode.
#            HMrat='ASM_HM/RATING',  #an H-Mode rating from 0 to 1 throughout the shot
            
            # EFIT calculation ################################################
            BT='EFM_BVAC_RMAG',
            Vloop='ESM_V_LOOP_DYNAMIC',	#Plasma surface Vloop, calculated allowing for the movement of the LCFS; i.e. in the observer's frame of reference.
#            BEPMHD='EFM_BETAP',
#            BETMHD='EFM_BETAT',
            
            #Magnetic configuration / geometry:
            RGEO='EFM_GEOM_AXIS_R(C)', # major radius
            AMIN='EFM_MINOR_RADIUS', # minor radius
            VOL='EFM_PLASMA_VOLUME', # plasma volume
            SAREA='ESM_SURFACE_AREA',	# plasma surface area
            AREA='EFM_PLASMA_AREA', # Area of poloidal cross-section of plasma; f(B)
            #basic EFIT values for LCFS
            LCFS_N='EFM_LCFS(N)_(C)', #No. of coords on LCFS (61x1)
            LCFS_R='EFM_LCFS(R)_(C)', #r-coords of seperatrix in m (61x2600)
            LCFS_Z='EFM_LCFS(Z)_(C)', #z-coords of seperatrix in m (61x2600)
            LCFS_L='EFM_LCFS_LENGTH', #length of LCFS in m (61x1)H
            LCFS_R_out='EFM_R(PSI100)_OUT', # Outboard radius of 100% normalised magnetic flux (seperatrix); f(B)
            LCFS_R_in='EFM_R(PSI100)_IN', # Inboard radius of 100% normalised magnetic flux (seperatrix); f(B)
            # X-point positions
            X1R='EFM_XPOINT1_R(C)', # Radius of first X-point; f(B)
            X1Z='EFM_XPOINT1_Z(C)', # Height of first X-point; f(B)
            X2R='EFM_XPOINT2_R(C)', # Radius of second X-point; f(B)
            X2Z='EFM_XPOINT2_Z(C)', # Height of second X-point; f(B)
            # Strike point positions (?)
            ILSPZ='ESM_ILSPZ', # IL SP height [m] (inner lower strike point?)
            IUSPZ='ESM_IUSPZ', # IU SP height [m] (inner upper strike point?)
            OLSPR='ESM_OLSPR', # OL SP radius [m] (outer lower strike point?)
            OUSPR='ESM_OUSPR', # OU SP radius [m] (outer upper strike point?)
            # configuration parameter:
#            dell='EFM_TRIANG_LOWER',	
#            delu='EFM_TRIANG_UPPER',	
            KAPPA='EFM_ELONGATION',
            
            # energies and power
            WMHD='EFM_PLASMA_ENERGY',
            DWMHD='ESM_W_DOT', # rate of change of plasma energy
            POHM='ESM_PPHIX', # ohmic power, ESM_P_PHI - ESM_X.
            Ploss='ESM_P_LOSS',	#Power crossing the separatrix, given as Paux + Pf - dW/dt - X. The auxiliary power is taken as ESM_P_AUX
            #Plossguess='ESM_P_LOSS_GUESS', 
            Paux='ESM_P_AUX', #Auxiliary power to the plasma, adjusted from ANB_TOT_SUM_POWER # basically the same as PINJ but on different timebasis
            PINJ='ANB_TOT_SUM_POWER', #NBI power
            PRAD='ABM_PRAD_POL	', #Total radiated power from poloidal array

            # confinement parameters
            Q95='EFM_Q_95',	
            TAUTOT='ESM_TAU_E_GUESS')


