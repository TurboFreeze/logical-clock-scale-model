from Model import Model
from random import randint
import thread

class Controller():

    vms = [None, None, None]

    def __init__(self):
        """
        Initialization of controller for scale model
        """
        print "Controller init"

        speed_range = 6
        # Initializing the virtual machines
        self.vms[0] = Model(randint(1, speed_range), 0, self)
        self.vms[1] = Model(randint(1, speed_range), 1, self)
        self.vms[2] = Model(randint(1, speed_range), 2, self)

        # thread 'em out
        thread.start_new_thread(self.vms[0].start, ())
        thread.start_new_thread(self.vms[1].start, ())
        thread.start_new_thread(self.vms[2].start, ())


    def handle_message(self, vm_index, msg):
        """
        Pass message on to appropriate receiving machine
        :param vm_index: ID of receiving machine
        :param msg: Message being sent
        """
        self.vms[vm_index].messages.append(msg)
