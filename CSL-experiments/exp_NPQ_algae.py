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

    blue_param["offset"] = 0*250*sec + 20*sec
    blue_param["period"] = 30*min
    blue_param["duration"] = 15*min
    blue_param["analog_value"] = 255//5
    blue_param["secondary"] = 1
    

    purple_param["offset"] = 0*250*sec + 10*sec
    purple_param["period"] = 20*sec
    purple_param["duration"] = 200 #ms
    purple_param["analog_value"] = 190
    purple_param["secondary"] = 0

    
    
    trigger_param["offset"] = 15
    trigger_param["period"] = 1*sec


ex = Experiment('NPQ_leaf', ingredients=[arduino_LED, save_folder ])
ex.observers.append(MongoObserver())



@ex.config
def cfg(arduino_LED):
        framerate = 1000/arduino_LED['trigger_param']['period']
        exp_duration = 250 + 30*60
        downscale = 10

@ex.named_config
def Daheng():
    cam_type = "C:/Users/alien/Documents/Github/CSL-forge/CSL-camera/MMConfig/Daheng.json"

    cam_param = {"Exposure": 150*1000,
                 "Gain": 23,
                 "SensorHeight":2048,
                "SensorWidth":2448,
                "TriggerMode": "On",
                "TriggerSource":"Line2"}

@ex.config
def UEye():
    cam_type = "C:/Users/alien/Documents/Github/CSL-forge/CSL-camera/MMConfig/UEye.json" 
    cam_param = {"Frame Rate":1,
                "Exposure": 170,
                 "Gain": 100}

#@ex.capture()
#def open_camera():
#    cam = Camera(cam_type, cam_param, downscale)
#    return cam

@ex.automain
def run(_run, exp_duration, framerate, arduino_LED, cam_type, cam_param, downscale):
    #ipdb.set_trace()
    save_folder =  make_folder(_run)
    ### initialize devices
    ##ARDUINO
    arduino_light = get_arduino_light(arduino_LED['port_arduino'])

    cam = ControlCamera(cam_type, cam_param, downscale)
    #cam.camera_mode = "snap_video"
    #cam.N_im = framerate*exp_duration

    
    #camera trigger
    arduino_light.add_digital_pulse(arduino_LED['trigger_param'])

    #blue LED
    arduino_light.add_digital_pulse(arduino_LED['blue_param'])

    #purple LED
    arduino_light.add_primary_digital_pulse(arduino_LED['purple_param'])



    #purple LED
    #add_primary_digital_pulse(link, purple_param)
    print('It will last ', exp_duration, 'seconds.')

    #cam.start()
    
    arduino_light.start_measurement()

    cam.snap_video(framerate*exp_duration)
    arduino_light.stop_measurement()
    #cam.join()

    result, timing = cam.save_video(_run)

    for i, frame in enumerate(result):
        _run.log_scalar("Fluorescence", np.mean(frame), i)
        _run.log_scalar("Time", timing[i], i)