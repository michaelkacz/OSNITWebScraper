#import * from tkinter to develop GUI
from cgitb import text
from tkinter import *
from xml.sax.xmlreader import InputSource
import twint
import pandas as pd
import requests
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

def RedditCrawlClick():
    #generate label
    redditlabel = Label(winD, text="Enter your favorite subreddit:")
    redditlabel.pack()
    #generate entry
    redditentry = Entry(winD)
    redditentry.pack()

    def RedditStart():
        subredditResult = redditentry.get()
        #Reddit API, Secrets Keys for David Singer (hard coded them so it works for us all)
        CLIENT_ID = 'Z67JznUGNKehngQw6zsxxg'
        SECRETS_KEY = 'CNIwnX7gon7lqWYSVsorJZupN-rt1A'

        auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRETS_KEY)

        #need to log in to reddit account that has access. - normally we'd hide this in a .gitignore file and pull it locally, but who cares for this accnt.
        data = {
            'grant_type': 'password',
            'username': 'MaintenanceNeither16',
            'password': 'OSINTProject'
        }

        #basically naming this api and the version of the "app"
        headers = {'User-Agent': 'MyApi/0.0.1'}

        #send request for auth token
        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=headers)
        TOKEN = res.json()['access_token']
        print(TOKEN)

        #this token is something we have to add to the header whenever we use the api (ps: ** doesnt really do anything)
        headers = {**headers, **{'Authorization': f'bearer {TOKEN}'}}
        print(headers)

        #now we can make requests: this checks to see if we get a return of "200", meaning everything is okay - now add .json and we get a ton of info
        #this is NOT needed, just a test
        #requests.get('https://outh.reddit.com/api/v1/me', headers=headers)

        #lets grab subredit, replace hot with new to get new posts, add params to set parameters: params={'limit': '49'} = 50 posts
        res = requests.get(f'https://oauth.reddit.com/r/{subredditResult}/hot', headers=headers, params={'limit': '49'})
        res.json()

        #make empty data frame
        dfReddit = pd.DataFrame()

        #loop posts
        for post in res.json()['data']['children']:
            dfReddit = dfReddit.append({
                        'subreddit': post['data']['subreddit'],
                        'title':  post['data']['title'],
                        'selftext': post['data']['selftext'],
                        'upvote_ratio': post['data']['upvote_ratio'],
                        'ups': post['data']['ups'],
                        'downs': post['data']['downs'],
                        'score': post['data']['score']
            }, ignore_index=True)

        dfReddit.to_csv(f'{subredditResult}Reddit.csv')

    #frame to house enter button
    redditFrame = LabelFrame(winD, padx=5, pady=5)
    redditFrame.pack(padx=10, pady=10)

    #scrape subreddits button
    topicbutton = Button(redditFrame, text="Get Reddit Data", padx=50, command=RedditStart)
    topicbutton.grid()

#end of reddit API

#create frame to house buttons
buttonframe = LabelFrame(winD, padx=5, pady=5)
buttonframe.pack(padx=10, pady=10)

#Reddit button
redditbutton = Button(buttonframe, text="Reddit", padx=60, pady=40, bg="#F28C28", command=RedditCrawlClick)
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
