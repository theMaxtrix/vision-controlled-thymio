# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 21:42:17 2015

@author: theMaxtrix
"""


import socket

import numpy as np
from cPickle import dumps

def initSocket(IP = '192.168.86.98'):
    TCP_PORT = 51111 #5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, TCP_PORT))
    return sock

def sendImage(image, sock):
    converted = dumps(image)
    sock.send(converted)
    
if __name__ == '__main__':
    sock = initSocket()
    theImage =  np.ones((5,5))
    theImage[3,3] = 255
    sendImage(theImage, sock)
