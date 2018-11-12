import numpy as np
import matplotlib.pyplot as plt
import statistics as st
#%% -------------------- ONDA TRIANGULAR DE 1Vpp Y 1000Hz MIDIENDO CON DISTINTAS fs -------------------------------------------

path = r'C:\Users\sofia\Documents\Facultad\Instrumentación y control\mediciones 17-10\conjuncion_chunks/'

fs_1000 = np.loadtxt(path+'barrido_frec_rampa0.01.txt', delimiter = '\t', unpack = True)
fs_48000 = np.loadtxt(path+'barrido_frec_rampa0.01_48000.txt', delimiter = '\t', unpack = True)

#%%

def conjuncion_chunks(data, fs, xi_rampa, xf_rampa, num_fig):
    
    #tomamos mediciones en unq rampa creciente de la triangular
    
    xi = int(xi_rampa)
    xf = int(xf_rampa)
    
    #quiero definir mi inicio de rampa como la primer medicion del primer chunk que viva enteramente en un flanco creciente    
    for i in range(xi,xi*2):
        if i%1000 == 0:
            index_i = i
            break  #cuando encuentra el primero frena
            
    #defino mi fin de rampa como la primer medicion del ultimo chunk que viva en el flanco creciente  
    for i in range(int(xf/2),xf):
        if i%1000 == 0:
            index_f = i #se queda con el ultimo que encontro

    recorte_data = data[index_i:index_f]
    
    plt.figure(num = num_fig, tight_layout = True)
    plt.title('Medición de rampa creciente - señal triangular de 0.01 Hz - fs = {} Hz'.format(fs), fontsize = 40)
    plt.plot(recorte_data, linewidth = 3)
    plt.tick_params(axis = 'both', which = 'both', width = 2, length = 4, labelsize = 40)
    plt.ylabel('Vpp [V]', fontsize = 40)
    plt.xlabel('Samples', fontsize = 40)
    plt.grid(axis = 'both', which = 'both', alpha = 0.8, linewidth = 2, linestyle = '--')
    
    
    #intervalo entre un sample y otro
    
    L =  len(recorte_data)
    delta = np.empty(L-1)
    for i in range(L-1):
        delta[i] = recorte_data[i+1] - recorte_data[i]

    
    #plot intervalo entre mediciones delimitando chunks

    cant_chunks = int(L/1000) #divido por 1000 porque creo que al final mide 1000 puntos en un chunk en vez de 1024
    
    plt.figure(num = num_fig + 1, tight_layout = True)
    plt.title('Intervalos entre mediciones - señal triangular de 0.01 Hz - fs = {} Hz'.format(fs), fontsize = 40)
    plt.plot(delta, linewidth = 3)
    plt.tick_params(axis = 'both', which = 'both', width = 2, length = 4, labelsize = 30)    
    plt.ylabel(r'$\Delta V$ [Vpp]', fontsize = 40)
    plt.xlabel(r'$\Delta Sample$', fontsize = 40)
    for i in range(cant_chunks-1):
        plt.axvline(1000*(i+1), color = 'r', label = '_nolegend_' if i > 0  else 'limite chunk') #hay un limite de chunk que va a estar corrido en 1 por hacer el deltaV
    plt.legend(loc = 0, fontsize = 35)
    plt.grid(axis = 'both', which = 'both', alpha = 0.8, linewidth = 2, linestyle = '--')
    
    return recorte_data, delta, cant_chunks

    
datos_1000, conj_1000, cant_chunks_1000 = conjuncion_chunks(fs_1000, 1000, 3500, 52100, 1)
datos_48000, conj_48000, cant_chunks_48000 = conjuncion_chunks(fs_48000, 48000, 1.2224e6, 2.3229e6, 3)

#%%

#busco umbral para separar las intermitencias entre mediciones por ruido
#tendriamos que calcular cuanto equivale el umbral en tiempo para ver si se esta superando fs

def hist_umbral(datos, fs, fr, cant_chunks, num_fig):
    
    #determino umbral como 1 sigma de la dist gaussiana del hist
    umbral = st.stdev(datos)
    
    plt.figure(num = num_fig, tight_layout = True)
    plt.title('Determinación de umbral de ruido - señal triangular de {} Hz - fs = {} Hz'.format(fr, fs), fontsize = 40)
    plt.hist(datos, 20)
    plt.axvline(umbral, color = 'r', linewidth = 3, label = 'umbral ruido')
    plt.tick_params(axis = 'both', which = 'both', width = 2, length = 4, labelsize = 40)
    plt.ylabel(r'Cantidad de samples', fontsize = 40)
    plt.xlabel(r'$\Delta V$ [Vpp]', fontsize = 40)
    plt.xlim(xmin = 0) #ploteo para > 0 por simetria
    #plt.ylim(ymax = cant_chunks) #espero como maximo ver tantos picos como mi cant de chunks, hago zoom en esa cant de picos para ver mejor la region que me interesa
    plt.legend(loc = 0, fontsize = 35)
    plt.grid(axis = 'both', which = 'both', alpha = 0.8, linewidth = 2, linestyle = '--')
    
    return umbral

umbral_1000 = hist_umbral(conj_1000, 1000, 0.01, cant_chunks_1000, 5)
umbral_48000 = hist_umbral(conj_48000, 48000, 0.01, cant_chunks_48000, 6)

