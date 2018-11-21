# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 15:39:06 2018

@author: Publico
"""
#%%
import numpy as np
#import funciones_daq as fdaq
from importlib import reload
import matplotlib.pyplot as plt
from clase_daq import DAQ
from clase_pid import PIDController as PID

#%%

reload(DAQ)
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
            
            senal = DAQ.medir_volt_anal()
            print(senal)
                    
            senal_completa = np.append(senal_completa, senal)
            
            if senal < minimo:
                DAQ.prender_digital()
            elif senal > maximo:
                DAQ.apagar_digital()
            else:
                pass
    except KeyboardInterrupt:
    
        return senal_completa 


#%% Medir transitorio (como se calienta R desde T ambiente)

DAQ.prender_digital()
transitorio = DAQ.medir_senal_anal(20,500)
DAQ.apagar_digital()

transitorio_stack = np.hstack(transitorio)

path = r'D:\ALUMNOS\GitHub\Grupo-Burne-Zanini-V2\Mediciones/'
np.savetxt(path+'transitorio_8V_500fs_enfriamiento.txt', transitorio_stack, delimiter = '\t')
#%%
plt.plot(transitorio_stack[0,:])

#%%

trans = np.loadtxt(path+'transitorio_8V_500fs_enfriamiento.txt', delimiter = '\t', unpack = True)

plt.plot(trans)

#%% Controlador on_off
mydaq = DAQ(1)

mydaq.apagar_digital()
temp_onoff = control_on_off(58,62)
num = 3
np.savetxt(path+'temperatura_control_onoff_{}.txt'.format(num), temp_onoff, delimiter = '\t')

plt.plot(temp_onoff)

#%%

temp_ = np.loadtxt(path+'mediciones 7-11/temperatura_control_onoff.txt', delimiter = '\t', unpack = True)
plt.plot(temp_)







#%% ---------------------PID--------------------------------

def controlador_pid(dev, kp, ki, kd, setpoint, pulso_inicial = 0.5):

    mydaq = DAQ(dev)
    
    mypid = PID(setpoint,kp,ki,kd)
    
    mydaq.pulso(pulso_inicial)
    
    senal_completa = np.array([])
    
    try: 
            while True:
                
                temp_actual = mydaq.medir_volt_anal()*100 #temp_actual es temperatura en grados
                print(temp_actual)
                        
                senal_completa = np.append(senal_completa, temp_actual)
                
                actuador = mypid.calculate(temp_actual)
                
                mydaq.pulso(actuador)
                
                
    except KeyboardInterrupt:

        np.savetxt('ultima_medicion', senal_completa, delimiter = '\t')        
        
        return senal_completa



datos_temp = controlador_pid(1, 0.5, 0.0, 0.0, 60)

num_medicion = 1
np.savetxt('controlador_pid_temp{}'.format(num_medicion), datos_temp, delimiter = '\t')












