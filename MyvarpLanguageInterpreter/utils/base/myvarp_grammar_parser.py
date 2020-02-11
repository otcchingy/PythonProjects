from utils.base.myvarp_error import Error
from utils.base.myvarp_word import Word
from utils.base.processors.operation import BinaryOperation, UnaryOperation, VarAssignOperation, VarAccessOperation, \
    Identifier, KeyWord, Operation, DecisionOperation
from utils.builtins.classes import Number, String, Boolean, Empty
from utils.builtins.helper_functions import de_string


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
            return self.__current_token

    def get_current_token(self):
        return self.__current_token

    def get_previous_token(self):
        if self.__current_token_index > 0:
            return self.get_tokens()[self.__current_token_index - 1]

    def parse(self):
        self.advance()
        self.__result = self.expression()

    def get_binary_operation(self, func, operators):

        left = func()
        if self.has_error(): return left

        while self.get_current_token().is_match(operators):
            operator = self.get_current_token()
            self.advance()
            if operator.is_type_of('/'):
                right = self.get_binary_operation(func, ['*', '/'])
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
        else:
            self.set_error(Error('InvalidSyntaxError', 'Expected type int, float, -, +!'))

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
            self.set_error(Error('InvalidSyntaxError', 'Expected type int, float, -, +!'))

    def term(self):
        return self.get_binary_operation(self.factor, ['*', '/'])

    def arith_expression(self):
        return self.get_binary_operation(self.term, ['+', '-'])

    def comp_expression(self):
        return self.get_binary_operation(self.arith_expression, ['<', '>', '==', '<=', '>='])

    def decision_expression(self):
        if self.get_previous_token().is_match(['if']):
            if_cases = []
            else_case = None
            if_scope_type = ''
            condition = self.expression()
            if self.get_current_token().is_match(['{', ':']):
                if_scope_type = self.get_current_token().get_value()
                self.advance()
                expression = self.expression()
                if_cases.append((condition, expression))
                if if_scope_type == '{':
                    proceed = self.get_current_token().is_match(['}'])
                else:
                    proceed = True
                print(proceed)
                if proceed:
                    self.advance()
                    while self.get_current_token().is_match(['elseif']):
                        self.advance()
                        condition = self.expression()
                        print(condition)
                        if self.get_current_token().is_match(['{', ':']):
                            if if_scope_type == '{':
                                proceed = self.get_current_token().is_match(['{'])
                            else:
                                proceed = self.get_current_token().is_match(':')

                            if proceed:
                                self.advance()
                                expression = self.expression()
                                print(expression)
                                if_cases.append((condition, expression))
                                if if_scope_type == '{':
                                    proceed = self.get_current_token().is_match(['}'])
                                    if proceed:
                                        self.advance()
                                    else:
                                        self.set_error(Error('InvalidSyntaxError', 'Expected \'}\''))
                                        return None
                            else:
                                self.set_error(Error('InvalidSyntaxError', 'Expected \'{\', \':\''))
                                return None
                        else:
                            self.set_error(Error('InvalidSyntaxError', 'Expected \'{\', \':\''))
                            return None

                    print(self.get_current_token())
                    if self.get_current_token().is_match('else'):
                        self.advance()
                        if self.get_current_token().is_match(['{', ':']):
                            if if_scope_type == '{':
                                proceed = self.get_current_token().is_match(['{'])
                            else:
                                proceed = self.get_current_token().is_match(':')

                            if proceed:
                                self.advance()
                                else_case = self.expression()

                                if if_scope_type == '{':
                                    proceed = self.get_current_token().is_match(['}'])
                                else:
                                    proceed = self.get_current_token().is_match('endif')

                                if proceed:
                                    print(1, if_cases, else_case)
                                    return DecisionOperation(if_cases, else_case)
                                else:
                                    self.set_error(Error('InvalidSyntaxError', 'Expected \'}\', \'endif\''))
                                    return None
                            else:
                                self.set_error(Error('InvalidSyntaxError', 'Expected \'{\', \':\''))
                                return None
                        else:
                            self.set_error(Error('InvalidSyntaxError', 'Expected \'{\', \':\''))
                            return None
                    print(2, if_cases, else_case)
                    return DecisionOperation(if_cases, else_case)
                else:
                    self.set_error(Error('InvalidSyntaxError', 'Expected \'}\''))
                    return None
            else:
                self.set_error(Error('InvalidSyntaxError', 'Expected \'{\', \':\''))
                return None

    def expression(self):

        result = self.get_binary_operation(self.comp_expression, ['and', 'or', '||', '&&'])

        if isinstance(result, KeyWord) and result.is_match(['if']):
            return self.decision_expression()

        elif isinstance(result, VarAccessOperation):

            if self.get_current_token().is_type_of('operator') and self.get_current_token().is_type_of('='):
                if self.has_next_token():
                    self.advance()
                    word = self.expression()
                    if isinstance(word, KeyWord) and word.is_type_any(['ref', 'val', 'new']):
                        value = self.expression()
                        if isinstance(value, VarAccessOperation):
                            return VarAssignOperation(result.get_child_node(), word, value.get_child_node())
                        else:
                            self.set_error(Error('InvalidSyntaxError', 'Expected an identifier'))
                            return None
                    else:
                        return VarAssignOperation(result.get_child_node(), Word('keyword', 'val'), word)
                else:
                    self.set_error(Error('InvalidSyntaxError', 'Expected ref, val or expression'))
                    return None

            return result

        else:
            return result
