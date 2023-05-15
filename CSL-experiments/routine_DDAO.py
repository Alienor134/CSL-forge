"""
  
  Copyright (C) 2022 Sony Computer Science Laboratories
  
  Author(s) Aliénor Lahlou
  
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
import pickle

import pandas as pd
import pymmcore
import os.path
import time
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import tempfile
import ipdb

import tifffile
from serial import *

from ingredient_csl_leds import arduino_LED, get_arduino_light
from ingredient_save_folder import save_folder, make_folder
from CSLcamera import ControlCamera


from sacred.observers import MongoObserver
from sacred import Experiment

sec = 1000
min = 60*1000

@arduino_LED.config
def update_cfg(blue_param, purple_param, trigger_param):
    blue_param["offset"] = 0
    blue_param["period"] = 10*min
    blue_param["duration"] = 10*min
    blue_param["analog_value"] = 150

    purple_param["offset"] = 0
    purple_param["period"] = 10*min
    purple_param["duration"] = 10*min
    purple_param["analog_value"] = 150

    trigger_param["period"] = 1*sec


ex = Experiment('DDAO', ingredients=[arduino_LED, save_folder ])
ex.observers.append(MongoObserver())

@ex.named_config
def Daheng():
    cam_type = "C:/Users/alien/Documents/Github/CSL-forge/CSL-camera/MMConfig/Daheng.json"

    cam_param = {"TriggerMode":"Off",
                 "TriggerSource":"Software",
                "Exposure": 900000,
                 "Gain": 23,
                 "SensorHeight":2048//4,
                "SensorWidth":2448//4,}

@ex.config
def UEye(arduino_LED):
    cam_type = "C:/Users/alien/Documents/Github/CSL-forge/CSL-camera/MMConfig/UEye.json" 
    cam_param = {"Frame Rate":1,
                "Exposure": 170,
                 "Gain": 100}
    exp_duration = 2
    framerate = 1000/arduino_LED['trigger_param']['period']


@ex.automain
def run(_run, cam_type, cam_param, exp_duration, framerate, arduino_LED):
    #ipdb.set_trace()
    save_folder =  make_folder(_run)
    ### initialize devices
    ##ARDUINO
    arduino_light = get_arduino_light(arduino_LED['port_arduino'])


    cam = ControlCamera(cam_type, cam_param)


    #blue LED
    #add_digital_pulse(link,  arduino_LED['blue_param'])

    #purple LED
    arduino_light.add_digital_pulse(arduino_LED['blue_param'])

    #camera trigger
    arduino_light.add_digital_pulse(arduino_LED['trigger_param'])

    #purple LED
    #add_primary_digital_pulse(link, purple_param)
    print('It will last ', exp_duration, 'seconds.')
    arduino_light.start_measurement()

    cam.snap_image()

    arduino_light.stop_measurement()
    
    im = np.array(cam.frame)
    fname = save_folder + "/image.tiff"
    tifffile.imwrite(fname, im, photometric="minisblack")
            
    cam.reset()

    _run.add_artifact(fname, "image.tiff")

    _run.log_scalar("Fluorescence", np.mean(im), arduino_LED['blue_param']['analog_value'])
    

