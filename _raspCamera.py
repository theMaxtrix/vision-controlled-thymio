import picamera
import picamera.array 

def initCam():
	with picamera.PiCamera() as camera:
    	camera.resolution = (50,50)
    	camera.framerate = 60
    	with picamera.array.PiYUVArray(camera) as stream:
        camera.capture(stream, format="yuv")
	return
def captureImage():
	return
def closeCamera():
	return
#make ready
#get image
#close