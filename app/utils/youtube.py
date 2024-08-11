# app/utils/youtube.py

import re
from pytube import YouTube
import os

def fetch_youtube_data(video_url):
    print("Starting YouTube data extraction")
    
    try:
        yt = YouTube(video_url)
        youtube_data = {
            "video_url": video_url,
            "title": yt.title,
            "likes": yt.views,  # Pytube ne fournit pas de likeCount directement
            "comments": "",  # Pytube ne supporte pas les commentaires directement
            "views": yt.views,
            "username": yt.author,
            "followers": "",  # Pytube ne supporte pas le comptage des abonnés
            "following": "",  # YouTube n'a pas de concept explicite de "following"
            "publications": "",  # Pas de moyen direct d'obtenir le nombre de vidéos de la chaîne
            "profile_url": yt.channel_url
        }

    except Exception as e:
        print(f"Error during YouTube data extraction: {e}")
        raise

    print(f"YouTube data extracted: {youtube_data}")
    return youtube_data

def extract_youtube_video_id(url):
    match = re.search(r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([A-Za-z0-9-_]{11})', url)
    if not match:
        raise ValueError("Invalid YouTube URL")
    return match.group(1)

def download_youtube_video(video_url, output_path="."):
    print(f"Starting download of YouTube video from {video_url}")
    try:
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        video_path = stream.download(output_path=output_path)
        print(f"Video downloaded to {video_path}")
        return video_path
    except Exception as e:
        print(f"Error during video download: {e}")
        raise
