
from utils.base.myvarp_error import Error
from utils.base.myvarp_word import Word
from utils.base.processors.operation import BinaryOperation, UnaryOperation, VarAssignOperation, VarAccessOperation, \
    Identifier
from utils.builtins.classes import Number


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

    def parse(self):
        self.advance()
        self.__result = self.expression()

    def get_binary_operation(self, func, operators):

        left = func()
        if self.has_error(): return left

        while self.get_current_token().is_type_any(operators):
            operator = self.get_current_token()
            self.advance()
            right = func()
            if self.has_error(): return right
            left = BinaryOperation(left, operator, right)

        return left

    def atom(self):
        if self.get_current_token().is_type_of('number'):
            word = self.get_current_token()
            self.advance()
            return Number(word.get_value())

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

            if self.get_current_token().is_type_any(['+', '-']):
                operator = self.get_current_token()
                if self.has_next_token():
                    self.advance()
                    factor = self.factor()
                    if not self.has_error():
                        return UnaryOperation(None, operator, factor)

            return self.atom()

        else:
            self.set_error(Error('InvalidSyntaxError', 'Expected type int, float, -, +!'))

    def term(self):
        return self.get_binary_operation(self.factor, ['*', '/'])

    def expression(self):

        # if self.get_current_token().is_type_of('identifier'):
        #
        #     var = Identifier(self.get_current_token().get_value())
        #
        #     if self.has_next_token():
        #         self.advance()
        #
        #         if self.get_current_token().is_type_of('operator'):
        #             if self.get_current_token().is_type_of('='):
        #                 if self.has_next_token():
        #                 self.advance()
        #                 word = self.expression()
        #
        #                 if word.is_type_any(['ref', 'val']):
        #                     _type = word
        #                     if self.has_next_token():
        #                         self.advance()
        #                         value = self.expression()
        #                         if not word.get_child_node().is_type_of('identifier'):
        #                             self.set_error(Error('InvalidSyntaxError', 'Expected identifier'))
        #                             return None
        #                     else:
        #                         self.set_error(Error('InvalidSyntaxError', 'Expected value expression'))
        #                         return None
        #                 else:
        #                     _type = Word('keyword', 'ref')
        #                     value = word
        #
        #                 return VarAssignOperation(var, _type, value)
        #
        #             else:
        #                 self.set_error(Error('InvalidSyntaxError', 'Expected value expression, ref or val'))
        #                 return None
        #
        #         else:
        #             self.set_error(Error('InvalidSyntaxError', 'Expected value operator'))
        #             return None
        #
        #     else:
        #         return VarAccessOperation(var)

        return self.get_binary_operation(self.term, ['+', '-'])
