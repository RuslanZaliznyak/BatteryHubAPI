import os
from dotenv import load_dotenv


class Config:
    """
    This class defines the configuration settings for a Flask application.
    """

    load_dotenv('.env')

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Secret Key
    SECRET_KEY = os.environ.get('SECRET_KEY')
