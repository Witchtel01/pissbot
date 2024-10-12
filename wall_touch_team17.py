#wall_stop.py
from basehat import UltrasonicSensor #import the sensor library
from buildhat import Motor #import the motor library
from basehat import Button
import time #import a way to wait

def main(): #define main function
    pin = 5 #define int 5 as pin
    print("Initiating BuildHAT and motors") #print this statement
    print("this may take a while (~10 seconds)") #print this statement
    motorL = Motor('A') #initialize motor l
    motorR = Motor('B') #init motor r

    ultra = UltrasonicSensor(pin) #init sensor
    button = Button(22) #init button

    pressed = 0
    while pressed < 2:
        buttonval = button.value
        if buttonval:
            pressed += 1
        time.sleep(.2)
    try: #error handling
        while True: #loop
            try: #error handling
                value = ultra.getDist #get value of sensor
                buttonval = button.value
                print(f"Sensor: {value} Motor A: {motorL.get_position()}  B: {motorR.get_position()} ") #print values of motors and sensor
                if buttonval: #if button is pressed
                    print("Stopped") #print that
                    motorL.stop() #stop motor l
                    motorR.stop() #stop motor r
                else: #otherwise
                    if (value != None and value < 10): #if distance not none or less than 10cm
                        motorR.start(-30) #r moto fwd
                        motorL.start(30) #l moto fwd
                        while (value != None and value < 15): #val < 15
                            value = ultra.getDist
                        motorR.run_for_degrees(-180)
                        motorL.run_for_degrees(-180)
                    motorR.start(30) #start motor r with speed 30
                    motorL.start(-30) #start motor l with speed -30
                time.sleep(.2) #wait

            except IOError: #error handlnig
                print ("\nError occurred while attempting to read values.") #print error
                motorL.stop() #stop motor l
                motorR.stop() #stop motor r
                break #quit loop

    except KeyboardInterrupt: #error handling by ctrl+c
        print("\nCtrl+C detected. Exiting...") #print that
        motorL.stop() #stop l motor
        motorR.stop() #stop r motor

if __name__ == '__main__': #ifmain
    main() #run main function
    motorL = Motor('A') #setup l motor
    motorR = Motor('B') #setup r motor
    motorL.stop() #stop l motor
    motorR.stop() #stop r motor