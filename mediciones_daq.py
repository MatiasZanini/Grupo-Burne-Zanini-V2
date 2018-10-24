# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 17:59:15 2018

@author: Publico
"""
import numpy as np
import funciones_daq as fdaq
import matplotlib.pyplot as plt
from importlib import reload

#%%
reload(fdaq)

#%%
#---------------------Medir conjuncion de los chunks------------------------------

signal=fdaq.medir_senal_anal(10,4000)
tipo='sinusoidal'
frec_rampa = 100 #frecuencia en Hz de la rampa enviada con el generador
sample_frec = 4000
#
#f = np.array([1000])
#len_f = len(f)
#signal = []
#for n in range(len_f):
#    signal.append(str(f[n]))    
#    signal.append(fdaq.medir_senal_anal(2, f[n]))
##    freq = 'frecuencia='+str(f[n])
##    signal.append(freq+data)
#
#signal_ = np.asarray(signal).T

signal_ = np.asarray(signal)
np.savetxt('prueba_señal_{}_frec_{}Hz_sample_{}.txt'.format(tipo,frec_rampa,sample_frec), signal_, delimiter = '\t')




