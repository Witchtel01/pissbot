import time

import buildhat
from basehat.Button import Button
from basehat.LineFinder import LineFinder
from buildhat import MotorPair

driveTrain = MotorPair('A','B')

finderLeft = LineFinder(5)
finderRight = LineFinder(22)

but = Button(24)


def main():
    # Remember to set A in negative direction!
    
    driveTrain.start(-25,25)
    while not but.value:
        if finderLeft.value:
            # Turn Right
            driveTrain.stop()
            time.sleep(.25)
            driveTrain.start(25,25)
            while finderLeft.value:
                pass
            driveTrain.stop()
            time.sleep(.25)
            driveTrain.start(-25,25)
        if finderRight.value:
            # Turn Left
            driveTrain.stop()
            time.sleep(.25)
            driveTrain.start(-25,-25)
            while finderRight.value:
                pass
            driveTrain.stop()
            time.sleep(.25)
            driveTrain.start(-25,25)
        time.sleep(0.1)
    driveTrain.stop()