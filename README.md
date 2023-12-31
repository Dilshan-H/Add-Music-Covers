# ADD-MUSIC-COVERS

<center>

![Banner](https://github.com/Dilshan-H/Add-Music-Covers/assets/77499497/303c6a88-008c-4a19-b97b-2aa8bad3d3b6)

</center>

This project allows you to add album cover images and other metadata to your local music files easily. It uses the Spotify API to retrieve metadata for your music files, and then adds the album covers and other information to the music files automatically.

✅ **UPDATE**: Now `ADD-MUSIC-COVERS` supports adding following metadata to your files as well.
- Song Title
- Artist
- Album
- Genre
- Year
- Track Number

<!-- Shield Badges -->

![GitHub license](https://img.shields.io/github/license/Dilshan-H/Add-Music-Covers?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/Dilshan-H/Add-Music-Covers?style=for-the-badge)

<!-- ![GitHub issues](https://img.shields.io/github/issues/Dilshan-H/Add-Music-Covers?style=for-the-badge)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Dilshan-H/Add-Music-Covers?style=for-the-badge)

![GitHub stars](https://img.shields.io/github/stars/Dilshan-H/Add-Music-Covers?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/Dilshan-H/Add-Music-Covers?style=for-the-badge) -->

## Installation & Usage

1. Clone the repository: `git clone https://github.com/Dilshan-H/Add-Music-Covers.git`
2. Navigate to the project directory: `cd Add-Music-Covers`
3. Create a virtual environment: `python3 -m venv venv`
4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux: `source venv/bin/activate`
5. Install the required dependencies: `pip install -r requirements.txt`
6. Create a Spotify application - [Find More Info](https://developer.spotify.com/documentation/web-api)
7. Copy the Client ID and Client Secret of your Spotify application and paste them as follows within a new file named `.env` in the project directory:

   ```
   CLIENT_ID=your_client_id
   CLIENT_SECRET=your_client_secret
   ```

8. Create a directory named `songs` in the project directory and add your music files to it.
9. Run the script: `python3 main.py`
10. The script will automatically add the album covers to the song files in the `songs` directory. Just follow the instructions in the terminal.

## License & Copyrights

**The MIT License**

This program is free software: you can redistribute it and/or modify it under the terms of the MIT License
Refer to the LICENSE file for more details.

Spotify copyrights and/or trademarks of their respective owners.

## How to Contribute

If you would like to contribute to this project, you can follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b my-branch`
3. Make your changes and commit them: `git commit -m "my changes"`
4. Push your changes to your fork: `git push origin my-branch`
5. Create a pull request.

We welcome all contributions!

## Disclaimer

This project uses the Spotify API to retrieve album covers for music files. Please note that the use of the Spotify API is subject to certain limitations and restrictions, as outlined in the [Spotify Developer Terms of Service](https://developer.spotify.com/terms).

This project is not affiliated with or endorsed by Spotify, and the use of Spotify's API and trademarks does not imply any endorsement or affiliation with Spotify.

By using this project, you agree to comply with all applicable laws and regulations, including the Spotify Developer Terms of Service and any other terms and conditions imposed by Spotify. The author of this project is not responsible for any misuse or violation of Spotify's terms and conditions.
