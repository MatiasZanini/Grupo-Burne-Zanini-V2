import sounddevice as sd
import numpy as np
#import pylab as lab
#import matplotlib.pyplot as plt
#import time
#from scipy.signal import find_peaks
#from scipy import signal
#%%
def playrec_tone(frecuencia, duracion, amplitud, fs=20000, ch_in=2, ch_out=1, block=False):
    """
    Emite un tono y lo graba.
    """
    sd.default.samplerate = fs # frecuencia de muestreo
    sd.default.channels = int(ch_in),int(ch_out)  # numero de canales input,output
    
    cantidad_de_periodos = duracion*frecuencia
    puntos_por_periodo = int(fs/frecuencia)
    puntos_totales = puntos_por_periodo*cantidad_de_periodos

    tiempo = np.linspace(0, duracion, puntos_totales)  # interpola puntos_totales entre 0 y duracion

    data = amplitud*np.sin(2*np.pi*frecuencia*tiempo)  # funcion que genera los datos para el ono
    
    if block:
        grabacion = sd.playrec(data, blocking=True)        # graba los datos de entrada (line in)
    
    else:
        grabacion = sd.playrec(data, blocking=False)
#si no funciona para hacer dos mediciones simultaneas: probar llamarla dos veces con blocking=False y channels=1

#    plt.subplot(2,1,1)                                 
#    plt.plot(tiempo, data,'b.--')                      # grafica datos emitidos
#    plt.xlim([0.524, 0.525])
#    plt.subplot(2,1,2)
#    plt.plot(tiempo, grabacion,'r.--')                 # grafica datos grabados (line in o input) 
#    plt.xlim([0.524, 0.525])

    return tiempo, data, grabacion
