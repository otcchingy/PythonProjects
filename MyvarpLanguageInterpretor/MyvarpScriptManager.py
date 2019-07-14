import sys
import time
# import date
# import datetime
# import subprocess
import logging

from MyvarpLanguageInterpretor.utils.builtins.constants import DEFAULT_ENVIRON, EXPECT_AFTER_DATA
from MyvarpLanguageInterpretor.utils.collections.script_reader import ScriptReader
from MyvarpLanguageInterpretor.utils.collections.stack import Stack

"""
configuring logger
"""

logging.basicConfig(format="%(levelname)-8s [%(lineno)d] %(message)s", level=logging.DEBUG)
# logging.disable(logging.DEBUG)
logging = logging.getLogger(__name__)


class MyvarpScriptRunner:
    #  script fields

    _run_type: str  # console or file
    _temp = None
    _return = None
    _lines = None  # an enumeration of file lines
    _output: str
    _status = None
    _environ: dict
    _lines_count: int
    _comments_active: bool
    _comment_hash_count: int
    _comments_type: str

    #  builder fields

    _script: ScriptReader
    _builder_stack: Stack
    _string_active: str
    _possible_expression_hint: list
    _previous_expression_hint: Stack
    _full_expression_data: list
    _current_expression_data: list

    def __init__(self, script_lines='', **kwargs):

        self._lines_count = 0
        self._comment_hash_count = 0
        self._comments_active = False
        self._comments_type = None
        self._string_active = ''
        self._builder_stack = Stack()
        self._possible_expression_hint = []
        self._previous_expression_hint = Stack()
        self._full_expression_data = []
        self._current_expression_data = []

        name = ''
        path = ''
        size = 0
        start = 0
        stop = 0

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

        self._script = ScriptReader(script_lines, start=start, stop=stop)

        self._environ = DEFAULT_ENVIRON
        self._environ['info']['line_stop'] = stop
        self._environ['info']['line_start'] = start
        self._environ['info']['script_name'] = name
        self._environ['info']['script_path'] = path

    def run(self, line):
        self._prepare_line(line)
        self._script.add_all_items(line)
        self.__process_line__()

    def _prepare_line(self, line):
        if not self._lines:
            self._lines = ''
        self._lines += line
        self._lines_count += 1
        # logging.debug("line to process = {} ".format(line))
        # print(f'line {self._lines_count} to process = {line} ')

    def _get_lines_count(self):
        return self._lines_count

    def validate_file_as_script(self):
        # check if string is valid file path
        # check if file has extension .mv
        pass

    def build_variable(self):
        pass

    def build_method(self):
        pass

    def build_class(self):
        pass

    def run_method(self):
        pass

    def get_variable(self):
        pass

    def instantiate_class(self):
        pass

    def perform_operation(self):
        pass

    def is_keyword(self, line):
        if line in DEFAULT_ENVIRON['builtins']['keywords']:
            return True

    def is_string(self, line):
        if isinstance(line, str) and not line.isspace() and line != '':
            if line[0] == '"' and line[-1] == '"':
                return True
            if line[0] == "'" and line[-1] == "'":
                return True

    def de_string(self, line):
        return line[1:-1]

    def is_string_active(self):
        return self._string_active != ''

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

    def get_next_collection(self):
        return self.get_next_not_space()

    def get_next_data_object(self):
        return self.get_next_not_space()

    def get_next_string(self):
        string_data = ''
        if self._script.is_next_string():
            if self._string_active == '':
                self._string_active = self._script.peek_next()

            while self.is_string_active():
                data = self._script.peek_next()

                if data == self._string_active and string_data != '':
                    self._string_active = ''
                string_data += str(self.get_next_not_space())

            return string_data

    def get_next_bool(self):
        return self.get_next_not_space()

    def get_next_parenthesis_opener(self):  # takes argument to match default - any
        return self.get_next_not_space()

    def get_next_parenthesis_closer(self):  # takes arg to make default - any
        return self.get_next_not_space()

    def get_next_function_call(self):
        return self.get_next_not_space()

    def get_next_method_call(self):
        return self.get_next_not_space()

    def get_next_operation(self):
        return self.get_next_not_space()

    def get_next_comment(self):

        if self._script.is_next_comment() or self._comments_active:
            if self._script.peek_next() == '#' and not self._comments_active:
                self.get_next()
                if self._script.peek_next() == '#':
                    self.get_next()
                    if self._script.peek_next() == '#':
                        self.get_next()
                        self._comments_type = 'multi'
                else:
                    self._comments_type = 'single'

            while self._script.has_next():
                if self._comments_type == 'single':
                    if self._script.is_next_new_line():
                        self._comments_active = False
                        self._comments_type = ''
                        self._comment_hash_count = 0
                        break
                    self.get_next()
                else:
                    if self._comments_type == 'multi':
                        if self._script.peek_next() != '#':
                            self._comment_hash_count = 0
                            self.get_next()
                        else:
                            self._comment_hash_count += 1
                            self.get_next()
                            if self._comment_hash_count == 3:
                                self._comments_active = False
                                self._comments_type = ''
                                self._comment_hash_count = 0
                                break

    def get_next_argument(self):
        return self.get_next_not_space()

    def get_next_assignment(self):
        return self.get_next_not_space()

    def get_next_scope(self):
        return self.get_next_not_space()

    def get_next_group(self):
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

    def get_next_group_item(self):
        return self.get_next_not_space()

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
            #
            # if self._comments_active:
            #     self.get_next_comment()
            #
            # elif self._script.is_next_data_object() or self._script.is_next_identifier():
            #
            #     if self._script.is_next_identifier():
            #         # if self.is_builtin(self._script.peek_next()):
            #         #     self.add_expression_data({'builtins.keyword': self.get_next_not_space()})
            #
            #         self.add_expression_data({'data.identifier': self.get_next_not_space()})
            #         # self.add_all_expected(EXPECT_AFTER_DATA)
            #
            #     elif self._script.is_next_string():
            #         self.add_expression_data({'data.string': self.get_next_string()})
            #     elif self._script.is_next_int():
            #         self.add_expression_data({'data.integer': self.get_next_not_space()})
            #     elif self._script.is_next_float():
            #         self.add_expression_data({'data.float': self.get_next_not_space()})
            #     elif self._script.is_next_bool():
            #         self.add_expression_data({'data.bool': self.get_next_not_space()})
            #     elif self._script.is_next_byte():
            #         self.add_expression_data({'data.byte': self.get_next_not_space()})
            #
            # # elif self._script.is_next_group():
            # #     self.add_expression_data(self.get_next_group())
            #
            # elif self._script.is_next_operator():
            #
            #     if self._script.is_next_assignment():
            #         self.add_expression_data({'operator.=': self.get_next_not_space()})
            #
            #     elif self._script.is_next_method_call():
            #         self.add_expression_data({'operator.accessor': self.get_next_not_space()})
            #
            #     else:
            #         self.add_expression_data(
            #             {'operator.operation'+str(self._script.peek_next()): self.get_next_operation()}
            #         )
            #
            # # elif self._script.is_next_scope_opener():
            # #     self.add_expression_data({'expression.scope': self.get_next_scope()})
            #
            # elif self._script.is_next_comment():
            #     self.get_next_comment()
            #
            # elif self._script.is_next_new_line():
            #
            #     self.add_expression_data({'expression.newline': self.get_next()})
            #
            # # elif self._script.is_next_function_call():
            # #     self.add_expression_data({'expression.args': self.get_next_function_call()})
            #
            # else:
            #     self.add_expression_data(
            #         {'expression.helper.' + self._script.peek_next_not_space(): self.get_next_not_space()}
            #     )  # ; : , $ @ ^ \ !

            print(self.get_next_not_space())
            self.__process_line__()

        # print(self.get_expression_data())

    def __interpret_expression_data(self):

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