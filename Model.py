from datetime import datetime
from random import randint
from time import sleep

class Model():

    # Virtual machine characteristics: ticks per second, parent controller, virtual machine ID
    ticks = None
    parent = None
    vm_id = None

    def __init__(self, ticks, vm_id, controller):
        """
        Instantiate a virtual machine model
        :param ticks: Define cycle speed in Hz for the virtual machine instance (ticks per second generated randomly by controller)
        :param vm_id: Identify the virtual machine instance with unique ID (1, 2, 3)
        :param controller: Refernce to parent controller
        """
        print "model init", ticks
        # Set initialization values
        self.ticks = ticks
        self.vm_id = vm_id
        self.parent = controller
        # Calculate the ID for the two machines
        self.recipient_a = (self.vm_id + 1) % 3
        self.recipient_b = (self.vm_id + 2) % 3

    def start(self):
        """
        Internal initialization and setup of virtual machine
        Define message queue, logical clock, and log file
        """
        # Define the message queue, logical clock, and log file
        self.messages = []
        self.clock = 0
        filename = "log" + str(self.vm_id) + ".txt"
        self.log = open(filename, "w")
        # Call the primary run() method
        self.run()

    def pop_message(self):
        """
        Helper method for virtual machine to determine and handle messages in queue
        """
        if len(self.messages) != 0:
            # Get the message
            message = self.messages.pop(0)
            # Update local clock according to logical clock rules
            self.clock = max(self.clock + 1, int(message))
            # Create the entry in the log and write
            log_entry = "RECEIVE: " + "[message] " + message + "; [global] " + str(datetime.now()) + "; [queue length] " + str(len(self.messages)) + "; [logical clock time] " + str(self.clock) + "\n"
            self.log.write(log_entry)
        return None

    def run(self):
        """
        Virtual machine instance runs within this method when operational
        """
        # Keep looping when active
        while True:
            # Sleep for certain period according to clock speed
            sleep(1.0 / self.ticks)
            if len(self.messages) == 0:
                # For this cycle, when no messages are in queue, generate an action
                operation = randint(1, 10)
                # Depending on the operation generated, send a message, update the logical clock. and log the send
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
                    # Update clock, +0 since no relative action is taking place (no sending or receiving)
                    pass
            else:
                # For this cycle, process messages in the queue if the queue is not empty
                self.pop_message()

    def log_send(self, recipient):
        """
        Log the sending of a message
        :param recipient: The ID of the virtual machine that should receive the message
        """
        log_entry = "SEND: [global] " + str(datetime.now()) + "; [recipient] " + str(recipient) + "; [queue length] " + str(len(self.messages)) + "; [logical clock time] " + str(self.clock) + "\n"
        self.log.write(log_entry)
