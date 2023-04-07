# CSL-LEDs

This repository demonstrates how to control light sources with Arduino and Python, and output a trigger signal to synchronize a camera. 

The codes rely on [Arduino](https://www.arduino.cc/) and [pyserial](https://github.com/pyserial/pyserial).


**Prerequisites**:
- Install RomiSerial and the Arduino software XXXX
- The LEDs are already set-up (Note: to build an LED controller refer to this [OpenUC2 repository](https://github.com/SonyCSLParis/UC2_Fluorescence_microscope), otherwise you might already use one of these [Thorlabs controlers](https://www.thorlabs.com/navigation.cfm?guide_id=2109)
- The light sources can be controlled by a pulse, or pulse-width modulated signal (PWM) 
- The code was tested on Windows and Linux
  

## Install the library

```
git clone XXXXXXXX
cd CSL-LEDs
python setup.py develop
```



## Control the LEDs 
1. Connect the LED controller to the Arduino. 

2. Open the [.ino](/ArduinoControl/LEDControl/LEDControl.ino) file.
3. Select the Arduino board type in the "Tools/card type"
<p align="center">
<a> <img src="./Images/2023-04-07-18-41-01.png" width="500"></a>
</p>
4. Select the COM port. If the name of the board doesn't appear near any port, change the port USB until the name appears.

<p align="center">
<a> <img src="./Images/2023-01-30-10-16-46.png" width="300"></a>
</p>

5. Press the check sign. If an error related to "RomiSerial" appears, verify that you have properly followed the instructions in the CSL-Serial repository. 
<p align="center">
<a> <img src="./Images/2023-04-07-18-48-09.png" width="500"></a>
</p>

6. If no error appears you can click the arrow to load the code in the Arduino. 
 
7. To test that you can properly interact with the Arduino, click on the magnifying glass in the upper right to open the serial monitor and type: "#?:xxxx" and ensure you get this output: 
 <p align="center">
<a> <img src="./Images/2023-01-30-10-18-53.png" width="300"></a>
</p>


8. Run the code, you should see the LEDs blink.


On Windows

```python CSLleds/CSLleds.py```

or

```python CSLleds/CSLleds.py --port COMx```


On Linux

```python3 CSLleds/CSLleds.py --port /dev/ttyACM0```


8. Open the python code to see how it works. Open the python code [CSLleds.py](CSLleds/CSLleds.py). The code is commented and allows to control the frequency and amplitude of the LEDs. Set the parameters: 
The content of interest is after ``if __name__ == __main__:`` 
- replace the COM port with the one of your set-up ([tutorial](https://www.arduino.cc/en/Guide/ArduinoUno)). 
- input the correct ports for the LED control. The port 3 and 11 are good choices because they are PWM pins which allow to control the intensity level of the LEDs rather than only ON-OFF. 
- you can change the other parameters that correspond to this scheme: 

 <p align="center">
<a> <img src="./Images/square_wave_python.png" width="400"></a>
</p>



### License

This project is licensed under the [GNU General Public License v3.0](https://www.tldrlegal.com/license/gnu-general-public-license-v3-gpl-3)