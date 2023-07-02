import datetime
import importlib
import json
from pprint import pprint
from typing import List, Dict, Any
from app.services.barcode_gen import barcode_gen
from flask import abort
from sqlalchemy import exc, asc, text, desc, update

from app.extensions import db
from app.models.parameters import Name, Color, Source, Voltage, Resistance, Capacity, Weight
from app.models.records import BatteryData, RealParameters, StockParameters
from app.validator.records_model import APIData
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions import EmptyFieldError


class Database:
    """
    Database Class

    This class provides methods for interacting with the database.

    Methods:
        serialize_record(record): Serialize a database record to a dictionary.
        query_to_db(): Generate the base query for retrieving records from the database.
        get_or_create_record(model, field_name, value): Get or create a record in the specified table.
        add_record(records): Add multiple records to the database.
        get_records_by_sorting(res): Get records from the database based on sorting conditions.
        get_record_by_barcode(barcode): Get a record from the database by barcode.
        get_records_by_limit(limit_records): Get a specified number of records from the database.
        get_records(): Get all records from the database.
        delete(barcode): Delete a record from the database by barcode.
    """

    @classmethod
    def process_data_to_database(cls, record_data: dict):
        try:
            print(f'process_data_to_database: {record_data}')

            name_id = cls.get_or_create_record(Name, 'name',
                                               record_data['name'])
            color_id = cls.get_or_create_record(Color, 'color',
                                                record_data['color'])
            voltage_id = cls.get_or_create_record(Voltage, 'voltage',
                                                  record_data['voltage'])
            resistance_id = cls.get_or_create_record(Resistance, 'resistance',
                                                     record_data['resistance'])
            capacity_id = cls.get_or_create_record(Capacity, 'capacity',
                                                   record_data['capacity'])
            weight_id = cls.get_or_create_record(Weight, 'weight',
                                                 record_data['weight'])
            source_id = cls.get_or_create_record(Source, 'source',
                                                 record_data['source'])
            print('before params')
            params = RealParameters.query.filter_by(name_id=name_id,
                                                    color_id=color_id,
                                                    resistance_id=resistance_id,
                                                    voltage_id=voltage_id,
                                                    capacity_id=capacity_id,
                                                    weight_id=weight_id
                                                    ).first()
            print(params)
            if not params:
                new_params = RealParameters(name_id=name_id,
                                            color_id=color_id,
                                            resistance_id=resistance_id,
                                            voltage_id=voltage_id,
                                            capacity_id=capacity_id,
                                            weight_id=weight_id
                                            )
                db.session.add(new_params)
                db.session.flush()
                params_id = new_params.id
            else:
                params_id = params.id

            return {'params_id': params_id, 'source_id': source_id}
        except SQLAlchemyError as ex:
            error_msg = f"Error occurred while processing data to the database: {ex}"

    @classmethod
    def update_record(cls, barcode, record_data: dict):
        try:
            record = cls.get_record_by_barcode(barcode=barcode)
            processed_data_ids = cls.process_data_to_database(record_data)

            update_stmt = update(BatteryData).where(BatteryData.id == record['id']).values(
                barcode=barcode,
                real_params_id=processed_data_ids['params_id'],
                source_id=processed_data_ids['source_id'],
                datetime=datetime.datetime.now()
            )
            db.session.execute(update_stmt)
            db.session.commit()

            return {'status': 'Record updated successfully.'}
        except SQLAlchemyError as ex:
            error_msg = f"Error occurred while updating record: {ex}"
            return {'error': error_msg, 'description': 'Database error'}
        except Exception as ex:
            error_msg = f"Error occurred while updating record: {ex}"
            return {'error': error_msg, 'description': 'Unknown error'}

    @classmethod
    def serialize_record(cls, record) -> Dict[str, Any]:
        try:
            return {
                'id': record.id,
                'barcode': record.barcode,
                'name': record.name if record.name is not None else 'Unknown',
                'color': record.color,
                'voltage': float(record.voltage),
                'resistance': float(record.resistance),
                'source': record.source if record.source is not None else 'Unknown',
                'weight': float(record.weight) if record.weight is not None else 'Unknown',
                'capacity': int(record.capacity) if record.capacity is not None else 'Unknown',
                'datetime': record.datetime
            }
        except Exception as ex:
            error_msg = f"Error occurred while serializing record: {ex}"
            return {'error': error_msg, 'description': 'Serialization error'}

    @classmethod
    def query_to_db(cls):
        try:
            query = db.session.query(
                BatteryData.id,
                BatteryData.barcode,
                BatteryData.datetime,
                Name.name,
                Color.color,
                Voltage.voltage,
                Resistance.resistance,
                Source.source,
                Weight.weight,
                Capacity.capacity
            ).join(
                RealParameters, BatteryData.real_params_id == RealParameters.id
            ).outerjoin(
                Source, BatteryData.source_id == Source.id
            ).outerjoin(
                Name, RealParameters.name_id == Name.id
            ).join(
                Color, RealParameters.color_id == Color.id
            ).join(
                Resistance, RealParameters.resistance_id == Resistance.id
            ).join(
                Voltage, RealParameters.voltage_id == Voltage.id
            ).outerjoin(
                Weight, RealParameters.weight_id == Weight.id
            ).outerjoin(
                Capacity, RealParameters.capacity_id == Capacity.id
            )
            return query
        except Exception as ex:
            error_msg = f"Error occurred while generating the database query: {ex}"

    @classmethod
    def get_or_create_record(cls, model, field_name, value) -> Any | None:
        try:
            print('get or create record')
            record = model.query.filter_by(**{field_name: value}).first()
            if model == Source and field_name == 'source' and value is None:
                return None

            if record is None:
                new_record = model(**{field_name: value})
                db.session.add(new_record)
                db.session.flush()
                db.session.refresh(new_record)
                return new_record.id
            return record.id
        except Exception as ex:
            return f"Error occurred while getting or creating a record: {ex}"

    @classmethod
    def add_record(cls, record: dict) -> dict[str, str] | dict[str, str] | list[dict[str, str | int]]:
        try:
            print(f'add_record: {record}')
            processed_data_ids = cls.process_data_to_database(record_data=record)

            new_record = BatteryData(barcode=barcode_gen(),
                                     real_params_id=processed_data_ids['params_id'],
                                     source_id=processed_data_ids['source_id'],
                                     datetime=datetime.datetime.now())
            db.session.add(new_record)
            db.session.commit()
            return {'success': 'Record added successfully.'}
        except SQLAlchemyError as ex:
            error_msg = f"Error occurred while adding record: {ex}"
            return {'error': error_msg, 'description': 'Database error'}
        except Exception as ex:
            error_msg = f"Error occurred while adding record: {ex}"
            return {'error': error_msg, 'description': 'Unknown error'}

    @classmethod
    def get_records_by_sorting(cls, res: dict) -> list[dict[str, Any]] | dict[str, str]:
        try:
            query = cls.query_to_db()
            records = query.filter(*res).all()

            records_list = [cls.serialize_record(record) for record in records]
            return records_list
        except Exception as ex:
            error_msg = f"Error occurred while retrieving records by sorting: {ex}"
            return {'error': error_msg, 'description': 'Unknown error'}

    @classmethod
    def get_record_by_barcode(cls, barcode: int) -> Dict[str, Any]:
        """
        Retrieves a record from the database based on the barcode.

        Args:
            barcode (int): The barcode of the record.

        Returns:
            Dict[str, Any]: A dictionary representing the retrieved record.
        """
        if not isinstance(barcode, int) and len(str(barcode)) != 6:
            return {'error': 'Barcode must be an int and a 6-digit number.'}

        record = cls.query_to_db().filter(BatteryData.barcode == int(barcode)).first()

        if record is None:
            return {'error': 'Record is None or empty'}

        return cls.serialize_record(record)

    @classmethod
    def get_records_by_limit(cls, limit_records: int) -> dict[str, str] | dict[str, str] | list[dict[str, Any]]:
        """
        Retrieves a specific number of records from the database based on a limit.

        Args:
            limit_records (int): The maximum number of records to retrieve.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the retrieved records.
        """
        query = cls.query_to_db()

        if not isinstance(limit_records, int) and limit_records < 0:
            return {'error': 'Limit records must be a positive integer'}

        records = query.order_by(BatteryData.datetime.desc()).limit(limit_records).all()

        if not records:
            return {'error': 'Records is None or empty'}

        records_list = [cls.serialize_record(record) for record in records]
        return records_list

    @classmethod
    def get_records(cls) -> dict[str, str] | list[dict[str, Any]]:
        """
        Retrieves all records from the database.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the retrieved records.
        """
        query = cls.query_to_db()

        records = query.all()

        if not records:
            return {'error': 'Records is None'}

        records_list = [cls.serialize_record(record) for record in records]
        return records_list

    @classmethod
    def delete(cls, barcode: int) -> Dict[str, Any]:
        """
        Deletes a record from the database based on the barcode.

        Args:
            barcode (int): The barcode of the record to be deleted.

        Returns:
            Dict[str, Any]: A dictionary representing the result of the deletion.
        """
        try:
            record = db.session.query(BatteryData).filter(
                BatteryData.barcode == int(barcode)).first()

            if record:
                db.session.delete(record)
                db.session.commit()
                return {'success': 'Record deleted successfully.'}
            else:
                return {'error': 'Record not found.'}

        except exc.IntegrityError as ex:
            db.session.rollback()
            return {'error': f'Integrity error occurred: {ex}'}
