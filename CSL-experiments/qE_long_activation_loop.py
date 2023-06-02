from subprocess import call
import time


def focus():
    print("FOCUS")
    #call(["python", "autofocus_wider.py"])
    call(["python", "routine_autofocus.py"])

def dark_adaptation():
    print("DARK ADAPTATION")
    time.sleep(15*60)

def measurement_loop(n):
    print("MEASUREMENT LOOP")
    # MEASUREMENTS BEFORE ACTIVATION
    for i in range(n):
        call(["python", "exp_NPQ_algae.py"])
        
    
def activation_and_rest(activation_time_HL = 240,
                        level_HL = 255//5,
                        
                        rest_time_LL=45, 
                        level_LL=1, 
                        ):
    # 2H ACTIVATION   
    print("ACTIVATION") 
    call(["python", "exp_TREATMENT.py", "with", "exp_duration=%d"%activation_time_HL, "arduino_LED.blue_param.analog_value=%d"%level_HL])    
    print("RELAX LOW LIGHT")
    call(["python", "exp_TREATMENT.py", "with", "exp_duration=%d"%rest_time_LL,  "arduino_LED.blue_param.analog_value=%d"%level_LL])

    
# before activation
#activation_and_rest(activation_time_HL=0)#level_HL = 250, activation_time_HL=60*3) #2H45 - 2H HL 45min LL

#focus()
dark_adaptation() #15min
measurement_loop(4) # total 2H, 15 min HL-15min dark en boucle

#activation
for i in range(5, 90): # 3x de suite 2H de haute lumière et entre chaque exposition regarder l'état des algues
    #focus()
    #activation_and_rest(activation_time_HL=2*60*60)#level_HL = 250, activation_time_HL=60*3) #2H45 - 2H HL 45min LL
    #focus()
    #dark_adaptation() #15min
    measurement_loop(4) #total 2H, 15 min HL-15min dark en boucle

