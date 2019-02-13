
# session 06Oct11:
shotnos = [27030, #standard shot, intermittent h-mode
           27031, #repeat standard shot, ok.
           27032, #bad shot
           27033, #NBI lost at 0.17
           27034, #one breakdown during SS injection
           27035, #poor density control -> event at 0.31
           27036, #h-mode but later entry, smaller faster ELMs than ref 26500. density on target at 0.22s but higher by time h-mode starts
           27037, #not bad, later smaller elms than reference
           27038, #abort elm a
           27039, #ok. earlier h-mode but dropped out soon after
           
           26500 #From 7 July 11, a reference shot referenced in the 6 Oct session.
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
