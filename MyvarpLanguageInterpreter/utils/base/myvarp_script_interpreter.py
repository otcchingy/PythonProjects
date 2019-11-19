from collections import namedtuple

from utils.base.myvarp_memory import MyvarpMemory
from utils.base.myvarp_processor import *
from utils.base.myvarp_script_reader import MyvarpScriptReader
from utils.builtins.constants import DEFAULT_STARTUP_ENVIRON
from utils.builtins.helper_functions import *
from utils.collections.stack import Stack
import logging

logging.basicConfig(format="%(levelname)-8s [%(lineno)d] %(message)s", level=logging.DEBUG)
# logging.disable(logging.DEBUG)
logging = logging.getLogger(__name__)

Process = namedtuple("Process", ["type", "object", "method", "args", "result", "status"])

# TODO : bugs list
"""
fix collecting string like 'name\''
throw error for unknown words
fix generate word processor function
add word_processors - current and previous
fix IdentifierWordProcessor
fix AssignmentWordProcessor
"""


def set_process_fields(p, **kwargs):
    s = {
        'type': p.type,
        'object': p.object,
        'method': p.method,
        'args': p.args,
        'result': p.result,
        'status': p.status
    }
    for i, j in kwargs.items():
        s[i] = j
    return Process(s['type'], s['object'], s['method'], s['args'], s['result'], s['status'])


