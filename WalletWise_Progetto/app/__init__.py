from flask import Flask
from config import Config
from .db import init_db
from .blueprints.auth import auth_bp
from .blueprints.main import main_bp

def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    # init DB + tabelle + categorie base
    with app.app_context():
        init_db(app.config["DB_PATH"])

    # blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)

    return app
