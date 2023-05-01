Experimental framework based on Sacred
======

All the information about sacred are here: [visit Sacred](https://github.com/IDSIA/sacred)

Example of adaptation of [CSL-lights](XXX)
-------
+-----------------------------------------------+--------------------------------------------------------+
| **Script to control a light source**          | **The same script as Sacred experiment**               |
+===============================================+========================================================+
| .. code:: python                              | .. code:: python                                       |
|                                               |                                                        |
|   from serial import Serial                   |   from serial import Serial                            |
|   import CSLlight                             |   import CSLlight                                      |
|   arduino_port = "COM5"                       |   from sacred.observers import MongoObserver           |
|   sec = 1000 #conversion ms to s              |   from sacred import Experiment                        |
|   LED_param = {'pin':11,                      |   ex = Experiment('blink_LED')                         |
|   'offset':0.5*sec,                           |   ex.observers.append(MongoObserver(db_name = "demo")) |
|   'period': 5*sec,                            |                                                        |
|   'duration': 2*sec,                          |   @ex.config:                                          |
|   'analog_value': 255,                        |   def cfg():                                           |
|   }                                           |     arduino_port = "COM5"                              |
|                                               |     sec = 1000 #conversion ms to s                     |
|   link = Serial(arduino_port)                 |     LED_param = {'pin':11,                             |
|   CSLLight.add_digital_pulse(link, LED_param) |                  'offset':0.5*sec,                     |
|   CSLlight.start_measurement(link)            |                  'period': 5*sec,                      |
|   time.sleep(300)                             |                  'duration': 2*sec,                    |
|   CSLlight.stop_measurement(link)             |                  'analog_value': 255,                  |
|                                               |                  }                                     |
|                                               |   @ex.capture                                          |
|                                               |   def blink():                                         |
|                                               |     link = Serial(arduino_port)                        |
|                                               |     CSLLight.add_digital_pulse(link, LED_param)        |
|                                               |     CSLlight.start_measurement(link)                   |
|                                               |     time.sleep(300)                                    |
|                                               |     CSLlight.stop_measurement(link)                    |
|                                               |                                                        |
|                                               |   @ex.automain                                         |
|                                               |   def run():                                           |
|                                               |     blink()                                            |
|                                               |                                                        |
+-----------------------------------------------+--------------------------------------------------------+

Example of adaptation of [CSL-motors](XXX)
-------

+--------------------------------------------+--------------------------------------------------------+
| **Script to control a motor**              | **The same script as Sacred experiment**               |
+============================================+========================================================+
| .. code:: python                           | .. code:: python                                       |
|                                            |                                                        |
|   from CSLstage.CSLstage import CSLstage   |   from serial import Serial                            |
|                                            |   import CSLlight                                      |
|   arduino_port = "COM6"                    |   from sacred.observers import MongoObserver           |
|                                            |   from sacred import Experiment                        |
|   stage = CSLstage(arduino_port, [1,1,1])  |   ex = Experiment('blink_LED')                         |
|   #gearbox ratio of X, Y and Z axis        |   ex.observers.append(MongoObserver(db_name = "demo")) |
|   stage.handle_enable(1)                   |                                                        |
|   stage.move_dx(10)                        |   @ex.config:                                          |
|   stage.handle_enable(0)                   |   def cfg():                                           |
|   stage.link.close()                       |     arduino_port = "COM5"                              |
|                                            |     gears = [1,1,1]                                    |
|                                            |                                                        |
|                                            |   @ex.capture                                          |
|                                            |   def get_stage():                                     |
|                                            |     stage = CSLstage(arduino_port, [1,1,1])            |
|                                            |                                                        |
|                                            |   @ex.automain                                         |
|                                            |   def run():                                           |
|                                            |     stage = get_stage()                                |
|                                            |                                                        |
|                                            |     stage.handle_enable(1)    stage.move_dx(10)        |
|                                            |     stage.handle_enable(0)                             |
|                                            |     stage.link.close()                                 |
|                                            |                                                        |
+--------------------------------------------+--------------------------------------------------------+

Example of adaptation of [CSL-camera](XXX)
-------
