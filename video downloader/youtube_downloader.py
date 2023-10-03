#!/usr/bin/env python3
import pytube


def Download(link):
    youtubeObject = pytube.YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
    except:
        print("[DOWNLOAD FAILED]")
    else:
        print("[DOWNLOAD FINISHED]")


link = input("Enter the YouTube video URL: ")
Download(link)
