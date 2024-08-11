# app/routes.py
# Gestion des routes API pour récupérer le script d'une vidéo Instagram et vérifier l'état des tâches.

from flask import Blueprint, request, jsonify
from app.utils.instagram import fetch_instagram_data
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
    try:
        instagram_data = fetch_instagram_data(video_url)
        print(f"Données Instagram prêtes pour le traitement: {instagram_data}")

        #task = process_video_task.apply_async(args=[instagram_data['video_url']])
        transcribe = process_video_task(instagram_data['video_url'])
        instagram_data['script'] = transcribe
        #instagram_data['script'] = task

        return jsonify({'post': instagram_data}), 202

    except Exception as e:
        print(f"Erreur lors de l'extraction des données Instagram: {e}")
        return jsonify({'error': str(e)}), 500

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
