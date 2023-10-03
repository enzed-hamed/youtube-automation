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

