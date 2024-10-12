# Import for pi:
# from basehat import Button, LightSensor

import threading
import time

# Import for laptop pylint:
from basehat.Button import Button
from basehat.LightSensor import LightSensor
from buildhat import MotorPair

# constants
FPS = 10
PERCENTAGE_THRESHOLD = 25/100
CHECK_LENGTH = 3

driveTrain = MotorPair('A','B')

l = LightSensor(0)
r = LightSensor(2)

but = Button(24)
# When we have a second button, use to quit the program:
# but.when_activated = quit



# Because run for is blocking 💀💀💀
def asyncTurn(rotations: float, speedL: int, speedR: int):
    turnThread = threading.Thread(
        target=driveTrain.run_for_rotations,
        args=(rotations, speedL, speedR)
    )
    turnThread.start()
    

def main() -> None:
    # Bruh I need it here too wth??
    global listL, listR
    
    # wait until unpresses button
    but.wait_for_inactive()
    
    # set to quit on button pressed again
    but.when_activated = quit
    
    # setup light values
    listL = [l.light for _ in range(CHECK_LENGTH)]
    listR = [r.light for _ in range(CHECK_LENGTH)]
    
    def updateLight():
        # idk why i need this, but it has something to do with
        # variable scope. Don't change!
        global listL
        global listR
        
        # propogate light values back 1
        listL.pop(0)
        listL.append(l.light)
        listR.pop(0)
        listR.append(r.light)
    
    # Game tick() method for equal distancing between "frames"
    def tick(now : float) -> None:
        if time.time_ns() - now < 1/FPS:
            time.sleep(1/FPS - (time.time_ns() - now))
    
    frame = 0
    updateSpacing = 3
    driveTrain.start(-15,15)

    while True:
        # Setup timings every loop
        now = time.time_ns()
        
        if frame % updateSpacing == 0:
            updateLight()
            
            # if value from 2 readings ago compared to current
            # difference greater than 25% of 2 readings ago, then
            # it is on the line now
            if abs(listL[0] - listL[len(listL) - 1]) >\
                listL[0] * PERCENTAGE_THRESHOLD:
                
                # stop robot in place, wait for a moment to settle
                driveTrain.stop()
                time.sleep(0.1)
                
                subFrame = 0
                subUpdateSpacing = 3
                
                # 0.1 because 0 causes an error
                driveTrain.start(0.1, 10)
                
                # while no change is detected, just wait
                while not abs(listL[0] - listL[len(listL) - 1]) >\
                    listL[0] * PERCENTAGE_THRESHOLD:
                
                    subNow = time.time_ns()
                    if subFrame % subUpdateSpacing == 0:
                        updateLight()
                    tick(subNow)
                    subFrame += 1
                    
                
                # after change has been detected, stop and restart
                # going forwards
                driveTrain.stop()
                time.sleep(0.1)
                driveTrain.start(-15, 15)
                
            
            # same as above except other side (aka i'm too lazy to
            # write the comments twice)
            if abs(listR[0] - listR[len(listR) - 1]) >\
                listR[0] * PERCENTAGE_THRESHOLD:
                
                driveTrain.stop()
                time.sleep(0.1)
                subFrame = 0
                subUpdateSpacing = 3
                driveTrain.start(-0.1, -10)
                while not abs(listR[0] - listR[len(listR) - 1]) >\
                    listR[0] * PERCENTAGE_THRESHOLD:
                
                    if subFrame % subUpdateSpacing == 0:
                        updateLight()
                    tick(now)
                    subFrame += 1
                driveTrain.stop()
                driveTrain.start(-15, 15)
        
        # Keep equal distance between checks as not to check
        # brightness too quickly (we need the 3rd value a good
        # bit of space prior to the 1st value)
        tick(now)
        frame += 1


if __name__ == "__main__":
    but.wait_for_active()
    main()