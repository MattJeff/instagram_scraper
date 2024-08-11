# app/utils/video_processing.py
# Téléchargement et traitement des vidéos (extraction de l'audio).

import requests
import tempfile
import os
from moviepy.editor import VideoFileClip

def download_video(video_url):
    print(f"Début du téléchargement de la vidéo: {video_url}")
    try:
        response = requests.get(video_url, stream=True, timeout=30)
        response.raise_for_status()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
            for chunk in response.iter_content(chunk_size=8192):
                temp_video.write(chunk)
            return temp_video.name

    except requests.RequestException as e:
        print(f"Erreur lors du téléchargement de la vidéo: {e}")
        raise

def extract_audio(video_path):
    print(f"Extraction de l'audio de {video_path}")
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
        output_path = temp_audio.name
        try:
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(output_path, codec='mp3')
            print(f"Audio extrait et sauvegardé à {output_path}")
            return output_path
        finally:
            video.close()
