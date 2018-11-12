import numpy as np
import matplotlib.pyplot as plt
#%%
#-------------------------------Analisis de intervalo entre chunks----------------------------
#ojo puede que sea ; no tab

interchunk1000 = np.loadtxt('barrido_frec_rampa0.01.txt', delimiter = '\t', unpack = True)
#plt.plot(interchunk1000)

interchunk48000 = np.loadtxt('barrido_frec_rampa0.01_48000.txt', delimiter = '\t', unpack = True)
#plt.plot(interchunk48000)
#plt.plot(interchunk48000[int(1.2E6):int(2.3E6)])
interchunk48000 = interchunk48000[int(1.2E6):int(2.3E6)]

path = r'D:\ALUMNOS\GitHub\Grupo-Burne-Zanini-V2\Mediciones/'
sens10kHz = np.loadtxt(path+'sensibilidad_señal_rampa_frec_10000Hz_sample_48000.txt', delimiter = '\t', unpack = True)
plt.plot(sens10kHz[:2048])
#plt.plot(sens10kHz)
#%%
#tomamos un flanco creciente de la senal de rampa

#para frec sampleo 1000Hz
inicio_rampa= (np.abs(interchunk1000 + 0.85)).argmin()
fin_rampa = (np.abs(interchunk1000 - 1)).argmin()

plt.plot(interchunk1000[inicio_rampa:fin_rampa])
interchunk1000_rec=interchunk1000[inicio_rampa:fin_rampa]
L = len(interchunk1000_rec)

#para frec sampleo 48000Hz
inicio_rampa48000 = (np.abs(interchunk48000 + 0.47)).argmin()
fin_rampa48000 = (np.abs(interchunk48000 - 0.47)).argmin()

plt.plot(interchunk48000[inicio_rampa48000:fin_rampa48000])
interchunk48000_rec=interchunk48000[inicio_rampa48000:fin_rampa48000]
L48000 = len(interchunk48000_rec)
#%%
#para frec sampleo 1000Hz
conjuncion = np.empty(L-1)
for i in range(L-1):
    conjuncion[i] = interchunk1000[i+1] - interchunk1000[i]

cant_chunks=int(L/1024)
plt.plot(conjuncion)
for i in range(cant_chunks-1):
    plt.axvline(1024*(i+1), color = 'r')

#para frec sampleo 48000Hz
conjuncion48000 = np.empty(L48000-1)
for i in range(L48000-1):
    conjuncion48000[i] = interchunk48000[i+1] - interchunk48000[i]

cant_chunks48000=int(L48000/1024)
plt.plot(conjuncion48000[:10240])
for i in range(10): #ploteamos los 10 primeros chuncks nomas porque son demasiados
    plt.axvline(1024*(i+1), color = 'r')
#%%
#-------------------------------Estudio de aliasing----------------------------

signal = np.loadtxt(r"C:\Users\Matías\Documents\GitHub\Grupo-Burne-Zanini-V2\Mediciones\mediciones 17-10\señal_sinusoidal_frec_100Hz_sample_200.txt", delimiter = '\t', unpack = True)
plt.plot(signal, '.-')
N = len(signal)
num_chuncks = int(N/1000)
for i in range(num_chuncks-1):
        plt.axvline(1000*(i+1), color = 'r')
plt.tick_params(axis = 'both', which = 'both', width = 2, length = 4, labelsize = 15)        
plt.xlabel('sample', fontsize=15)
plt.ylabel('Voltaje [V]', fontsize=15)
#plt.title('Señal sinusoidal de 100 Hz medidos con una frecuencia de sampleo de 4000 Hz')
plt.grid(True)
plt.title('Señal sinusoidal de 100 Hz, frecuencia de muestreo de 200 Hz', fontsize= 15)
#plt.title('Ampliación de la señal sinusoidal de 100 Hz, frecuencia de sampleo 4000 Hz, dentro de un chunk')
#plt.grid(True)

#%%

#para hacer una transformada de fourier hay que recortar "signal" en un chunk y despues aplicarle:

# fft= np.fft.fft(señal_recortada)    
signal_rec = signal[1000:2000]

transf = np.fft.fft(signal_rec)

plt.plot(transf)
plt.grid(True)

#%%
# Prueba del multiplexor

ch1, ch2 = np.loadtxt(r"C:\Users\Matías\Documents\GitHub\Grupo-Burne-Zanini-V2\Mediciones\mediciones 24-10\simultaneidad2CH_RSE_señal_rampa_frec_5000Hz_sample_24000.txt", delimiter = '\t', unpack = True)

ch1=ch1[:70]
ch2=ch2[:70]
pepe=plt.subplot(1,2,1)

plt.plot(ch1, 'r.-', label = 'Ch 1')
plt.plot(ch2, 'b.-', label = 'Ch 2')
plt.xlabel('sample')
plt.ylabel('voltaje [V]')
plt.title('Señal triangular de 5 kHz a 24000 samples por segundo')

plt.tick_params(axis = 'both', which = 'both', width = 2, lenth = 4, labelsize = 30)

plt.legend(loc = 0, fontsize= 10)
plt.grid(True)

plt.subplot(1,2,2, sharey=pepe)
plt.grid(True)

plt.plot(ch1-ch2,'.-')
plt.xlabel('sample')

plt.title('Resta de las señales de ambos canales')    
plt.grid(True)    
    
