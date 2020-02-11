import logging

from utils.base.myvarp_memory import MyvarpMemory
from utils.base.myvarp_grammar_parser import MyvarpGrammarParser
from utils.base.myvarp_word import Word
from utils.base.myvarp_error import Error
from utils.base.processors.process import Process
from utils.base.myvarp_script_reader import MyvarpScriptReader
from utils.base.processors.grammar_processor import MyvarpGrammarProcessor
from utils.builtins.constants import DEFAULT_STARTUP_ENVIRON
from utils.builtins.helper_functions import *
from utils.collections.stack import Stack

logging.basicConfig(format="%(levelname)-8s [%(lineno)d] %(message)s", level=logging.DEBUG)
# logging.disable(logging.DEBUG)
logger = logging.getLogger(__name__)

# TODO : bugs list
"""
throw error for unknown words
fix generate word processors function
add word_processors - current and previous
fix IdentifierWordProcessor
fix AssignmentWordProcessor
"""


class MyvarpScriptInterpreter(MyvarpScriptReader):
    __temp = None
    __error = None
    __return = None

    __environ: dict
    __line_type: str
    __call_stack: Stack
    __work_tokens: list
    __is_expression_complete: bool

    def __init__(self, script_lines='', **kwargs):

        self.__parents = []
        self.__line_type = ''
        self.__param_details = []
        self.__word_tokens = []
        self.__error = None
        self.__attr_dict__ = {'access_spec': 'protected', 'modifier_access': 'normal', 'access_state': 'normal'}

        stop = 0
        start = 0
        name = ''
        path = ''
        argv = []

        script_source = 'console<stdin>'

        for spec in self.__attr_dict__.keys():
            if kwargs.keys().__contains__(spec):
                self.__attr_dict__[f'{spec}'] = kwargs[f'{spec}']

        if kwargs.keys().__contains__('parent'):
            self.__parents.append(kwargs['parent']) if kwargs['parent'] is not None and \
                                                       isinstance(kwargs['parent'], MyvarpScriptInterpreter) else None

        if kwargs.keys().__contains__('start'):
            start = 0 if kwargs['start'] is None or kwargs['start'] < 0 else kwargs['start']

        if kwargs.keys().__contains__('stop'):
            stop = 0 if kwargs['stop'] is None or kwargs['start'] < 0 else kwargs['stop']

        if kwargs.keys().__contains__('name'):
            name = '' if kwargs['name'] is None else kwargs['name']

        if kwargs.keys().__contains__('path'):
            path = '' if kwargs['path'] is None else kwargs['path']

        if kwargs.keys().__contains__('argv'):
            argv = [] if kwargs['argv'] is None else kwargs['argv']

        if kwargs.keys().__contains__('script_source'):
            script_source = 'console' if kwargs['script_source'] is None or \
                                         kwargs['script_source'] not in ['console', 'file'] else kwargs['script_source']

        _environ = dict(DEFAULT_STARTUP_ENVIRON)
        _environ['info']['line_stop'] = stop
        _environ['info']['line_start'] = start
        _environ['info']['script_name'] = name
        _environ['info']['script_source'] = script_source
        _environ['info']['script_path'] = path
        _environ['info']['script_argv'] = argv
        _environ['memory'] = MyvarpMemory()

        self.__environ = _environ

        super().__init__(script_lines=script_lines, start=start, stop=stop)

    def add_token(self, word: Word):
        self.__word_tokens.append(word)

    def get_tokens(self):
        return self.__word_tokens

    def set_error(self, error):
        self.__error = error

    def get_error(self):
        return self.__error

    def clear_error(self):
        self.set_error(None)
        self.__word_tokens.clear()

    def has_error(self):
        return self.get_error() is not None

    def show_error(self):
        print(self.get_error())

    def clear_result(self):
        self.__return = None

    def get_access_spec(self):
        """
        :return: public | protected | private
        """
        return self.get_attribute('access_spec')

    def get_access_state(self):
        """
        :return: final | constant
        """
        return self.get_attribute('access_state')

    def get_modifier_access(self):
        """
        :return: static | normal
        """
        return self.get_attribute('modifier_access')

    def set_attribute(self, key, value):
        self.__attr_dict__[f'{key}'] = value

    def get_attribute(self, key):
        return self.__attr_dict__[f'{key}']

    def set_environ(self, environ):
        self.__environ = environ

    def get_environ(self):
        return self.__environ

    def get_memory(self):
        return self.__environ['memory']

    def set_status(self):
        pass

    def get_status(self):
        pass

    def get_parents(self):
        return self.__parents

    def add_parent(self, parent):
        self.__parents.append(parent)

    def get_result(self):
        return self.__return

    def set_result(self, value):
        self.__return = value

    def import_to_module(self):
        pass

    def import_module(self):
        pass

    def add_positional_param(self, param, expected_type='all', default_val=None):
        self.add_param_details(param, 'positional', expected_type)
        self.set_property(param, default_val)

    def add_kwargs_param(self, param, expected_type='all', default_val=None):
        self.add_param_details(param, 'kwargs', expected_type)
        self.set_property(param, default_val)

    def get_param_value(self, param):
        self.get_data_from_memory(param)

    def set_param_value(self, param, value):
        self.set_property(param, value)

    def add_param_details(self, param, param_type, expected_data_type):
        num_of_params = len(self.__param_details)
        error_found = False
        if num_of_params > 0:
            if param_type == 'positional':
                if self.__param_details[num_of_params - 1]['param-type'] != 'positional':
                    error_found = True
                    # TODO: throw error cannot add positional param kwargs param
            else:
                error_found = True
                # TODO: throw error cannot add param kwargs param

        if not error_found:
            self.__param_details.append({
                'param': param,
                'param-type': param_type,
                'expected-data-type': expected_data_type,
                'index': len(self.__param_details)})

    def get_param_details(self, param):
        for i in self.__param_details:
            if i['param'] == param:
                return i

    def get_all_params(self):
        return self.__param_details

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

    def set_property(self, key, value, **kwargs):
        self.get_memory().set_item(key, value, **kwargs)

    def has_property(self, key):
        result = self.get_property(key)
        if isinstance(result, Process):
            if result.get_type() == 'exception':
                return False
        return True

    def get_property(self, key):
        data = self.get_memory().get_data_for(key)

        if data is None:

            data = Process(type='exception', object='NameException :: Undefined Name', state='failed')
            parents = self.get_parents()

            if parents:
                for i in range(len(parents)):
                    parent = parents[len(parents) - i]
                    data = parent.get_property(key)
                    if isinstance(data, Process) and data.get_type() != 'exception':
                        continue
                    else:
                        break
            return data

        return Process(type='object.data', object=key, method="?", result=data)

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
        logger.debug(f'word tokens list: {self.get_tokens()}')
        if len(self.get_tokens()) > 0:
            self.__interpret()

    def __process_line__(self):

        # try:
        word = Word(None, None)

        if self.has_next_needed():

            self.move_to_next_needed()

            # logging.debug(f'|{self._script.peek_next()}|')

            if self._script.is_next_comment() or self.is_comments_active():
                self.get_next_comment()

            elif self._script.is_next_string() or self.is_string_active():
                if self.has_string_data():
                    word = Word('builtins.data.string', self.get_string_data())
                else:
                    self.get_next_string()

            elif self._script.is_next_new_line() or self._script.is_next_line_terminator():
                word = Word('expression.helper.run', self.get_next().replace('\n', '<newline>'))

            elif self._script.is_next_data_object() or self._script.is_next_identifier():
                if self._script.is_next_identifier():

                    if is_builtin(self._script.peek_next()):
                        if is_keyword(self._script.peek_next()):
                            word = Word('builtins.keyword.' + self._script.peek_next_not_space(),
                                        self.get_next_not_space())
                        elif is_builtin_type(self._script.peek_next()):
                            word = Word('builtins.object.type', self.get_next_not_space())
                        elif is_builtin_object(self._script.peek_next()):
                            word = Word('builtins.object', self.get_next_not_space())
                    else:
                        # if is_object(self._script.peek_next_not_space()) then get type and create object
                        word = Word('data.identifier', self.get_next_not_space())

                elif self._script.is_next_number():
                    number = self.get_next_number()
                    if number.__contains__('--error--'):
                        number = number.replace('--error--:', '')
                        self.set_error(Error('InvalidSyntaxError', f'cannot parse \'{number}\' into number!'))
                    else:
                        word = Word('builtins.data.number.integer', number)  # TODO: create get next number

                elif self._script.is_next_float():  # TODO: remove line
                    word = Word('builtins.data.number.float', self.get_next_not_space())
                elif self._script.is_next_bool():
                    word = Word('builtins.data.bool', self.get_next_not_space())
                elif self._script.is_next_byte():
                    word = Word('builtins.data.byte', self.get_next_not_space())

            elif self._script.is_next_operator():

                if self._script.is_next_dot_operator():
                    word = Word('operator.accessor', self.get_next_not_space())
                else:
                    operator = self.get_next_operator()
                    if operator:
                        word = Word('operator.' + operator, operator)
                    else:
                        self.set_error(Error('InvalidSyntaxError', f'cannot parse \'{operator}\' into operator!'))
            elif self._script.is_next_collection():

                if self._script.is_next_collection_opener():
                    word = Word('expression.collection.opener.' + self._script.peek_next(),
                                self.get_next_not_space())

                elif self._script.is_next_collection_closer():
                    word = Word('expression.collection.closer.' + self._script.peek_next(),
                                self.get_next_not_space())

            elif self._script.is_next_syntax_helper():
                word = Word('expression.helper.' + self._script.peek_next_not_space(), self.get_next_not_space())
                # ; : , $ @ \ !
            else:
                self.set_error(
                    Error('UnExpectedWordError', f'The word \'{self._script.peek_next_not_space()}\' is invalid!'))
                word = Word('exception.invalid-word.' + self._script.peek_next_not_space(), self.get_next_not_space())
                logger.debug(word)
                return word
                pass

            if word.get_type() is not None:
                # print(word)
                self.add_token(word)
            self.__process_line__()

        else:
            if word.get_type() is not None:
                # print(word)
                self.add_token(word)

                # except Exception as e:
                #     self.set_error(e)

    def __interpret(self):

        if not self.has_error():
            parser = MyvarpGrammarParser(self.get_tokens())
            parser.parse()
            if parser.has_error():
                self.set_error(parser.get_error())
            else:
                parse_result = parser.get_result()
                logger.debug(f'ParseResult: {parse_result}')
                processor = MyvarpGrammarProcessor(self, parse_result)
                processor.process()
                if processor.has_error():
                    logger.debug(f'submitting error: {processor.get_error()}')
                    self.set_error(processor.get_error())
                if not self.has_error():
                    logger.debug(f'submitting result: {processor.get_result()}')
                    self.set_result(processor.get_result())

        self.get_tokens().clear()

    def interpret_assignment(self, identifier, value, **kwargs):
        # myvarp_object = MyvarpObject(parent=self, script=process.args).call()
        self.set_property(identifier, value, kwargs)

    def interpret_class(self):
        pass  # MyvarpClass(parent=self, expression_data=data)

    def interpret_function(self):
        pass  # MyvarpFunction(parent=self, expression_data=data)

    def interpret_decision_tree(self):
        pass

    def interpret_for_loop(self):
        pass

    def interpret_while_loop(self):
        pass

    def interpret_do_while(self):
        pass

    def interpret_switch_case(self):
        pass

    def interpret_with_object_as(self):
        pass

    def get_data_from_memory(self, key):
        pass

    def evaluate_line(self, line):
        logger.debug(f'evaluating line {line}')
        self.add_line(line + '\n')
        self.run_script()

    def __eval__(self, source):
        # eval(source, self.locals(), self.globals())
        pass

    def __eval_python__(self, source):
        # eval(source, self.locals(), self.globals())
        pass

    def has_parent(self):
        return len(self.get_parents()) > 0
