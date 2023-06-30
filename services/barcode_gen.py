import random
from app import db
from app.models.records import BatteryData


def barcode_gen() -> int:
    """
      Generate a unique barcode number.

      This function checks for the presence of a barcode in the database table.
      If no barcode exists, it generates a unique barcode number and returns it.

      Returns:
          int: Unique barcode number.
      """
    existing_barcodes = db.session.query(BatteryData.barcode).all()
    existing_barcodes = set(barcode[0] for barcode in existing_barcodes)

    while True:
        barcode = random.randint(100000, 999999)
        if barcode not in existing_barcodes:
            return barcode
