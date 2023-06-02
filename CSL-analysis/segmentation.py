
import numpy as np
import matplotlib.pyplot as plt
import glob
import skimage


#image analysis
import sys
import os

import cv2

import pandas as pd
import skimage.io
from alienlab.improcessing import normalize, grey_to_rgb, make_binary
import alienlab.segment
from alienlab.fo import FramesOperator
import glob
from alienlab.regression_func import *
import time
import os
import numpy as np
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
from joblib import wrap_non_picklable_objects
import tqdm

import imageio
import itertools


import alienlab.plot
p = alienlab.plot.ShowFigure()
p.save_folder = "results/"
p.fontsize=18
p.fonttick=12
p.date = False
p.extension = ".pdf"

def init_image(file_path):
    frames_full = skimage.io.imread(file_path)

    #frames_full = np.stack([frames_full[:,:,1]]*10, 0) 
    #uncomment this line if you have a single RGB image. The [:,:,1] stands for selection of the green channel

    FO = FramesOperator(frames_full)
    im = normalize(FO.frames[0], 0, 1)
    im = grey_to_rgb(im)*255
    FO.compute_stats()

    # CROP
    #y, x = alienlab.io.select_roi(np.uint8(im)) #select area of interest

    FO.x = 100, 800
    FO.y = 100, 800
    #FO.crop() #crop image
    return FO


def segment_image(FO, contrast, autolevel, dist_max, dist_seg, disk_size, max_contrast, interact = True, showit = False):
    
    start_time = time.time()
    FO.selected_inds = np.linspace(250, 2050, 91).astype(int)

    
    def make_mask(contrast, autolevel, dist_max, dist_seg, disk_size, max_contrast, soft_hard_contrast, soft_hard_autolevel):
        #apply contrast filter to all frames
        frames_contrast = FO.apply(skimage.filters.rank.enhance_contrast,  footprint = skimage.morphology.disk(contrast))
        #apply autolevel filter to all frames
        frames_autolevel = FO.apply(skimage.filters.rank.autolevel, footprint = skimage.morphology.disk(autolevel))
        #sum the contrast images to get a reference grey-level contrast image
        frame_contrast = np.sum(frames_contrast, axis = 0)
        #sum the autolevel images to get a reference grey-level autolevel image
        frame_autolevel = np.sum(frames_autolevel, axis = 0)
        #obtain contrast mask from reference contrast image
        mask_contrast = make_binary(frame_contrast, soft_hard = soft_hard_contrast)
        #otbain autolevel mask from reference autolevel image
        mask_autolevel =  make_binary(frame_autolevel, soft_hard = soft_hard_autolevel)
        #intersection of contrast aud autolevel masks
        mask_intersect = mask_contrast * mask_autolevel
        #clean the masks with a binary opening
        mask_intersect = skimage.morphology.binary_opening(mask_intersect, footprint = skimage.morphology.disk(disk_size))
        #mask_intersect = skimage.morphology.binary_erosion(mask_intersect, selem = skimage.morphology.disk(disk_size))

        #reference image of altitude for the watershed
        auto_contrast = normalize(mask_intersect * frame_autolevel)
        print("--- Computed binary mask in %04f seconds ---" % (time.time() - start_time))

        p.cmap = "inferno"
        if showit:
            p.figsize = (20,8)
            p.title_list =  'contrast', 'contrast threshold', 'mask intersect','autolevel', 'autolevel threshold','segmentation image'
            p.col_num = 3
            fig = p.multi([frame_contrast, mask_contrast, mask_intersect, 
                           frame_autolevel, mask_autolevel,  auto_contrast])
            p.save_name = 'Segmentation reference'
            p.saving(fig)
            
        return auto_contrast, mask_intersect
    auto_contrast, mask_intersect = make_mask(contrast, autolevel, dist_max, dist_seg, disk_size, max_contrast, soft_hard_contrast = 1, soft_hard_autolevel = 1)
    ref, mask = make_mask(contrast, autolevel, dist_max, dist_seg, disk_size, max_contrast, soft_hard_contrast = 0.3, soft_hard_autolevel = 0.5)

    start_time = time.time()

    #locate the local maxima
    local_maxi = alienlab.segment.local_maxima(auto_contrast, max_contrast, p,
                                                     ref_distance = dist_max, mask = mask_intersect, show = showit)
    #perform watershed segmentation
    watershed_im_mask = alienlab.segment.watershed(ref*mask_intersect, mask , local_maxi,
                                                         p, ref_distance = dist_seg, show = showit)
    segmented = watershed_im_mask
    print("--- Computed segmentation in %04f seconds ---" % (time.time() - start_time))

    if showit:
        alienlab.segment.show_segmentation(FO, segmented, p)
        
    if interact == False:
       return watershed_im_mask, FO    