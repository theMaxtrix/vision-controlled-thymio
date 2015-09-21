import dbus
import dbus.mainloop.glib
import gobject
from optparse import OptionParser
 
proxSensorsVal=[0,0,0,0,0]
network = 0

def init():
    global network
    network = __getGetThymioNetwork()

def setLeft(value):
    network.SetVariable("thymio-II", "motor.left.target", [value])

def setRight(value):
    network.SetVariable("thymio-II", "motor.right.target", [value])


def getProxSensors():
    return network.GetVariable("thymio-II", "prox.horizontal")
    # prox.horizontal[0] : front left
    # prox.horizontal[1] : front middle-left
    # prox.horizontal[2] : front middle
    # prox.horizontal[3] : front middle-right
    # prox.horizontal[4] : front right
    # prox.horizontal[5] : back left
    # prox.horizontal[6] : back right

def getMicSensors():
    return network.GetVariable("thymio-II", "mic.intensity")

def getGroundSensorA():
    # 0 - Left
    # 1 - Right 
    return network.GetVariable("thymio-II", "prox.ground.ambiant")

def getGroundSensorR():
    # 0 - Left
    # 1 - Right 
    return network.GetVariable("thymio-II", "prox.ground.reflected")

def __getGetThymioNetwork():
    parser = OptionParser()
    parser.add_option("-s", "--system", action="store_true", dest="system", default=False,help="use the system bus instead of the session bus")
 
    (options, args) = parser.parse_args()
 
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
 
    if options.system:
        bus = dbus.SystemBus()
    else:
        bus = dbus.SessionBus()
 
    #Create Aseba network 
    network = dbus.Interface(bus.get_object('ch.epfl.mobots.Aseba', '/'), dbus_interface='ch.epfl.mobots.AsebaNetwork')
 
    #print in the terminal the name of each Aseba NOde
    print "This is the node you are looking for: " + str(network.GetNodesList())

    return network


if __name__ == '__main__':

    init()
    
    while True:
        groundSensors = getGroundSensorR()
        if groundSensors[0] < 100 or groundSensors[1] < 100:
            setRight(0)
            setLeft(0)
        else:
            print getMicSensors()
            setRight(50)
            setLeft(50)
        #print getGroundSensorR() 
        #print getGroundSensorA() [0]
    #delayed = 1
    #delayedImg = "test"
    #camerSetup
