
import numpy as np
import nidaqmx as ndaq
#from nidaqmx.types import CtrTime
import math
from nidaqmx.constants import LineGrouping
import time
from nidaqmx.constants import (AcquisitionType)

#--------------------------Medir voltaje analógico-------------------------------

class DAQ:
    
    def __init__(self, num_device):
        self.prefix = 'Dev{}/'.format(num_device)
        
    def medir_volt_anal(self):
        with ndaq.Task() as task:
             task.ai_channels.add_ai_voltage_chan(self.prefix + "ai0")
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
            
    def prender_digital(self):   
        with ndaq.Task() as task:
            task.do_channels.add_do_chan(
                self.prefix + 'port0/line0',
                line_grouping=LineGrouping.CHAN_PER_LINE)
        
            print(task.write(True))
    
    
    def apagar_digital(self):   
        with ndaq.Task() as task:
            task.do_channels.add_do_chan(
                self.prefix + 'port0/line0',
                line_grouping=LineGrouping.CHAN_PER_LINE)
        
            print(task.write(False))    
    
    #%%
    #-------------------------------Medición continua----------------------------
    
    def medir_senal_anal(self, duracion, fs, chunk=1024, modo='dif'):
    
        modos = ('dif', 'rse', '2rse') #1 señal dif, 1 señal rse, 2 señales rse 
    
        if modo not in modos:
            raise ValueError('%s is not a valid mode %s' % (modo, modos))
    
        datos = []
        cant_puntos=duracion*fs
        cant_med=math.floor(cant_puntos/chunk)+1
        with ndaq.Task() as task:
            if modo == 'dif':
                ai0 = task.ai_channels.add_ai_voltage_chan(self.prefix +"ai0",
                                                           terminal_config=ndaq.constants.TerminalConfiguration.DIFFERENTIAL)
            elif modo == 'rse':
                ai0 = task.ai_channels.add_ai_voltage_chan(self.prefix +"ai0",
                                                           terminal_config=ndaq.constants.TerminalConfiguration.RSE)
            else:
                ai0 = task.ai_channels.add_ai_voltage_chan(self.prefix +"ai0",
                                                           terminal_config=ndaq.constants.TerminalConfiguration.RSE)
                ai1 = task.ai_channels.add_ai_voltage_chan(self.prefix +"ai1",
                                                           terminal_config=ndaq.constants.TerminalConfiguration.RSE)
                                                           
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
    def pulso(self, duty, freq = 366, wait = 2.11):
        
        duty = np.clip(duty,0.00001,0.99999)
        
        with ndaq.Task() as wtask:
            print('a')
            wtask.co_channels.add_co_pulse_chan_freq(self.prefix +'ctr0', freq, duty_cycle=duty) #366 es el maximo valor de frecuencia
            print('b')            
            wtask.timing.cfg_implicit_timing(sample_mode=AcquisitionType.CONTINUOUS) 
            #no emite nada por default
            #si no le ponemos CONTINUOUS no emite nada.
            print('c')            
            wtask.start()
            print('d')
            time.sleep(wait)
            print('e')        
    
