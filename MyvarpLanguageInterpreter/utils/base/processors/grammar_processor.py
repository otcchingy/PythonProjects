import logging

from utils.base.myvarp_error import Error
from utils.base.processors.operation import Identifier
from utils.builtins.classes import Number, Empty

logging.basicConfig(format="%(levelname)-8s [%(lineno)d] %(message)s", level=logging.DEBUG)
# logging.disable(logging.DEBUG)
logger = logging.getLogger(__name__)


class MyvarpGrammarProcessor:
    def __init__(self, interpreter, operation):
        self._error = None
        self._result = None
        self._operation = operation
        self._interpreter = interpreter

    def get_interpreter(self):
        return self._interpreter

    def set_error(self, error):
        self._error = error
        self.get_interpreter().set_error(error)

    def get_error(self):
        return self._error

    def has_error(self):
        return self._error is not None

    def get_result(self):
        return self.process(self.get_operation())

    def get_operation(self):
        return self._operation

    def set_result(self, obj):
        self._result = obj

    def process(self, operation):
        method_name = f'process_{type(operation).__name__}'
        logger.debug(f'trying to run method {method_name}')
        method = getattr(self, method_name, self.process_invalid_operation)
        return method(operation)

    def process_invalid_operation(self, operation):
        raise Exception(f'method for operation {operation} does not exist!')

    def process_Number(self, operation):
        logger.debug(f'Number: {operation.get_value()}')
        return operation

    def process_String(self, operation):
        logger.debug(f'String: {operation.get_value()}')
        return operation

    def process_Identifier(self, operation):
        logger.debug(f'Identifier: {operation.get_name()}')
        return operation

    def process_VarAccessOperation(self, operation):
        logger.debug(f'doing var access: {operation}')
        process = self.get_interpreter().get_property(operation.get_child_node().get_name())
        if process.get_type() == 'exception':
            return self.set_error(Error('UndefinedNameError',
                                        f'The Symbol \'{operation.get_child_node().get_name()}\' does not exist'
                                        )
                                  )
        else:
            return process.get_result()

    def process_VarAssignOperation(self, operation):
        logger.debug(f'doing assignment: {operation}')
        identifier = self.process(operation.get_left_node())
        assign_type = operation.get_operator()
        value = self.process(operation.get_right_node())
        self.get_interpreter().set_property(identifier.get_name(), value)
        return None

    def process_UnaryOperation(self, operation):
        number = self.process(operation.get_child_node())
        if isinstance(number, Number):
            if operation.get_operator().is_type_of('+'):
                return Number(0).plus(number)
            elif operation.get_operator().is_type_of('-'):
                return Number(0).minus(number)

    def process_BinaryOperation(self, operation):
        number1 = self.process(operation.get_left_node())
        number2 = self.process(operation.get_right_node())
        if isinstance(number1, Number) and isinstance(number2, Number):
            if operation.get_operator().is_type_of('+'):
                return number1.plus(number2)
            elif operation.get_operator().is_type_of('-'):
                return number1.minus(number2)
            elif operation.get_operator().is_type_of('/'):
                result = number1.div(number2)
                if isinstance(result, Number):
                    return result
                else:
                    return self.set_error(result)
            elif operation.get_operator().is_type_of('*'):
                return number1.mul(number2)

    def __repr__(self):
        return f'MyvarpGrammarProcessor<{self.get_operation()}>'



"""
        get previous type
        get current type
        get expecting type list

        if current type == force process current:
            if previous = none and current = data:
                do current as data and set previous to data

        if previous type is none and current type == none //get data/identifier

        if previous type is none and current = data/identifier:
            turn on validate operator:
            if next is operator:
                set previous to identifier | current to operator | set expecting data
                if operator in [=, algebraic, comparators]:
                    expect data/data expression //get the data
                    turn on validate data
                else if operator in ['([{']:
                    expect group params or args //get next params or args
                    turn on validate arg/param group
            else if none:
                wait for next word..
                if is new expression do current as data
                    set next to current
                else:
                    set current to previous | next to current

        elif previous = data and current type is operator/keyword freeze next process until next data (args/params as group)
            if is param :
                set previous none | set current object for build
                set expectation scope //get next scope
                turn on validate scope
            else if args :
                set previous none | do object call with args save current as data with result value
                set expect operator/none //get next operator or none


        elif current type is object for build
            if next == valid scope:
                build object and save to memory
            else:
                show error

        :param _next:
        :return:
        """

"""
note: data can be none

identifier/data operator identifier/data/expression
identifier/data keyword (identifier/data/expression)
identifier '(...params/args(identifier/data/expression)..)'
identifier '[...indexing(identifier/data/expression)..]'

"""
