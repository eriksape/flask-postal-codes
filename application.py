from flask import Flask, jsonify
from flask_cors import CORS
from os import environ as env


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


@application.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


if __name__ == "__main__":
    debug = (env.get("DEBUG") == 'true')
    port = int(env.get("PORT", 5000))
    host = env.get("HOST", '127.0.0.1')

    application.run(debug=debug, port=port, host=host)
