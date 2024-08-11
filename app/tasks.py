# app/tasks.py
# Définition des tâches Celery pour le traitement vidéo et la transcription audio.

# app/tasks.py
from celery import Celery
from app.utils.video_processing import download_video, extract_audio
from app.utils.audio_transcription import transcribe_audio_with_api
from app.utils.validation import validate_video_file
from app.utils.instagram import fetch_instagram_data
from app.utils.youtube import fetch_youtube_data
from app.utils.tiktok import fetch_tiktok_data
import os

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task(bind=True)
def process_video_task(self, platform, video_url):
    temp_video_path = None
    temp_audio_path = None
    try:
        if platform == 'instagram':
            video_data = fetch_instagram_data(video_url)
        elif platform == 'youtube':
            video_data = fetch_youtube_data(video_url)
        elif platform == 'tiktok':
            video_data = fetch_tiktok_data(video_url)
        else:
            raise ValueError("Unsupported platform")

        temp_video_path = download_video(video_data['video_url'])
        validate_video_file(temp_video_path)

        temp_audio_path = extract_audio(temp_video_path)
        transcription = transcribe_audio_with_api(temp_audio_path)
        print(f"Transcription for {video_url}: {transcription.text}")
        return transcription.text
    except Exception as e:
        print(f"Error processing the video: {e}")
        raise
    finally:
        if temp_video_path and os.path.exists(temp_video_path):
            os.remove(temp_video_path)
        if temp_audio_path and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

