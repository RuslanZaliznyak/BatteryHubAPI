import logging

from flask import Flask
from waitress import serve

from app.config import Config
from app.extensions import db
from flask_restx import Api


def create_app(config_class=Config):
    """
    Create and configure the Flask application.

    :param config_class: The configuration class for the application.
    :return: The Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.logger.setLevel(logging.DEBUG)
    db.init_app(app)
    api = Api(app, title="BatteryHub API", version="0.0.1")

    from app.api.endpoints import bp as api_bp
    app.register_blueprint(api_bp)

    return app


if __name__ == '__main__':
    """
    Run the Flask application.
    """
    logging.basicConfig(level=logging.DEBUG)
    app = create_app()
    serve(app, host='127.0.0.1', port=5002)
