from flask import Flask
from flask_cors import CORS




def create_app(config_filename):
    application = Flask(__name__)
    application.config.from_object(config_filename)
    
    from app import api_bp
    application.register_blueprint(api_bp, url_prefix='/api')

    from models import db
    db.init_app(application)
    CORS(application)

    return application

application = create_app("config")

if __name__ == "__main__":
    
    application.run(debug=True)