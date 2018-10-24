import numpy as np
import matplotlib.pyplot as plt
import time
import voltaje_sd as volt
from importlib import reload
#%% emitir armonica y medir
circuito = 'calibracion_ch2'
frecuencia = 800  # frecuencia del tono que se desea emitir en Hz
duracion = 20       # duracion del tono en segundos
amplitud = 1   
#R = 4591
R2 = 900

tiempo, signal, grabacion = volt.playrec_tone(frecuencia,duracion,amplitud)     # datos contiene los arrays concatenados de tiempo, data, grabacion
L_tiempo = len(tiempo)

#%%
una_medicion = np.empty([L_tiempo,4])
una_medicion[:,0] = tiempo
una_medicion[:,1] = signal
una_medicion[:,2] = grabacion[:,0] #un channel del mic
una_medicion[:,3] = grabacion[:,1] #otro channel del mic

np.savetxt('medicion_{}_{}.txt'.format(circuito,frecuencia), una_medicion, delimiter = ',')

V_diodo = grabacion[:,0]-grabacion[:,1]
I_diodo = grabacion[:,1]/R2
plt.plot(V_diodo, I_diodo)
#with open("resultados_frecuencia=" + str(frecuencia) + ".txt", "w") as out_file:     # abre un archivo .txt, str(imprime el valor de la frecuencia)
#    for i in range(len(tiempo)):                                           # tiempo, data y grabacion tienen las mismas dimensiones, un for para leer todo el array
#        out_string = ""                                                    # string vacio
#        out_string += str(tiempo[i])                                       # escribimos los valores de tiempo,data y grabacion
#        out_string += "," + str(data[i])
#        out_string += "," + str(grabacion[i])
#        out_string += "\n"
#        out_file.write(out_string) 

                                        # escribe el string en el archivo de salida
#%%
#Respuesta en frecuencia de la placa de audio.
numero_archivo = 3
amp, dur = 0.5, 5    
#freqs=np.concatenate((np.arange(5,105,10) , np.linspace(105, 20000, 10) , np.linspace(20000,44100,30)))
freqs = np.arange(0.1,3,0.05)
Nfreq=len(freqs)

amplitudes = np.empty(Nfreq)
for i in range(Nfreq):
    _,_, grabacion = volt.playrec_tone(freqs[i],dur,amp,ch_in=1,ch_out=1,block=True)
    amplitudes[i] = np.max(grabacion)
    time.sleep(0.5)
#comentario: en vez de un sleep podriamos hacer algun tipo de lazo de control
# que solo continue iterando una vez finalizada la iteracion anterior
# este lazo iria en playrec_tone, como indicador de finalizacion de medicion

mediciones_barrido = np.empty([Nfreq,2])
mediciones_barrido[:,0] = freqs
mediciones_barrido[:,1] = amplitudes
np.savetxt('barrido_frec{}.txt'.format(numero_archivo), mediciones_barrido, delimiter = ',')
plt.plot(freqs, amplitudes)
#%%













