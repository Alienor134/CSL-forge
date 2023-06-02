import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import subprocess

import sys
from copy import copy
import scipy
import imageio
sys.path.append("../")
import itertools
from scipy.stats import norm
import matplotlib.mlab as mlab
from mvgavg import mvgavg
import json
import matplotlib.patches as mpatches
from matplotlib import gridspec
import matplotlib.patches as mpatch
from lovely_numpy import lo

from matplotlib.ticker import FormatStrFormatter


save_folder = "G:/DREAM/from_github/thesis/Figures/LDA/"
import seaborn as sns

from random import randrange
from joblib import wrap_non_picklable_objects


import alienlab
from alienlab import regression_func
import pickle as pk
from alienlab import plot
from activation_experiment import activation_experiment


from scipy.stats.stats import pearsonr


import skimage.registration


#from useful_func import dtw, get_path, plot_warped_timeseries
#from useful_func import spectrum_a, spectrum_d
#from useful_func import residuals, exp_decay, get_fit, sigmoid, exp_decay_max
#from useful_func import gradient_magnitude, gradient_orientation, gaussian_kernel, assign_orientation, crop_center, cconv, get_algae_im
#from useful_func import make_svm, make_pca
#from useful_func import fit_biexp, fit_exp, fit_monoexp


from numpy import genfromtxt

from joblib import Parallel, delayed
from sklearn.decomposition import PCA

from mpl_toolkits.axes_grid1 import make_axes_locatable



import sklearn
import sklearn.discriminant_analysis
import pandas as pd


import skimage


import tifffile as tiff
import random
import matplotlib


import alienlab.plot

p = alienlab.plot.PlotFigure()
p.extension = ".png"

p.date = False
p.figsize = (10,10)
p.fonttick=12
p.fontsize=18

TEI = ["qT-0-0", "0-qE-0", "0-0-qI"]



#########################################################
data_folder = "../data/"


traces_list = np.load(data_folder + 'traces_list.npy') # pulses
pulses = np.load(data_folder + 'pulses_list.npy')
Z = {}
method_list = ['combine0', 'combine1', 'combine2', 'combine3', 'combine4', "pulses", "dict", "simple", "simple_bad_qE", "simple_bad_qT", "simple_bad_qI", "lda_only", "pca"]
for method in method_list:
    Z[method] = np.load(data_folder + method + "_array_proj.npy") # projections des dictionnaires 3D résultat LDA
    
label_list = np.load(data_folder + 'label_list.npy') #0_0_0
algae_list = np.load(data_folder + 'algae_list.npy')
imref_list = np.load(data_folder + 'imref_list.npy')
mask_list = np.load(data_folder + 'mask_list.npy')
time_list = np.load(data_folder + 'time_list.npy')
time_listo =  time_list - time_list[:,0:1]
time_pulses = time_listo[:,250::20]

class_match = json.load(open(data_folder + "class_match.json"))

exp_match = json.load(open(data_folder + "description_match.json"))
colmap = json.load(open(data_folder + "color_map.json"))# colormap 
colmap = {int(k):v for k,v in colmap.items()}
id_list = np.load(data_folder + 'id_list.npy') #1 per 0_0_0
exp_array = np.load(data_folder + 'exp_list.npy')

lims = {}
for method in method_list:
    lims[method] = json.load(open(data_folder + method + "_array_ax_lim.json"))

    

purple = [0, 162, 354]#, 162, 182, 198] #0_0_0
            
blue = [2, 164, 356]#[2, 164, 184, 200, 356]#[1, 2, 367]#[2, 3] #165, 185, 201, #0_0_3
            
#orange = [6, 120, 168, 188, 204, 360,#0_1_2
#            7, 121, 169, 189, 205, 361] #0_1_3
orange = [  7 , 169, 361]            
#green = [ 14, 15, 57, 251, 252, 464, 465, 475, 476]
        #[ 14,  15,  57, 220, 221, 251, 252, 256, 257, 379, 380, 409, 410, 432, 433, 448 ,449] #1_0_3
            #229, 239, 228, 238, 36, 46, 35, 45,
green = [15, 465, 476, 488]#15,252,#[465, 475, 476, 487, 488]

    
grey = [12, 55, 249]#1_0_0

red = [17,18, 19]

wt4_activation = [57, 60, 61, 64, 65, 68, 69] #chunck activation

cc124_activation = [257, 260, 261, 264]
cc124_activation_13 = [268, 272, 275, 280]

