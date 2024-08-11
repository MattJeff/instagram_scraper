# app/utils/youtube.py
import re
import os
import googleapiclient.discovery
from googleapiclient.errors import HttpError

def fetch_youtube_data(video_url):
    print("Starting YouTube data extraction")
    
    video_id = extract_youtube_video_id(video_url)
    youtube_data = {}

    api_key = os.getenv("YOUTUBE_API_KEY")
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

    try:
        request = youtube.videos().list(part="snippet,contentDetails,statistics", id=video_id)
        response = request.execute()

        video_details = response['items'][0]

        youtube_data = {
            "video_url": video_url,
            "likes": video_details['statistics']['likeCount'],
            "comments": video_details['statistics']['commentCount'],
            "views": video_details['statistics']['viewCount'],
            "username": video_details['snippet']['channelTitle'],
            "followers": "",  # Requires a separate API call to get channel details
            "following": "",  # YouTube does not make this clear
            "publications": "",  # Requires a separate API call
            "profile_url": f"https://www.youtube.com/channel/{video_details['snippet']['channelId']}"
        }

    except HttpError as e:
        print(f"Error during YouTube data extraction: {e}")
        raise

    print(f"YouTube data extracted: {youtube_data}")
    return youtube_data

def extract_youtube_video_id(url):
    match = re.search(r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9-_]{11})', url)
    if not match:
        raise ValueError("Invalid YouTube URL")
    return match.group(1)
