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
    sock = _raspClient.initSocket('192.168.86.98')

    with picamera.PiCamera() as camera:
        camera.resolution = (500,500)
        camera.framerate = 60
        camera.hflip = True
        camera.vflip = True
        with picamera.array.PiRGBArray(camera) as stream:
            for i in camera.capture_continuous(stream, format="bgr", use_video_port = True):
            	print stream.array.shape
                _raspClient.sendImage(stream.array, sock)
                stream.truncate(0)