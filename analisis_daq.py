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

signal = np.loadtxt('señal_sinusoidal_frec_100Hz_sample_200.txt', delimiter = '\t', unpack = True)

plt.plot(signal, '.-')
N = len(signal)
num_chuncks = int(N/1024)
for i in range(num_chuncks-1):
        plt.axvline(1024*(i+1), color = 'r')
    
    
    
    
    
