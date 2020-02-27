from flask_restful import Resource
from .PostalCodeService import search

class PostalCode(Resource):
    def get(self, code):
        results = search(code)
        if results:
            return results
        else:
            return {}