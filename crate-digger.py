#!/usr/bin/env python3

import librosa
from pytube import Playlist
from pathvalidate import sanitize_filename
import ffmpeg
import os
import sys

SOURCE_BPM = 120
playlist = Playlist(sys.argv[1])

print("####################################################")
print("# Crate Digger Starting...")
print("####################################################")
for video in playlist.videos:
    title = video.title
    track_filename = f"{sanitize_filename(title.replace(' ', '-'))}.mp4"
    watch_url = video.watch_url
    video_id = video.video_id

    # Download Track from Youtube
    #--------------------------------------
    print("")
    print(f"TRACK TITLE: {title}")
    print(f"WATCH URL: {watch_url}")
    print(f"VIDEO ID: {video_id}")
    video.streams.filter(only_audio=True).get_audio_only().download(filename=track_filename)

    # Convert Audio
    #--------------------------------------
    input_file = ffmpeg.input(track_filename)
    new_filename = os.path.splitext(track_filename)[0]+'.flac'
    input_file.output(new_filename, acodec='flac', loglevel="quiet").run()
    os.remove(track_filename)
    track_filename = new_filename

    # Extract BPM From Track
    #--------------------------------------
    y, sr = librosa.load(track_filename)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    print(f"ESTIMATED BPM: {tempo}") 
    os.remove(track_filename)
    if abs(SOURCE_BPM - tempo) > 2:
        print("TRACK NOT WITHIN BPM RANGE")
    else:   
        print("TRACK IS WITHIN BPM RANGE")
    

