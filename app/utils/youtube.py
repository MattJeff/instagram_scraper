# app/utils/youtube.py

import re
import ssl
import requests
from pytube import YouTube
import os
import yt_dlp


#desactiver le ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Désactiver la vérification des certificats SSL pour 'requests'
requests.packages.urllib3.disable_warnings()

def fetch_youtube_data(video_url):
    print("Starting YouTube data extraction")
    
    try:
     

        ydl_opts = {
        'format': 'mp4',
        'outtmpl': '%(title)s.%(ext)s',
                }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            
        
        youtube_data = {
        "video_url": video_url,
        "title": info_dict.get('title', ''),
        "views": info_dict.get('view_count', 0),
        "username": info_dict.get('uploader', ''),
        "profile_url": info_dict.get('uploader_url', '')
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

        ydl_opts = {
            'format': 'mp4',
            'outtmpl': '%(title)s.%(ext)s',
                }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_path = ydl.prepare_filename(info_dict)
         
        print(f"Video downloaded to {video_path}")
        return video_path
    
    except Exception as e:
        print(f"Error during video download: {e}")
        raise
