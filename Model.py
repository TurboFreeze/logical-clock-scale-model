from datetime import datetime
from random import randint
from time import sleep

class Model():
    
    
    ticks = None
    parent = None
    vm_id = None
    
    def __init__(self, ticks, vm_id, controller):
        print "model init", ticks
        self.ticks = ticks
        self.vm_id = vm_id
        self.parent = controller
        self.recipient_a = (self.vm_id + 1) % 3
        self.recipient_b = (self.vm_id + 2) % 3
        
    def start(self):
        self.messages = []
        self.clock = 0
        filename = "log" + str(self.vm_id) + ".txt"
        self.log = open(filename, "w")
        self.run()
    
    def pop_message(self):
        if len(self.messages) != 0:
            message = self.messages.pop(0)
            # Update local clock according to logical rules
            self.clock = max(self.clock + 1, int(message))
            # Create the entry
            log_entry = "RECEIVE: " + "[message] " + message + "; [global] " + str(datetime.now()) + "; [queue length] " + str(len(self.messages)) + "; [logical clock time] " + str(self.clock) + "\n"
            self.log.write(log_entry)
        return None
        
    def run(self):
        while True:
            sleep(1.0 / self.ticks)
            if len(self.messages) == 0:
                operation = randint(1, 10)
                if operation == 1:
                    # Send message to next machine
                    self.parent.handle_message(self.recipient_a, str(self.clock))
                    self.clock += 1
                    self.log_send(self.recipient_a)
                elif operation == 2:
                    # Send message to previous machine (+2 is same as -1 intuitively)
                    self.parent.handle_message(self.recipient_b, str(self.clock))
                    self.clock += 1
                    self.log_send(self.recipient_b)
                elif operation == 3:
                    # Send message to both users
                    self.parent.handle_message(self.recipient_a, str(self.clock))
                    self.parent.handle_message(self.recipient_b, str(self.clock))
                    self.clock += 1
                    self.log_send(self.recipient_a)
                    self.log_send(self.recipient_b)
                else:
                    # Internal event
                    # Update clock, +0?
                    pass
            else:
                self.pop_message()
                
    def log_send(self, recipient):
        log_entry = "SEND: [global] " + str(datetime.now()) + "; [queue length] " + str(len(self.messages)) + "; [logical clock time] " + str(self.clock) + "\n"
        self.log.write(log_entry)
