
import numpy as np
import nidaqmx as daq
from nidaqmx.types import CtrTime
import math
from nidaqmx.constants import LineGrouping
import time


#%% 

#--------------------------Medir voltaje analógico-------------------------------




def medir_volt_anal():
    with daq.Task() as task:
         task.ai_channels.add_ai_voltage_chan("Dev10/ai0")
         voltaje=task.read()
         return voltaje


#def prender_digital_lapso(tiempo):   
#    with daq.Task() as task:
#        task.do_channels.add_do_chan(
#            'Dev6/port0/line0',
#            line_grouping=LineGrouping.CHAN_PER_LINE)
#    
#        print(task.write(True))
#        #time.sleep(tiempo)
#        #print(task.write(False))   
        
def prender_digital():   
    with daq.Task() as task:
        task.do_channels.add_do_chan(
            'Dev10/port0/line0',
            line_grouping=LineGrouping.CHAN_PER_LINE)
    
        print(task.write(True))


def apagar_digital():   
    with daq.Task() as task:
        task.do_channels.add_do_chan(
            'Dev10/port0/line0',
            line_grouping=LineGrouping.CHAN_PER_LINE)
    
        print(task.write(False))    

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
            ai0 = task.ai_channels.add_ai_voltage_chan("Dev10/ai0",
                                                       terminal_config=daq.constants.TerminalConfiguration.DIFFERENTIAL)
        elif modo == 'rse':
            ai0 = task.ai_channels.add_ai_voltage_chan("Dev10/ai0",
                                                       terminal_config=daq.constants.TerminalConfiguration.RSE)
        else:
            ai0 = task.ai_channels.add_ai_voltage_chan("Dev10/ai0",
                                                       terminal_config=daq.constants.TerminalConfiguration.RSE)
            ai1 = task.ai_channels.add_ai_voltage_chan("Dev10/ai1",
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
    
    
    
#%%
#-------------------------Crear señal cuadrada con duty cicle-----------------------------

co_channels='Dev10/port0/line0'

with nidaqmx.Task() as task_co:
    
    chan_co = daq.configure_pwm(
            task_co,
            physical_channels = co_channels,
            frequency = pwm_freq,
            duty_cycle = pwm_duty_cycle
            )
    
    
    
    