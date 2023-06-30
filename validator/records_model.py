from pydantic import BaseModel, validator, Field, ValidationError
import datetime
from typing import Union


class APIData(BaseModel):
    """
    Represents the HTML form validator for adding a new battery.
    """

    barcode: int
    name: str = Field(..., min_length=1, max_length=10)
    color: str = Field(..., min_length=2, max_length=20)
    resistance: float
    voltage: float
    source: str = Field(max_length=50)
    capacity: Union[float, str]
    weight: Union[float, str]
    datetime: str

    @validator('datetime')
    def validate_datetime(cls, value):
        try:
            datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise ValueError('Invalid datetime format. Expected format: %Y-%m-%d %H:%M:%S')
        return value

    @validator('source')
    def validate_source(cls, source):
        if not source:
            return None
        return source

    @validator('name')
    def validate_name(cls, name):
        if not name:
            return None
        return name

    @validator('barcode')
    def validate_barcode(cls, barcode):
        if not isinstance(barcode, int):
            raise ValueError('Barcode must be an integer')
        barcode_str = str(barcode)
        if len(barcode_str) != 6:
            raise ValueError('Barcode must be 6 digits long')
        return barcode

    @validator('resistance')
    def validate_resistance(cls, resistance):
        if not isinstance(resistance, float):
            raise ValueError('Resistance must be a float')
        if resistance > 999.99:
            raise ValueError('Resistance must be between 0.01 and 999.99')
        return resistance

    @validator('voltage')
    def validate_voltage(cls, voltage):
        if not isinstance(voltage, float):
            raise ValueError('Voltage must be a float')
        if voltage > 4.5:
            raise ValueError('Voltage must be between 0 and 4.5')
        return voltage

    @validator('weight')
    def validate_weight(cls, weight):
        if isinstance(weight, str):
            return None
        return weight

    @validator('capacity')
    def validate_capacity(cls, capacity):
        if isinstance(capacity, str):
            return None
        return capacity

