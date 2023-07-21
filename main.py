# pylint: disable=import-error invalid-name anomalous-backslash-in-string

"""
This script adds cover images to your song files.
Supported file formats: .mp3, .flac

Author: Dilshan-H 
Date: 2023-07-21
License: MIT License
"""

import os
import logging
import base64
import requests
from dotenv import load_dotenv
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

# Load environment variables from .env file
load_dotenv()

# Spotify API credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Set up logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def get_access_token():
    """Get the access token from Spotify API"""
    logging.info("Getting the access token...")
    print("---> Authorization process started.")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic "
        + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    }
    data = {"grant_type": "client_credentials"}
    try:
        response = requests.post(url, headers=headers, data=data, timeout=3)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error("Authorization Failure: %s", e)
        raise SystemExit(e) from e
    return response.json()["access_token"]


def get_track_id(access_token, song_name, artist_name):
    """Get the track ID of a song from Spotify API"""
    query = f"{song_name} artist:{artist_name}"
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": "Bearer " + access_token}
    params = {"q": query, "type": "track", "limit": 1}
    logging.info("Searching for %s...", query)
    response = requests.get(url, headers=headers, params=params, timeout=3)
    return response.json()["tracks"]["items"][0]["id"]


def get_cover_image_url(access_token, track_id):
    """Get the cover image URL of a song from Spotify API"""
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = {"Authorization": "Bearer " + access_token}
    logging.info("Getting the cover image URL...")
    response = requests.get(url, headers=headers, timeout=3)
    return response.json()["album"]["images"][0]["url"]


def add_cover_image(song_file, image_url):
    """Add cover image to a song file"""
    audio = MP3(song_file, ID3=ID3)

    # Add ID3 tag if it doesn't exist
    try:
        audio.add_tags()
    except error:
        pass

    logging.info("Adding the cover image to %s...", song_file)
    audio.tags.add(
        APIC(
            encoding=3,  # 3 is for utf-8
            mime="image/jpeg",  # image/jpeg or image/png
            type=3,  # 3 is for the cover image
            desc="Cover",
            data=requests.get(image_url, timeout=3).content,
        )
    )
    audio.save()


def main():
    """Main function"""
    logging.info("Starting the script...")
    print(
        """
        _             _ _            _         _   
       / \  _   _  __| (_) ___      / \   _ __| |_ 
      / _ \| | | |/ _` | |/ _ \    / _ \ | '__| __|
     / ___ \ |_| | (_| | | (_) |  / ___ \| |  | |_ 
    /_/   \_\__,_|\__,_|_|\___/  /_/   \_\_|   \__|
    
    ----------------------------------------------------
    This script adds cover images to your song files.
    Supported file formats: .mp3, .flac

    Author: Dilshan-H 
    Date: 2023-07-21
    License: MIT License
    ----------------------------------------------------
    """
    )
    print("Press Ctrl+C to exit the script.\n")
    access_token = get_access_token()
    folder = os.getcwd()  # Use the current directory that the Python file runs on
    logging.info("Looking for song files in %s...", folder)
    for song_file in os.listdir(folder):
        if song_file.endswith((".mp3", ".flac")):
            song_name = os.path.splitext(song_file)[
                0
            ]  # Use the current file name as the song name
            logging.info("Adding cover image to %s...", song_name)
            print(f"Processing song: {song_name[:50]}")
            artist_name = ""  # You need to get the artist name
            track_id = get_track_id(access_token, song_name, artist_name)
            image_url = get_cover_image_url(access_token, track_id)
            add_cover_image(os.path.join(folder, song_file), image_url)
    logging.info("Process completed successfully.")
    print("\n---> Process completed successfully.")


if __name__ == "__main__":
    main()
