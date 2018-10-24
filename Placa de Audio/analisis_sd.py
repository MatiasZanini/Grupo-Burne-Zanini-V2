# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 11:56:48 2018

@author: Matías
"""
import matplotlib.pyplot as plt
import numpy as np

#%%
#--------------------------------CALIBRACIÓN--------------------------------------------------------------------

t_cal, entrada_cal, canal1_cal, canal2_cal = np.loadtxt('medicion_calibracion_ch1_800.txt', delimiter = ',', unpack =True)

amp_ch1=np.max(canal1_cal) #amplitud medida en el canal 1

amp_medida=1.3 #voltaje medido por el osciloscopio 

factorconv=amp_medida/amp_ch1







#%%
#---------------------------------Barrido en frecuencia----------------------------



f, a = np.loadtxt('barrido_frec.txt', delimiter = ',', unpack =True)
f=f/1000
fzoom, azoom = np.loadtxt('barrido_frec2.txt', delimiter = ',', unpack =True)

plt.subplots(1,2, sharey=True)
plt.suptitle('Respuesta en frecuencia de la placa de audio',size=20)

g1 = plt.subplot(1,2,1)
plt.plot(f,a,linewidth=3)
plt.xlabel('Frecuencia (kHz)',size=20)
plt.ylabel('Amplitud',size=20)
plt.yticks(np.arange(0,0.45,0.05))
plt.grid(True)
plt.tick_params(axis = 'both', which = 'both', length = 4, width = 2, labelsize = 20)
plt.subplot(1,2,2, sharey=g1)
plt.plot(fzoom,azoom,linewidth=3)
plt.xlabel('Frecuencia (Hz)',size=20)
plt.ylabel('Amplitud',size=20)
plt.xlim(xmin=0, xmax=3)
plt.grid(True)
plt.tick_params(axis = 'both', which = 'both', length = 4, width = 2, labelsize = 20)

#%%

#-------------------------------Señal cruda diodo--------------------------------------------

fs=20000
frecuencia=550
puntos_periodo = int(fs/frecuencia)

t, entrada, canal1, canal2 = np.loadtxt('medicion_diodo_450 - tab delimited.txt', delimiter = '\t', unpack =True)

plt.plot(t, entrada,color='C1',label='Entrada')
plt.plot(t,canal1,color='r',label='Canal 1')
plt.plot(t,canal2,color='b',label='Canal 2')

plt.tick_params(axis = 'both', which = 'both', length = 4, width = 2, labelsize = 20)
plt.legend(loc=0,fontsize=16)
plt.xlabel('Tiempo (s)',size=20)
plt.ylabel('Amplitud',size=20)
plt.grid(True)





#%%
# ------------------------------Curva IV diodo--------------------------------

t, entrada, canal1, canal2 = np.loadtxt('medicion_diodo_450 - tab delimited.txt', delimiter = '\t', unpack =True)
R2 = 900
fs=20000
frecuencia=550
Vdiodo=(canal1-canal2)*factorconv   #en volts
Idiodo=canal2/R2*factorconv*1000   #en miliamper


Vdiodo_sin_transitorio=(canal1[59400:]-canal2[59400:])*factorconv
Idiodo_sin_transitorio=canal2[59400:]*factorconv/R2*1000



plt.plot(Vdiodo_sin_transitorio,Idiodo_sin_transitorio,'.')
plt.tick_params(axis = 'both', which = 'both', length = 4, width = 2, labelsize = 20)

puntos_periodo = int(fs/frecuencia)
 

plt.xlabel('Voltaje (V)',size=20)
plt.ylabel('Corriente (mA)',size=20)
plt.grid(True)





Vf=np.max(Vdiodo_sin_transitorio) #en volts

indicevf=(np.abs(Vdiodo_sin_transitorio-Vf)).argmin()

If=Idiodo_sin_transitorio[indicevf] #en miliamper

Pf=Vf*If*1000 #en miliwats











