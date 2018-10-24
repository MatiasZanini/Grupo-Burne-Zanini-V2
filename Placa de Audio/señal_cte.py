#Importamos las librerías

import numpy as np
import pyaudio
from pyaudio import PyAudio as pa

#%% Seteamos el rate

BITRATE=44100
#%%

def Cte(amp_cte,dur_cte):  #Señal constante de voltaje amp_cte y duracion dur_cte, asumiendo que la placa entrega de 0V a 1.2V
    
    if amp_cte <=1.20:
        cant_puntos = int(BITRATE * dur_cte)
        silencios = cant_puntos % BITRATE
        amp_bit= amp_cte*256/1.20 #convierte de volts a bits
        señal_cte_lista=list(np.zeros(cant_puntos)+amp_bit)
        señal_cte=''
        
        for x in range(cant_puntos):
            señal_cte += chr(int(señal_cte_lista[x]))
            
        for x in range(silencios):
            señal_cte += chr(128)
#            
#            #Llenamos lo que falta de duracion con silencios
#            señal_cte= np.append(señal_cte, np.zeros(silencios))
#            
#            señal_cte=señal_cte.astype(np.float32).tostring()
    
        p = pa()
        stream = p.open(
                   format=p.get_format_from_width(1),
                   channels=1,
                   rate=BITRATE,
                   output=True,
                   )
        stream.write(señal_cte)
        stream.stop_stream()
        stream.close()
        p.terminate()
    else:
        return ('El voltaje debe ser menor a 1.20V')