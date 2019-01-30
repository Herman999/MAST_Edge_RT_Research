# -*- coding: utf-8 -*-
"""
@author: Jan-Peter Baehner
Version X.0 ; 20.10.2016
"""
import numpy as np
import matplotlib.pyplot as pl
  
# Plot-Funktionen  
def plot_data(x,y,xerror=[],yerror=[],xLabel='',yLabel='',title='',legend=True,dataname='data',legendloc='best',linestyle='.'):
    '''Plottet die Funktionswerte mit Errorbalken
    Nur Funktionswerte erforderlich

    Plots the function values ​​with error bars
    Only functional values ​​required
    '''
    if not list(xerror) and not list(yerror):
        pl.errorbar(x,y,fmt=linestyle,ecolor="red",label=dataname)
    elif not list(xerror) and list(yerror):
        pl.errorbar(x,y,yerr=yerror,fmt=linestyle,ecolor="red",label=dataname)
    elif list(xerror) and not list(yerror):
        pl.errorbar(x,y,xerr=xerror,fmt=linestyle,ecolor="red",label=dataname)
    elif list(xerror) and list(yerror):
        pl.errorbar(x,y,xerr=xerror,yerr=yerror,fmt=linestyle,ecolor="red",label=dataname)
    pl.xlabel(xLabel)
    pl.ylabel(yLabel)
    pl.title(title)
    if legend==True:
        pl.legend(fontsize=12,loc=legendloc)
    
def plot_data_odrFit(fitfunction,output,x,y,xerror=[],yerror=[],xLabel='',yLabel='',title='',dataname='data',legendloc='best',linestyle='.'):
    '''Plottet die Funktionswerte mit Errorbalken und der gefitteten Funktion
    fitfunction: gefittete Funktion, muss als Funktion übergeben werden
    output = odr_output

    Plots the function values ​​with error bars and the fitted function
    fitfunction must be passed as a function
    '''
    #Plot der Daten inkl. Fehler (data including errors):
    plot_data(x,y,xerror,yerror,xLabel=xLabel,yLabel=yLabel,title=title,legend=False,dataname=dataname)
    #Plot des Fits:
    xfit=np.linspace(min(x),max(x),10*len(x))     #array für eine schöne Fitfunktion (for a nice fit function)
    fy=fitfunction(output.beta,xfit)          #array mit Werten den Fitfunktion (diese muss numpy-array verarbeiten können)  (array with values ​​of the fit function (which must be able to process numpy-array))
    pl.plot(xfit,fy,label='fit')
    pl.legend(fontsize=12,loc=legendloc)

def plot_data_curveFit(fitfunction,popt,x,y,xerror=[],yerror=[],xLabel='',yLabel='',title='',dataname='data',legendloc='best',linestyle='.'):
    '''Plottet die Funktionswerte mit Errorbalken und der gefitteten Funktion
    fitfunction: gefittete Funktion, muss als Funktion übergeben werden
    popt aus scipy.optimize.curve_fit
    
    Plots the function values ​​with error bars and the fitted function
    fitfunction must be passed as a function
    pops out scipy.optimize.curve_fit
    '''
    #Plot der Daten inkl. Fehler:
    plot_data(x,y,xerror,yerror,xLabel=xLabel,yLabel=yLabel,title=title,legend=False)
    #Plot des Fits:
    xfit=np.linspace(min(x),max(x),10*len(x))     #array für eine schöne Fitfunktion
    fy=fitfunction(xfit,*popt)          #array mit Werten den Fitfunktion (diese muss numpy-array verarbeiten können)
    pl.plot(xfit,fy)
    pl.legend([dataname,"fit","error"],fontsize=14,loc=legendloc)

def plot_residuals(x, res, res_error=[], xLabel='', res_unit='',title='',lang='DE'):
    '''Bilingual residues plot function
    erstellt Residuenplot/ gives plot of residuals
    select language with lang='DE'/'EN' '''
    #erstelle y-Achsen-Beschriftung
    ytext={'DE':'Residuen','EN':'residuals'}
    if res_unit:
        yLabel=ytext[lang]+" in " + res_unit
    else :
        yLabel=ytext[lang]
    #erstelle Titel   
    restext={'DE':'Residuen zu ','EN':'residuals to '}
    if title:
        resname=restext[lang]+title
        pl.title(resname)
    else:
        resname=''
    #Plot
    plot_data(x,res,yerror=res_error,xLabel=xLabel,yLabel=yLabel,title=resname,legend=False)
    nulllinie = np.zeros(len(x))
    pl.plot(x,nulllinie,color='black')

    
'''zum schnellen plotten von Spektren aus der HEXOS-Kalibration
for fast plotting spectra from the HEXOS calibration'''
def specplot(data,names,xlimit=[],ylimit=[],thres=None):
    if thres==None:
        thres=np.zeros(len(data))
    for i in range(len(data)):
        pl.figure(i)
        pl.plot(data[i][0],data[i][1])
        pl.hlines(thres[i],min(data[i][0]),max(data[i][0]))
        pl.xlabel('wavelength /nm')
        pl.ylabel('intensity')
        if xlimit:
            pl.xlim(xlimit[i])
        if ylimit:
            pl.ylim(ylimit[i])
        pl.title(names[i])
        
#eigentlich unnötig: (actually unnecessary:)
def savePlotAs(name,datatype='png',facecolor='w'):
    '''Speichert den Plot in einen Ordner Plots, dieser muss selbst erstellt werden !!!!!!
    datatype="svg" oder "pdf" für eine Vektorgrafik'''
    arg = "Plots/"+name + "." + datatype
    pl.savefig(arg, facecolor=facecolor)