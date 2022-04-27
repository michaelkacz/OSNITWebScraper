#import * from tkinter to develop GUI
from cgitb import text
from tkinter import *
from xml.sax.xmlreader import InputSource
import twint
import pandas as pd
#To install twint:
    #pip3 install twint
    #pip3 install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint
    #pip install aiohttp==3.7.0

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

#Facebook button
redditbutton = Button(buttonframe, text="Reddit", padx=60, pady=40, bg="#F28C28")
redditbutton.grid()

#onclick to web scrape twitter
def twittercrawlclick():
    #generate label
    twitterlabel = Label(winD, text="Please enter topic:")
    twitterlabel.pack()
    #generate entry
    twitterentry = Entry(winD)
    twitterentry.pack()

    def topiccrawl():
        #get string from entry in previous function
        twitterstring = twitterentry.get()
        twitterscrape = twint.Config()
        twitterscrape.Search = [twitterstring]
        twitterscrape.Limit = 500
        twitterscrape.Store_csv = True
        #output to topic with csv file extension
        twitterscrape.Output = twitterstring + ".csv"

        #runs search on specified topic
        twint.run.Search(twitterscrape)
        df = pd.read_csv(twitterstring + '.csv')

    #frame to house enter button
    twitterframe = LabelFrame(winD, padx=5, pady=5)
    twitterframe.pack(padx=10, pady=10)

    #scrape twitter topic button
    topicbutton = Button(twitterframe, text="Scrape Topic", padx=50, command=topiccrawl)
    topicbutton.grid()

#Twitter button
twitterbutton = Button(buttonframe, text="Twitter", padx=60, pady=40, bg="blue", command=twittercrawlclick)
twitterbutton.grid()

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
