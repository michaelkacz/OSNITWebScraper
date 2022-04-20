#import * from tkinter to develop GUI
from cgitb import text
from tkinter import *
from xml.sax.xmlreader import InputSource

#create a window for GUI
#instantiate an instance of WinD
winD = Tk();
#change the size of winD, using geometry function
winD.geometry("1280x768");
#create title for window frame, WinD
winD.title("OSINT Project");
#change background of window frame
winD.config(background="#8c1414");

#create frame to house buttons
buttonframe = LabelFrame(winD, padx=5, pady=5)
buttonframe.pack(padx=10, pady=10)

#create buttons for GUI
#Twitter button
twitterbutton = Button(buttonframe, text="Twitter", padx=60, pady=40, bg="blue")
twitterbutton.grid()
#Facebook button
facebookbutton = Button(buttonframe, text="Facebook", padx=60, pady=40, bg="#6495ED")
facebookbutton.grid()

#onclick function to open input 
def webcrawlclick():
    crawllabel = Label(winD, text="Please enter web address:")
    crawllabel.pack()
    linkinput = Entry(winD)
    linkinput.pack()

#web crawl button
webcrawlbutton = Button(buttonframe, text="Web Crawler", padx=60, pady=40, bg="black", fg="white", command=webcrawlclick)
webcrawlbutton.grid()

#back/exit button
backbutton = Button(buttonframe, text="Back", padx=50)
exitbutton = Button(buttonframe, text="Exit", padx=50)
#add buttons to grid
backbutton.grid(row=3, column=0)
exitbutton.grid(row=3, column=1)

#display window frame on screen
winD.mainloop();
