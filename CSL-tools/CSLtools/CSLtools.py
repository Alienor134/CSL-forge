import numpy as np
import matplotlib.pyplot as plt

from matplotlib.ticker import MultipleLocator, FormatStrFormatter

def set_figure("%0.1e", "0.1e", figsize = (10,10)):
    
    fig, ax = plt.subplots(figsize = figsize)
    
    rc = {"font.family" : "Arial", 
            "mathtext.fontset" : "dejavusans",
         "axes.labelsize"=15,
         "axes.labelsize"=12}
    
    plt.rcParams.update(rc)

    
    formatx = FormatStrFormatter(formatx)
    formaty = FormatStrFormatter(formaty)

    ax.xaxis.set_major_formatter(formatx)
    ax.yaxis.set_major_formatter(formaty)
    
    return fig, axs