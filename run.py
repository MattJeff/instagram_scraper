# run.py
# Point d'entrée de l'application Flask pour l'Instagram Scraper API.

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
 