# app/__init__.py
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # Isso permite solicitações de cross-origin do seu app React Native
    
    from .views import views as views_blueprint
    app.register_blueprint(views_blueprint)

    return app