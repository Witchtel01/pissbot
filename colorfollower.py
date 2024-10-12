from buildhat import ColorSensor, MotorPair
from basehat.Button import Button
import time

driveTrain = MotorPair('A', 'B')

cs = ColorSensor('C')
but = Button(24)
lightLeftPort = 0
lightRightPort = 2

def follow_line():
    but.wait_for_inactive()
    driveTrain.start(-15,15)
    while not but.value:
        if cs.get_color() != 'black':
            driveTrain.stop()
            time.sleep(.25)
            turnAmount = 0.05
            while cs.get_color() != 'black':
                driveTrain.run_for_rotations(turnAmount,10,10)
                turnAmount *= -2
                time.sleep(.1)
            driveTrain.start(-15,15)
    driveTrain.stop()

print('ready')
but.wait_for_active()
follow_line()
