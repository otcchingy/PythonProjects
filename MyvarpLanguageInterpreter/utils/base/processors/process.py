class Process:
    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def get(self, key):
        try:
            return self._kwargs[f'{key}']
        except KeyError:
            return None

    def set(self, key, value):
        self._kwargs[f'{key}'] = value

    def set_type(self, value):
        self.set('type', value)

    def set_object(self, value):
        self.set('object', value)

    def set_method(self, value):
        self.set('method', value)

    def set_args(self, value):
        self.set('args', value)

    def set_result(self, value):
        self.set('result', value)

    def set_state(self, value):
        self.set('state', value)

    def get_type(self):
        return self.get('type')

    def get_object(self):
        return self.get('object')

    def get_method(self):
        return self.get('method')

    def get_args(self):
        return self.get('args')

    def get_result(self):
        return self.get('result')

    def get_state(self):
        return self.get('state')

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'Process({self._kwargs})'
