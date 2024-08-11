# app/routes.py
# Gestion des routes API pour récupérer le script d'une vidéo Instagram et vérifier l'état des tâches.

from flask import Blueprint, request, jsonify
from app.utils.instagram import fetch_instagram_data
from app.utils.tiktok import fetch_tiktok_data
from app.utils.youtube import fetch_youtube_data
from app.tasks import process_video_task
from celery.result import AsyncResult

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return jsonify({'message': 'Bienvenue sur l\'API Instagram Scraper'})

@routes.route('/get_script', methods=['POST'])
def get_script():
    data = request.get_json()
    if 'url' not in data:
        return jsonify({'error': 'URL manquante'}), 400

    video_url = data['url']
    platform = detect_platform(video_url)

    try:
        if platform == "instagram":
            platform_data = fetch_instagram_data(video_url)
        elif platform == "youtube":
            platform_data = fetch_youtube_data(video_url)
        elif platform == "tiktok":
            platform_data = fetch_tiktok_data(video_url)
        else:
            return jsonify({'error': 'Platform not supported'}), 400

        print(f"Platform data ready for processing: {platform_data}")

        #task = process_video_task.apply_async(args=[platform_data['video_url']])
        transcribe = process_video_task(platform_data['video_url'])
        platform_data['script'] = transcribe

        return jsonify({'post': platform_data}), 202

    except Exception as e:
        print(f"Error extracting data: {e}")
        return jsonify({'error': str(e)}), 500

def detect_platform(url):
    if 'instagram.com' in url:
        return 'instagram'
    elif 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    elif 'tiktok.com' in url:
        return 'tiktok'
    else:
        return None

@routes.route('/task_status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Pending...'}
    elif task.state != 'FAILURE':
        response = {'state': task.state, 'result': task.result}
    else:
        response = {'state': task.state, 'status': str(task.info)}
    return jsonify(response)
