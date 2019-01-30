# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 12:28:08 2018

@author: Tomas
"""

# Import this using below:

#import sys
#sys.path.append(r'C:\Users\Tomas\Imperial College London\Battle, Ronan - Shared MSci project\Scripts') # "/Users/Tomas/Imperial\ College London/Battle,\ Ronan\ -\ Shared\ MSci\ project/Scripts")
#from Shot_Class import Shot


from data_access_funcs import load_signal_data
import matplotlib.pyplot as plt

    
class Shot():
    def __init__(self, ShotNumber, signals):
#       must define signals dictionary here based on shot number/session series
        self.data = {} # initialise data dictionary
        self.ShotNumber = ShotNumber
        for sig in signals:
            try:
                fn = str(ShotNumber) + '_' + sig + '.p'
                self.data[sig] = load_signal_data(fn)
            except FileNotFoundError:
                pass
    
    def signals_present(self):
        return self.data.keys()
    
    def print_signal(self, SignalName):
        # this should go into another file anyway with plotting stuff
        x,y = self.data[SignalName]['time'], self.data[SignalName]['data']
        try:
            plt.plot(x,y)
        except:
            print('Can\'t deal with this signal yet')
            
            