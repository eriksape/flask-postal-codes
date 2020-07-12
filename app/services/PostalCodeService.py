from flask import current_app as app
from sqlalchemy import desc, asc

from app.models import (
    Estado,
    Municipio,
    Asentamiento
)


def validate_zip_code(country_code, zip_code):
    """Checks if the zip code is a valid one"""
    import re
    from app.consts.PostalCodeRegex import zipcodes_regex
    verify = re.compile(zipcodes_regex[country_code])
    return verify.match(zip_code)


def search(codigo_postal):
    settlements = app.session.query(Asentamiento).filter_by(codigo_postal=codigo_postal).all()
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


def get_settlements(limit=100, offset=0, page=1, sort='codigo_postal', order='ASC'):
    if offset < 1:
        offset = limit * (page - 1)

    settlements = app.session.query(Asentamiento).join(Asentamiento.municipio).join(Municipio.estado)

    if sort == 'codigo_postal':
        sort = Asentamiento.codigo_postal
    elif sort == 'estado':
        sort = Estado.nombre
    elif sort == 'municipio':
        sort = Municipio.nombre

    if order == 'ASC':
        settlements = settlements.order_by(asc(sort)).limit(limit).offset(offset)
    else:
        settlements = settlements.order_by(desc(sort)).limit(limit).offset(offset)

    data = list()
    for settlement in settlements:
        data.append({
            'codigo_postal': settlement.codigo_postal,
            'estado': {
                'codigo': settlement.municipio.estado.c_estado,
                'nombre': settlement.municipio.estado.nombre
            },
            'municipio': {
                'codigo': settlement.municipio.c_mnpio,
                'nombre': settlement.municipio.nombre
            }
        })
    return data


def get_settlements_count():
    settlements = app.session.query(Asentamiento).count()
    return settlements
