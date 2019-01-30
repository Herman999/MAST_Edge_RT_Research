# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 13:10:29 2018

@author: jb4317, Jan-Peter Baehner

Collection of Pth scalings from several publications.
"""
import numpy as np

# J.A. Snipes, 2002, 'Multi-Machine Global Confinement and H-mode Threshold Analysis', 
# ITPA Confinement and H-mode Threshold Database Working Group presented by J. A. Snipes; Topic: CT/P-04
def Snipes02_scaling1(n,B,a,R):
    '''Multi machine scaling from 'Multi-Machine Global Confinement and H-mode Threshold Analysis', ITPA Confinement and H-mode Threshold Database Working Group presented by J. A. Snipes. 2002. Topic: CT/P-04
    n - density in 10^20 m^-3
    B - toroidal magn. field in T
    a - minor radius in m
    R - major radius in m
    Returns Pth in MW
    '''
    Pth=1.67* n**0.61 *abs(B)**0.78 *a**0.89 *R**0.94
    return Pth

def Snipes02_scaling2(n,B,S):
    '''Multi machine scaling from 'Multi-Machine Global Confinement and H-mode Threshold Analysis', ITPA Confinement and H-mode Threshold Database Working Group presented by J. A. Snipes. 2002. Topic: CT/P-04
    7 tokamak scaling
    n - density in 10^20 m^-3
    B - toroidal magn. field in T
    S - plasma surface area in m^2
    Returns Pth in MW
    '''
    Pth=0.042* n**0.64 *abs(B)**0.78 *S**0.94 
    return Pth

# =============================================================================
# =============================================================================

# Y R Martin et al 2008 J. Phys.: Conf. Ser. 123 012033

def Martin08_scaling1(n,B,a,R):
    '''Latest global scaling from ITPA threshold data base working group.
    Y R Martin et al 2008 J. Phys.: Conf. Ser. 123 012033
    Includes 7700 time slices (ts) from 14 tokamaks.
    n - density in 10^20 m^-3
    B - toroidal magn. field in T
    a - minor radius in m
    R - major radius in m
    Returns Pth in MW
    '''
    Pth=2.15* n**0.782 *abs(B)**0.772 *a**0.975 *R**0.999
    return Pth

def Martin08_scaling2(n,B,S):
    '''Latest global scaling from ITPA threshold data base working group.
    Y R Martin et al 2008 J. Phys.: Conf. Ser. 123 012033
    Includes 7700 time slices (ts) from 14 tokamaks.
    n - density in 10^20 m^-3
    B - toroidal magn. field in T
    S - plasma surface area in m^2
    Returns Pth in MW
    '''
    Pth=0.0488* n**0.717 *abs(B)**0.803 *S**0.941 
    return Pth

# =============================================================================
# =============================================================================

# He scaling from D C McDonald et al 2004 Plasma Phys. Control. Fusion 46 519 with Martin_2008 as D-scaling

def McDonald04_scaling1(n,B,a,R):
    '''He scaling based on Martin08 scaling
    n - density in 10^20 m^-3
    B - toroidal magn. field in T
    a - minor radius in m
    R - major radius in m
    Returns Pth in MW
    '''
    Pth_Dmartin08=2.15* n**0.782 *abs(B)**0.772 *a**0.975 *R**0.999
    M=2 # mass normalized to mass of D
    Z=2 # charge normalized to charge of D
    Pth_He=M**(-1.1)*Z**1.6*Pth_Dmartin08
    return Pth_He

def McDonald04_scaling2(n,B,S):
    '''He scaling based on Martin08 scaling
    n - density in 10^20 m^-3
    B - toroidal magn. field in T
    S - plasma surface area in m^2
    Returns Pth in MW
    '''
    Pth_Dmartin08=0.0488* n**0.717 *abs(B)**0.803 *S**0.941 
    M=2 # mass normalized to mass of D
    Z=2 # charge normalized to charge of D
    Pth_He=M**(-1.1)*Z**1.6*Pth_Dmartin08
    return Pth_He

def McDonald04_scaling3(Pth):
    '''He scaling based on input Pth for deuterium
    Pth for deuterium
    Returns Pth_He in MW
    '''
    M=2 # mass normalized to mass of D
    Z=2 # charge normalized to charge of D
    Pth_He=M**(-1.1)*Z**1.6*Pth
    return Pth_He

# =============================================================================
# =============================================================================

# new scaling from Takizuka_2004 (ITPA H-mode Power Threshold Database Working Group presented by T Takizuka 2004 Plasma Phys. Control. Fusion 46 A227)
mu0=4e-7*np.pi #vacuum magnetic permeability

def Takizuka04_scaling(n,Bt,S,a,R,Ip,n_err,Bt_err,S_err,a_err,R_err,Ip_err):
    '''Alternative scaling including effects of aspect ration A, effective charge Zeff, and absolute magn. field at outer mid-plane plasma surface.
    Not considering the effect of Zeff here, but calcualting an error.
    n - density in 10^20 m^-3
    Bt - toroidal magn. field in T
    S - plasma surface area in m^2
    a - minor radius in m
    R - major radius in m
    Ip - plasma current  in MA
    n_err,Bt_err,S_err,a_err,R_err,Ip_err - errors of quantities above
    
    Returns [Pth,Pth_err] in MW
    0.072*|B|out^0.7*n20^0.7*S^0.9*F(A)^gamma
    |B|out=(Btout2=Bpout2)2 with Btout=Bt x A/(A+1) and Bpout=(Ipmu0 / 2pi a) x (A-1+1)
    f(A) = 1-{2/(1+A)}0.5 ;  F(A) propto A/f(A)
    '''
    A=R/a # aspect ratio
    
    Btout=Bt*A/(A+1) # toroidal field at outer mid-plane
    Bpout=Ip*mu0/(2*np.pi*a)*(1+A**-1) # poloidal field at outer mid-plane
    Btot=np.sqrt(Btout**2 + Bpout**2) # total magnetic field at outer mid-plane surface
    # factor of effect of A:
    f=1-np.sqrt(2/(1+A))
    F=A/f
    #scaling: exponent of F is quite uncertain with 0.5+-0.5
    gamma=0.5
    #gamma_err=0.5 ignore error of gamma
    Pth=0.072* Btot**0.7 *n**0.7 *S**0.9 *F**gamma
    
    #calculate error:
    errs=[n_err,Bt_err,S_err,a_err,R_err,Ip_err]#gamma_err,
    #derivatives, normalized by Pth:
    #dPdgamma=np.log(F)
    dPdn=0.7/n
    dPdS=0.9/S
    dPdBt=0.7*Bt/(Bt**2+(Ip*mu0)**2/(2*np.pi*a)**2)
    dPdIp=0.7/Ip/((Bt*2*np.pi*a/Ip/mu0)**2+1)**2
    dPda=0.7/(a+R) + gamma/a*(R/(2*(a+R)*((2/(1+R/a))**(-1/2)-1))-1) - 0.7/a/((Bt*2*np.pi*a/Ip/mu0)**2+1)
    dPdR=-0.7/(a+R)/A - gamma/R*(R/(2*(a+R)*((2/(1+R/a))**(-1/2)-1))-1)
    #list of derivatives:
    derivs=[dPdn,dPdBt,dPdS,dPda,dPdR,dPdIp]#dPdgamma,
    squares=[(derivs[i]*errs[i])**2 for i in range(len(errs))]
    Pth_err=Pth*np.sqrt(sum(squares))
    
    return [Pth,Pth_err]

def Takizuka04_scalingZeff(n,Bt,S,a,R,Ip,Scross,k,Vloop,W,V,Zeff=None):#
    '''Alternative scaling including effects of aspect ration A, effective charge Zeff, and absolute magn. field at outer mid-plane plasma surface.
    Including the effect of Zeff here.
    n - density in 10^20 m^-3
    Bt - toroidal magn. field in T
    S - plasma surface area in m^2
    a - minor radius in m
    R - major radius in m
    Ip - plasma current in A
    Scross - plasma cross-sectional area in m^2
    k - elongation
    Vloop - surface loop voltage
    W - plasma stored energy
    V - plasma volumeReturns Pth in MW
    '''
    
    A=R/a # aspect ratio
    
    if not Zeff:
        Teff=W/(3*n*V) # effective temperature
        Scross=np.pi*k*a**2 # plasma cross-sectional area
        Zeff=Vloop*Scross*Teff**1.5 /(2*np.pi*R*Ip) # effective charge number
        print('Zeff=',Zeff)
    
    Btout=Bt*A/(A+1) # toroidal field at outer mid-plane
    Bpout=Ip*mu0/(2*np.pi*a)*(1+A**-1) # poloidal field at outer mid-plane
    Btot=np.sqrt(Btout**2 + Bpout**2) # total magnetic field at outer mid-plane surface
    
    f=1-np.sqrt(2/(1+A))
    F=A/f
    
    #scaling: exponent of F is quite uncertain with 0.5+-0.5
    Pth=0.072* Btot**0.7 *n**0.7 *S**0.9 *F**0.5 *(Zeff/2)**0.7

    return Pth