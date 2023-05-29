"""
  
  Copyright (C) 2022 Sony Computer Science Laboratories
  
  Author(s) Peter Hanappe, Aliénor Lahlou
  
  free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  General Public License for more details.
  
  You should have received a copy of the GNU General Public License
  along with this program.  If not, see
  <http://www.gnu.org/licenses/>.
  
"""

import time
import json
import argparse

from CSLserial import ControlSerial

    
class ControlLight():
    def __init__(self, arduino_port):
        
        self.arduino_port = arduino_port

        self.arduino = ControlSerial(self.arduino_port)




    def add_digital_pulse(self, dic_param):
        """create a digital pulse function. See next function to understand the "secondary" parameter"""

        pin = dic_param['pin'] 
        offset = dic_param['offset']
        period = dic_param['period']
        duration = dic_param['duration']
        secondary = dic_param['secondary'] #secondary=0: indépendant, secondary=1: dependant
        analog_value = dic_param['analog_value']

        offset_s = offset//1000
        offset_ms = offset%1000
        period_s = period//1000
        period_ms = period%1000
        duration_s = duration//1000
        duration_ms = duration%1000
        self.arduino.send_command("d[%d,%d,%d,%d,%d,%d,%d,%d,%d]" % (pin, offset_s, offset_ms, period_s,period_ms, duration_s,
                                                        duration_ms, secondary, analog_value))

    def add_primary_digital_pulse(self, dic_param): 
        """create a primary digital pulse function. When the primary is set to UP, all the secondary pulses are set to DOWN"""

        pin = dic_param['pin'] 
        offset = dic_param['offset']
        period = dic_param['period']
        duration = dic_param['duration']
        secondary = dic_param['secondary'] #secondary=0: indépendant, secondary=1: dependant
        analog_value = dic_param['analog_value']
    
        offset_s = offset//1000
        offset_ms = offset%1000
        period_s = period//1000
        period_ms = period%1000
        duration_s = duration//1000
        duration_ms = duration%1000
        self.arduino.send_command("m[%d,%d,%d,%d,%d,%d,%d,%d,%d]" % (pin, offset_s, offset_ms, period_s,period_ms, duration_s,
                                                        duration_ms, secondary, analog_value))


    def start_measurement(self):
        """start the experiment"""
        self.arduino.send_command("b")

    def stop_measurement(self):
        """stop the experiment"""
        self.arduino.send_command("e")
        self.arduino.reset_arduino()





if __name__ == "__main__":


################ PARAMETERS

    parser = argparse.ArgumentParser(prog = 'SwitchLEDs')
    parser.add_argument('--port', default='COM5')
    args = parser.parse_args()
    
    ## ARDUINO connection
    port_arduino = args.port
    LEDs = ControlLight(port_arduino)
    LEDs.set_debug(True)
    time.sleep(2.0)

    blue_param = {'pin': 3,
            'offset': 500, #ms
            'period': 5*1000, #ms
            'duration': 2*1000, #ms
            'secondary': 1,
            'analog_value': 255,
            }

    # purple
    purple_param = {'pin': 11,
                'offset': 0,
                'period': 5*1000,
                'duration': 2*1000,
                'secondary': 0,
                'analog_value': 255,
                 }

                 
    LEDs.add_digital_pulse(blue_param)
    LEDs.add_primary_digital_pulse(purple_param)

    LEDs.start_measurement()

    time.sleep(30)

    LEDs.stop_measurement()
