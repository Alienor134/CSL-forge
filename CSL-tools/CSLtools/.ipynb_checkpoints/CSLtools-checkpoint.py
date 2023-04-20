import numpy as np
import matplotlib.pyplot as plt

from matplotlib.ticker import MultipleLocator, FormatStrFormatter

from matplotlib.cm import get_cmap
from matplotlib.colors import Normalize



def set_figure(formatx = "%0.1e", formaty = "0.1e", figsize = (10,10)):
    inch = 2.35
    fig, ax = plt.subplots(figsize = (figsize[0]/inch, figsize[1]/inch))
    
    rc = {"font.family" : "Arial", 
          "mathtext.fontset" : "dejavusans",
          "axes.labelsize":15,
         "axes.labelsize":12}
    
    plt.rcParams.update(rc)

    
    formatx = FormatStrFormatter(formatx)
    formaty = FormatStrFormatter(formaty)

    ax.xaxis.set_major_formatter(formatx)
    ax.yaxis.set_major_formatter(formaty)
    
    return fig, ax



def val_cmap(cmap_name, values):
    #source: chatgPT
    cmap = get_cmap(cmap_name)
    # create a normalization object to scale values to the range [0, 1]
    norm = Normalize(vmin=np.min(values), vmax=np.max(values))
    # create a colormap object that maps values to colors
    mapper = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    
    return mapper.to_rgba

def random_cmap(cmap, N):
    cmap = matplotlib.colormaps[cmap]
    start = N//2
    cmap = cmap(np.linspace(0, 1, N+start))
    cmap = cmap[start:]
    random.seed(4)
    random.shuffle(cmap)
    return cmap