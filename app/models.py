from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from .database import Base
import datetime


class DictMixIn:
    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            if not isinstance(
                getattr(self, column.name), (datetime.datetime, datetime.date)
            )
            else getattr(self, column.name).isoformat()
            for column in self.__table__.columns
        }

class Estado(Base, DictMixIn):
    """
        Modelo para estados
    """
    __tablename__ = 'estado'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    #municipios = relationship('Municipio', backref='estado', lazy='dynamic')
    c_estado = Column(String(32))
    municipio = relationship('Municipio',
                                 back_populates='estado')

class Municipio(Base, DictMixIn):
    """
        Modelo para municipios
    """
    __tablename__ = 'municipio'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    estado_id = Column(Integer, ForeignKey('estado.id'))
    c_mnpio = Column(String(32))
    asentamientos = relationship('Asentamiento', back_populates='municipio')
    estado = relationship("Estado", back_populates="municipio")


class Asentamiento(Base, DictMixIn):
    """
        Modelo para colonias
    """
    __tablename__ = 'asentamiento'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    tipo = Column(String(50))
    codigo_postal = Column(String(16))
    ciudad = Column(String(64))
    municipio_id = Column(Integer, ForeignKey('municipio.id'))
    codigo_oficina_postal = Column(String(16))
    zona = Column(String(50))
    id_asenta_cpcons = Column(String(32))
    c_cve_ciudad = Column(String(32))
    municipio = relationship("Municipio", back_populates="asentamientos")


class Deployed(Base, DictMixIn):
    """
        Modelo para colonias
    """
    __tablename__ = 'deployed'
    ms_time = Column(BigInteger, primary_key=True)