#%%
'''
quiero array que sea: indices de samples con deltaV > umbral
hist de ese array me va a dar: cant de cuentas que superan umbral vs indice de la cuenta
'''

def hist_saltos(datos, fs, fr, umbral, cant_chunks, num_fig):
    
    #armo vector de indices para los que se supera el valor umbral de deltaV
    
    indices_saltos = np.array([])
    
    for i in range(len(datos)):
        if datos[i] > umbral:
            indices_saltos = np.append(indices_saltos, i)
    
    #corro todas las mediciones al primer chuk: por ej el sample 1400 -> 400, 5000 -> 1000 , etc
    
    #los samples  <500 no los quiero, me voy a querar centrar en torno a mult de 1000 y mirar 500 de un chunk y 500 del siguiente
    indices_saltos_list = list(indices_saltos)
    for i in range(501):
        if i in indices_saltos_list:
            indices_saltos_list.remove(i)
    indices_saltos_ = np.asarray(indices_saltos_list)
    
    indices_mult = np.empty_like(indices_saltos_)
    for n in range(cant_chunks + 1):
        for i in range(len(indices_saltos_)):
            if indices_saltos_[i] in range(n*1000 + 500, n*1000 + 1500):
                indices_mult[i] = indices_saltos_[i] - n*1000
    
    
    #el hist de ese vector me dara la cant de cuentas que superan umbral vs indice de la cuenta
    
    plt.figure(num = num_fig, tight_layout = True)
    plt.title('señal triangular de {} Hz - fs = {} Hz'.format(fr, fs), fontsize = 40)
    plt.hist(indices_mult, 20)
    plt.tick_params(axis = 'both', which = 'both', width = 2, length = 4, labelsize = 40)
    plt.ylabel('Cantidad de samples\npor encima del umbral', fontsize = 40)
    plt.xlabel('Número de sample\nen multiplos de 1000', fontsize = 40)
    #plt.legend(loc = 0, fontsize = 20)
    plt.grid(axis = 'both', which = 'both', alpha = 0.8, linewidth = 2, linestyle = '--')
    
    return indices_saltos_
    
#hago los histogramas para los primeros 10 chunks
sample_sup_umbr_1000  = hist_saltos(conj_1000[:10000], 1000, 0.01, umbral_1000, 10, 7)
sample_sup_umbr_48000  = hist_saltos(conj_48000[:10000], 48000, 0.01, umbral_48000, 10, 8)


#%% -------------------- ONDA TRIANGULAR DE 1Vpp ALTA FREC (10Hz) Y MIDIENDO CON fs = 48000Hz-------------------------------------------

path2 = r'C:\Users\sofia\Documents\Facultad\Instrumentación y control\mediciones 24-10\conjuncion_chuncks_altafrec/'


fr_10 = np.loadtxt(path2+'sensibilidad_señal_rampa_frec_10Hz_sample_48000.txt', delimiter = '\t', unpack =  True)
#fr_500 = np.loadtxt(path2+'sensibilidad_señal_rampa_frec_500Hz_sample_48000.txt', delimiter = '\t', unpack =  True)
#fr_10000 = np.loadtxt(path2+'sensibilidad_señal_rampa_frec_10000Hz_sample_48000.txt', delimiter = '\t', unpack =  True)


recorte_fr10 = fr_10[1000:6000] #miramos unos 5 chunks

plt.figure(num = 9, tight_layout = True)
plt.title('Medición de rampa creciente - señal triangular de 10 Hz - fs = 48000 Hz', fontsize = 40)
plt.plot(recorte_fr10, linewidth = 3)
plt.tick_params(axis = 'both', which = 'both', width = 2, length = 4, labelsize = 40)
plt.ylabel('Vpp [V]', fontsize = 40)
plt.xlabel('Samples', fontsize = 40)
plt.grid(axis = 'both', which = 'both', alpha = 0.8, linewidth = 2, linestyle = '--')


#intervalo entre un sample y otro

L_fr10 =  len(recorte_fr10)
delta_fr10 = np.empty(L_fr10-1)
for i in range(L_fr10-1):
    delta_fr10[i] = recorte_fr10[i+1] - recorte_fr10[i]


#plot intervalo entre mediciones delimitando chunks

cant_chunks_fr10 = int(L_fr10/1000) #divido por 1000 porque creo que al final mide 1000 puntos en un chunk en vez de 1024

plt.figure(num = 10, tight_layout = True)
plt.title('Intervalos entre mediciones - señal triangular de 10 Hz - fs = 48000 Hz', fontsize = 40)
plt.plot(delta_fr10, linewidth = 3)
plt.tick_params(axis = 'both', which = 'both', width = 2, length = 4, labelsize = 40)    
plt.ylabel(r'$\Delta V$ [Vpp]', fontsize = 40)
plt.xlabel(r'$\Delta Sample$', fontsize = 40)
#for i in range(cant_chunks_fr10-1):
#    plt.axvline(1000*(i+1), color = 'r', label = '_nolegend_' if i > 0  else 'limite chunk') #hay un limite de chunk que va a estar corrido en 1 por hacer el deltaV
#plt.legend(loc = 0, fontsize = 20)
plt.grid(axis = 'both', which = 'both', alpha = 0.8, linewidth = 2, linestyle = '--')



