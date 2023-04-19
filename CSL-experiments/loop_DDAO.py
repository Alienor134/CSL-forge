#from qE_OJIP_Benjamin import ex
from routine_DDAO import ex as ex
import numpy as np
import time
import ipdb 
import matplotlib.pyplot as plt
import pandas as pd
import datetime

intensities = list(np.linspace(0, 255, 10))[::-1] + list(np.linspace(0, 255, 10))

for i, intensity in enumerate(intensities):
                r = ex.run(config_updates={'arduino_LED':
                                           {'purple_param':
                                            {'analog_value':intensity}
                                           }
                                          }
                          )
                time.sleep(1)

                