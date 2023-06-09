from CSLlight import ControlLight

#arduino_port = "COM5"
arduino_port = "/dev/ttyACM0"

sec = 1000

blue_param = {'pin': 6,
              'offset': 0,
              'period': 1*sec,
              'duration': 0.5*sec,
              'analog_value': 255,
              }

arduino_light = ControlLight(arduino_port)
arduino_light.add_digital_pulse(blue_param)

arduino_light.start_measurement(60*sec)
arduino_light.wait()