class MyvarpScriptInterpreter(MyvarpScriptReader):
    __temp = None
    __return = None
    __parent = None

    _environ: dict
    __expecting: list
    __line_type: str
    __call_stack: Stack
    __syntax_stack: Stack
    __is_expression_complete: bool
    __interpretable_expression_data: list
    __current_expression_data: list

    class Word:

        def __init__(self, _type, _value):
            self._type = _type
            self._value = _value

        def is_type_of(self, name):
            if name in self._type:
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

    def __init__(self, script_lines='', **kwargs):

        self.__parent = None
        self.__line_type = ''
        self.__is_expression_complete = True  # change to None
        self.__expecting = 'data|data_expression|keyword'.split('|')  # TODO : note identifier maybe keyword
        self.__interpretable_expression_data = []
        self.__current_expression_data = []
        self.__word_processor = EmptyLiteral(self)

        stop = 0
        start = 0
        name = ''
        path = ''
        script_source = 'console'

        if kwargs.keys().__contains__('expression_data'):
            self.__current_expression_data = kwargs['expression_data'] \
                if kwargs['expression_data'] is not None and isinstance(kwargs['parent'], list) else []

        if kwargs.keys().__contains__('parent'):
            self.__parent = kwargs['parent'] if kwargs['parent'] is not None and \
                                                isinstance(kwargs['parent'], MyvarpScriptInterpreter) else None

        if kwargs.keys().__contains__('stop'):
            stop = 0 if kwargs['stop'] is not None and kwargs['stop'] == 0 else kwargs['stop']

        if kwargs.keys().__contains__('start'):
            start = 0 if kwargs['start'] is not None and kwargs['start'] == 0 else kwargs['start']

        if kwargs.keys().__contains__('name'):
            name = '' if kwargs['name'] is not None and kwargs['name'] == 0 else kwargs['name']

        if kwargs.keys().__contains__('path'):
            path = '' if kwargs['path'] is not None and kwargs['path'] == 0 else kwargs['path']

        if kwargs.keys().__contains__('script_source'):
            script_source = 'console' if kwargs['script_source'] is None or \
                                         kwargs['script_source'] not in ['console', 'file'] else kwargs['script_source']

        _environ = dict(DEFAULT_STARTUP_ENVIRON)
        _environ['info']['line_stop'] = stop
        _environ['info']['line_start'] = start
        _environ['info']['script_name'] = name
        _environ['info']['script_source'] = script_source
        _environ['info']['script_path'] = path
        _environ['memory'] = MyvarpMemory()

        self._environ = _environ

        super().__init__(script_lines=script_lines, start=start, stop=stop)

    def set_environ(self, environ):
        self._environ = environ

    def get_environ(self):
        return self._environ

    def get_memory(self):
        return self._environ['memory']

    def get_last_word(self) -> MyvarpWordProcessor:
        return self.__word_processor

    def set_last_word(self, word: MyvarpWordProcessor):
        self.__word_processor = word

    def set_status(self):
        pass

    def get_status(self):
        pass

    def get_parent(self):
        return self.__parent

    def set_parent(self, parent):
        self.__parent = parent

    def get_return_value(self):
        return self.__return

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

    def build_object(self):
        pass

    def build_primitive(self):
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

    def run_method(self, name, args):
        pass

    def make_myvarp_object(self, param):
        return param

    def make_myvarp_class(self, param):
        return param

    def make_myvarp_function(self, param):
        return param

    def run_script(self):
        self.__process_line__()

    def add_expression_data(self, data):
        self.__current_expression_data.append(data)

    def get_expression_data(self):
        return self.__current_expression_data

    def clear_expression_data(self):
        self.__current_expression_data.clear()

    # def __process_line__(self):
    #
    #     if self.has_next_needed():
    #
    #         self.move_to_next_needed()
    #
    #         # logging.debug(f'|{self._script.peek_next()}|')
    #
    #         if self._script.is_next_comment() or self.is_comments_active():
    #             self.get_next_comment()
    #
    #         elif self._script.is_next_string() or self.is_string_active():
    #
    #             if self.has_string_data():
    #                 self.add_expression_data({'data.string': self.get_string_data()})
    #             else:
    #                 self.get_next_string()
    #
    #         elif self._script.is_next_new_line() or self._script.is_next_line_terminator():
    #
    #             # self.add_expression_data({'expression.newline': self.get_next()})
    #             self.get_next()
    #             self.__interpret_current_expression_data()
    #
    #         elif self._script.is_next_data_object() or self._script.is_next_identifier():
    #
    #             if self._script.is_next_identifier():
    #
    #                 if is_builtin(self._script.peek_next()):
    #                     if is_keyword(self._script.peek_next()):
    #                         self.add_expression_data({'builtins.keyword': self.get_next_not_space()})
    #                     elif is_builtin_type(self._script.peek_next()):
    #                         self.add_expression_data({'builtins.class': self.get_next_not_space()})
    #                     elif is_builtin_function(self._script.peek_next()):
    #                         self.add_expression_data({'builtins.function': self.get_next_not_space()})
    #                 else:
    #                     self.add_expression_data({'data.identifier': self.get_next_not_space()})
    #
    #             elif self._script.is_next_int():
    #                 self.add_expression_data({'data.number.integer': self.get_next_not_space()})
    #             elif self._script.is_next_float():
    #                 self.add_expression_data({'data.number.float': self.get_next_not_space()})
    #             elif self._script.is_next_bool():
    #                 self.add_expression_data({'data.bool': self.get_next_not_space()})
    #             elif self._script.is_next_byte():
    #                 self.add_expression_data({'data.byte': self.get_next_not_space()})
    #
    #         elif self._script.is_next_operator():
    #
    #             if self._script.is_next_dot_operator():
    #                 self.add_expression_data({'operator.accessor': self.get_next_not_space()})
    #
    #             else:
    #                 operator = self.get_next_operator()
    #                 if operator:
    #                     self.add_expression_data({'operator.' + operator: operator})
    #
    #         elif self._script.is_next_collection():
    #
    #             if self._script.is_next_collection_opener():
    #                 self.add_expression_data(
    #                     {'expression.collection.opener.' + self._script.peek_next(): self.get_next_not_space()}
    #                 )
    #             elif self._script.is_next_collection_closer():
    #                 self.add_expression_data(
    #                     {'expression.collection.closer.' + self._script.peek_next(): self.get_next_not_space()}
    #                 )
    #
    #         else:
    #             self.add_expression_data(
    #                 {'expression.helper.' + self._script.peek_next_not_space(): self.get_next_not_space()}
    #             )  # ; : , $ @ ^ \ !
    #
    #         self.__process_line__()
    #
    #         # if self.has_next_needed():
    #         #     self.move_to_next_needed()
    #         #
    #         #     if self.processor is not None:
    #         #         self.processor = PrevPresentNext(self, self._script.get_next(), None, None)
    #         #     else:
    #         #         self.processor.set_next(self._script.get_next())
    #
    #     else:
    #         # print("peek_next : " + str(self._script.peek_next()))
    #         self.__interpret_current_expression_data()

    def __process_line__(self):

        word = self.Word(None, None)

        if self.has_next_needed():

            self.move_to_next_needed()

            # TODO : = doesnt appear fix
            # logging.debug(f'|{self._script.peek_next()}|')

            if self._script.is_next_comment() or self.is_comments_active():
                self.get_next_comment()

            elif self._script.is_next_string() or self.is_string_active():
                if self.has_string_data():
                    word = self.Word('data.string', self.get_string_data())
                else:
                    print("got here: remove this")
                    word = self.Word('data.string', self.get_next_string())

            elif self._script.is_next_new_line() or self._script.is_next_line_terminator():
                # self.add_expression_data({'expression.newline': self.get_next()})
                word = self.Word('expression.helper.run', self.get_next())

            elif self._script.is_next_data_object() or self._script.is_next_identifier():
                if self._script.is_next_identifier():

                    if is_builtin(self._script.peek_next()):
                        if is_keyword(self._script.peek_next()):
                            word = self.Word('builtins.keyword', self.get_next_not_space())
                        elif is_builtin_type(self._script.peek_next()):
                            word = self.Word('builtins.class', self.get_next_not_space())
                        elif is_builtin_function(self._script.peek_next()):
                            word = self.Word('builtins.function', self.get_next_not_space())
                    else:
                        word = self.Word('data.identifier', self.get_next_not_space())

                elif self._script.is_next_int():
                    word = self.Word('builtins.data.number.integer', self.get_next_not_space())
                elif self._script.is_next_float():
                    word = self.Word('builtins.data.number.float', self.get_next_not_space())
                elif self._script.is_next_bool():
                    word = self.Word('builtins.data.bool', self.get_next_not_space())
                elif self._script.is_next_byte():
                    word = self.Word('builtins.data.byte', self.get_next_not_space())

            elif self._script.is_next_operator():

                if self._script.is_next_dot_operator():
                    word = self.Word('operator.accessor', self.get_next_not_space())

                else:
                    operator = self.get_next_operator()
                    if operator:
                        word = self.Word('operator.' + operator, operator)

            elif self._script.is_next_collection():

                if self._script.is_next_collection_opener():
                    word = self.Word('expression.collection.opener.' + self._script.peek_next(),
                                     self.get_next_not_space())

                elif self._script.is_next_collection_closer():
                    word = self.Word('expression.collection.closer.' + self._script.peek_next(),
                                     self.get_next_not_space())

            elif self._script.is_next_syntax_helper():
                word = self.Word('expression.helper.' + self._script.peek_next_not_space(), self.get_next_not_space())
                # ; : , $ @ ^ \ !
            else:
                # TODO: invalid word
                word = self.Word('exception.invalid-word.' + self._script.peek_next_not_space(),
                                 self.get_next_not_space())
                print(word)
                return word
                pass

            self.__interpret_current_expression_data(word)
            # get next word
            self.__process_line__()

        else:
            # print("peek_next : " + str(self._script.peek_next()))
            self.__interpret_current_expression_data(word)
            # self.__interpret_current_expression_data()

    # def __interpret_current_expression_data(self):
    #     if len(self.get_expression_data()) > 0:
    #         self.__return = self.start_interpreting_process()
    #         return self.__return

    def __interpret_current_expression_data(self, word: Word):
        if word.get_type() is not None:
            self.get_last_word().add_word_to_right(word)

    def __is_expecting_equals(self, data):
        expecting_list: list = self.__expecting

        if isinstance(data, str):
            exp_list = data.split("|")
        else:
            exp_list = data

        if len(expecting_list) == len(exp_list):
            for item in exp_list:
                if item not in expecting_list:
                    return False
            return True
        return False

    def __is_expecting_contains_any(self, data):
        expecting_list: list = self.__expecting

        if isinstance(data, str):
            exp_list = data.split("|")
        else:
            exp_list = data

        for item in exp_list:
            if item in expecting_list:
                return True
        return False

    def __is_expecting_contains_all(self, data):
        expecting_list: list = self.__expecting

        if isinstance(data, str):
            exp_list = data.split("|")
        else:
            exp_list = data

        for item in exp_list:
            if item not in expecting_list:
                return False
        return True

    def start_interpreting_process(self):
        return self.__interpret(self.get_expression_data())

    def __interpret(self, expression: list):

        """
        on word
            check if word i builtin
                if True:
                    do builtin
                else:
                    if value:
                        do value
                    else:
                        if identifier:
                            check in memory scope of self and parents
                            if exist do word (value|class|function)
                            else: do exception
                        else:
                            if expression.helper :
                                if valid helper continue
                                else do exception
                            else:
                                do exception


        :param expression:
        :return:
        """

        # TODO : create function to check value in expecting // check in expecting args.str args.list
        print(f'\nprocessing line = {expression} :: expecting : {self.__expecting}\n')

        if not self.__interpretable_expression_data:
            self.__interpretable_expression_data = []
            print("done assigning expression")

        for i in range(len(self.__current_expression_data)):
            word: self.Word = self.__current_expression_data[i]
            key = word.get_type()

            print("current word : " + str(word))

            if self.__is_expecting_equals('data|data_expression|keyword'):

                if 'identifier' in key or 'data' in key:
                    self.__expecting = 'operator|keyword|end'.split('|')
                    self.__line_type = 'data'
                    print("in next is identifier")

                elif 'keyword' in key:
                    self.__expecting = 'identifier|data|args.opener'.split('|')
                    self.__line_type = 'run_keyword'  # TODO :keyword types function, flow control
            elif self.__is_expecting_contains_all('operator|keyword|end'):
                if 'keyword' in key:
                    # TODO : check if is assignment keyword = as True ? expect identifier
                    pass
                elif 'operator' in key:
                    if '=' in key:
                        self.__expecting = ['data|data_expression']
                        self.__line_type = 'assignment'
                        break
                    else:
                        # TODO : collect operation and process for value
                        pass
                        # TODO : trow error
                else:
                    pass

            elif self.__is_expecting_contains_all('syntax.helper|end'):
                pass

            print(f'word {i} : key = {key} : expecting = {self.__expecting}')

        # use stack to determine type of line // assignment operation data condition flow control function call
        # also validate syntax

        return self.__interpret_expression_data()

    def __interpret_expression_data(self):
        result = None

        if self.__line_type == 'assignment':
            print("try perform assignment : line = " + str(self.__current_expression_data))
            result = self.__interpret_next_expression_as_assignment()
        elif self.__line_type == 'data':
            print("try perform data : line = " + str(self.__current_expression_data))
            result = self.__interpret_next_expression_as_data()
        elif self.__line_type == 'function':
            print("try perform data : line = " + str(self.__current_expression_data))
            result = self.__interpret_next_expression_as_class()
        elif self.__line_type == 'class':
            result = self.__interpret_next_expression_as_function()
            print("try perform data : line = " + str(self.__current_expression_data))
        elif 'flow_control' in self.__line_type:

            print("processing flow control : line = " + str(self.__current_expression_data))

            if 'flow_control.decision_tree' == self.__line_type:
                result = self.__interpret_next_expression_as_decision_tree()
            elif 'flow_control.for_loop' == self.__line_type:
                result = self.__interpret_next_expression_as_for_loop()
            elif 'flow_control.while_loop' == self.__line_type:
                result = self.__interpret_next_expression_as_while_loop()
            elif 'flow_control.do_while' == self.__line_type:
                result = self.__interpret_next_expression_as_do_while()
            elif 'flow_control.switch_case' == self.__line_type:
                result = self.__interpret_next_expression_as_switch_case()
            elif 'flow_control.with_as' == self.__line_type:
                result = self.__interpret_next_expression_as_with_object_as()

        self.__current_expression_data = []
        self.__interpretable_expression_data = []
        self.__expecting = 'data|data_expression|keyword'.split('|')

        if isinstance(result, Process) and result.type == 'exception':
            print(result.object)
        elif isinstance(result, Process) and result.type == 'object.data' and \
                        self._environ['info']['script_source'] == 'console':
            print('processed data = ' + str(result.result))

        # TODO : remove this line
        print(self._environ['memory'])

        return result

    def __interpret_next_expression_as_assignment(self):
        return self.__interpret_assignment()

    def __interpret_assignment(self):
        # TODO create new var with value in self.environ['memory']
        # TODO : collect all data needed for assignment while checking syntax
        if self._is_expression_line_complete():
            data = self.__get_interpretable_expression_data()

            process = Process('assignment', data[0].get_value(), '=',
                              "".join(map(lambda x: x.get_value(), data[2:])), None, 'ongoing')

            # myvarp_object = MyvarpObject(parent=self, script=process.args).call()
            self.do_assignment_for_memory_key(process.object, process.args)

            return set_process_fields(process, status='done')
        else:
            return self.__interpret_assignment()

    def __interpret_next_expression_as_data(self):
        print("data  = " + str(self.__get_interpretable_expression_data()))
        if self.__get_interpretable_expression_data()[0].is_type_of('identifier'):
            key = self.__get_interpretable_expression_data()[0].get_value()
            return self.get_data_from_memory(key)
        else:
            value = self.__get_interpretable_expression_data()[0].get_value()
            logging.debug(value)
            # TODO logging.debug data to console if in console mode else pass
            return str(value)

    def _is_expression_line_complete(self):
        return self.__is_expression_complete

    def __get_interpretable_expression_data(self):
        # TODO : return self.interpretable_expression_data
        return self.__current_expression_data

    def __interpret_next_expression_as_class(self):
        return "Class"  # MyvarpClass(parent=self, expression_data=data)

    def __interpret_next_expression_as_function(self):
        return "Function"  # MyvarpFunction(parent=self, expression_data=data)

    def get_data_from_memory(self, key):
        data = self.get_memory().get_data_for(key)
        if data is None:
            temp = self
            print('has parent = ' + str(self.has_parent()))
            while temp.has_parent():
                print('checking parent...')
                temp = temp.get_parent()
                if temp.get_memory().has_key(key):
                    data = temp.get_memory().get_data_for(key)
                    return Process('object.data', key, "?", None, data, None)
            return Process('exception', 'NameException :: Undefined Name', None, None, None, 'failed')
        return Process('object.data', key, "?", None, data, None)

    def do_assignment_for_memory_key(self, key, value):
        self.get_memory().set_item(key, value)

    def evaluate_line(self, line):
        print(f'evaluating line {line}')
        self.add_line(line + '\n')
        self.run_script()
        print('result = ' + str(self.__interpret_current_expression_data()))

    def evaluate_expression_list(self, line):
        return self.__interpret(line)

    def __eval__(self, source):
        # eval(source, self.locals(), self.globals())
        pass

    def __eval_python__(self, source):
        # eval(source, self.locals(), self.globals())
        pass

    def has_parent(self):
        return self.__parent is not None
