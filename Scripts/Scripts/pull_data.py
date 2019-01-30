# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21  2018

@author: jb4317, Jan-Peter Baehner

version2

New routine to pull data from MAST data base via pyuda and transfere to files
"""
import pyuda
client=pyuda.Client()   #set up pyuda

from data_access_funcs import save_signal_data,signals

shotno=int(input('Please enter shot-number: ')) # shot number, e.g. 22652 for helium session
loaded=[]
notloaded=[]
for sig in signals:
    try:
        temp_obj=client.get(signals[sig],shotno) #create temporary object pulled form MAST database
        filename=str(shotno)+'_'+sig+'.p' #create filename
        save_signal_data(temp_obj,filename) #save data of parameter in pickle file
        loaded.append(sig)
    except pyuda.UDAException as err: #exception for param not in database
        notloaded.append(sig)

#%% print out info on loaded signals:
if not loaded:
    print('No signal could be loaded!')
elif not notloaded:
    print('All signals could be loaded and saved!')#: ',*loaded)
else:
    #print('Signals loaded and saved: ',*loaded)
    print('Signals that could not be loaded: ',*notloaded)
