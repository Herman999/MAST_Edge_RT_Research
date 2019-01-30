# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 14:49:44 2016

@author: Jan-Peter Baehner

(Version 1.0 - 20.10.2016)
Version 2.0 - 27.06.2018 - translated to English, edited plot of curve_complete

"""
import numpy as np
import plotter
import matplotlib.pyplot as pl
from scipy.odr import Model, RealData, ODR
from scipy.optimize import curve_fit

'''################# Fit funktionen ##############'''

def ODR_Fit(function,p0,x,y,xerror=[],yerror=[],fit_type=None):
    '''Fit with ODR from 'scipy'-library
    function : arbitrary fct, needs to be defined beforehand: function(p,x); p is an array of the fcn's parameter
    x, y: arrays with data
    xerror, yerror: arrays with uncertainties for x and y respectively (must not be 0!!), optional
    fit_type: default None for orthogonal distance regression, fit_type=2 for least square fit
    documentation: http://docs.scipy.org/doc/scipy/reference/generated/scipy.odr.Output.html#scipy.odr.Output'''
    model = Model(function) #scipy.ord.Model(function)
    if not list(xerror) and not list(yerror):
        data = RealData(x,y)
    elif not list(xerror) and list(yerror):
        data = RealData(x,y,sy=yerror)
    elif list(xerror) and not list(yerror):
        data = RealData(x,y,sx=xerror)
    elif list(xerror) and list(yerror):
        data = RealData(x,y,sx=xerror,sy=yerror)
    odr = ODR(data,model,beta0=p0)
    odr.set_job(fit_type=fit_type)
    return odr.run()

def print_odr_Output(output):
    '''Prints out overview of most important results from ODR-Fit'''    
    print("Estimated parameters with standard errors:")
    for i in range(len(output.beta)):
        print("p%i : %.3E (%.3E)" %(i, output.beta[i], output.sd_beta[i]))
    #print("Kovarianzmatrix: ")
    #print(output.cov_beta)
    print( "Chi^2 = ", round(output.sum_square,4))
    print( "Chi^2 / ndf = ", round(output.res_var,4))

def data_selector(data,xlimit=[]):
    '''Selects data in xlimit (if no xlimit or xlimit=0 the whole data is taken)
    gives x,xerror,y,yerror (the errors are 0 if not given in data)
    given three arguments in data will assume x,y,yerror'''
    if xlimit: 
        irange=[i for i in range(len(data[0])) if data[0][i]>=xlimit[0] and data[0][i]<=xlimit[1]]
        a=min(irange)
        b=max(irange)
        #print(a,b)
    else:
        a=0
        b=len(data[0])
    if len(data)==4:
        x,xerror,y,yerror=data[0][a:b],data[1][a:b],data[2][a:b],data[3][a:b]
    elif len(data)==3:
        x,y,yerror=data[0][a:b],data[1][a:b],data[2][a:b]
        xerror=[]
    elif len(data)==2:
        x,y = data[0][a:b],data[1][a:b]
        xerror=[]
        yerror=[]
    else:
        raise ValueError('data has wrong form')
    return x,xerror,y,yerror
    
'''######################## ODR-Fitter ##################'''

def odr_complete(data,function,difffunction,p0,xlimit=[],printer=False,plot=True,title='',xname='',yname='',dataname='data',legendloc='best',save=False,plotdatatype='png',res_unit='',lang='EN',fit_type=None):
    """-fits the function "function" to "data" using scipy.odr.ODR
    -Creates plot, residual plot and can save them in folder 'Plots'
    -prints out parameter of fit including errors, covariance matrix and Chi^2
    -returns: array([fit parameter, errors])"""
    #Required:  
    #data=[x,xerror,y,yerror]
    #function(p,x) of the form  .. p[1]*m+p[0].. i.e. p is an array
    #difffunction(p,x) = derivative of funtion with same p
    #p0=[,,,] initial guess for the fitfuntion, must have same form as p
    
    #Optional:
    #xlimit= limits of x-axis to be fitted; [] implies whole regime of x-data
    #printer = boolean for whether or not the fit parameters are supposed to be printed out
    #plot = boolean for whether or not the fit is supposed to be plotted
    
    #The following are only relevant for plot=True:
    #title= title of plot
    #xname = description of x data or x-axis
    #yname = description of y data or y-axis
    #dataname = label of dataset (for legend)
    #legendloc = position of legend in plot
    #save = boolean for whether or not the plot is supposed to be saved
    #plotdatatype = datatype of plotdfiles, e.g. 'pdf','jpeg' etc.
    #res_unit = units of residuals as a string
    #lang = 'language' - language of plot-labels ('EN'-english, 'DE'-german)
    #fit_type = None (default) for orthogonal distance regression, fit_type=2 for least square fit
    
    #select Data
    x,xerror,y,yerror=data_selector(data,xlimit)
    #Fit
    output=ODR_Fit(function,p0,x,y,xerror,yerror,fit_type=fit_type)
    if printer:
        print_odr_Output(output)                         #print out fit data
    
       
    if plot:
        #data-plot
        facecolor=(.9,.9,.9)
        fig=pl.figure('fitplot'+title+dataname,figsize=(20,15),facecolor=facecolor)
        fig.subplots_adjust(hspace=0) 
        axs1=pl.subplot(211)
        plotter.plot_data_odrFit(function,output,x,y,xerror,yerror,xname,yname,title=title,dataname=dataname,legendloc=legendloc)
        
        #create residuals as array (x,y as arrays)
        res=y-function(output.beta,x)
        #create error on residuals as array
        if not list(xerror) and not list(yerror):
            reserror=[]
        elif not list(xerror) and list(yerror):
            reserror=yerror
        elif list(xerror) and not list(yerror):
            reserror=[np.sqrt(xerror[i]**2*(difffunction(output.beta,x[i]))**2) for i in range(len(x))]
        elif list(xerror) and list(yerror):
            reserror=[np.sqrt(yerror[i]**2+xerror[i]**2*(difffunction(output.beta,x[i]))**2) for i in range(len(x))]

        #residual-plot
        axs2=pl.subplot(212, sharex=axs1)
        plotter.plot_residuals(x,res,reserror,xLabel=xname,res_unit=res_unit,lang=lang)
        #pl.tight_layout()  #gives a thight look of the subplots
        if save:
            pl.savefig(title+'_'+dataname+'fitplot.'+plotdatatype,facecolor=facecolor)
        pl.show()
        return [output.beta,output.sd_beta,output.res_var]
    else:
        return [output.beta,output.sd_beta,output.res_var]

'''######################## Curve-Fitter ##################'''


def curve_complete(data,function,p0,xlimit=[],printer=False,plot=True,title='',xname='',yname='',dataname='',legendloc='best',save=False,plotdatatype='png',res_unit='',lang='EN'):
    """--fits the function "function" to "data" using scipy.optimize.curve_fit (does not need uncertainties on data, but can only handle uncertainties on y-data)
    -Creates plot, residual plot and can save them in folder 'Plots'
    -prints out parameter of fit including errors from covariance matrix
    -returns: (popt,pcov) fitparameter and covariance matrix """    
    #Required:  
    #data=[x,y(,yerror)]
    #function(x,a,b,c) of form  .. a*x+b.. i.e. parameter must be handed over to fcn individually
    #derivative of function is not needed, since there are no uncertainties on x
    #p0=[,,,] initial guess for fitfuntion
    
    #Optional:
    #xlimit= limits of x-axis to be fitted; [] implies whole regime of x-data
    #printer = boolean for whether or not the fit parameters are supposed to be printed out
    #plot = boolean for whether or not the fit is supposed to be plotted
    
    #The following are only relevant for plot=True:
    #title= title of plot
    #xname = description of x data or x-axis
    #yname = description of y data or y-axis
    #dataname = label of dataset (for legend)
    #legendloc = position of legend in plot
    #save = boolean for whether or not the plot is supposed to be saved
    #plotdatatype = datatype of plotdfiles, e.g. 'pdf','jpeg' etc.
    #res_unit = units of residuals as a string
    #lang = 'language' - language of plot-labels ('EN'-english, 'DE'-german)
    
    
    #select Data
    x,xerror,y,yerror=data_selector(data,xlimit)
    #Fit
    if list(yerror):
        popt,pcov=curve_fit(function,x,y,p0=p0,sigma=yerror)       #Fit
    else:
        popt,pcov=curve_fit(function,x,y,p0=p0)       #Fit
    if printer: #prints the fit data
        print("fit parameter and errors from covariance matrix")
        for i in range(len(popt)):                                 
            print("p%i : %.4E (%.4E)" %(i, popt[i], pcov[i,i]))
    
    if plot:
        #data-plot
        facecolor=(.9,.9,.9)
        fig=pl.figure('fitplot'+title+dataname,figsize=(20,15),facecolor=facecolor)
        fig.subplots_adjust(hspace=0)
        ax1=pl.subplot(211)
        plotter.plot_data_curveFit(function,popt,x,y,xerror,yerror,yLabel=yname,title=title,dataname=dataname,legendloc=legendloc)
        
        #create residuals as array (x,y as arrays)
        res=y-function(x,*popt)
        #create error on residuals as array
        reserror=yerror #since no xerror
        
        #residual-plot    
        axs2=pl.subplot(212, sharex=ax1)
        plotter.plot_residuals(x,res,reserror,xLabel=xname,res_unit=res_unit,lang=lang)
        #pl.tight_layout() #gives a thight look of the subplots
        if save:
            pl.savefig(title+'_'+dataname+'fitplot.'+plotdatatype,facecolor=facecolor)
        pl.show()
    return [popt,pcov]
    
    
'''################# useful functions to use for ODR #################'''
    
def straight_odr(p,x):
    return p[0]*x+p[1]
def diffstraight_odr(p,x):
    return p[0]    
    
def gauss_odr(p,x):
    return p[0]*np.exp(-(x-p[1])**2/p[2])+p[3]      # p=(1/2*pi*sig^2;mu,2*sig^2,const)   
def diffgauss_odr(p,x):
    return p[0]*np.exp(-(x-p[1])**2/p[2])*(p[1]-x)/(p[2]/2)
    
def lorentz_odr(p,x):
    return p[0]*p[1]/np.pi/((x-p[2])**2+p[1]**2)+p[3]
def difflorentz(p,x):
    return p[0]*p[1]/np.pi*2*(p[2]-x)/((x-p[2])**2+p[1]**2)**2

#Pseudo-Voigt-distribution
def pvoigt_odr(p,x):
    if 0 < p[2] and p[2] < 1:
        return (  (1-p[2])*np.exp(-((x-p[0])/p[1])**2)  +  p[2]/(1+((x-p[0])/p[1])**2)  )*p[3]  +  p[4]
    else:
        return -1
def diffpvoigt_odr(p,x):
    return ((1-p[2])*np.exp(-((x-p[0])/p[1])**2) +  p[2]/(1+((x-p[0])/p[1])**2)**2)  *2*(p[0]-x)/p[1]  *p[3]

    
'''################# practical example functions for Curve_Fit #################'''
    
def straight_curve(x,m,n):
    return m*x+n
    
def gauss_curve(x,a,b,c,d):
    return a*np.exp(-(x-b)**2/c)+d      # p=(1/2*pi*sig^2;mu,2*sig^2,const)   
    
def lorentz_curve(x,a,b,c,d):
    return a*b/np.pi/((x-c)**2+b**2)+d
#Pseudo-Voigt-distribution
def pvoigt_curve(x,x0,w,n,a,c):
    if 0 < n and n < 1:
        return (  (1-n)*np.exp(-((x-x0)/w)**2)  +  n/(1+((x-x0)/w)**2)  )*a  +  c
    else:
        return -1
