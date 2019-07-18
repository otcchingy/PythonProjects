from MyvarpLanguageInterpretor.MyvarpScriptManager import MyvarpScriptReader, DEFAULT_ENVIRON


class MyvarpScriptInterpreter(MyvarpScriptReader):
    _script_reader: MyvarpScriptReader
    _script_source = None  # console or file
    _source = None
    _temp = None
    _return = None
    _lines = ""  # an enumeration of file lines
    _status = None
    _environ = None

    def __init__(self, script_lines='', **kwargs):
        name = ''
        path = ''
        size = 0
        start = 0
        stop = 0
        script_source = ''

        try:
            stop = 0 if kwargs['stop'] is not None and kwargs['stop'] == 0 else kwargs['stop']
        except KeyError:
            stop = 0

        try:
            start = 0 if kwargs['start'] is not None and kwargs['start'] == 0 else kwargs['start']
        except KeyError:
            start = 0

        try:
            name = '' if kwargs['name'] is not None and kwargs['name'] == 0 else kwargs['name']
        except KeyError:
            name = ''

        try:
            path = '' if kwargs['path'] is not None and kwargs['path'] == 0 else kwargs['path']
        except KeyError:
            path = ''

        try:
            script_source = 'console' if kwargs['script_source'] is None or \
                                         kwargs['script_source'] not in ['console', 'file'] else kwargs['script_source']
        except KeyError:
            script_source = 'console'

        self._script_source = script_source
        self._environ = DEFAULT_ENVIRON
        self._environ['info']['line_stop'] = stop
        self._environ['info']['line_start'] = start
        self._environ['info']['script_name'] = name
        self._environ['info']['script_path'] = path

        self._script_reader = MyvarpScriptReader(script_lines=script_lines, start=start, stop=stop),

    def get_environ(self):
        return self._environ

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

    def import_to_module(self):
        pass

    def import_module(self):
        pass

    def add_argument(self):
        pass

    def get_argument_value(self):
        pass

    def set_argument_value(self):
        pass

    def build_variable(self):
        pass

    def build_method(self):
        pass

    def build_class(self):
        pass

    def instantiate_class(self):
        pass

    def perform_operation(self):
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

    def __interpret_expression_data(self):
        # TODO : recreate get comment and get string with multiple line string and comments

        """
        condition                       expect


        *single line comment            next line

        *multiple line comment          end of multiple line comment - ''' ### */

        *string opener   ' "           end for string opener - ''' ### */

        *stack.is empty                  keyword - builtins
                                        data - int, bool, string etc
                                        identifier : function , variable name

        *identifier                     operation
                                        assignment
                                        method call
                                        next line | enter key
                                        parenthesis_closer

        *operator                       raw data
                                        identifier
                                        next line | spaces

        *function opener                function closer
                                        identifier
                                        raw data
                                        keyword arguments (assignment in parenthesis, type hinting, type declaration)
                                        //NOTE : type declaration can be var_name = data_type | var_name as data_type

        *collection [] {} ()            expect group item(s) or index or key for []

        *circle brackets ()             ; : | {

        public private protected        identifier | class | interface | abstract

        @  and .                        identifier

        string                          ; or space or () function call

        , comma                         identifier | raw data

        after scope ends pop scope opener with closer eg { - } |  : anything else



        :return:
        """
