from flask import jsonify, request
from app.api import bp
from app.services.api import APIHandler
from app.services.db import Database


@bp.route('/api/records', methods=['POST'])
def add_record():
    data = request.get_json()
    result = Database.add_record(data)

    if 'error' in result:
        return jsonify(result), 400

    return jsonify({'success': 'Record added successfully.'}), 200


@bp.route('/api/records/<barcode>', methods=['PUT'])
def update_record(barcode):
    record_data = request.get_json()
    result = Database.update_record(barcode=barcode, record_data=record_data)

    response = {'success': 'Record updated successfully.'}

    if 'error' in result:
        response = result

    return jsonify(response), 200


@bp.route('/api/records', methods=['GET'])
def get_records():
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

    response = db_args

    return jsonify(response), 200


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
    if record is None:
        return jsonify({'error': 'Record not found'}), 404

    return jsonify(record), 200


@bp.route('/api/records/<barcode>', methods=['DELETE'])
def delete_record(barcode: int):
    """
    Delete a record from the database by barcode.

    Parameters:
    - barcode: record barcode

    Returns:
    - JSON object with the operation result
    """
    record = Database.delete(barcode)
    if record:
        return jsonify(record), 200
    else:
        return jsonify({'error': 'Record not found.'}), 404

