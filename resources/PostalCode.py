from flask_restful import Resource, abort
from .PostalCodeService import search, validate


class PostalCode(Resource):
    def get(self, code):
        """Get a valid zip code data"""
        if validate('MX', code) is None:
            return abort(400, message="Not a valid code")
        results = search(code)
        if results == {}:
            return abort(404, message="Code not found")
        return results
