from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from src.config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from routes.auth_routes import auth_bp
    from routes.fingerprint_routes import fingerprint_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(fingerprint_bp)

    return app

@login_manager.user_loader
def load_user(id):
    from src.auth.models import User
    return User.query.get(int(id)) 