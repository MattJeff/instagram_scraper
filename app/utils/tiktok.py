from TikTokApi import TikTokApi
import re

def fetch_tiktok_data(video_url):
    print("Starting TikTok data extraction")
    
    api = TikTokApi()
    video_id = extract_tiktok_video_id(video_url)
    
    try:
        video = api.video(id=video_id).info()

        tiktok_data = {
            "video_url": video['video']['downloadAddr'],
            "likes": video['stats']['diggCount'],
            "views": video['stats']['playCount'],
            "username": video['author']['uniqueId'],
            "profile_url": f"https://www.tiktok.com/@{video['author']['uniqueId']}"
        }

    except Exception as e:
        print(f"Error during TikTok data extraction: {e}")
        raise

    print(f"TikTok data extracted: {tiktok_data}")
    return tiktok_data

def extract_tiktok_video_id(url):
    print(f"Extracting video ID from TikTok URL: {url}")
    match = re.search(r'tiktok\.com/@[^/]+/video/(\d+)', url)
    if not match:
        raise ValueError("Invalid TikTok URL")
    return match.group(1)
