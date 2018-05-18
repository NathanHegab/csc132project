# csc132project
# Names: Nathan Hegab, Dawson Markham, Nicole Robles
# Date:  5 May, 2018
# Client Description: 
Program sends information to the server Rpi and creates a GUI to decide what infromation is sent. The GUI created has two display numbers which are
controlled by individual plus and subtract buttons. There are two other buttons that send information to the server which consist of a key, color and
number. This information is sent as a string.

# Server Description:
Program creates server in order to communicate with another system wirelessly.
A string is received from the client, and is then converted into an instance
of an Instruction, which is ultimately used in checking the values given and
in controlling the appropriate GPIO pins which are used in opening solenoid
valves.
