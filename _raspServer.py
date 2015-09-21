# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 21:32:43 2015

@author: theMaxtrix
"""

#!/usr/bin/env python

import socket
import numpy as np
import cv2
from cPickle import loads
import matplotlib.pyplot as plt

def waitForImage(sock):
    BUFFER_SIZE = 1024 
    acc = ""
    while len(acc) < 3 or acc[-4:] != "\ntb.":
        data = sock.recv(BUFFER_SIZE)
        acc = acc + data
    #sock.close()
    return loads(acc)
    
def initSocket(IP = '0.0.0.0'):
    TCP_PORT = 51111
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, TCP_PORT))
    s.listen(1)
    sock, addr = s.accept()
    return sock

if __name__ == '__main__':

    sock = initSocket()
    while True:
        image = waitForImage(sock)
        print("left: %.3f, right: %.3f" % (np.mean(image.clip(0)),np.mean((-image).clip(0))))
        image = cv2.resize(image, (500,500))
        #image = np.hstack((image,-image))
        print image.shape
        cv2.imshow("outPut", image)
        cv2.waitKey(1)
        #plt.imshow(image)
        #plt.show()
        #print image
    sock.close()

    