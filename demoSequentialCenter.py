#asebamedulla "ser:device=/dev/ttyACM0" & python vision-controlled-thymio/demoCenter.py 
import thymio
import emd 
import io
from time import clock
from time import sleep
import picamera
import picamera.array 
import numpy as np
import scipy.misc
import os
import _raspClient
import _div 

if __name__ == '__main__':
    thymio.init()
    #sock = _raspClient.initSocket('192.168.86.98')
    speed = 100
    #timeMeasure = 0.01
    #timeTurn = 0.01
    with picamera.PiCamera() as camera:
        camera.resolution = (50,50)
        camera.framerate = 60
        camera.hflip = True
        camera.vflip = True
        with picamera.array.PiYUVArray(camera) as stream:
            camera.capture(stream, format="yuv")
            stream.truncate(0)
            while True:
                
                #_div.clear()

                #FW PHASE

                thymio.setBothSaveWaitUntilReadyAndReturnTime(speed, speed)
                t0 = clock()
                # while thymio.getLeft() != speed or thymio.getRight() != speed:
                #     print thymio.getLeft()
                #     print thymio.getRight()
                camera.capture(stream, format="yuv", use_video_port = True)
                image1 = emd.getReceptiveFields(stream.array, nOCellsX = 50, nOCellsY = 50)
                stream.truncate(0)

                #sleep(timeMeasure)

                camera.capture(stream, format="yuv", use_video_port = True)
                image2 = emd.getReceptiveFields(stream.array, nOCellsX = 50, nOCellsY = 50)
                stream.truncate(0)

                motionX = emd.getMotionX(image1, image2)

                #TURN PHASE
          
                emdsLeft = (-motionX[0:motionX.shape[0],0:motionX.shape[1]/2]).clip(min = 0)
                emdsRight = motionX[0:motionX.shape[0],motionX.shape[1]/2:motionX.shape[1]].clip(min = 0)

                meanLeft = np.mean(emdsLeft)
                meanRight = np.mean(emdsRight)

                adjustmentProportionLeft = meanLeft/(meanLeft+meanRight)
                adjustmentProportionRight = meanRight/(meanLeft+meanRight)

                t1 = clock()

                thymio.setBothSaveWaitUntilReadyAndReturnTime(speed * adjustmentProportionLeft * 2, speed * adjustmentProportionRight * 2)

                sleep(t1 -t0)
                
                _div.clear()

                print (t1-t0)

                


                #sleep(timeTurn)

                # groundSensors = thymio.getGroundSensorR()
                # if groundSensors[0] < 100 or groundSensors[1] < 100:
                #     print("Warning Thymio is about to fall from the table")
                #     thymio.setRight(0)
                #     thymio.setLeft(0)
                # else:
                #     print("left: %.3f, right: %.3f" % (meanMovementLeft,meanMovementRight))
                #     wantedAdjustmentProportionLeft = meanLeft/(meanLeft+meanRight)
                #     wantedAdjustmentProportionRight = meanRight/(meanLeft+meanRight)

                # print "end"
                # break

                #     currentSpeedLeft = thymio.getLeft()
                #     currentSpeedRight = thymio.getRight()
                #     currentSpeedSum = currentSpeedLeft + currentSpeedRight

                #     if(currentSpeedSum != 0):
                #         lastAdjustmentProportionLeft = currentSpeedLeft/currentSpeedSum
                #         lastAdjustmentProportionRight = currentSpeedRight/currentSpeedSum
                #     else:
                #         lastAdjustmentProportionLeft = 0.5
                #         lastAdjustmentProportionRight = 0.5

                #     # actualAdjustmentProportionLeft = (wantedAdjustmentProportionLeft + lastAdjustmentProportionLeft) / 2
                #     # actualAdjustmentProportionRight = (wantedAdjustmentProportionRight + lastAdjustmentProportionRight) / 2

                #     actualAdjustmentProportionLeft = 0.5 + wantedAdjustmentProportionLeft - lastAdjustmentProportionLeft 
                #     actualAdjustmentProportionRight = 0.5 + wantedAdjustmentProportionRight - lastAdjustmentProportionRight 

                #     # leftSpeed = baseSpeed + (turnSpeed * (meanLeft/(meanLeft+meanRight)))**1.5
                #     # rightSpeed = baseSpeed + (turnSpeed * (meanRight/(meanLeft+meanRight)))**1.5

                #     # thymio.setLeft(leftSpeed)
                #     # thymio.setRight(rightSpeed)
                #     thymio.setLeft(baseSpeed * actualAdjustmentProportionLeft * 2)
                #     thymio.setRight(baseSpeed * actualAdjustmentProportionRight * 2)

                # #print motionX
                # #network.SetVariable("thymio-II", "motor.left.target", [speed*meanLeft])
                # #network.SetVariable("thymio-II", "motor.right.target", [speed*meanRight])

                # # network.SetVariable("thymio-II", "motor.left.target", [0])
                # # network.SetVariable("thymio-II", "motor.right.target", [0])

                # #_raspClient.sendImage(np.hstack((movementLeft,movementRight)), sock)
                # stream.truncate(0)

