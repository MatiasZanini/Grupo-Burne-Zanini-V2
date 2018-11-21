
import numpy as np
import nidaqmx as daq
from nidaqmx.types import CtrTime
import math
from nidaqmx.constants import LineGrouping
import time


#%% 

num_dev= 7

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
def actuador(duty, setpoint):    
    with nidaqmx.Task() as rtask: 
        conf_medir(rtask, sample_rate)
        duty = .5
        setpoint = 0.01
        while True:
            with nidaqmx.Task() as wtask:
                wtask.co_channels.add_co_pulse_chan_freq('Dev{}/ctr0'.format(num_dev), freq=366, duty_cycle=duty) #366 es el maximo valor de frecuencia
                wtask.timing.cfg_implicit_timing(sample_mode=AcquisitionType.CONTINUOUS) 
                #no emite nada por default
                #si no le ponemos CONTINUOUS no emite nada.
                wtask.start()
                time.sleep(5)
                data = medir(rtask, samples_per_channel)
                T = periodo(data, sample_rate)
    
                
                if T > setpoint:
                    duty = duty + .1
                else:
                    duty = duty - .1
                
                print(duty)


















#co_channels='Dev10/port0/line0'
#
#with nidaqmx.Task() as task_co:
#    
#    chan_co = daq.configure_pwm(
#            task_co,
#            physical_channels = co_channels,
#            frequency = pwm_freq,
#            duty_cycle = pwm_duty_cycle
            )
    
    
    
    