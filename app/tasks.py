# app/tasks.py
# Définition des tâches Celery pour le traitement vidéo et la transcription audio.

from celery import Celery
from app.utils.video_processing import download_video, extract_audio
from app.utils.audio_transcription import transcribe_audio_with_api
from app.utils.validation import validate_video_file
import os

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task(bind=True)
def process_video_task(self, video_url):
    temp_video_path = None
    temp_audio_path = None
    try:
        temp_video_path = download_video(video_url)
        validate_video_file(temp_video_path)

        temp_audio_path = extract_audio(temp_video_path)
        transcription = transcribe_audio_with_api(temp_audio_path)
        print(f"{transcription.text}")
        print(f"Transcription pour {video_url}: {transcription}")
        return transcription.text
    except Exception as e:
        print(f"Erreur lors du traitement de la vidéo: {e}")
        raise
    finally:
        if temp_video_path and os.path.exists(temp_video_path):
            os.remove(temp_video_path)
        if temp_audio_path and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
