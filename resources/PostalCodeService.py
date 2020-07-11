from models import (
    Estado,
    Municipio,
    Asentamiento
)
from .PostalCodeRegex import zipcodes_regex


def validate(country_code, zip_code):
    """Checks if the zip code is a valid one"""
    import re
    verify = re.compile(zipcodes_regex[country_code])
    return verify.match(zip_code)


def search(codigo_postal):
    settlements = Asentamiento.query.filter_by(codigo_postal=codigo_postal).all()
    if len(settlements) > 0:
        codigo_postal = {
            'zip_code': settlements[0].codigo_postal,
            'state': {
                'id': settlements[0].municipio.estado.id,
                'name': settlements[0].municipio.estado.nombre,
                'c_estado': settlements[0].municipio.estado.c_estado
            },
            'municipality': {
                'id': settlements[0].municipio.id,
                'name': settlements[0].municipio.nombre,
                'c_mnpio': settlements[0].municipio.c_mnpio
            },
            'settlements': []
        }
        for settlement in settlements:
            codigo_postal['settlements'].append({
                'id': settlement.id,
                'name': settlement.nombre,
                'type': settlement.tipo,
                'id_asenta_cpcons': settlement.id_asenta_cpcons,
                'c_cve_ciudad': settlement.c_cve_ciudad
            })
        return codigo_postal
    return {}


def get_states(**kwargs):
    elements = []

    try:
        states = Estado.query.filter_by(**kwargs)
        for state in states:
            elements.append({
                'id': state.id,
                'name': state.nombre,
                'c_estado': state.c_estado
            })
    except Exception as e:
        print('Error:', str(e))

    return elements


def get_municipalities(**kwargs):
    elements = []

    _nested = kwargs.get('nested', False)
    try:
        del kwargs['nested']
    except Exception as e:
        pass

        municipalities = Municipio.query.filter_by(**kwargs)
        for municipality in municipalities:
            if _nested:
                elements.append({
                    'id': municipality.id,
                    'name': municipality.nombre,
                    'c_mnpio': municipality.c_mnpio,
                    'state': {
                        'id': municipality.estado.id,
                        'name': municipality.estado.nombre,
                        'c_estado': municipality.estado.c_estado
                    }
                })
            else:
                elements.append({
                    'id': municipality.id,
                    'name': municipality.nombre,
                    'c_mnpio': municipality.c_mnpio,
                    'state_id': municipality.estado.id
                })
    except Exception as e:
        print('Error:', str(e))

    return elements


def get_settlements(**kwargs):
    elements = []

    _nested = kwargs.get('nested', False)
    try:
        del kwargs['nested']
    except Exception as e:
        pass

    try:
        settlements = Asentamiento.query.filter_by(**kwargs)
        for settlement in settlements:
            if _nested:
                elements.append({
                    'id': settlement.id,
                    'name': settlement.nombre,
                    'type': settlement.tipo,
                    'id_asenta_cpcons': settlement.id_asenta_cpcons,
                    'c_cve_ciudad': settlement.c_cve_ciudad,
                    'municipality': {
                        'id': settlement.municipio.id,
                        'name': settlement.municipio.nombre,
                        'c_mnpio': settlement.municipio.c_mnpio,
                        'state': {
                            'id': settlement.municipio.estado.id,
                            'name': settlement.municipio.estado.nombre,
                            'c_estado': settlement.municipio.estado.c_estado
                        }
                    }
                })
            else:
                elements.append({
                    'id': settlement.id,
                    'name': settlement.nombre,
                    'type': settlement.tipo,
                    'id_asenta_cpcons': settlement.id_asenta_cpcons,
                    'c_cve_ciudad': settlement.c_cve_ciudad,
                    'municipality_id': settlement.municipio.id,
                    'state_id': settlement.municipio.estado.id
                })
    except Exception as e:
        print('Error:', str(e))

    return elements
