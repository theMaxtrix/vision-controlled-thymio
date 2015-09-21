import io
import time 
import picamera
import picamera.array 
import numpy as np
import scipy.misc
import os
import _raspClient
#import matplotlib.pyplot as plt 

def clear():
    os.system(["clear","cls"][os.name == "nt"])
#clear = lambda: os.system("cls")
#import cProfile

def grayScale(image):
    rs = 0.299 
    gs = 0.587
    bs = 0.114
    return np.sum(image * np.array((bs,gs,rs)), axis = 2)

def getReceptiveFields(image, nOCellsX = 20, nOCellsY = 20): #REPLACE WITH LAYOUT FROM GREENBRAIN
    #imgGray = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY) #Check in which order to do this
    #imgGray = grayScale(image)
    imgRS = scipy.misc.imresize(image[:,:,0], (nOCellsX,nOCellsY), interp='bilinear')
    #imgRS = cv2.resize(imgGray, (nOCellsY,nOCellsX))
    return imgRS.astype(np.float)/255

def getMotionY(delayed, current):
    positiveMovement = current[1:,:-1]* delayed[:-1,:-1] #down  
    negativeMovement = current[:-1,:-1]* delayed[1:,:-1] #up 
    motionPicture = positiveMovement-negativeMovement
    return motionPicture
    
def getMotionX(delayed, current):
    positiveMovement = current[:-1, 1:]* delayed[:-1,:-1] #right
    negativeMovement = current[:-1, :-1]* delayed[:-1,1:] #left
    motionPicture = positiveMovement-negativeMovement
    return motionPicture

if __name__ == '__main__':
    sock = _raspClient.initSocket('192.168.86.98')

    with picamera.PiCamera() as camera:
        camera.resolution = (50,50)
        camera.framerate = 60
        with picamera.array.PiYUVArray(camera) as stream:
            camera.capture(stream, format="yuv")
            delayed = getReceptiveFields(stream.array, nOCellsX = 50, nOCellsY = 50)
            stream.truncate(0)
            for i in camera.capture_continuous(stream, format="yuv", use_video_port = True):
                current = getReceptiveFields(stream.array, nOCellsX = 50, nOCellsY = 50)
                motionX = getMotionX(delayed, current)
                delayed = current
                clear()
                print motionX
                _raspClient.sendImage(motionX, sock)
                #print str(np.sum(motionX)[0:5]
                #plt.imshow(motionX)
                #print  stream.array[0,0,0]
                stream.truncate(0)

            #camera.capture(stream, format ="bgr")

    #    time.sleep(2)
    #    camera.capture(stream, format ="jpep")
    #    camera.stop_preview()
    #data = np.fromstring(stream.getvalue(), dtype=np.uint8)
    #print str(data.shape)
    print "alles gut"
