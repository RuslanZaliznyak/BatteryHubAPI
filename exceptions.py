class EmptyFieldError(Exception):
    def __init__(self, field_name):
        self.field_name = field_name

    def __str__(self):
        return f'Field is empty: {self.field_name}'
