from MyvarpLanguageInterpretor.utils.collections.script_reader import ScriptReader


class MyvarpScript:
    _s_enum: ScriptReader

    _run_type = None  # console or file
    _source = None
    _temp = None
    _return = None
    _lines = ""  # an enumeration of file lines
    _output = None
    _status = None
    _environ = None

    def __init__(self, script_source, run_type='file'):
        self._s_enum = ScriptReader(script_source)

    def initialize_fields(self):
        self._environ = {
            'info': {
                'name': '',
                'size': '',
                'path': '',
                'file_name': '',
                'line_start': '',
                'line_end': ''
            },
            'temp': {},
            'classes': {},
            'functions': {},
            'variables': {}
        }

    def get_environ(self):
        pass

    def add_environ(self):
        pass

    def set_status(self):
        pass

    def get_status(self):
        pass

    def get_return_value(self):
        pass

    def set_return_value(self):
        pass

    def get_lines(self):
        pass

    def set_lines(self):
        pass

    def import_to_module(self):
        pass

    def import_module(self):
        pass

    def get_return_value(self):
        pass

    def add_argument(self):
        pass

    def get_argument_value(self):
        pass

    def set_argument_value(self):
        pass

    def add_class(self):
        pass

    def get_class(self):
        pass

    def add_method(self):
        pass

    def get_method(self):
        pass

    def add_variable(self):
        pass

    def get_variable(self):
        pass

    def has_variable(self):
        pass

    def has_function(self):
        pass

    def has_class(self):
        pass

    def run_method(self):
        pass
