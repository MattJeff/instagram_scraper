# Instagram Scraper API

Une API Flask permettant de récupérer le script d'une vidéo Instagram et les informations associées à un post Instagram.

## Fonctionnalités
- Téléchargement de vidéos Instagram.
- Extraction et transcription de l'audio à partir des vidéos.
- Récupération des informations du post Instagram (likes, commentaires, vues, etc.).
- Tâches asynchrones pour gérer le traitement de vidéos.

## Installation

### Prérequis
- Python 3.x
- Redis (pour Celery)
- Git

### Étapes
1. Cloner le dépôt
   ```bash
   git clone https://github.com/your_username/instagram_scraper.git
   cd instagram_scraper


```bash
git clone https://github.com/your_username/instagram_scraper.git
cd instagram_scraper
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
