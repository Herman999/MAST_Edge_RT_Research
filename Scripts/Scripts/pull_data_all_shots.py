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

#shotno=int(input('Please enter shot-number: ')) # shot number, e.g. 22652 for helium session
shotnos=[#He sessions:
        20841, 20842, 20843, 20848, 20849, 20850, 20852,                       #06NOV08
        22647, 22649, 22650, 22652, 22653, 22656,                              #10JUN09
        20856, 20859, 20861, 20862, 20863,                                     #11NOV08
        20474, 20475, 20476, 20479, 20480,                                     #25SEP08
        20377, 20378, 20379, 20380, 20381,                                     #18SEP08
        # X-point hight variation sessions
        13042, 13043, 13044, 13045, 13046, 13047,                              #26MAY05
        13704, 13705, 13706, 13707, 13708, 13709, 13710, 13711,                #10AUG05
        14545, 14546, 14547, 14548, 14552, 14554, 14555]                       #08NOV08
#        23822, 23824, 23825, 23826, 23827, 23832, 23835, 23837, 23841, 23842, 23843, 23844] #09DEC09 - not used

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
