#touch_motors                        ''

import time     # import the time library for the sleep function
from basehat import Button
from buildhat import Motor

motorA = Motor('A')
motorB = Motor('B')
motorC = Motor('C')
# motorD = Motor('D')

port = 22
button = Button(port)

try:
    print("Press button on port 22 to run motors")
    
    speed = 0
    adder = 1
    while True:

        
        value = button.value
        
        if value:                             # if the button is pressed
            if speed <= -100 or speed >= 100: # if speed reached 100, start ramping down. If speed reached -100, start ramping up.
                adder = -adder
            speed += adder
        else:                                 # else the buton is not pressed or not configured, so set the speed to 0
            speed = 0
            adder = 1
        
        # Set the motor speed for all four motors
        motorA.start(speed)
        motorB.start(speed)
        motorC.start(speed)
        # motorD.start(speed)
        
        try:
            # Each of the following BP.get_motor_encoder functions returns the encoder value (what we want to display).
            print("Encoder A: %6d, Encoder B: %6d, Encoder C: %6d" % (motorA.get_position(), motorB.get_position(), motorC.get_position()))
			# print("Encoder A: %6d, Encoder B: %6d, Encoder C: %6d, Encoder D: %6d" % (motorA.get_position(), motorB.get_position(), motorC.get_position(), motorD.get_position()))
        except IOError as error:
            print(error)
        
        time.sleep(0.02)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        motorA.stop()
        motorB.stop()
        motorC.stop()
        # motorD.stop()     