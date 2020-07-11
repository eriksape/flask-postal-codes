from os import environ

from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException


def create_app(config_filename):
    application = Flask(__name__)
    application.config.from_object(config_filename)

    from app import api_bp
    application.register_blueprint(api_bp)

    from models import db
    db.init_app(application)
    CORS(application)

    return application


application = create_app("config")


@application.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    data = dict(
        message=e.description,
    )
    return jsonify(data), e.code


if __name__ == "__main__":
    debug = (environ.get("DEBUG") == 'true')
    port = int(environ.get("PORT", 5000))
    host = environ.get("HOST", '127.0.0.1')

    application.run(debug=debug, port=port, host=host)
