from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Estado(db.Model):
    """
        Modelo para estados
    """
    __tablename__ = 'estado'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    municipios = db.relationship('Municipio', backref='estado', lazy='dynamic')
    c_estado = db.Column(db.String(32))

    def __init__(self, nombre, c_estado):
        self.nombre = nombre
        self.c_estado = c_estado


class Municipio(db.Model):
    """
        Modelo para municipios
    """
    __tablename__ = 'municipio'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    estado_id = db.Column(db.Integer, db.ForeignKey('estado.id'))
    asentamientos = db.relationship('Asentamiento', backref='municipio', lazy='dynamic')
    c_mnpio = db.Column(db.String(32))

    def __init__(self, nombre, estado_id, c_mnpio):
        self.nombre = nombre
        self.estado_id = estado_id
        self.c_mnpio = c_mnpio


class Asentamiento(db.Model):
    """
        Modelo para colonias
    """
    __tablename__ = 'asentamiento'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    tipo = db.Column(db.String(50))
    codigo_postal = db.Column(db.String(16))
    ciudad = db.Column(db.String(64))
    municipio_id = db.Column(db.Integer, db.ForeignKey('municipio.id'))
    codigo_oficina_postal = db.Column(db.String(16))
    zona = db.Column(db.String(50))
    id_asenta_cpcons = db.Column(db.String(32))
    c_cve_ciudad = db.Column(db.String(32))

    def __init__(self, nombre,
                       tipo,
                       codigo_postal,
                       ciudad,
                       municipio_id,
                       id_asenta_cpcons,
                       codigo_oficina_postal = None,
                       zona = None,
                       c_cve_ciudad=None):
        self.nombre = nombre
        self.tipo = tipo
        self.codigo_postal = codigo_postal
        self.ciudad = ciudad
        self.municipio_id = municipio_id
        self.id_asenta_cpcons = id_asenta_cpcons
        self.codigo_oficina_postal = codigo_oficina_postal
        self.zona = zona
        self.c_cve_ciudad = c_cve_ciudad
