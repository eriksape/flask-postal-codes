from flask_restful import Resource, abort
from .PostalCodeService import search, validate


class PostalCode(Resource):
    def get(self, code):
        """Get a valid zip code data"""
        if validate('MX', code) is None:
            abort(400, message="Not a valid code")
        results = search(code)
        if results:
            return results
        else:
            return {}