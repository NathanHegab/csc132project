##############################################################################################
# Names: Nathan Hegab, Dawson Markham, Nicole Robles
# Date:  5 May, 2018
# Description: Program creates server in order to communicate with another system wirelessly.
#               A string is received from the client, and is then converted into an instance
#               of an Instruction, which is ultimately used in checking the values given and
#               in controlling the appropriate GPIO pins which are used in opening solenoid
#               valves.
#############################################################################################

# import libraries
import RPi.GPIO as GPIO
import sys
import socket
from time import sleep

# Instruction class
class Instructions(object):
        # instance has a key, color, and number
        def __init__(self, key, color, number):
                self.key = key
                self.color = color
                # convert number into an integer
                self.number = int(number)
     
        # accessors and mutators
        @property
        def key(self):
                return self._key

        @key.setter
        def key(self, string):
                self._key = string

        @property
        def color(self):
                return self._color

        @color.setter
        def color(self, string):
                self._color = string

        @property
        def number(self):
                return self._number

        @number.setter
        def number(self, value):
                # if value is outside the range [0,3], set the number to 0
                if (value <= 0 or value > 3):
                        self._number = 0

                # else, set the number to the specified value
                else:
                        self._number = value

        # define function that checks the key
        def checkKey(self):
                # if the key is equal to the correct key, return True
                if (self.key == KEYS[index % 6]):
                        return True

                # else, return False
                else:
                        return False
             
        #  define function that determines the GPIO pin needed               
        def findGPIO(self):
                # if color is blue, return variable blue
                if (self.color == "blue"):
                        return blue

                # else if color is red, return variable red
                elif (self.color == "red"):
                        return red
             
        def solControl(self):
                GPIO.output(self.findGPIO(), True)
                sleep(0.1)
                GPIO.output(self.findGPIO(), False)
                sleep(0.5)
             
########
# MAIN #
########

# server setup
# define port that will be used
PORT = 3863

# use socket library to create a socket for the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to PORT to create server
s.bind(("", PORT))
# the server has a maximum of one connection
s.listen(0)

# GPIO setup
GPIO.setmode(GPIO.BCM)
# define variables red and blue to be used with GPIO
blue  = 17
red   = 18
# set the GPIO pins to be output
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)

# define variable to be used in finding an item in a list
index = 0

# define a list
KEYS = ["123456", "123456789", "qwerty", "12345678", "111111", "password"]                               

# use try/except block to prevent the program from stopping due to error without properly closing the GPO and server                         
try:
        # loop that continues forever unless there is external intervention
        while (True):
                # allow server to accept a connection
                c, addr = s.accept()
                #c.settimeout(5.0)

                # receive data from client
                data = c.recv(4096)

                # data has been received run through the instructions given
                while (len(data) != 0):
                        # split data into a list of strings
                        action = data.split(':')

                        # if the list has a length of three, continue instructions
                        if (len(action)==3):
                                # create an instance of an Instruction
                                inst = Instructions(action[0], action[1], action[2])
                             
                                # if valid key is given, continue with the instructions
                                if (inst.checkKey()):
                                        # increment the index by one
                                        index += 1

                                        # if a valid color is given, control the solenoid as directed
                                        if (inst.color == "blue" or inst.color() == "red"):
                                                # use a 'for' loop to open the solenoid the directed number of times (modulus of 4 used to limit the loop to three cycles
                                                for i in range(0, inst.number % 4):
                                                        # run the solControl function
                                                        inst.solControl()
     
                        # output the received data
                        sys.stdout.write(data)
                        # display the output
                        sys.stdout.flush()
                        print ""

                        # receive data from client
                        data = c.recv(4096)
                     
# except block
except:
        # properly close the GPIO pins
        GPIO.cleanup()
        # properly close the server
        s.shutdown(socket.SHUT_RDWR)
        s.close()


