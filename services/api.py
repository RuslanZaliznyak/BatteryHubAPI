import datetime

from flask import request
from app.models.parameters import Voltage, Capacity, Resistance, Name, Color, Source
from app.services.barcode_gen import barcode_gen
from app.validator.records_model import APIData


class APIHandler:
    @classmethod
    def sorting_args_handler(cls, args_list):
        """
        Handle sorting arguments and generate sorting conditions for SQLAlchemy query.

        Args:
        - args_list: a dictionary of sorting arguments

        Returns:
        - A list of SQLAlchemy filtering conditions
        """
        args = ['min_voltage', 'max_voltage',
                'min_capacity', 'max_capacity', 'min_resistance',
                'max_resistance', 'name', 'color', 'source']

        args_validate = {}

        for arg in args:
            if arg in args_list and args_list[arg] != '':
                args_validate[arg] = args_list[arg]

        sorting_conditions = []

        if 'min_voltage' in args_validate and 'max_voltage' in args_validate:
            sorting_conditions.append(Voltage.voltage.between(
                args_validate['min_voltage'],
                args_validate['max_voltage']
            ))

        if 'min_voltage' in args_validate:
            sorting_conditions.append(Voltage.voltage > args_validate['min_voltage'])

        if 'max_voltage' in args_validate:
            sorting_conditions.append(Voltage.voltage < args_validate['max_voltage'])

        if 'min_resistance' in args_validate and 'max_resistance' in args_validate:
            sorting_conditions.append(Resistance.resistance.between(
                args_validate['min_resistance'],
                args_validate['max_resistance']
            ))

        if 'min_resistance' in args_validate:
            sorting_conditions.append(Resistance.resistance > args_validate['min_resistance'])

        if 'max_resistance' in args_validate:
            sorting_conditions.append(Resistance.resistance < args_validate['max_resistance'])

        if 'min_capacity' in args_validate and 'max_capacity' in args_validate:
            sorting_conditions.append(Capacity.capacity.between(
                args_validate['min_capacity'],
                args_validate['max_capacity']
            ))

        if 'min_capacity' in args_validate:
            sorting_conditions.append(Capacity.capacity > args_validate['min_capacity'])

        if 'max_capacity' in args_validate:
            sorting_conditions.append(Capacity.capacity < args_validate['max_capacity'])

        if 'name' in args_validate:
            sorting_conditions.append(Name.name == args_validate['name'])

        if 'color' in args_validate:
            sorting_conditions.append(Color.color == args_validate['color'])

        if 'source' in args_validate:
            sorting_conditions.append(Source.source == args_validate['source'])

        return sorting_conditions

    @classmethod
    def records_handler(cls, data_form: request):
        """
        Handle records data from the request and convert it into a list of APIData objects.

        Args:
        - data_form: the request object

        Returns:
        - A list of APIData objects representing the records data
        """
        try:
            json_records = data_form.get_json()
            current_datetime = \
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            api_data = APIData(
                    barcode=int(barcode_gen()),
                    name=json_records['name'],
                    color=json_records['color'],
                    resistance=float(json_records['resistance']),
                    voltage=float(json_records['voltage']),
                    source=json_records['source'],
                    capacity=int(json_records['capacity']),
                    weight=float(json_records['weight']),
                    datetime=current_datetime)
            return api_data
        except KeyError as ex:
            return f"Missing key in JSON record: {ex}"
        except (TypeError, ValueError) as ex:
            return f"Invalid value in JSON record: {ex}"
        except Exception as ex:
            return f"Error processing JSON records: {ex}"

