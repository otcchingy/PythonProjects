from utils.base.myvarp_class import MyvarpClass
from utils.base.myvarp_error import Error


class Number(MyvarpClass):

    def __init__(self, value):
        self.__value = value
        super().__init__()
        self.set_name("Number")

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.get_value())

    def get_value(self):
        return int(self.__value)

    def plus(self, other):
        if isinstance(other, Number):
            return Number(self.get_value()+other.get_value())

    def minus(self, other):
        if isinstance(other, Number):
            return Number(self.get_value()-other.get_value())

    def mul(self, other):
        if isinstance(other, Number):
            return Number(self.get_value()*other.get_value())

    def div(self, other):
        if isinstance(other, Number):
            try:
                number = Number(self.get_value()/other.get_value())
                return number
            except ZeroDivisionError:
                return Error('DivisionByZeroError', 'you are trying to divide a number by 0')

    def abs_div(self, other):
        if isinstance(other, Number):
            try:
                number = Number(self.get_value()//other.get_value())
                return number
            except ZeroDivisionError:
                return Error('DivisionByZeroError', 'you are trying to divide a number by 0')

    def pow(self, other):
        if isinstance(other, Number):
            return Number(self.get_value()**other.get_value())


class Empty(MyvarpClass):

    def is_empty(self):
        return True
