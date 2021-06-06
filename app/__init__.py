"""Main init file to initialise all Flask related packages and create the app."""

from flask import Flask
from config import Config
from flask_login import LoginManager

login = LoginManager()
login.login_view = 'auth.login'


def create_app(config_class=Config):
    """
    Function that will be called on the main app module. This function initialises all flask related packages,
    load config, as well as the set blueprints in the app.
    """

    app = Flask(__name__)
    app.config.from_object(config_class)
    login.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app


from app import models