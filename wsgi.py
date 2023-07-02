import logging

from waitress import serve

from app import create_app

logging.basicConfig(level=logging.DEBUG)
app = create_app()
serve(app, host='127.0.0.1', port=5011)