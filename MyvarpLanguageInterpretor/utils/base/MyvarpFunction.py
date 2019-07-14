from MyvarpLanguageInterpretor.utils.base.MyvarpClass import MyvarpClass


class MyvarpFunction(MyvarpClass):

    _func_dict_: dict

    def __init__(self):
        super().__init__()
        self._func_dict_ = {
            'params': {
                'arguments': ['args', 'start', 'sep', 'endl', 'kwargs'],
                'defaults': {'start': '', 'sep': ' ', 'endl': '\n', 'kwargs': {}}
            },
            'method': self.__dict__,
            'return': None
        }
