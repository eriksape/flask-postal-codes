from flask import abort, request

from app.services.PostalCodeService import search, validate_zip_code


class PostalCodeController:
    @staticmethod
    def get(code):
        """Get a valid zip code data"""
        if validate_zip_code('MX', code) is None:
            return abort(400, description="Not a valid code")
        results = search(code)
        if results == {}:
            return abort(404, description="Code not found")
        return results

    @staticmethod
    def get_all():
        return (1,2,3)
