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

signal=fdaq.medir_senal_anal(10,48000) # signal=(cant de chuncks, cant de canales, cant de puntos)
tipo='rampa'
frec_rampa = 10000 #frecuencia en Hz de la rampa enviada con el generador
sample_frec = 48000
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

path = r'D:\ALUMNOS\GitHub\Grupo-Burne-Zanini-V2\Mediciones/'
np.savetxt(path+'sensibilidad_señal_{}_frec_{}Hz_sample_{}.txt'.format(tipo,frec_rampa,sample_frec), signal, delimiter = '\t')

#estamos guardando matriz de matrices
#si hacemos np.hstack(signal) tenemos matriz (cant canales, cant de puntos total) (ojo en general esto es de forma traspuesta a lo que estamos acostumbrados)

#%%
#---------------------Medir simultaneidad entre canales------------------------------

signal_rse = fdaq.medir_senal_anal(10,24000, modo = '2rse') #fs tiene que ser a lo sumo la mitad de la fs maxima para modo dif. Tiene sentido ya que ahora son 2 ch en vez de 1.
tipo ='rampa'
frec_rampa = 5000 #frecuencia en Hz de la rampa enviada con el generador
sample_frec = 24000

signal_rse_stack = np.hstack(signal_rse).T
path = r'D:\ALUMNOS\GitHub\Grupo-Burne-Zanini-V2\Mediciones/'
np.savetxt(path+'simultaneidad2CH_RSE_señal_{}_frec_{}Hz_sample_{}.txt'.format(tipo,frec_rampa,sample_frec), signal_rse_stack, delimiter = '\t')

#para juntar todos los chuncks en una misma lista: np.hstack(signal_rse)

