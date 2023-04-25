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

from serial import *


import numpy as np
from sacred import Ingredient

from CSLleds import CSLleds
from CSLserial import CSLserial

arduino_LED = Ingredient('arduino_LED')

@arduino_LED.config
def cfg():

    port_arduino = "COM5"

    blue_param = {'pin': 3,
            'offset': 500, #ms
            'period': 5*1000, #ms
            'duration': 2.5*1000, #ms
            'secondary': 1,
            'analog_value': 255,
            }

    # purple
    purple_param = {'pin': 11,
                'offset': 0,
                'period': 10*1000,
                'duration': 5*1000,
                'secondary': 0,
                'analog_value': 255,
                 }
    
    framerate = 1
    trigger_param = {"pin": 6,
                "offset": 0,
                "period": int(1000/framerate),
                "duration": 20,
                "secondary": 0,
                "analog_value": 255
                }


@arduino_LED.capture
def create_link(port_arduino):
    return CSLserial.create_link(port_arduino)

@arduino_LED.capture
def add_digital_pulse(link, dic_param):
    return CSLleds.add_digital_pulse(link, dic_param)


@arduino_LED.capture
def add_primary_digital_pulse(link, dic_param): 
    return CSLleds.add_primary_digital_pulse(link, dic_param)

@arduino_LED.capture
def start_measurement(link):
    return CSLleds.start_measurement(link)

@arduino_LED.capture
def stop_measurement(link):
    return CSLleds.stop_measurement(link)
