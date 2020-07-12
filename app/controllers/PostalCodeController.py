from flask import abort, request

from app.services.PostalCodeService import search, validate_zip_code, get_settlements, get_settlements_count


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
        limit = (request.args.get('limit'), '100')[request.args.get('limit') is None]
        if not limit.isnumeric():
            return abort(400, description="Not a valid value for limit")

        offset = (request.args.get('offset'), '0')[request.args.get('offset') is None]
        if not offset.isnumeric():
            return abort(400, description="Not a valid value for offset")

        page = (request.args.get('page'), '1')[request.args.get('page') is None]
        if not page.isnumeric():
            return abort(400, description="Not a valid value for page")

        sort = (request.args.get('sort'), 'codigo_postal')[request.args.get('sort') is None]
        if sort not in ('codigo_postal', 'municipio', 'estado'):
            return abort(400, description="Not a valid value for sort")

        order = (request.args.get('order'), 'ASC')[request.args.get('order') is None]
        if order not in ('ASC', 'DESC'):
            return abort(400, description="Not a valid value for order")

        limit = int(limit)
        offset = int(offset)
        page = int(page)

        return {
            "data": get_settlements(limit, offset, page, sort, order),
            "total": get_settlements_count()
        }

