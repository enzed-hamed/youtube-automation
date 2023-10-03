#!/usr/bin/env python3
import os
import sqlite3
from bs4 import BeautifulSoup


# Function to check if the database file exists
def database_exists():
    return os.path.isfile("comments.db")


# Function to retrieve the number of users and processed videos
def get_database_stats():
    conn = sqlite3.connect("comments.db")
    cursor = conn.cursor()

    # Count the number of users
    cursor.execute("SELECT COUNT(*) FROM users")
    num_users = cursor.fetchone()[0]

    # Get the list of processed video IDs
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    processed_videos = [row[0] for row in cursor.fetchall() if row[0] != "users"]

    conn.close()

    return num_users, len(processed_videos), processed_videos


# Function to list all usernames
def list_all_usernames():
    conn = sqlite3.connect("comments.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")
    usernames = [row[0] for row in cursor.fetchall()]
    conn.close()
    return usernames


# Function to query a username's comments for a video
def query_username_comments(username):
    conn = sqlite3.connect("comments.db")
    cursor = conn.cursor()

    # Query all videos associated with the username
    cursor.execute("SELECT videos FROM users WHERE username=?", (username,))
    videos = cursor.fetchone()

    if videos is None:
        return None

    video_list = videos[0].split(",")
    user_comments = {}

    # Retrieve comments for each video
    for video_id in video_list:
        cursor.execute(
            f"SELECT comments FROM '{video_id}' WHERE username=?", (username,)
        )
        comments = cursor.fetchone()
        if comments is not None:
            user_comments[video_id] = comments[0].split("*#*#")

    conn.close()
    return user_comments


# Main menu function
def main_menu():
    while True:
        print("")
        print("_________________________________________")
        print("[Please select a task from below options]")
        print("1  List all usernames")
        print("2  Query a username's comments")
        print("3  Exit")
        choice = input(">> ")

        if choice == "1":
            usernames = list_all_usernames()
            print(f"[+] Database consists of {len(usernames)} users")
            print("\n#################")
            print("### USERNAMES ###")
            print("#################")
            for username in usernames:
                print(f'"{username}"')
        elif choice == "2":
            username = input("Enter a username: ")
            user_comments = query_username_comments(username)
            if user_comments is None:
                print(f'[-] User "{username}" not found in the database.')
            else:
                margin = " ################# "
                message = f'### USER "{username}" COMMENTS ###'
                print(" " * len(margin) + "#" * len(message))
                print(margin + message + margin)
                print(" " * len(margin) + "#" * len(message))
                for video_id, comments in user_comments.items():
                    margin = " --------- "
                    message = f"https://www.youtube.com/watch?v={video_id}"
                    print(" " * len(margin) + "-" * len(message))
                    print(margin + message + margin)
                    print(" " * len(margin) + "-" * len(message))
                    for comment in comments:
                        soup = BeautifulSoup(comment, "html.parser")
                        # Extract text without HTML tags
                        comment = soup.get_text()
                        print(comment)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid input. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    if not database_exists():
        print("[-] No database exists")
        exit()

    num_users, num_videos, processed_videos = get_database_stats()
    print(f"[+] Database consists of {num_users} users")
    print(f"[+] {num_videos} YouTube videos processed")

    main_menu()
