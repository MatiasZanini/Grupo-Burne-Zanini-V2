
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

def medir_senal_anal(duracion, fs, chunk=1024, modo='diferencial'):

#modos: rse=10083 ; diferencial=10106

    modo_dict = {'diferencial' : 10106,
                 'rse' : 10083}

    datos = []
    cant_puntos=duracion*fs
    cant_med=math.floor(cant_puntos/chunk)+1
    with daq.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev5/ai0")
        #task.ai_channels.add_ai_voltage_chan("Dev1/ai1")
        task.timing.cfg_samp_clk_timing(fs)
        daq.constants.TerminalConfiguration(modo_dict[modo])
        # print mwchan.physical_channel.ai_term_cfgs (con mwchan=task.ai_channels.add_ai_voltage_chan("Dev1/ai0"))
    
        # while True:
        for i in range(0, cant_med):
            tdata = task.read(number_of_samples_per_channel=chunk)
            datos.extend(tdata)
           
    return datos