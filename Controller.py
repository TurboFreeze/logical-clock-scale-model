from Model import Model
from random import randint
import thread

class Controller():
    
    vms = [None, None, None]
    
    def __init__(self):
        # print "Controller init"
        # TODO threading?
        self.vms[0] = Model(randint(1,6), 0, self) # TODO get rid of spaghetti with sockets
        self.vms[1] = Model(randint(1,6), 1, self)
        self.vms[2] = Model(randint(1,6), 2, self)
        
        # thread 'em out
        thread.start_new_thread(self.vms[0].start, ())
        thread.start_new_thread(self.vms[1].start, ())
        thread.start_new_thread(self.vms[2].start, ())
    
    
    def handle_message(self, vm_index, msg):
        self.vms[vm_index].messages.append(msg) # TODO re-examine
    
    
