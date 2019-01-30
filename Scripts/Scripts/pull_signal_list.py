# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 14:14:24 2018

@author: jb4317, Jan-Peter Baehner

Routine to write list of accessible signals for an individual shot.
"""
import pyuda
client=pyuda.Client()

#ask for shot number
shotno=int(input('Please enter shot-number: ')) # shot number, e.g. '22652' in helium session

#load list of all accessible analysed (type A) signals for shot:
rA=client.list(pyuda.ListType.SIGNALS,shot=shotno,signal_type='A')

#%% write list to txt-file
filename='signals_A_%d.txt' %shotno #create filename specific to shot number
filedir='../MASTdata/'+filename
s=open(filedir,'w') #open/create txt-file in 'write'-modus

for sig in rA: #loop through signals in list
    siglist=''
    for item in sig:
        siglist+=item+';'   #seperate properties of each signal by ';' - easy to import by MS Excel
    siglist=siglist[:-1]    #delete last ';'
    s.write('%s\n' %siglist)#write line of signal to txt-file
s.close()