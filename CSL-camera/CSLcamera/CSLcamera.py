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
import pymmcore_plus
import os.path
import time
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import json
import threading
import skimage
import ipdb
import copy

def clip(input_image, high = 99.99, low = 0.001):
    im = copy.copy(input_image)
    im[im<np.percentile(im, low)]=np.percentile(im, low)
    im[im>np.percentile(im, high)]=np.percentile(im, high)
    return im



class Camera(threading.Thread):
    def __init__(self, config_file, cam_param, downscale=3, mm_dir = "C:/Program Files/Micro-Manager-2.0/"):
      threading.Thread.__init__(self)
      f = open(config_file)
      config = json.load(f)
      self.name = config["name"]
      self.video = []
      self.timing = []
      self.downscale = downscale
      self.camera_mode = "continuous_stream" #snap_image, snap_video
      self.N_im = 10

      self.mmc = pymmcore_plus.CMMCorePlus()
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

    def clip_im(self, im, mini = 0.1, maxi = 0.9):
      image = np.copy(im)
      Q1 = np.quantile(image, mini)
      Q3 = np.quantile(image, maxi)

      image[image<Q1]=Q1
      image[image<Q3]=Q3
      return image

       

    def update_param(self, key, val):
        self.mmc.setProperty(self.name, key, val)

    def get_param(self, key):
        return self.mmc.getProperty(self.name, key)



    def continuous_stream(self):
      cv2.namedWindow('live',cv2.WINDOW_NORMAL)
      self.mmc.startContinuousSequenceAcquisition(1)
      while True:
        if self.mmc.getRemainingImageCount() > 0:
          self.frame = self.mmc.popNextImage()
          self.image = np.array(Image.fromarray(np.uint8(self.frame)))
          cv2.imshow('live', cv2.normalize(self.image, None, 255,0, cv2.NORM_MINMAX, cv2.CV_8UC1))

        if cv2.waitKey(1) & 0xFF == ord('q'):
          break

      cv2.destroyAllWindows()
      self.mmc.stopSequenceAcquisition()
      
    def reset(self):
       self.mmc.reset()

    def snap_image(self):
        self.mmc.snapImage()
        self.frame = self.mmc.getImage()
        #image = np.array(Image.fromarray(np.uint8(frame)))


    def snap_video(self, N_im): 
      self.video = []
      self.timing = []
      cv2.namedWindow('live',cv2.WINDOW_AUTOSIZE)
      self.mmc.startContinuousSequenceAcquisition(1)
      i=0
      while True:
        if self.mmc.getRemainingImageCount() > 0:
          frame = self.mmc.popNextImage()
          frame = np.mean(frame, axis = 2)
          self.video.append(skimage.transform.downscale_local_mean(frame, self.downscale))
          self.timing.append(time.time())
          self.image = np.array(Image.fromarray(np.uint8(frame)))
          cv2.imshow('live',  cv2.normalize(clip(self.image), None, 255,0, cv2.NORM_MINMAX, cv2.CV_8UC1))
          #print(np.mean(frame))
          i+=1

        if cv2.waitKey(1) & 0xFF == ord('q'): 
          break

        if i>=N_im:
          break

      cv2.destroyAllWindows()
      self.mmc.stopSequenceAcquisition()
      self.mmc.reset()


    def run(self):
        # call the appropriate method based on a flag or some other logic
        if self.camera_mode == 'continuous_stream':
            self.continuous_stream()
        elif self.camera_mode == 'snap_video':
            self.snap_video(self.N_im)
        else:
            raise ValueError("Invalid mode: {}".format(self.camera.mode))      


if __name__== "__main__": 
    
  """ init camera"""

  """ DAHENG """
  cam_param = {"TriggerSource": "Software"}
  cam = Camera("C:/Users/alien/Documents/Github/CSL-forge/CSL-camera/MMconfig/Daheng.json", cam_param)

  """ UEYE """
  #cam_param = {"Trigger": "internal"}
  #cam = Camera("C:/Users/alien/Documents/Github/CSL-forge/CSL-camera/MMConfig/UEye.json", cam_param)

  """ ANDOR """
  #cam_param = {}
  #cam = Camera("C:/Users/alien/Documents/Github/CSL-forge/CSL-camera/MMConfig/Andor.json", cam_param)

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

  cam.snap_video(N_im)
  print(len(cam.video))



  """
  
  im = image_list[3][500:1500,500:1500,0];lap = skimage.filters.laplace(im);plt
.imshow(clip(lap), cmap="gray");plt.savefig("blur_lap.pdf",bbox_inches="tight");plt
.show()
  
plt.imshow(lap24, cmap='gray', vmin=lap24.min(),vmax=lap24.max());plt.axis('o
ff');plt.savefig("noblur_lap.pdf");plt.show()

lap3


EXPS 573, 568, 567
  """