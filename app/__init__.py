# app/__init__.py
# Initialisation de l'application Flask et enregistrement des routes.

from flask import Flask
from app.routes import routes
from config import Config

def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes)
    app.config.from_object(Config)
    return app
