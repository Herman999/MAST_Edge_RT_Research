# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 11:44:23 2019

@author: rbatt

pyautogui features for dealing with manual data checks
"""
import pyautogui as pag
import matplotlib.pyplot as plt

pag.FAILSAFE = True

class ohno:
    def __init__(self, figname, result):
        self._fig = figname
        self._result = result
        self.w = pag.getWindow(self._fig) 
        
    def get_fig(self):
        self._close_others() # close what don't care about
        self.w.maximize()
        self.w.set_foreground() # bring the figure to front
        
    def close_fig(self):
        # this may not destroy figure but 'minimize' instead
        
        self.w.close()
        #plt.close()
    
    def _close_others(self):
        """
        CAUTION: closes all windows bar the figure
        """
        for wind in pag.getWindows():
            if wind != self._fig:
                w = pag.getWindow(wind)
                w.minimize()
        
    def _prompt(self):
        self._close_others()
        result = pag.confirm(text=self._result)
        if result == 'OK':
            print('yes ', self._result)
            self.verify = True
        else:
            print('noo ', self._result)
            self.verify = False
    
    def _reopen_Spyder(self):
        spy = 'Spyder (Python 3.6)'
        ws = pag.getWindow(spy)
        ws.restore()        
    
    def do_verify(self):
        self.get_fig()
        self._prompt()
        self._reopen_Spyder()
        self._close_others()
        