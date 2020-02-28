from flask import Blueprint
from flask_restful import Api
from resources.PostalCode import PostalCode

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(PostalCode, '/postal-codes/<code>')