from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String

from zezin.app import db


class Partner(db.Model):
    _id = Column('id', Integer, autoincrement=True, primary_key=True)
    trading_name = Column(String(50), nullable=False)
    owner_name = Column(String(50), nullable=False)
    document = Column(String(50), nullable=False, unique=True)
    coverage_area = Column(Geometry(geometry_type='MULTIPOLYGON'))
    address = Column(Geometry(geometry_type='POINT'))
