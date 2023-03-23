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

arduino = Ingredient('arduino')

@arduino.config
def cfg():
    port_arduino = "COM5"


#Source ROMI Github: https://github.com/romi/romi-rover-build-and-test

@arduino.capture
def create_link(port_arduino):
    link = Serial(port_arduino, 115200)
    time.sleep(2.0)
    return link


@arduino.capture
def send_command(link, s):
    """send serial command to the arduino to create or execute a function"""
    print("Command: %s" % s)
    command = "#" + s + ":xxxx\r\n"
    print(command)
    print(link.write(command.encode('ascii')))

    return assert_reply(read_reply(link))

@arduino.capture   
def read_reply(link):
    """read reply from the arduino"""
    while True:
        s = link.readline().decode("ascii").rstrip()
        if s[0] == "#":
            if s[1] == "!":
                print("Log: %s" % s)
            else:
                print("Reply: %s" % s)
                break;
    return s

@arduino.capture
def assert_reply(line):
    """assert the intergity of the reply """
    s = str(line)
    start = s.find("[")
    end = 1 + s.find("]")
    array_str = s[start:end]
    return_values = json.loads(array_str)

    print(return_values)
    status_code = return_values[0]
    success = (status_code == 0)
    if not success:
        raise RuntimeError(return_values[1]) 
    return return_values


#Source: https://forum.arduino.cc/index.php?topic=38981.0
@arduino.capture
def reset_arduino(link):
    link.setDTR(False) # Drop DTR
    time.sleep(0.022)    # 22ms is what the UI does.
    link.setDTR(True)  # UP the DTR back
    time.sleep(2)




if __name__ == "__main__":


################ PARAMETERS

    parser = argparse.ArgumentParser(prog = 'SwitchLEDs')
    parser.add_argument('--port', default='COM5')
    args = parser.parse_args()
    
    ## ARDUINO connection
    port_arduino = args.port
    link = Serial(port_arduino, 115200)
    time.sleep(2.0)

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
    add_digital_pulse(link, blue_param)
    add_digital_pulse(link, purple_param)

    start_measurement(link)

    time.sleep(300)

    stop_measurement(link)
