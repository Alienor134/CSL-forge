from CSLlight import ControlLight

#arduino_port = "COM5"
arduino_port = "/dev/ttyACM0"

ms = 1
sec = 1000

blue_param = {}
purple_param = {}

purple_param["pin"] = 11
purple_param["offset"] = 0
purple_param["duration"] = 10*ms
purple_param["period"] = 50*ms
purple_param["analog_value"] = 255

blue_param["pin"] = 6
blue_param["offset"] = 0
blue_param["duration"] = 0.5*sec
blue_param["period"] = 1*sec
blue_param["analog_value"] = 255

arduino_light = ControlLight(arduino_port)
arduino_light.arduino.set_debug(True)

arduino_light.add_digital_pulse(blue_param)
arduino_light.add_digital_pulse(purple_param)
arduino_light.set_secondary(purple_param, blue_param)

arduino_light.start_measurement(20*sec)
arduino_light.wait()
