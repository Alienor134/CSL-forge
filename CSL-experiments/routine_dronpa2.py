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

from ingredient_csl_leds import arduino_LED, add_primary_digital_pulse, add_digital_pulse, start_measurement, stop_measurement, create_link
from ingredient_save_folder import save_folder, make_folder
from CSLcamera.CSLcamera import Camera


from sacred.observers import MongoObserver
from sacred import Experiment

sec = 1000
min = 60*1000

@arduino_LED.config
def update_cfg(blue_param, purple_param, trigger_param):
    blue_param["offset"] = 0
    blue_param["period"] = 10*min
    blue_param["duration"] = 10*min
    blue_param["analog_value"] = 100

    trigger_param["period"] = 1*sec


ex = Experiment('Dronpa2', ingredients=[arduino_LED, save_folder ])
ex.observers.append(MongoObserver())


@ex.config
def cfg(arduino_LED):

    framerate = 1000/arduino_LED['trigger_param']['period']
    cam_type = "C:/Users/alien/Documents/Github/CSL-forge/CSL-camera/MMConfig/Daheng.json" #"MMconfig/UEye.json"
    cam_param = {"Exposure": 900000,
                 "Gain": 23,
                 "SensorHeight":2048//4,
                "SensorWidth":2448//4,}
    
    exp_duration = 60*250//arduino_LED["blue_param"]["analog_value"]



@ex.automain
def run(_run, cam_type, cam_param, exp_duration, framerate, arduino_LED):
    #ipdb.set_trace()
    save_folder =  make_folder(_run)
    ### initialize devices
    ##ARDUINO
    link = create_link(arduino_LED['port_arduino'])


    cam = Camera(cam_type, cam_param)


    #blue LED
    add_digital_pulse(link,  arduino_LED['blue_param'])

    #camera trigger
    add_digital_pulse(link,  arduino_LED['trigger_param'])

    #purple LED
    #add_primary_digital_pulse(link, purple_param)
    print('It will last ', exp_duration, 'seconds.')
    start_measurement(link)

    cam.snap_video(exp_duration*framerate)

    stop_measurement(link)

    result, timing = np.array(cam.video), np.array(cam.timing)
    fname = save_folder + "/video.tiff"
    tifffile.imwrite(fname, result[:,:,:,1],photometric="minisblack")
            
    fname_t = save_folder + '/video_timing.csv'
    pd.DataFrame(timing).to_csv(fname_t)


    #ftmp = tempfile.NamedTemporaryFile(delete=False)
    #fname = ftmp.name + ".pkl"
    #with open(fname,'wb') as f:
    #    pickle.dump(result, f)

    #_run.add_artifact(fname, "video.npy")

    _run.add_artifact(fname, "video.tiff")
    _run.add_artifact(fname, "video_timing.csv")

    for i, frame in enumerate(result):
        _run.log_scalar("Fluorescence", np.mean(frame), i)
        _run.log_scalar("Time", i/framerate, i)