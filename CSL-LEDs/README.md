# CSL-LEDs

This repository demonstrates how to control light sources with Arduino and Python, and output a trigger signal to synchronize a camera. 

The codes rely on [Arduino](https://www.arduino.cc/) and [pyserial](https://github.com/pyserial/pyserial).


**Prerequisites**:
- The LEDs are already set-up (To build such a set-up, refer to: https://github.com/SonyCSLParis/UC2_Fluorescence_microscope)
- The light sources can be controlled by a pulse-width modulated signal (PWM) 
- The code was tested on Windows and Linux


## Install the library

```
git clone XXXXXXXX
cd CSL-LEDs
python setup.py develop
```



## Control the LEDs 
1. Connect the LED controller to the Arduino. (Note: to build an LED controller refer to this [OpenUC2 repository](https://github.com/SonyCSLParis/UC2_Fluorescence_microscope), otherwise you might already use one of these [Thorlabs controlers](https://www.thorlabs.com/navigation.cfm?guide_id=2109). 

2. If you have never used an Arduino you can start with the [tutorial](https://www.arduino.cc/en/Guide/ArduinoUno).

3. In the [ArduinoControl](/ArduinoControl/) folder you will find a [zip file](/ARDUINO/RomiSerial.zip) that you can **extract** in the folder where Arduino fetches libraries (usually "Documents/Arduino/Libraries on Windows").

4. Open the [.ino](/ArduinoControl/LEDControl/LEDControl.ino) file and load the code on the Arduino. The code allows to generate sequences of excitation to control the LEDs. To check that the serial interaction works open the serial connection, select the following parameters: 

<p align="center">
<a> <img src="./Images/2023-01-30-10-16-46.png" width="300"></a>
</p>


5. To test that you can properly interact with the Arduino, click on the loop in the upper right to open the serial monitor and type: "#?:xxxx" and ensure you get this output: 
 <p align="center">
<a> <img src="./Images/2023-01-30-10-18-53.png" width="300"></a>
</p>

1. You can now test the python code to interact with the Arduino. Open the python code [switch_LEDs.py](/switch_LEDs.py). The code is commented and allows to control the frequency and amplitude of the LEDs. Set the parameters: 
The content of interest is after ``if __name__ == __main__:`` 
- replace the COM port with the one of your set-up ([tutorial](https://www.arduino.cc/en/Guide/ArduinoUno)). 
- input the correct ports for the LED control. The port 3 and 11 are good choices because they are PWM pins which allow to control the intensity level of the LEDs rather than only ON-OFF. 
- you can change the other parameters that correspond to this scheme: 

 <p align="center">
<a> <img src="./Images/square_wave_python.png" width="400"></a>
</p>


1. Run the code, you should see the LEDs blink.


On Windows

```python3 switch_LEDs.py```

or

```python3 switch_LEDs.py --port COMx```


On Linux

```python3 switch_LEDs.py --port /dev/ttyACM0```

### License

This project is licensed under the [GNU General Public License v3.0](https://www.tldrlegal.com/license/gnu-general-public-license-v3-gpl-3)