#https://github.com/fotonicaOrg/daq/blob/master/main_temperatura.py

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 14:58:55 2018
@author: Axel Lacapmesure
"""

import sys
if "daq" not in sys.modules:
    import daq
else:
    import importlib.reload
    importlib.reload(daq)

import nidaqmx
import nidaqmx.stream_writers
import numpy as np
from matplotlib import pyplot as plt
import time

#%%
def adquisicion(
        task,
        n_samples,
        sample_frequency,
        task_co = None,
        chan_co = None,
        stream_co = None
        ):
    
    print('Acquire')
    
    data_count = 0
    n_channels = task.number_of_channels
    
    task.timing.cfg_samp_clk_timing(
            rate = sample_frequency,
            sample_mode = nidaqmx.constants.AcquisitionType.CONTINUOUS
            )
    task.in_stream.input_buf_size = 5 * n_samples
    
    data = np.zeros((n_channels, n_samples))
    
    try:
        print('Start')
        task.start()
        
        while True:
#           
            # 1) Sensor y calcular error
            data[0:n_channels, 0:n_samples] = np.array(task.read(n_samples))
            data_count += n_samples
            # calcular error
            
            #2)llamamos funcion PID (PID recibe error y devuelve correccion)            
            
            
            
            #time.sleep(0.5)
            # 3) Actuador
            stream_co.write_one_sample_pulse_frequency(
                    frequency = chan_co.co_pulse_freq,
                    duty_cycle = 0.9 #corregir este valor con PID
                    )
#
#            time.sleep(0.5)
#            stream_co.write_one_sample_pulse_frequency(
#                    frequency = chan_co.co_pulse_freq,
#                    duty_cycle = 0.1
#                    )
            
#            duty = 0.1
#            if stream_co != None:
#                time.sleep(1)
#                
#                if duty < 0.5:
#                    stream_co.write_one_sample_pulse_frequency(
#                            frequency = chan_co.co_pulse_freq,
#                            duty_cycle = 0.9
#                            )
#                    duty = 0.9
#                elif duty >= 0.5:
#                    stream_co.write_one_sample_pulse_frequency(
#                            frequency = chan_co.co_pulse_freq,
#                            duty_cycle = 0.1
#                            )
#                    duty = 0.1
#                print(duty)
        
    except KeyboardInterrupt:
        clk_rate = task.timing.samp_clk_rate
        task.stop()
        if task_co != None: task_co.stop()
        
        return (abs(data), clk_rate)

#%%

CAL = 100

ai_channels = ('Dev8/ai0')
co_channels = ('Dev8/ctr0')
pwm_freq = 100
pwm_duty_cycle = 0.5

voltage_range = ([-10,10])
n_samples = 100
freq = 5000

with nidaqmx.Task() as task_ai, nidaqmx.Task() as task_co:
    
    daq.configure_ai(
            task_ai,
            physical_channels = ai_channels,
            voltage_range = voltage_range,
            terminal_configuration = nidaqmx.constants.TerminalConfiguration.DIFFERENTIAL
            )
    
    chan_co = daq.configure_pwm(
            task_co,
            physical_channels = co_channels,
            frequency = pwm_freq,
            duty_cycle = pwm_duty_cycle
            )
    
    task_co.timing.cfg_implicit_timing(sample_mode = nidaqmx.constants.AcquisitionType.CONTINUOUS)
    
    stream_co = nidaqmx.stream_writers.CounterWriter(task_co.out_stream)
    task_co.start()
    
    (data, real_freq) = adquisicion(
                task = task_ai,
                n_samples = n_samples,
                sample_frequency = freq,
                task_co = task_co,
                stream_co = stream_co,
                chan_co = chan_co[0]
                )

time = np.arange(data.size) / real_freq
#
#plt.plot(time, data[0,:])
#plt.xlabel('Tiempo (s)')
#plt.ylabel('Tensión registrada (V)')
#plt.grid()
