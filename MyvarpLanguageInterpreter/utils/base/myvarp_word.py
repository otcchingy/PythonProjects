
class Word:
    def __init__(self, _type, _value):
        self._type = _type
        self._value = _value

    def is_type_of(self, name):
        if name in self._type:
            return True
        return False

    def is_type_any(self, names):
        for name in names:
            if name in self._type:
                return True
        return False

    def is_match(self, names):
        for name in names:
            if name == self._value:
                return True
        return False

    def get_type(self):
        return self._type

    def get_value(self):
        return self._value

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'Word({self.get_type()}: {self.get_value()})'
