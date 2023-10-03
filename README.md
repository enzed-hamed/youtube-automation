# Youtube Tools
In this project, I have wrote a handful of scripts to perform useful tasks with regard to youtube. Mostly I make use of Google APIs.

## Subtitle/Audionscript/Transcript Downloader
`python audioscript.py  video_url`<br />
This will go ahead and list out all the available subtitles which are Manual, Auto-generated, and Translated in this order with their language code.
You have to select language by its code and it will download and store it into an excel sheet (sorry this was for an student project). If subtitle disabled by video owner, script will notify you.


## Video Downloader
`python video_downloader.py`<br />
This is a simple youtube video downloader that asks for the video url and downloads highest quality available in the same folder.

## Extract Channel Info
`python youtube.py`<br />
This Script asks for a Youtube channel url, it supports different forms of url. It fetches all the information on the channel including total number of views, subscribers, creation date, country, etc. Then it fetches all the statistics and info of all channel's videos. Finally Information of channel and Videos are stored in two seperate spreadsheets.

## comment database
`python comment_crawler.py  youtube_video_url`<br />
`python comment_query`<br />
I was tasked by my professor to find an osint service that has the ability to cross-reference a user that has made a comment on one video across all youtube videos. I didn't find such service so I decided to make a platform of my own to do just that. This includes a ***comment_crawler*** program which receives a video url and fetches all comments and usernames and stores it in a sqlite database. We can do this for as many usernames as we want, they all will be stored in our database file.<br /> 
Now the second script ***comment_query*** can list all usernames that every made a comment. And by specifying/querying a username it list all the videos the user made comment for along with the actual comment text.
