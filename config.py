# config.py
# Fichier de configuration centralisé pour l'application Flask.

import os
from dotenv import load_dotenv
from pathlib import Path

# Obtenir le chemin absolu du fichier .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Vérifier si le fichier .env existe
if os.path.exists(dotenv_path):
    print(f"Fichier .env trouvé à : {dotenv_path}")
else:
    print("Erreur : Fichier .env introuvable !")

print(f"ASSEMBLYAI_API_KEY: {os.getenv('ASSEMBLYAI_API_KEY')}")
print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")

class Config:
    ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", 'redis://localhost:6379/0')
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

    @staticmethod
    def check_config():
        if not Config.ASSEMBLYAI_API_KEY:
            print("Erreur : ASSEMBLYAI_API_KEY n'est pas défini.")
        if not Config.OPENAI_API_KEY:
            print("Erreur : OPENAI_API_KEY n'est pas défini.")
        if not Config.CELERY_BROKER_URL:
            print("Erreur : CELERY_BROKER_URL n'est pas défini.")
        if not Config.CELERY_RESULT_BACKEND:
            print("Erreur : CELERY_RESULT_BACKEND n'est pas défini.")

# Appel de la méthode pour vérifier les configurations
Config.check_config()
