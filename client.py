##############################################################################################
# Names: Nathan Hegab, Dawson Markham, Nicole Robles
# Date:  5 May, 2018
# Description: Program sends information to the server Rpi and creates a GUI to decide what
#               infromation is sent. The GUI created has two display numbers which are
#               controlled by individual plus and subtract buttons. There are two other 
#               buttons that send information to the server which consist of a key, color and
#               number. This information is sent as a string.
#############################################################################################

#libraries
import socket
from Tkinter import *

class Instructions(object):
    #constructor
    def __init__(self, index, color, number):
        self.color = color
        self.number = number
        self.index = index
        self.key = self.createKey()

    #when calling keys call from the list KEYS
    def createKey(self, KEYS = KEYS):
        return KEYS[self.index % 6]

    #turns everything sent to the server into a string
    def string(self):
        instructions = "{}:{}:{}".format(self.key, self.color, self.number)
        return instructions

# the main GUI
class MainGUI(Frame):
    #constructor
    def __init__(self, parent):
        Frame.__init__(self, parent, bg="white")
        parent.attributes("-fullscreen", True)
        self.setupGUI()
        self.Guibuttonsend = False
        self.index = 0


    #sets up the GUI
    def setupGUI(self):
        #sets counter to 0 for drops
        self.counter_red = 0
        self.counter_blue = 0

        #the number for the counter of red drops
        self.display_red = Label(self, text= self.counter_red, bg="red", height=1, width=15, font=("TexGyreAdventor", 45))
        self.display_red.grid(row=3, column=2, columnspan=1, sticky=E+W+N+S)

        #the number for the counter of blue drops
        self.display_blue = Label(self, text= self.counter_blue, bg="blue", height=1, width=15, font=("TexGyreAdventor", 45))
        self.display_blue.grid(row=3, column=5, columnspan=1, sticky=E+W+N+S)

        # configure the rows and columns of the Frame to adjust to
        # the window
        # there are 7 rows (0 through 6)
        for row in range(7):
            Grid.rowconfigure(self, row, weight=1)
        # there are 6 columns (0 through 5)
        for col in range(6):
            Grid.columnconfigure(self, col, weight=1)


        #send red button 
        img = PhotoImage(file="redsendbutton.png")
        button = Button(self, bg="white", image=img, borderwidth=0, highlightthickness=0, activebackground="white", command = lambda:self.process("sendred"))
        button.image = img
        button.grid(row=6, column=2, sticky=N+S+E+W)

        #send blue button
        img = PhotoImage(file="bluesendbutton.png")
        button = Button(self, bg="white", image=img, borderwidth=0, highlightthickness=0, activebackground="white", command = lambda:self.process("sendblue"))
        button.image = img
        button.grid(row=6, column=5, sticky=N+S+E+W)

        #+ for red button
        img = PhotoImage(file="add.png")
        button = Button(self, bg="white", image=img, borderwidth=0, highlightthickness=0, activebackground="white", command = lambda:self.process("red+"))
        button.image = img
        button.grid(row=0, column=2, sticky=N+S+E+W)

        #- for red button
        img = PhotoImage(file="sub.png")
        button = Button(self, bg="white", image=img, borderwidth=0, highlightthickness=0, activebackground="white", command = lambda:self.process("red-"))
        button.image = img
        button.grid(row=4, column=2, sticky=N+S+E+W)

        #+ for blue button
        img = PhotoImage(file="add.png")
        button = Button(self, bg="white", image=img, borderwidth=0, highlightthickness=0, activebackground="white", command = lambda:self.process("blue+"))
        button.image = img
        button.grid(row=0, column=5, sticky=N+S+E+W)

        #- for blue button
        img = PhotoImage(file="sub.png")
        button = Button(self, bg="white", image=img, borderwidth=0, highlightthickness=0, activebackground="white", command = lambda:self.process("blue-"))
        button.image = img
        button.grid(row=4, column=5, sticky=N+S+E+W)

        self.pack(fill=BOTH, expand=1)

    #processes the pushing of buttons
    def process(self, button):
        #controls the send red button funtions
        if (button == "sendred"):
            dropcount = self.display_red["text"]
            #sends information to the server
            sendInstructions = Instructions(self.index, "red", dropcount)
            s.send(sendInstructions.string(), socket.MSG_DONTWAIT)
            #going up one through the list of keys
            self.index += 1

        #controls the send blue button funtions
        elif (button == "sendblue"):
            dropcount = self.display_blue["text"]
            #sends the information to the server
            sendInstructions = Instructions(self.index, "blue", dropcount)
            s.send(sendInstructions.string(), socket.MSG_DONTWAIT)
            #going up one through the list of keys
            self.index += 1

        #controls the red plus button
        elif (button == "red+"):
            #checking to keep the drops below 4
            if (self.display_red["text"] < 3):
                 self.display_red["text"] += 1

        #controls the red minus button
        elif (button == "red-"):
            #checking to keep the drops above 0
            if (self.display_red["text"] > 0):
                self.display_red["text"] -= 1

        #controls the blue plus button
        elif (button == "blue+"):
            #checking to keep the drops below 4
            if (self.display_blue["text"] < 3):
                self.display_blue["text"] += 1

        #controls the blue minus button
        elif (button == "blue-"):
            #checking to keep the drops above 0
            if (self.display_blue["text"] > 0):
                self.display_blue["text"] -= 1

########
#MAIN
########

#establishing what pi to talk to
#if running on local machine change nothing
#if running on network change localhost to server pi's ip address
IP = "localhost"
PORT = 3863

#connectting to the server pi
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))

#the keys used to send to server
KEYS = ["123456", "123456789", "qwerty", "12345678", "111111", "passsword"]           

# create the window
window = Tk()

# set the window title
window.title("Cyber Storm Challenge")

# generate the GUI
gui = MainGUI(window)

# display the GUI and wait for user interaction
window.mainloop()






