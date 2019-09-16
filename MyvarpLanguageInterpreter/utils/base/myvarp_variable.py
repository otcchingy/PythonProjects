

class MyvarpVariable:
    _name = None
    _value = None
    _type = None

    def __init__(self):
        pass

    def set_variable_name(self, name):
        self._name = name

    def set_variable_value(self, value):
        self._value = value

    def get_variable_name(self):
        return self._name

    def get_variable_value(self):
        return self._value

    def get_variable_type(self):
        # TODO : get type from myvarp object in value
        return type(self._value)

    def to_string(self):
        # TODO : get tostring from myvarp object in value
        return str(self._value)
