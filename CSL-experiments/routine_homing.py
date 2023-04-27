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
  
"""
import time
from serial import *

from CSLstage.CSLstage import CSLstage


from sacred.observers import MongoObserver
from sacred import Experiment
sec = 1000
min = 60*1000


ex = Experiment('backlash')

ex.observers.append(MongoObserver())


@ex.config
def cfg():

    N=10
    step=-10

    gears = [1, 100, 1]
    arduino_motors = "COM6"


@ex.automain
def run(_run, arduino_motors, gears):
    

    stage = CSLstage(arduino_motors, gears)

    stage.handle_enable(1)

    stage.handle_set_homing()
    stage.handle_homing()
    time.sleep(4*60)
    for i in range(7):
        stage.move_dz(10000)
        time.sleep(11)

    stage.move_dz(6500) 
    time.sleep(7)   
    stage.handle_enable(0)
    
    