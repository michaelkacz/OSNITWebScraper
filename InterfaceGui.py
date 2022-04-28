#import * from tkinter to develop GUI
from cgitb import text
from tkinter import *
from tkinter import ttk
from ttkthemes import themed_tk as tk
from xml.sax.xmlreader import InputSource
import twint
import pandas as pd
import requests
from pygooglenews import GoogleNews
import json
import time
#To install twint:
    #pip3 install twint
    #pip3 install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint
    #pip install aiohttp==3.7.0

#To install PYGoogleNews:
    #pip install pygooglenews

#create a window for GUI
#instantiate an instance of WinD
winD = tk.ThemedTk();
winD.get_themes();
winD.set_theme("smog");
#change the size of winD, using geometry function

#create title for window frame, WinD
winD.title("OSINT Project");
#change background of window frame

def RedditCrawlClick():
    #generate label
    redditlabel = ttk.Label(winD, text="Enter your favorite subreddit:")
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
    redditFrame = ttk.LabelFrame(winD)
    redditFrame.pack(padx=15, pady=15)

    #scrape subreddits button
    topicbutton = ttk.Button(redditFrame, text="Get Reddit Data", command=RedditStart)
    topicbutton.pack(padx=50)

#end of reddit API

#create frame to house buttons
buttonframe = ttk.LabelFrame(winD)
buttonframe.pack(padx=15, pady=15)

#Reddit button
redditbutton = ttk.Button(buttonframe, text="Reddit", command=RedditCrawlClick)
redditbutton.pack(padx=60, pady=40)

#onclick to web scrape twitter
def twittercrawlclick():
    #generate label
    twitterlabel = ttk.Label(winD, text="Please enter topic:")
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
    topicbutton = ttk.Button(twitterframe, text="Scrape Topic", command=topiccrawl)
    topicbutton.pack(padx=50)

#Twitter button
twitterbutton = ttk.Button(buttonframe, text="Twitter", command=twittercrawlclick)
twitterbutton.pack(padx=60,pady=40)

#onclick function to open input
def newscrawlclick():
    newslabel = Label(winD, text="Please enter news topic:")
    newslabel.pack()
    newsinput = Entry(winD)
    newsinput.pack()

    def newstopiccrawl():
        #get string from entry in previous function
        newsstring = newsinput.get()
        newsarticle = GoogleNews()
        searchnews = newsarticle.search(newsstring)

        for entry in searchnews["entries"]:
            print(entry["published"])
            print(entry["source"])
            print(entry["link"])
            print(entry["title"])

        newsoutput = str(searchnews)
        pd.DataFrame(newsoutput).to_csv(newsstring + ".csv")
            
    #frame to house enter button
    newsframe = LabelFrame(winD, padx=5, pady=5)
    newsframe.pack(padx=10, pady=10)

    newscrawlbutton = Button(newsframe, text="Scrape News Topic", padx=50, command=newstopiccrawl)
    newscrawlbutton.grid()

#news crawl button
newscrawlbutton = Button(buttonframe, text="News Crawler", padx=60, pady=40, bg="black", fg="white", command=newscrawlclick)
newscrawlbutton.grid()

#back/exit button
backbutton = ttk.Button(buttonframe, text="Back")
backbutton.pack(padx=50)
exitbutton = ttk.Button(buttonframe, text="Exit")
exitbutton.pack(padx=50)
#add buttons to grid

#display window frame on screen
winD.mainloop();
