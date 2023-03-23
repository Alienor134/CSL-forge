"""
  
  Copyright (C) 2023 Sony Computer Science Laboratories
  
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
  
  #source https://github.com/mightenyip/neuronDetection/blob/14d64c44ab4a9e11af14c15961cd5ea4d22506e2/live_neuron_detection.py

"""
import pymmcore
import os.path
import time
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import json



class Camera:
    def __init__(self, config_file, cam_param, mm_dir = "C:/Program Files/Micro-Manager-2.0/"):
      f = open(config_file)
      config = json.load(f)
      self.name = config["name"]


      self.mmc = pymmcore.CMMCore()
      self.mmc.getCameraDevice()
      self.mmc.setDeviceAdapterSearchPaths([mm_dir])
      self.mmc.loadSystemConfiguration(config["MMconfig"])



      
      #basic config from config .json file
      for key in config:
        if key not in ["name", "MMconfig"]:
          self.mmc.setProperty(self.name, key, config[key])
      
      #local config update
      for key in cam_param:
          self.mmc.setProperty(self.name, key, cam_param[key])

    def update_param(self, key, val):
        self.mmc.setProperty(self.name, key, val)

    def get_param(self, key):
        return self.mmc.getProperty(self.name, key)

    def continuous_stream(self):
      cv2.namedWindow('live',cv2.WINDOW_NORMAL)
      self.mmc.startContinuousSequenceAcquisition(1)
      while True:
        if self.mmc.getRemainingImageCount() > 0:
          frame = self.mmc.popNextImage()
          image = np.array(Image.fromarray(np.uint8(frame)))
          cv2.imshow('live', cv2.normalize(image, None, 255,0, cv2.NORM_MINMAX, cv2.CV_8UC1))

        if cv2.waitKey(1) & 0xFF == ord('q'):
          break

      cv2.destroyAllWindows()
      self.mmc.stopSequenceAcquisition()
      self.mmc.reset()

    def snap_image(self):
        self.mmc.snapImage()
        frame = self.mmc.getImage()
        #image = np.array(Image.fromarray(np.uint8(frame)))
        return frame


    def snap_video(self, N_im): 
      frame_list = []
      time_list = []
      cv2.namedWindow('live',cv2.WINDOW_AUTOSIZE)
      self.mmc.startContinuousSequenceAcquisition(1)
      i=0
      while True:
        if self.mmc.getRemainingImageCount() > 0:
          frame = self.mmc.popNextImage()
          frame_list.append(frame)
          time_list.append(time.time())
          image = np.array(Image.fromarray(np.uint8(frame)))
          cv2.imshow('live', image)
          #print(np.mean(frame))
          i+=1

        if cv2.waitKey(1) & 0xFF == ord('q'): 
          break

        if i>=N_im:
          break

      cv2.destroyAllWindows()
      self.mmc.stopSequenceAcquisition()
      self.mmc.reset()

      return np.array(frame_list), np.array(time_list)

if __name__== "__main__": 
    
  """ init camera"""

  """ DAHENG """
  cam_param = {"TriggerSource": "Software"}
  cam = Camera("C:/Users/alien/Documents/Github/CSL-forge/CSL-camera/MMconfig/Daheng.json", cam_param)

  """ UEYE """
  #cam_param = {"Trigger": "internal"}
  #cam = Camera("C:/Users/alien/Documents/Github/CSL-forge/CSL-camera/MMConfig/UEye.json", cam_param)

  """ Acquisition """

  """ Continuous stream """
  #cam.continuous_stream()


  """ Single image """
  
  if False:
    im = cam.snap_image()
    plt.imshow(im)
    plt.show()
    time.sleep(10)

  """ Video acquisition """

  #exp_duration = 5 #s
  #N_im = exp_duration * float(cam.get_param("AcquisitionFrameRate"))
  N_im =  20

  video, timing = cam.snap_video(N_im)