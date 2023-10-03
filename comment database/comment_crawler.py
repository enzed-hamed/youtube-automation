#!/usr/bin/env python3
import urllib.parse as p
import sys
import os
import sqlite3
import googleapiclient.discovery
from googleapiclient.errors import HttpError


api_key = "AIzaSyAATZR1wuL-JUj0tQivp2P9p8CRu8aUNgs"
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)


def get_video_id_by_url(url):
    """
    Return the Video ID from the video `url`
    """
    # split URL parts
    parsed_url = p.urlparse(url)
    # get the video ID by parsing the query of the URL
    video_id = p.parse_qs(parsed_url.query).get("v")
    if video_id:
        return video_id[0]
    else:
        raise Exception(f"Wasn't able to parse video URL: {url}")


# Global dictionary to store comments
comments_dict = {}


# Function to fetch comments for a video and store them in comments_dict
def fetch_comments(video_id):
    comments = []
    nextPageToken = None

    while True:
        response = (
            youtube.commentThreads()
            .list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=nextPageToken,
            )
            .execute()
        )

        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]
            username = comment["authorDisplayName"]
            text = comment["textDisplay"]
            comments.append(text)

            if username in comments_dict:
                comments_dict[username].append(text)
            else:
                comments_dict[username] = [text]

        nextPageToken = response.get("nextPageToken")
        print(".", end="", flush=True)
        if not nextPageToken:
            break

    return comments


# Function to check and create the SQLite database
def create_database():
    db_file = "comments.db"
    if not os.path.isfile(db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE users (
                username TEXT PRIMARY KEY,
                videos TEXT
            )
            """
        )
        conn.commit()
        conn.close()


# Function to add a video to a user's list in the database
def add_video_to_user(username, video_id):
    conn = sqlite3.connect("comments.db")
    cursor = conn.cursor()

    cursor.execute("SELECT videos FROM users WHERE username=?", (username,))
    row = cursor.fetchone()

    if row is not None:
        videos = row[0].split(",")
        if video_id not in videos:
            videos.append(video_id)
            cursor.execute(
                "UPDATE users SET videos=? WHERE username=?",
                (",".join(videos), username),
            )
    else:
        cursor.execute(
            "INSERT INTO users (username, videos) VALUES (?, ?)", (username, video_id)
        )

    conn.commit()
    conn.close()


def table_exists(video_id):
    conn = sqlite3.connect("comments.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (video_id,)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None


# Function to create and populate a new table for the given video_id
def create_and_populate_table(video_id):
    conn = sqlite3.connect("comments.db")
    cursor = conn.cursor()

    # Create a new table for the video_id
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS "{video_id}" (
            username TEXT PRIMARY KEY,
            comments TEXT
        )
        """
    )

    # Populate the table with values from comments_dict
    for username, comments in comments_dict.items():
        comments_str = "*#*#".join(comments)
        cursor.execute(
            "INSERT INTO '{}' (username, comments) VALUES (?, ?)".format(video_id),
            (username, comments_str),
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    video_id = get_video_id_by_url(sys.argv[1])

    create_database()

    if table_exists(video_id):
        print("[-] This video already processed")
    else:
        print("> Processing comments ", end="", flush=True)
        comments = fetch_comments(video_id)
        for username in comments_dict.keys():
            add_video_to_user(username, video_id)
        create_and_populate_table(video_id)
        print(
            "\n\n[+] Comments and users extracted and stored in the database: 'comments.db'"
        )
