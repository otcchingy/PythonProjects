import logging

from utils.collections.script_reader import ScriptReader
from utils.builtins.helper_functions import *

"""
configuring logger
"""

logging.basicConfig(format="%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s", level=logging.DEBUG)
# logging.disable(logging.DEBUG)
logger = logging.getLogger(__name__)


class MyvarpScriptReader:
    #  script fields
    _lines: str
    _lines_count: int

    #  builder fields

    _script: ScriptReader
    _string_active: str
    _group_data: str
    _group_type: str

    def __init__(self, script_lines='', **kwargs):

        self._lines = ''
        self._lines_count = 0
        self._group_type = ''
        self._string_active = ''
        self._group_data = ''

        try:
            stop = 0 if kwargs['stop'] is not None and kwargs['stop'] == 0 else kwargs['stop']
        except KeyError:
            stop = 0

        try:
            start = 0 if kwargs['start'] is not None and kwargs['start'] == 0 else kwargs['start']
        except KeyError:
            start = 0

        self._script = ScriptReader(script_lines, start=start, stop=stop)

    def add_line(self, line):
        self._prepare_line(line)
        self._script.add_all_items(line)

    def _prepare_line(self, line):
        self._lines += line

    def _get_lines_count(self):
        return self._lines_count

    def validate_file_as_script(self):
        # check if string is valid file path
        # check if file has extension .mv
        pass

    def is_string_active(self):
        return self._string_active != ''

    def is_comments_active(self):
        return self._group_type != '' and not self.is_string_active()

    def get_script(self):
        return self._script

    def has_next(self):
        return self._script.has_next()

    def has_next_not_space(self):
        return self._script.has_next_not_space()

    def move_to_next_not_space(self):
        return self._script.move_to_next_not_space()

    def has_next_needed(self):
        return self._script.has_next_not_in(' \t\b\a')

    def move_to_next_needed(self):
        return self._script.move_to_next_not_in(' \t\b\a')

    def get_next(self):
        element = self._script.get_next()
        if not element:
            return False
        return element

    def get_next_not_space(self):
        element = self._script.get_next_not_space()
        if not element:
            return False
        return element

    def get_next_data_object(self):
        return self.get_next_not_space()

    def get_next_number(self):
        number = ''
        if self._script.is_next_number():
            number += self.get_next_not_space()
            if self._script.peek_next() == '.':
                number += self.get_next()
                if self._script.is_next_number():
                    number += self.get_next()
                    return number
                else:
                    number += self.get_next()
                    return '--error--:' + number
            else:
                return number

    def get_next_string(self):

        if self._script.is_next_string() or self.is_string_active():
            if self._script.peek_next() in ['`', "'", '"'] and not self.is_string_active():
                self._group_type = 'single'
                self._string_active = self._script.peek_next()
                self._group_data += "'"
                self.get_next()

            elif self._script.peek_next() in ['"""', "'''"] and not self.is_string_active():
                self._group_type = 'multi'
                self._string_active = self._script.peek_next()
                self._group_data += "'"
                self.get_next()

            escape = False

            while self.has_next():
                data = self.get_next()

                if not escape and data == self._string_active:
                    self._group_type = ''
                    self._group_data += "'"
                else:
                    for i in data:
                        if i == '\\' and not escape:
                            escape = True
                        elif escape:
                            escape = False

                        self._group_data += i

                if self._group_type == '':
                    break

    def get_next_bool_expression(self):
        return self.get_next_not_space()

    def get_next_parenthesis_opener(self):  # takes argument to match default - any
        return self.get_next_not_space()

    def get_next_parenthesis_closer(self):  # takes arg to make default - any
        return self.get_next_not_space()

    def get_next_function_call(self):
        return self.get_next_not_space()

    def get_next_method_call(self):
        return self.get_next_not_space()

    def get_next_operator(self):
        _operator = ''

        while self._script.is_next_operator():
            op = _operator + self._script.peek_next()
            if is_operator(op):
                _operator += self.get_next()
            else:
                break

        return _operator

    def get_next_comment(self):

        if self._script.is_next_comment() or self.is_comments_active():
            if self._script.peek_next() == '#' and not self.is_comments_active():
                self.get_next()
                self._group_type = 'single'
            elif self._script.peek_next() in ['###', '/*'] and not self.is_comments_active():
                self.get_next()
                self._group_type = 'multi'

            while self.has_next():
                if self._group_type == 'single':
                    if self._script.is_next_new_line():
                        self._group_type = ''
                        break
                    self.get_next()
                else:
                    if self._group_type == 'multi':
                        if self._script.is_next_comment() and self._script.peek_next() in ['###', '*/']:
                            self.get_next_not_space()
                            self._group_type = ''
                            break
                        self.get_next()

            if self._group_type == 'single':
                self._group_type = ''

    def get_next_arguments(self):
        return self.get_next_not_space()

    def get_next_scope(self):
        return self.get_next_not_space()

    def get_next_collection(self):
        if self._script.is_next_group():

            # get group then get type

            if self._script.is_next_group():
                self.add_expression_data({'data.collection.tuple': self.get_next_not_space()})
            elif self._script.is_next_bool():
                self.add_expression_data({'data.collection.list': self.get_next_not_space()})
            elif self._script.is_next_byte():
                self.add_expression_data({'data.collection.dict': self.get_next_not_space()})
            elif self._script.is_next_float():
                self.add_expression_data({'data.collection.set': self.get_next_not_space()})

    def has_string_data(self):
        if self.is_string_active() and self._group_data and not self._group_type:
            # logger.debug('has string data')
            return True

    def get_string_data(self):
        if self.has_next():
            temp = self._group_data
            self._group_data = ''
            self._string_active = ''
            return eval(f'"{temp}"')
        return ''

    def get_next_line(self):
        return self.get_next_not_space()
