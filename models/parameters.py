"""
Package Description: This package contains database models that integrate with SQLAlchemy
and provide database support and functionality.
It includes models for various tables related to battery data,
such as names, colors, capacities, currents, sources, voltages, resistances, photos,
and weights. These models allow seamless interaction with the
database, enabling efficient management and retrieval of battery information.

Class and Model Descriptions:
- Name: Represents the 'name' table storing battery names.
- Color: Represents the 'color' table storing battery colors.
- Capacity: Represents the 'capacity' table storing battery capacities.
- Current: Represents the 'current' table storing current values.
- Source: Represents the 'source' table storing battery sources.
- Voltage: Represents the 'voltage' table storing battery voltage values.
- Resistance: Represents the 'resistance' table storing battery resistance values.
- Photo: Represents the 'photo' table storing battery photos.
- Weight: Represents the 'weight' table storing battery weights.
"""

from sqlalchemy import DECIMAL
from app.extensions import db


class Name(db.Model):
    __tablename__ = 'name'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f'<Name "{self.name}">'


class Color(db.Model):
    __tablename__ = 'color'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    color = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f'<Color "{self.color}">'


class Capacity(db.Model):
    __tablename__ = 'capacity'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    capacity = db.Column(db.Integer, unique=True)

    def __repr__(self):
        return f'<Capacity {self.capacity}>'


class Current(db.Model):
    __tablename__ = 'current'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    current = db.Column(DECIMAL(precision=3, scale=2), unique=True)


class Source(db.Model):
    __tablename__ = 'source'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Battery source "{self.source}">'


class Voltage(db.Model):
    __tablename__ = 'voltage'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    voltage = db.Column(DECIMAL(precision=3, scale=2), unique=True, nullable=False)

    def __repr__(self):
        return f'<Battery voltage "{self.voltage}">'


class Resistance(db.Model):
    __tablename__ = 'resistance'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resistance = db.Column(DECIMAL(precision=5, scale=2), unique=True, nullable=False)

    def __repr__(self):
        return f'<Battery resistance "{self.resistance}">'


class Photo(db.Model):
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo = db.Column(db.LargeBinary)


class Weight(db.Model):
    __tablename__ = 'weight'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    weight = db.Column(DECIMAL(precision=4, scale=3), unique=True)