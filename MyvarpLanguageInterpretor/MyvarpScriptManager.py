# import date
# import datetime
# import subprocess
import logging

from MyvarpLanguageInterpretor.utils.collections.script_reader import ScriptReader
from MyvarpLanguageInterpretor.utils.builtins.helper_functions import *
from MyvarpLanguageInterpretor.utils.collections.stack import Stack

"""
configuring logger
"""

logging.basicConfig(format="%(levelname)-8s [%(lineno)d] %(message)s", level=logging.DEBUG)
# logging.disable(logging.DEBUG)
logging = logging.getLogger(__name__)


class MyvarpScriptReader:
    #  script fields
    _lines: str
    _lines_count: int

    #  builder fields

    _script: ScriptReader
    _builder_stack: Stack
    _string_active: str
    _group_data: str
    _group_type: str
    _possible_expression_hint: list
    _previous_expression_hint: Stack
    _full_expression_data: list
    _current_expression_data: list

    def __init__(self, script_lines='', **kwargs):

        self._lines = ''
        self._lines_count = 0
        self._group_type = ''
        self._string_active = ''
        self._group_data = ''
        self._builder_stack = Stack()
        self._possible_expression_hint = []
        self._previous_expression_hint = Stack()
        self._full_expression_data = []
        self._current_expression_data = []

        start: int
        stop: int

        try:
            stop = 0 if kwargs['stop'] is not None and kwargs['stop'] == 0 else kwargs['stop']
        except KeyError:
            stop = 0

        try:
            start = 0 if kwargs['start'] is not None and kwargs['start'] == 0 else kwargs['start']
        except KeyError:
            start = 0

        self._script = ScriptReader(script_lines, start=start, stop=stop)
        if script_lines:
            self.__process_line__()

    def add_line(self, line):
        self._prepare_line(line)
        self._script.add_all_items(line)
        self.__process_line__()

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
        return self._script.has_next_not_space()

    def move_to_next_needed(self):
        return self._script.move_to_next_not_space()

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

    def get_next_string(self):

        if self._script.is_next_string() or self.is_string_active():
            if self._script.peek_next() in ["'", '"'] and not self.is_string_active():
                self._string_active = self._script.peek_next()
                self._group_data += self.get_next()
                self._group_type = 'single'

            elif self._script.peek_next() in ['"""', "'''"] and not self.is_string_active():
                self._string_active = self._script.peek_next()
                self._group_data += self.get_next()
                self._group_type = 'multi'

            while self.has_next():
                data = self.get_next()

                if self._group_type == 'single':
                    if data == self._string_active:
                        self._group_type = ''
                    self._group_data += data

                    # print(self._group_data)
                elif self._group_type == 'multi':
                    if data == self._string_active:
                        self._group_type = ''
                    self._group_data += data

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

        if self._script.is_next_operator():
            while self._script.has_next():
                if is_operator(self._script.peek_next()):
                    _operator += self.get_next()
                else:
                    if _operator:
                        return _operator
                    break

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

    def get_next_argument(self):
        return self.get_next_not_space()

    def get_next_assignment(self):
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
            # print('has string data')
            return True

    def get_string_data(self):
        if self.has_next():
            temp = self._group_data
            self._group_data = ''
            self._string_active = ''
            return temp
        return ''

    def get_next_line(self):
        return self.get_next_not_space()

    def add_expression_data(self, data):
        self._current_expression_data.append(data)

    def get_expression_data(self):
        return self._current_expression_data

    def clear_expression_data(self):
        self._current_expression_data.clear()

    def add_expected(self, line: str):
        self._possible_expression_hint.append(line)

    def add_all_expected(self, lines: list):
        self._possible_expression_hint += lines

    def get_expected_expression(self):
        return self._possible_expression_hint

    def reset_expected(self):
        self._previous_expression_hint.push(self._possible_expression_hint)
        self._possible_expression_hint.clear()

    def __process_line__(self):
        if self.has_next_not_space():
            self.move_to_next_not_space()

            if self._script.is_next_comment() or self.is_comments_active():
                self.get_next_comment()

            elif self._script.is_next_string() or self.is_string_active():

                if self.has_string_data():
                    self.add_expression_data({'data.string': self.get_string_data()})
                else:
                    self.get_next_string()

            elif self._script.is_next_data_object() or self._script.is_next_identifier():

                if self._script.is_next_identifier():
                    # if self.is_builtin(self._script.peek_next()):
                    #     self.add_expression_data({'builtins.keyword': self.get_next_not_space()})

                    self.add_expression_data({'data.identifier': self.get_next_not_space()})
                    # self.add_all_expected(EXPECT_AFTER_DATA)

                elif self._script.is_next_int():
                    self.add_expression_data({'data.integer': self.get_next_not_space()})
                elif self._script.is_next_float():
                    self.add_expression_data({'data.float': self.get_next_not_space()})
                elif self._script.is_next_bool():
                    self.add_expression_data({'data.bool': self.get_next_not_space()})
                elif self._script.is_next_byte():
                    self.add_expression_data({'data.byte': self.get_next_not_space()})

            elif self._script.is_next_operator():

                if self._script.is_next_dot_operator():
                    self.add_expression_data({'operator.accessor': self.get_next_not_space()})

                else:
                    operator = self.get_next_operator()
                    if operator:
                        self.add_expression_data({'operator.' + operator: operator})

            elif self._script.is_next_scope_opener():
                self.add_expression_data({'expression.scope': self.get_next_scope()})

            elif self._script.is_next_new_line():

                self.add_expression_data({'expression.newline': self.get_next()})

            elif self._script.is_next_function_call():
                self.add_expression_data({'expression.helper.args': self.get_next_function_call()})

            else:
                self.add_expression_data(
                    {'expression.helper.' + self._script.peek_next_not_space(): self.get_next_not_space()}
                )  # ; : , $ @ ^ \ !

            if len(self._script.get_items()) - 1 == self._script.get_current_item_number():
                print(self._current_expression_data)

            self.__process_line__()

        print(self.get_expression_data())


