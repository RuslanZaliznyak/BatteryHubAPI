"""
Provides database functionality and integration with SQLAlchemy.
"""

from app.extensions import db


class BatteryData(db.Model):
    """
    Model representing the 'battery_data' table.
    This is the main table. The main parameters are stored here

    Attributes:
    id (int): The primary key of the table.
    barcode (int): The unique barcode of the battery.
    stock_params_id (int): Foreign key referencing the 'stock_parameters' table.
    real_params_id (int): Foreign key referencing the 'real_parameters' table.
    source_id (int): Foreign key referencing the 'source' table.
    photo_id (int): Foreign key referencing the 'photo' table.
    timestamp (DateTime): The timestamp of the battery data.
    """

    __tablename__ = 'battery_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    barcode = db.Column(db.Integer, unique=True, nullable=False)
    stock_params_id = db.Column(db.ForeignKey('stock_parameters.id'))
    real_params_id = db.Column(db.ForeignKey('real_parameters.id'))
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'))
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'))
    datetime = db.Column(db.DateTime)

    stock_params = db.relationship('StockParameters', backref='battery_data')
    real_params = db.relationship('RealParameters', backref='battery_data')
    source = db.relationship('Source', backref='battery_data')
    photo = db.relationship('Photo', backref='battery_data')


class StockParameters(db.Model):
    """
        Model representing the 'stock_parameters' table.
        Here are the stock batteries parameters

        Attributes:
        id (int): The primary key of the table.
        name_id (int): Foreign key referencing the 'name' table.
        capacity_id (int): Foreign key referencing the 'capacity' table.
        resistance_id (int): Foreign key referencing the 'resistance' table.
        charge_current_id (int): Foreign key referencing the 'current' table.
        max_charge_current_id (int): Foreign key referencing the 'current' table.
        discharge_current_id (int): Foreign key referencing the 'current' table.
        max_discharge_current_id (int): Foreign key referencing the 'current' table.
        """

    __tablename__ = 'stock_parameters'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_id = db.Column(db.Integer, db.ForeignKey('name.id'))
    capacity_id = db.Column(db. Integer, db.ForeignKey('capacity.id'))
    resistance_id = db.Column(db.Integer, db.ForeignKey('resistance.id'))
    charge_current_id = db.Column(db.Integer, db.ForeignKey('current.id'))
    max_charge_current_id = db.Column(db. Integer, db.ForeignKey('current.id'))
    discharge_current_id = db.Column(db.Integer, db.ForeignKey('current.id'))
    max_discharge_current_id = db.Column(db.Integer, db.ForeignKey('current.id'))


class RealParameters(db.Model):
    """
        Model representing the 'real_parameters' table.
        This is a table model where the actual battery parameters are stored

        Attributes:
        id (int): The primary key of the table.
        name_id (int): Foreign key referencing the 'name' table.
        color_id (int): Foreign key referencing the 'color' table.
        capacity_id (int): Foreign key referencing the 'capacity' table.
        resistance_id (int): Foreign key referencing the 'resistance' table.
        voltage_id (int): Foreign key referencing the 'voltage' table.
        weight_id (int): Foreign key referencing the 'weight' table.
        """

    __tablename__ = 'real_parameters'
    id = db.Column(db. Integer, primary_key=True, autoincrement=True)
    name_id = db.Column(db.Integer, db.ForeignKey('name.id'))
    color_id = db.Column(db.Integer, db.ForeignKey('color.id'), nullable=False)
    capacity_id = db.Column(db.Integer, db.ForeignKey('capacity.id'))
    resistance_id = db.Column(db.Integer, db.ForeignKey('resistance.id'), nullable=False)
    voltage_id = db.Column(db.Integer, db.ForeignKey('voltage.id'), nullable=False)
    weight_id = db.Column(db.Integer, db.ForeignKey('weight.id'))

    name = db.relationship('Name', backref='real_parameters')
    color = db.relationship('Color', backref='real_parameters')
    capacity = db.relationship('Capacity', backref='real_parameters')
    resistance = db.relationship('Resistance', backref='real_parameters')
    voltage = db.relationship('Voltage', backref='real_parameters')
    weight = db.relationship('Weight', backref='real_parameters')
