import json

from flask import jsonify, request
from app.api import bp
from app.services.api import APIHandler
from app.services.db import Database


@bp.route('/api/records/<barcode>', methods=['UPDATE'])
def update_record(barcode):
    record_data = request.get_json()
    record = Database.update_record(barcode=barcode, record_data=record_data)
    print(record)
    return 'ok'


@bp.route('/api/records', methods=['GET'])
def get_records():
    request_counts = {}

    max_requests_per_second = 1

    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'The token not is exist'}), 401

    if token in request_counts:
        request_counts[token] += 1
    else:
        request_counts[token] = 1

    if request_counts[token] > max_requests_per_second:
        return jsonify({'error': 'Перевищено ліміт запитів на секунду.'}), 429

    args_list = request.args.to_dict()
    args_handler = APIHandler.sorting_args_handler(args_list)
    db_args = Database.get_records_by_sorting(args_handler)

    order_by = args_list.get('order_by')
    sort_by = args_list.get('sort_by')

    if order_by:
        if order_by == 'desc':
            db_args = sorted(db_args, key=lambda x: x.get(sort_by, 0), reverse=True)
        elif order_by == 'asc':
            db_args = sorted(db_args, key=lambda x: x.get(sort_by, 0))
    elif sort_by:
        db_args = sorted(db_args, key=lambda x: x.get(sort_by, 0))

    return jsonify(db_args, 200)


@bp.route('/api/records', methods=['POST'])
def add_records():
    data = json.loads(request.get_json())
    print(Database.add_record(data))
    return jsonify(200)


@bp.route('/api/records/<barcode>', methods=['GET'])
def get_record(barcode):
    """
    Get a record from the database by barcode.

    Parameters:
    - barcode: record barcode

    Returns:
    - JSON object with the record data or an error message
    """
    record = Database.get_record_by_barcode(barcode=barcode)
    if isinstance(record, dict):
        return jsonify(record), 400

    return jsonify(record, 200)


@bp.route('/api/records/delete/<barcode>', methods=['DELETE'])
def delete_record(barcode: int):
    """
    Delete a record from the database by barcode.

    Parameters:
    - barcode: record barcode

    Returns:
    - JSON object with the operation result
    """
    record = Database.delete(barcode)
    print(record)
    return record