wt4_inhibition = [249, 250, 251, 252]
wt4_inhibition2 = [12, 13, 14, 15]





method = "combine4"
x = 0 #qT
y = 1 #qE

##########################################################

def cmap_from_ext(low, high, N):
    cvals  = [0,  1]
    colors = [low, high]

    norm=plt.Normalize(min(cvals),max(cvals))
    tuples = list(zip(map(norm,cvals), colors))
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", tuples)
    cmap = cmap(np.linspace(0, 1, N+N//3))[N//3:N]
    random.seed(4)
    random.shuffle(cmap)
    im = np.linspace(0, N-1, N).astype(int)
    plt.figure()
    u = np.tile(cmap[:,:3], (1, 1, 1))
    print(u.shape)
    plt.imshow(u)
    plt.axis('off')
    return cmap

def cmap_from_plt(cmap, N):
    cmap = matplotlib.colormaps[cmap]
    start = N//2
    cmap = cmap(np.linspace(0, 1, N+start))
    cmap = cmap[start:]
    random.seed(4)
    random.shuffle(cmap)
    #plt.figure()
    #u = np.tile(cmap[:,:3], (1, 1, 1))
    #plt.imshow(u)
    #plt.axis('off')
    return cmap

def generate_col(N): #colormap
    color_condition = {}
    
    color_condition["0_0_0"] = cmap_from_plt("Purples", N)

    color_condition["1_0_0"] = cmap_from_plt("Greys", N)

        
    color_condition["0_0_1"] = cmap_from_plt("Blues", N)
    color_condition["0_0_2"] = cmap_from_plt("Blues", N)
    color_condition["0_0_3"] = cmap_from_plt("Blues", N)

    
    color_condition["0_1_3"] = cmap_from_plt("Oranges", N)
    color_condition["0_1_2"] = cmap_from_plt("Oranges", N)

    color_condition["1_0_2"] = cmap_from_plt("Greens", N)
    color_condition["1_0_3"] = cmap_from_plt("Greens", N)
    color_condition["8_0_2"] = cmap_from_plt("Greens", N)
    color_condition["8_0_3"] = cmap_from_plt("Greens", N)
    color_condition["9_0_2"] = cmap_from_plt("Greens", N)
    color_condition["9_0_3"] = cmap_from_plt("Greens", N)

    color_condition["1_1_1"] = cmap_from_plt("Reds", N)
    color_condition["1_1_2"] = cmap_from_plt("Reds", N)
    color_condition["1_1_3"] = cmap_from_plt("Reds", N)
    
    color_condition["2_0_2"] = cmap_from_plt("Oranges", N)
    color_condition["2_0_3"] = cmap_from_plt("Oranges", N)
    
    color_condition["3_0_2"] = cmap_from_plt("terrain", N)
    color_condition["3_0_3"] = cmap_from_plt("terrain", N)
    
    return color_condition

def get_idxs(id_list, sel_classes): #select experiment
    idxs = []
    for i,c in enumerate(sel_classes):  
      nidxs=np.where(id_list==c)[0]
      idxs=np.concatenate([idxs,nidxs])
    return idxs

def create_fig_base(data, method, x, y, color_condition, fig, id_list, Z, label_list, lims, markersize = 2):
    Z0 = Z[method][data]
    label_list0 = label_list[data]
    id_list0 = id_list[data]

    class_color = np.zeros((len(label_list0),4)).astype(str)
    for i, c in enumerate(['0_1_2', '0_1_3', '1_0_2', '1_0_3', '0_0_2', '0_0_0']):#np.unique(label_list0)):
        pos = label_list0 == c
        class_color[label_list0 == c] = ["darkorange", "darkorange", "seagreen", "seagreen", "cornflowerblue", "slateblue"][i]#color_condition[c][id_list0[pos]%10]
        plt.scatter(x = Z0[pos,x], y = Z0[pos,y], c=class_color[pos], s= markersize)#id_list0.astype(str))#, color_discrete_sequence=colmap)
    #plt.scatter(x = Z0[:,x], y = Z0[:,y], c=class_color, s= markersize)#id_list0.astype(str))#, color_discrete_sequence=colmap)
    plt.xlim(lims[method]["%d,%d"%(x,y)][0])
    plt.ylim(lims[method]["%d,%d"%(x,y)][1])
    plt.xlabel(TEI[x])
    plt.ylabel(TEI[y])
    plt.legend()

    return fig

def create_fig(data, method, x, y, color_condition, fig, id_list, Z, label_list, lims, markersize = 2):
    Z0 = Z[method][data]
    label_list0 = label_list[data]
    id_list0 = id_list[data]

    class_color = np.zeros((len(label_list0),4)).astype(str)
    for i, c in enumerate(np.unique(label_list0)):
        pos = label_list0 == c
        #class_color[label_list0 == c] = ["darkorange", "darkorange", "seagreen", "seagreen", "cornflowerblue", "slateblue"][i]
        class_color[label_list0 == c] = color_condition[c][id_list0[pos]%10]

    plt.scatter(x = Z0[:,x], y = Z0[:,y], c=class_color, s= markersize)#id_list0.astype(str))#, color_discrete_sequence=colmap)
    plt.xlim(lims[method]["%d,%d"%(x,y)][0])
    plt.ylim(lims[method]["%d,%d"%(x,y)][1])
    plt.xlabel(TEI[x])
    plt.ylabel(TEI[y])
    plt.legend()

    return fig

def define_idxs(selected, method, id_list, Z):
    idxs = get_idxs(id_list, np.array(selected).astype(int))
    idxs = np.array(idxs, dtype=int)
    Z0 = Z[method][idxs]
    select = np.zeros(idxs.shape)
    for val in np.unique(id_list[idxs]):
        mask = id_list[idxs]==val
        zcrop = abs(Z0 - np.mean(Z0[mask], axis = 0)) < 2.5 * np.std(Z0[mask], axis = 0)
        zcrop = zcrop.min(axis = 1)   
        prod = mask*zcrop
        #print(val, np.sum(prod)/np.sum(mask)*100, '% kept')
        select += prod
    select = select.astype(bool)
    idxs = idxs[select]
    return idxs


def remove_nan(X,Y):
    mask = (X==X)*(Y==Y)
    return X[mask], Y[mask]

def clip_xy(X,Y, mini = 0.015, maxi = 0.985):
    X, Y = remove_nan(X,Y)
    x_min = np.quantile(X, mini)
    y_min = np.quantile(Y, mini)
    x_max = np.quantile(X, maxi)
    y_max = np.quantile(Y, maxi)
    print(x_min, x_max, y_min, y_max)
    mask = (X>x_min)*(X<x_max)*(Y>y_min)*(Y<y_max)
    return X[mask], Y[mask]

def select_ind(ref, required):
    base = ref != ref
    for req in required: 
        base += ref==req
    return base.astype(bool)




import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms


def confidence_ellipse(x, y, ax, n_std=1.0, facecolor='none', **kwargs):
    """
    source: https://matplotlib.org/3.1.1/gallery/statistics/confidence_ellipse.html#sphx-glr-gallery-statistics-confidence-ellipse-py
    Create a plot of the covariance confidence ellipse of `x` and `y`

    Parameters
    ----------
    x, y : array_like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    Returns
    -------
    matplotlib.patches.Ellipse

    Other parameters
    ----------------
    kwargs : `~matplotlib.patches.Patch` properties
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0),
        width=ell_radius_x*2,
        height=ell_radius_y*2,
        facecolor=facecolor,
        **kwargs)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ellipse


def create_ellipse(method, to_plot, x, y, id_list, Z, lims):
    p.fontsize = 18
    p.fonttick = 15
    fig = p.set_figure_flex("%d", "%d")#, figsize = (15,15))
    ax = plt.gca()
    
    ax.tick_params(axis='both', which='major', labelsize=20)

    ellipse_list = {}
    colors_ellipse = ["cornflowerblue", "slateblue", "darkorange", "seagreen", "red"]
    colors_ellipse = ["cornflowerblue", "darkorange", "seagreen"]
    
    #for en, classes in enumerate([blue, purple, orange, green, red]):
    for en, classes in enumerate(to_plot):

        data = define_idxs(classes, method, id_list, Z)

        color_ellipse = colors_ellipse[en]
        Z0 = Z[method][data]


        ellipse = confidence_ellipse( Z0[:,x], Z0[:,y], ax, facecolor=color_ellipse, alpha = 0.3)

        ax.add_patch(copy(ellipse))


        plt.xlim(lims[method]["%d,%d"%(x,y)][0])
        plt.ylim(lims[method]["%d,%d"%(x,y)][1])
        plt.xlabel(TEI[x])
        plt.ylabel(TEI[y])
        plt.legend()

    return fig, ax

