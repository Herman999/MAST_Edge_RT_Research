# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 23:36:11 2019

@author: Tomas
"""




# JP figure


jp_shot = Shot(27444, LHt=[(0.259,0.2545,0.2595)], HLt=[(0.32347,0.32347,0.32347)])


jp_shot.plot_JP_report(tlim = (0,0.39),plot_thomson = 4, label_thomson = False,
                       figsize=(13,9),fontsize=15,width=3)


# JP detail LH


jp_shot.plot_JP_report(tlim = (0.241,0.265),plot_thomson = 4, label_thomson = False,
                       figsize=(6,9),fontsize=15,width=2)
# JP detial HL

jp_shot.plot_JP_report(tlim = (0.31,0.335),plot_thomson = 4, label_thomson = False,
                       figsize=(6,9),fontsize=15,width=2)

#%%
jp_shot = Shot(27444, LHt=[(0.259,0.2545,0.2595)], HLt=[(0.32347,0.32347,0.32347)])

jp_shot.plot_JP_report(tlim = (0,0.39),plot_thomson = 4, label_thomson = True,
                       figsize=(13,9),fontsize=15,width=3)

jp_shot.fit_tanh_pedestal(67)




