
import numpy as np
import nidaqmx as daq
import math


#%% 

#--------------------------Medir voltaje analógico-------------------------------

def medir_volt_anal():
    with daq.Task() as task:
         task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
         voltaje=task.read()
         return voltaje
         



#%%
#-------------------------------Medición continua----------------------------

def medir_senal_anal(duracion, fs, chunk=1024, modo='dif'):

    modos = ('dif', 'rse', '2rse') #1 señal dif, 1 señal rse, 2 señales rse 

    if modo not in modos:
        raise ValueError('%s is not a valid mode %s' % (modo, modos))

    datos = []
    cant_puntos=duracion*fs
    cant_med=math.floor(cant_puntos/chunk)+1
    with daq.Task() as task:
        if modo == 'dif':
            ai0 = task.ai_channels.add_ai_voltage_chan("Dev5/ai0",
                                                       terminal_config=daq.constants.TerminalConfiguration.DIFFERENTIAL)
        elif modo == 'rse':
            ai0 = task.ai_channels.add_ai_voltage_chan("Dev5/ai0",
                                                       terminal_config=daq.constants.TerminalConfiguration.RSE)
        else:
            ai0 = task.ai_channels.add_ai_voltage_chan("Dev5/ai0",
                                                       terminal_config=daq.constants.TerminalConfiguration.RSE)
            ai1 = task.ai_channels.add_ai_voltage_chan("Dev5/ai1",
                                                       terminal_config=daq.constants.TerminalConfiguration.RSE)
                                                       
        task.timing.cfg_samp_clk_timing(fs)
        # print mwchan.physical_channel.ai_term_cfgs (con mwchan=task.ai_channels.add_ai_voltage_chan("Dev1/ai0"))
    
        # while True:
        for i in range(0, cant_med):
            tdata = task.read(number_of_samples_per_channel=chunk)
            datos.append(tdata)
            
           
    datos = np.asarray(datos)
    
    if modo == 'dif':
        datos = np.expand_dims(datos, axis=1)

    return datos