# app/utils/validation.py
# Validation des fichiers vidéo téléchargés.

import os

def validate_video_file(video_path):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Le fichier {video_path} n'existe pas.")
    if os.path.getsize(video_path) == 0:
        raise ValueError("Le fichier vidéo téléchargé est vide.")
    print(f"Fichier vidéo validé: {video_path}")
