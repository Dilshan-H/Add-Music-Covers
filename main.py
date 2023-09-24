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
import sys
import requests
from dotenv import load_dotenv
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from mutagen.easyid3 import EasyID3

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
    logging.info("Authorization process started - Getting access token")
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
    logging.info("Authorization process completed successfully.")
    print("---> Authorization process completed successfully.")
    return response.json()["access_token"]


def get_track_id(access_token, song_name, artist_name):
    """Get the track ID of a song from Spotify API"""
    query = f"{song_name} artist:{artist_name}"
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": "Bearer " + access_token}
    params = {"q": query, "type": "track", "limit": 1}
    logging.info("Searching for %s...", query)
    response = requests.get(url, headers=headers, params=params, timeout=3)
    if response.json()["tracks"]["items"] == []:
        logging.warning("No results found for %s.", query)
        print(f"--- WARNING: No results found for {query[:50]}.")
        # Get user input for song name and artist name
        song_name = input("--- Enter the song name manually: ")
        artist_name = input("--- Enter the artist name manually: ")
        return get_track_id(access_token, song_name, artist_name)
    return response.json()["tracks"]["items"][0]["id"]


def get_metadata(access_token, track_id):
    """Get the metadata of a song from Spotify API"""
    try:
        url = f"https://api.spotify.com/v1/tracks/{track_id}"
        headers = {"Authorization": "Bearer " + access_token}
        logging.info("Getting the cover image URL...")
        response = requests.get(url, headers=headers, timeout=3)
        track_image = response.json()["album"]["images"][0]["url"]
        track_title = response.json()["name"]
        track_artist = response.json()["artists"][0]["name"]
        track_album = response.json()["album"].get("name", "")
        track_number = response.json().get("track_number", "")
        track_genre = response.json()["artists"][0].get("genres", "")
        track_year = response.json()["album"].get("release_date", "")[:4]
        return {
            "image_url": track_image,
            "title": track_title,
            "artist": track_artist,
            "album": track_album,
            "track_number": track_number,
            "genre": track_genre,
            "year": track_year,
        }
    except Exception as e:
        logging.error("Error occurred while getting metadata: %s", e)
        print(f"--- ERROR: Failed to get metadata for track {track_id}. Skipping...")
        return None


def replace_cover_image(audio, song_file, metadata):
    """Replace the cover image of a song file"""
    logging.info("Replacing the cover image...")
    print("--- Replacing the cover image...")
    audio.delete()
    logging.info("Adding the cover image to %s...", song_file)
    audio.tags.add(
        APIC(
            encoding=3,  # 3 is for utf-8
            mime="image/jpeg",  # image/jpeg or image/png
            type=3,  # 3 is for the cover image
            desc="Cover",
            data=requests.get(metadata.get("image_url"), timeout=3).content,
        )
    )
    audio.save()


def add_metadata(song_file, metadata, replace_cover_choice):
    """Add metadata to a song file"""
    if metadata is None:
        return

    try:
        audio = MP3(song_file, ID3=ID3)
    except error:
        logging.error("Skipping file due to an error opening: %s", song_file)
        print(f"--- ERROR: Failed to open {song_file[:50]}. Skipping...")
        return

    # Add ID3 tag if it doesn't exist
    try:
        audio.add_tags()
        logging.info("Adding ID3 tag to %s...", song_file)
    except error:
        # If the ID3 tag already exists, pass
        pass
    audio.save()

    # Check if the APIC tag exists
    audio = MP3(song_file, ID3=ID3)

    if ("APIC:Cover" in audio) or ("APIC:" in audio):
        logging.warning("Cover image already exists in %s.", song_file)
        if replace_cover_choice == "1":
            replace_cover_image(audio, song_file, metadata)
        elif replace_cover_choice == "2":
            choice = input(
                "--- Existing cover image detected. Do you want to replace it? (y/n): "
            )
            if choice.lower() == "n":
                logging.info(
                    "Skip adding image due to user intervention %s...", song_file
                )
                print("--- Skipped adding cover image.")
            else:
                replace_cover_image(audio, song_file, metadata)
        elif replace_cover_choice == "3":
            pass
    else:
        replace_cover_image(audio, song_file, metadata)

    # Add metadata to the ID3 tag
    logging.info("--- Adding metadata to %s...", song_file)
    print("--- Adding metadata...")
    audio = EasyID3(song_file)
    audio["title"] = metadata.get("title")
    audio["artist"] = metadata.get("artist")
    audio["album"] = metadata.get("album")
    audio["genre"] = metadata.get("genre")
    audio["date"] = metadata.get("year")
    audio["tracknumber"] = str(metadata.get("track_number"))
    audio.save()
    logging.info("--- Metadata added successfully to %s.", song_file)


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
    This script adds cover images and other metadata to your song files.
    Supported file formats: .mp3, .flac

    Author: Dilshan-H
    Date: 2023-07-21
    License: MIT License
    ----------------------------------------------------
    """
    )
    print("Press Ctrl+C to exit the script.\n")
    # prompt if user wants to be asked for whether to replace existing cover images
    print(
        "Should the existing covers to be replaced without asking?\n"
        "----------------------------------------------------------\n"
        "1: Yes, replace them all\n"
        "2: No, ask me for each file\n"
        "3: No, skip them all (keep the current covers)\n"
    )
    replace_cover_choice = input("Enter your choice (1/2/3): ").strip()
    if replace_cover_choice not in ["1", "2", "3"]:
        print("Invalid choice. Exiting...")
        sys.exit(1)

    logging.info("User chose option %s.", replace_cover_choice)
    access_token = get_access_token()
    folder = os.path.join(os.getcwd(), "songs")
    logging.info("Looking for song files in %s...", folder)
    print(f"---> Looking for song files in {folder}...")

    # Keep count of files have valid extensions - mp3 or flac
    file_count = 0

    try:
        for song_file in os.listdir(folder):
            if song_file.endswith((".mp3", ".flac")):
                file_count += 1
                song_name = os.path.splitext(song_file)[
                    0
                ]  # Use the current file name as the song name
                logging.info("Processing song: %s...", song_name)
                print(f"■ Processing song: {song_name[:50]}")
                artist_name = ""
                track_id = get_track_id(access_token, song_name, artist_name)
                metadata = get_metadata(access_token, track_id)
                add_metadata(
                    os.path.join(folder, song_file), metadata, replace_cover_choice
                )
    except KeyboardInterrupt:
        logging.info("User interrupted the script.")
        print("\n---> Stopping the script...")
        sys.exit(0)
    except FileNotFoundError:
        logging.error(
            "The 'songs' directory does not exist in the current working directory."
        )
        print(
            "--- ERROR: The 'songs' directory does not exist in the current working directory."
        )
        logging.info("Stopping the script...")
        sys.exit(1)
    if file_count == 0:
        logging.warning("No valid song files found in %s.", folder)
        print(f"---> WARNING: No song files found in {folder}.")
    logging.info("Process completed successfully.")
    print("\n---> Process completed successfully.")


if __name__ == "__main__":
    main()
