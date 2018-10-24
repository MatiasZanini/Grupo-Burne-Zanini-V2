#importamos módulo para comunicarnos con la placa y librerias
import clase_voltaje as volt

import numpy as np
import matplotlib.pyplot as plt
import pyaudio
from pyaudio import PyAudio as pa
import wave
import time





#%% Generamos una senal
#volt.bitrate(44100) #creo que si lo hice bien, setea el BITRATE para todo el modulo clase_voltaje

senal = volt.armonica(500, 60) #esto lo elegimos según la senal que querramos emitir

def por_partes(arr, largo):
    larr = len(arr)
    cursor = 0
    while cursor < larr:
        yield arr[cursor:cursor+largo]
        cursor = min(cursor + largo, larr+1)


def continuo_por_partes(arr, largo):
    larr = len(arr)
    while True:
        cursor = 0    
        while cursor < larr:
            yield arr[cursor:cursor+largo]
            cursor = min(cursor + largo, larr+1)
        
gen = por_partes(senal, 1024)        

#modo callback

def callback_emision(in_data, frame_count, time_info, status):  #stream_callback pide una función de 4 argumentos.
    #data = senal.readframes(frame_count) #pedazo de senal
    parte = next(gen)
    return (parte, pyaudio.paContinue)   

#emision_call = volt.emitir(senal, callback_emision)     

#modo bloqueo
#%%

datos=volt.playrec(callback_emision,25)

plt.plot(datos)




#emision_block = volt.emitir(senal)

# probamos esto: volt.playrec(senal,callback_emision,volt.medir(10))
#ver print de pantalla (primero graba despues mide)
#%% Medimos senal

#modo callback

def callback_medición(in_data, frame_count, time_info, status):
    return (in_data, pyaudio.paContinue)
# no se si está bien así la callback para medir
    
medicion_call = volt.medir(500, callback_medicion)

#modo bloqueo

#medicion_block = medir(500)
