import thymio
import emd 
import io
import time 
import picamera
import picamera.array 
import numpy as np
import scipy.misc
import os
import _raspClient


if __name__ == '__main__':
    network = thymio.getGetThymioNetwork()
    #sock = _raspClient.initSocket('192.168.86.98')

    with picamera.PiCamera() as camera:
        camera.resolution = (50,50)
        camera.framerate = 60
        camera.hflip = True
        camera.vflip = True
        with picamera.array.PiYUVArray(camera) as stream:
            camera.capture(stream, format="yuv")
            delayed = emd.getReceptiveFields(stream.array, nOCellsX = 50, nOCellsY = 50)
            stream.truncate(0)
            for i in camera.capture_continuous(stream, format="yuv", use_video_port = True):
                current = emd.getReceptiveFields(stream.array, nOCellsX = 50, nOCellsY = 50)
                motionX = emd.getMotionX(delayed, current)
                delayed = current
                
                emd.clear()
                movementLeft = (-motionX[0:motionX.shape[0],0:motionX.shape[1]/2]).clip(min = 0)
                movementRight = motionX[0:motionX.shape[0],motionX.shape[1]/2:motionX.shape[1]].clip(min = 0)

                meanLeft = np.mean(movementLeft)
                meanRight = np.mean(movementRight)
                speed = 5000

                emd.clear()
                print("left: %.3f, right: %.3f" % (meanLeft,meanRight))

                #print motionX
                network.SetVariable("thymio-II", "motor.left.target", [speed*meanLeft])
                network.SetVariable("thymio-II", "motor.right.target", [speed*meanRight])

                # network.SetVariable("thymio-II", "motor.left.target", [0])
                # network.SetVariable("thymio-II", "motor.right.target", [0])

                #_raspClient.sendImage(np.hstack((movementLeft,movementRight)), sock)
                stream.truncate(0)
