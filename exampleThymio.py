import dbus
import dbus.mainloop.glib
import gobject
from optparse import OptionParser
import os
 
proxSensorsVal=[0,0,0,0,0]


def clear():
    os.system(["clear","cls"][os.name == "nt"])

def saveLoop():
    #get the values of the sensors
    network.GetVariable("thymio-II", "prox.horizontal",reply_handler=get_variables_reply,error_handler=get_variables_error)
 
    #print the proximity sensors value in the terminal
    #print proxSensorsVal[0],proxSensorsVal[1],proxSensorsVal[2],proxSensorsVal[3],proxSensorsVal[4]
    print "lala"
    #Parameters of the Braitenberg, to give weight to each wheels

 
    return True
 
def get_variables_reply(r):
    global proxSensorsVal
    proxSensorsVal=r
 
def get_variables_error(e):
    print 'error:'
    print str(e)
    loop.quit()
 
if __name__ == '__main__':
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
    print network.GetNodesList()
 
    #GObject loop
    #print 'starting loop'
    #loop = gobject.MainLoop()
    #call the callback of Braitenberg algorithm
    #handle = gobject.timeout_add (100, saveLoop) #every 0.1 sec
    #loop.run()

    while True:
        test = 0
        clear()
        print network.GetVariable("thymio-II", "prox.horizontal")[0] 
        #print proxSensorsVal