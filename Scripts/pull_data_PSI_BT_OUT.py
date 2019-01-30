# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21  2018

@author: jb4317, Jan-Peter Baehner

version2

New routine to pull data from MAST data base via pyuda and transfere to files
"""
import pyuda
client=pyuda.Client()   #set up pyuda

from data_access_funcs import save_signal_data

# session 06Oct11:
shotnos = [
    20377,	
    20377,	
    20378,	
    20378,	
    20379,	
    20379,	
    20380,	
    20380,	
    20381,	
    20381,	
    20476,	
    20476,	
    20479,	
    20479,	
    20480,	
    20480,	
    27030,	
    27030,	
    27035,	
    27035,	
    27036,	
    27036,	
    27037,	
    27037,	
    27444,	
    27444,	
    27446,	
    27446,	
    27448,	
    27448,	
    27449,	
    27449,	
    27450,	
    27450,	
    27451,	
    27451,	
    27451,	
    27451,	
    27453,	
    27453,	
    27454,	
    27454,	
    13704,	
    13704,	
    14545,	
    14545,	
    14546,	
    14546,	
    14547,	
    14547,	
    14548,	
    14548,	
    14552,	
    14552,	
    14554,	
    14554,	
    14555,	
    14555,	
    24134,	
    24134,	
    24133,	
    24133,	
    24133,	
    24133,	
    24132,	
    24132,	
    24132,	
    24132,	
    24131,	
    24131,	
    24130,	
    24130,	
    24129,	
    24129,	
    24128,	
    24128,	
    24127,	
    24127,	
    24126,	
    24126,	
    24125,	
    24125,	
    24124,	
    24124,	
    24215,	
    24215,	
    24216,	
    24216,	
    24216,	
    24216,	
    24324,	
    24324,	
    24324,	
    24324,	
    24325,	
    24325,	
    24325,	
    24325,	
    24326,	
    24326,	
    24327,	
    24327,	
    24328,	
    24328,	
    24329,	
    24329,	
    24329,	
    24329,	
    24330,	
    24330,	
]
# session ended early due to inadequate progress. h-mode weaker. suggestion its time to boronise.


# below lists signals currently in our data set, many more exist
signals=dict(# NEW AT TOP
            EFM_R_PSI100_OUT = 'EFM_R(PSI100)_OUT', # Outboard radius of 100% normalised magnetic flux; f(B)
            EFM_R_PSI90_OUT = 'EFM_R(PSI90)_OUT', # Outboard radius of 90% normalised magnetic flux; f(B)
            EFM_R_PSI95_OUT = 'EFM_R(PSI95)_OUT', # Outboard radius of 95% normalised magnetic flux; f(B)
            
            # BT OUT
            )     

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
