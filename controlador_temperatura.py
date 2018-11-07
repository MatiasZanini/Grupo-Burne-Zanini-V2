# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 15:39:06 2018

@author: Publico
"""
#%%
import numpy as np
import funciones_daq as fdaq
from importlib import reload
import matplotlib.pyplot as plt

#%%

reload(fdaq)
#%%


#def control_on_off_1(minimo, maximo): #este ej sirve si la linea dig se mantiene en el estado indicado por un dado tiempo
#    
#    prendido = Falso
#    
#    while True:
#        
#        senal = medir_volt_anal()
#        
#        if senal < minimo:
#            prendido = True
#        elif senal > maximo:
#            prendido = False
#        else:
#            # segui haciendo lo que hacias
#            pass
#        
#        if prendido:
#            prender_digital(2)
        
        

def control_on_off(minimo, maximo): #la linea dig se mantiene en el estado indicado hasta que se fuerce otro
    
    minimo = minimo/100.0
    maximo = maximo/100.0    
    
    senal_completa = np.array([])    
    
    try: 
        while True:
            
            senal = fdaq.medir_volt_anal()
            print(senal)
                    
            senal_completa = np.append(senal_completa, senal)
            
            if senal < minimo:
                fdaq.prender_digital()
            elif senal > maximo:
                fdaq.apagar_digital()
            else:
                pass
    except KeyboardInterrupt:
    
        return senal_completa 


#%% Medir transitorio (como se calienta R desde T ambiente)

fdaq.prender_digital()
transitorio = fdaq.medir_senal_anal(20,500)
fdaq.apagar_digital()

transitorio_stack = np.hstack(transitorio)

path = r'D:\ALUMNOS\GitHub\Grupo-Burne-Zanini-V2\Mediciones/'
np.savetxt(path+'transitorio_8V_500fs_enfriamiento.txt', transitorio_stack, delimiter = '\t')
#%%
plt.plot(transitorio_stack[0,:])

#%%

trans = np.loadtxt(path+'transitorio_8V_500fs_enfriamiento.txt', delimiter = '\t', unpack = True)

plt.plot(trans)

#%% Controlador on_off

temp_onoff = control_on_off(55,65)

np.savetxt(path+'temperatura_control_onoff.txt', temp_onoff, delimiter = '\t')

plt.plot(temp_onoff)