"""
API Blueprint

This blueprint defines routes and views for the API module.

Attributes:
    bp (Blueprint): The Flask Blueprint object representing the API module.

Usage:
    - Import the `bp` object in your application's main module and register it with the Flask app using the `app.register_blueprint` method.
"""


from flask import Blueprint

bp = Blueprint('api', __name__)
