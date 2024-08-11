# app/utils/instagram.py
# Extraction des données d'un post Instagram via Instaloader.

from instaloader import Instaloader, Post
import re

def fetch_instagram_data(video_url):
    print("Début de l'extraction des données d'Instagram")
    shortcode = extract_shortcode(video_url)
    loader = Instaloader()
    post = Post.from_shortcode(loader.context, shortcode)

    instagram_data = {
        "video_url": post.video_url,
        "likes": post.likes,
        "script": "",
        "comments": post.comments,
        "views": post.video_view_count,
        "username": post.owner_username,
        "followers": post.owner_profile.followers,
        "following": post.owner_profile.followees,
        "publications": post.owner_profile.mediacount,
        "profile_url": f"https://instagram.com/{post.owner_username}"
    }
    print(f"Données Instagram extraites: {instagram_data}")
    return instagram_data

def extract_shortcode(url):
    print(f"Extraction du shortcode à partir de l'URL: {url}")
    match = re.search(r'(?:https?://)?(?:www\.)?instagram\.com/(?:p|reel|tv)/([A-Za-z0-9-_]+)/?', url)
    if not match:
        raise ValueError("URL Instagram invalide")
    return match.group(1)
