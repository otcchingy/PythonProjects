import logging
from utils.base.myvarp_class import MyvarpClass
from utils.base.myvarp_error import Error
from utils.base.myvarp_word import Word
from utils.base.processors.operation import BinaryOperation, UnaryOperation, VarAssignOperation, VarAccessOperation, \
    Identifier, KeyWord, Operation, DecisionOperation
from utils.builtins.classes import Number, String, Boolean, Empty
from utils.builtins.helper_functions import de_string

logging.basicConfig(format="%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s", filename="grammar_processor",
                    level=logging.DEBUG)
# logging.disable(logging.DEBUG)
logger = logging.getLogger(__name__)


class MyvarpGrammarParser:
    def __init__(self, word_tokens: list):
        self.__token_list = word_tokens
        self.__current_token_index = -1
        self.__current_token: Word = None
        self.__result = None
        self.__error = None

    def set_error(self, error):
        self.__error = error

    def get_error(self):
        return self.__error

    def get_tokens(self):
        return self.__token_list

    def has_error(self):
        return self.get_error() is not None

    def get_result(self):
        return self.__result

    def has_next_token(self):
        if self.__current_token_index + 1 < len(self.get_tokens()):
            return True
        return False

    def advance(self):
        if self.has_next_token():
            self.__current_token_index += 1
            self.__current_token = self.get_tokens()[self.__current_token_index]
            # logger.debug("advancing from previous token: "+str(self.get_previous_token())+", current token: "+str(self.__current_token))
            return self.__current_token

    def get_current_token(self):
        return self.__current_token

    def get_previous_token(self):
        if self.__current_token_index > 0:
            return self.get_tokens()[self.__current_token_index - 1]

    def parse(self):
        self.advance()
        self.__result = self.statements()

    def get_binary_operation(self, func, operators):

        left = func()
        if self.has_error(): return left

        while self.get_current_token().is_match(operators):
            operator = self.get_current_token()
            self.advance()
            if operator.is_type_of('/') or operator.is_type_of('//'):
                right = self.get_binary_operation(func, ['*', '/', '//'])
            else:
                right = func()
            if self.has_error(): return right
            left = BinaryOperation(left, operator, right)

        return left

    def atom(self):

        if self.get_current_token().is_type_of('keyword'):
            word = self.get_current_token()
            self.advance()
            return KeyWord(word)

        elif self.get_current_token().is_type_of('number'):
            word = self.get_current_token()
            self.advance()
            return Number(word.get_value())

        elif self.get_current_token().is_type_of('string'):
            word = self.get_current_token()
            self.advance()
            return String(de_string(word.get_value()))

        elif self.get_current_token().is_type_of('object'):
            word = self.get_current_token()
            self.advance()
            if str(word.get_value()).lower() == 'true':
                return Boolean(1)
            elif str(word.get_value()).lower() == 'false':
                return Boolean(0)
            elif str(word.get_value()).lower() == 'none':
                return Empty()

        elif self.get_current_token().is_type_of('identifier'):
            word = self.get_current_token()
            identifier = Identifier(word.get_value())
            self.advance()
            return VarAccessOperation(identifier)

        elif self.get_current_token().is_type_of('('):
            self.advance()
            expr = self.expression()
            if self.has_error(): return
            if self.get_current_token().is_type_of(')'):
                self.advance()
            return expr

    def factor(self):

        if self.get_current_token() is not None:

            if self.get_current_token().is_type_any(['+', '-', '!', 'not']):
                operator = self.get_current_token()

                if self.has_next_token():
                    self.advance()
                    if operator.is_type_of('!'):
                        factor = self.comp_expression()
                    else:
                        factor = self.factor()
                    if not self.has_error():
                        return UnaryOperation(None, operator, factor)

            return self.atom()

        else:
            self.set_error(Error('InvalidSyntaxError', 'Expected an expression or a value!<1>'))

    def term(self):
        return self.get_binary_operation(self.factor, ['*', '**', '/', '//'])

    def arith_expression(self):
        return self.get_binary_operation(self.term, ['+', '-'])

    def comp_expression(self):
        return self.get_binary_operation(self.arith_expression, ['<', '>', '==', '<=', '>=', '!='])

    def decision_expression(self):
        """

        #case 1
        if condition:
            block
        (o|...)elseif condition:
            block
        (o)else:
            block
        endif

        #case 2
        if condition{
            block
        }
        (o|...)elseif condition{
            block
        }
        (o)else{
            block
        }
        :return: DecisionOperation
        """
        if self.get_previous_token().is_match(['if']):
            logger.debug("doing if")
            if_cases = []
            else_case = None
            condition = self.expression()
            if condition is None:
                self.set_error(Error('InvalidSyntaxError', 'Expected boolean expression'))
                return
            proceed, is_open, scope_opener, block = self.block()  # list of expressions

            if proceed:
                if_cases.append((condition, block))

                logger.debug("current word<1>: "+str(self.get_current_token()))

                while self.get_current_token().is_match(['elseif']):
                    logger.debug("doing else if")
                    self.advance()
                    condition = self.expression()
                    if condition is None:
                        self.set_error(Error('InvalidSyntaxError', 'Expected boolean expression'))
                        return
                    proceed, is_open, scope_opener, block = self.block()
                    if proceed:
                        if_cases.append((condition, block))
                    elif is_open:
                        expected_closer = "endif" if scope_opener == ':' else "}"
                        self.set_error(Error('InvalidSyntaxError', f'Expected {expected_closer}'))
                    else:
                        self.set_error(Error('InvalidSyntaxError', 'Expected { or :<4>'))
                        return

                logger.debug("current word<2>: "+str(self.get_current_token()))

                if self.get_current_token().is_match(['else']):
                    logger.debug("doing else")
                    self.advance()
                    proceed, is_open, scope_opener, block = self.block()
                    if proceed:
                        else_case = block

                if is_open:
                    expected_closer = "endif" if scope_opener.is_match([":"]) else "}"
                    logger.debug("current word<3>: " + str(self.get_current_token()))
                    if self.get_current_token().is_match([expected_closer]):
                        return DecisionOperation(if_cases, else_case)
                    else:
                        self.set_error(Error('InvalidSyntaxError', f'Expected {expected_closer}'))
                else:
                    return DecisionOperation(if_cases, else_case)

            elif is_open:
                expected_closer = "endif" if scope_opener == ':' else "}"
                self.set_error(Error('InvalidSyntaxError', f'Expected {expected_closer}'))
            else:
                self.set_error(Error('InvalidSyntaxError', 'Expected { or :<2>'))

            return DecisionOperation(if_cases, else_case)

    def expression(self):

        result = self.get_binary_operation(self.comp_expression, ['and', 'or', '||', '&&', 'is'])

        if isinstance(result, KeyWord) and result.is_match(['if']):
            return self.decision_expression()

        elif isinstance(result, VarAccessOperation):

            if self.get_current_token().is_type_of('operator') and self.get_current_token().is_type_of('='):
                if self.has_next_token():
                    self.advance()
                    word = self.expression()
                    if isinstance(word, KeyWord) and word.is_type_of('new'):
                        value = self.expression()
                        if isinstance(value, Operation) or isinstance(value, MyvarpClass):
                            return VarAssignOperation(result.get_child_node(), word, value)
                        else:
                            self.set_error(Error('InvalidSyntexaxError', 'Expected an expression'))
                            return None
                    elif isinstance(word, KeyWord) and word.is_type_any(['ref', 'val']):
                        value = self.expression()
                        if isinstance(value, VarAccessOperation):
                            return VarAssignOperation(result.get_child_node(), word, value.get_child_node())
                        else:
                            self.set_error(Error('InvalidSyntaxError', 'Expected an Identifier!'))
                            return
                    elif word is None:
                        self.set_error(Error('InvalidSyntaxError', 'Expected ref, val, new or expression'))
                    else:
                        return VarAssignOperation(result.get_child_node(), Word('keyword', 'val'), word)
                else:
                    self.set_error(Error('InvalidSyntaxError', 'Expected ref, val, new or expression'))
                    return None

            return result
        else:
            return result

    def statements(self):
        results = []
        expression = self.expression()
        while expression is not None:
            results.append(expression)
            if self.get_current_token().is_type_of('run'):
                self.advance()
                expression = self.expression()
            else:
                logger.debug("end statements: " + str(self.get_current_token()))
                break
        return results

    def block(self):
        if self.get_current_token().is_match(['{', ':']):
            scope_opener = self.get_current_token()
            scope_type = self.get_current_token().get_value()
            self.advance()
            statements = self.statements()
            if scope_type == '{':
                proceed = self.get_current_token().is_match(['}'])
                is_open = not proceed
                self.advance()
            else:
                proceed = True
                is_open = True

            return proceed, is_open, scope_opener, statements
        else:
            self.set_error(Error('InvalidSyntaxError', 'Expected { or : <1>'))
            return False, False, None, []
