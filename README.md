# Youtube Tools
In this project, I have wrote a handful of scripts to perform useful tasks with regard to youtube. Mostly I make use of Google APIs.

## Subtitle/Audionscript/Transcript Downloader
You can simply run the program as follow:<br />
`python audioscript.py  video_url`__
This will go ahead and list out all the available subtitles which are Manual, Auto-generated, and Translated in this order with their language code.
You have to select language by its code and it will download and store it into an excel sheet (sorry this was for an student project). If subtitle disabled by video owner, script will notify you.


## Video Downloader
This is a simple youtube video downloader that asks for the video url and downloads highest quality available in the same folder.
`python video_downloader.py`
