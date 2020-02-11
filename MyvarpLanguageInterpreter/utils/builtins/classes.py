from utils.base.myvarp_class import MyvarpClass
from utils.base.myvarp_error import Error
from utils.builtins.helper_functions import de_string


class Primitive(MyvarpClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__value = None

    def set_value(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

    def and_op(self, other):
        try:
            result = Boolean(bool(self.get_value()) and bool(other.get_value()))
            return result
        except Exception as e:
            return Error('InvalidSyntaxError', str(e))

    def or_op(self, other):
        try:
            result = Boolean(bool(self.get_value()) or bool(other.get_value()))
            return result
        except Exception as e:
            return Error('InvalidSyntaxError', str(e))

    def __str__(self):
        return self.get_value()

    def __repr__(self):
        return f'Primitive<{self.get_value()}>'


class Number(Primitive):
    def __init__(self, value):
        super().__init__()
        self.set_name("Number")
        self.set_value(value)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.get_value())

    def get_value(self):
        return float(super().get_value()) if str(super().get_value()).__contains__('.') else int(super().get_value())

    def plus(self, other):
        if isinstance(other, Number):
            number = Number(self.get_value() + other.get_value())
            return number
        else:
            try:
                number = Number(self.get_value() + int(other.get_value()))
                return number
            except Exception as e:
                return Error('InvalidSyntaxError', str(e))

    def minus(self, other):
        if isinstance(other, Number):
            number = Number(self.get_value() - other.get_value())
            return number
        else:
            try:
                number = Number(self.get_value() - int(other.get_value()))
                return number
            except Exception as e:
                return Error('InvalidSyntaxError', str(e))

    def mul(self, other):
        if isinstance(other, Number):
            number = Number(self.get_value() * other.get_value())
            return number
        else:
            try:
                number = Number(self.get_value() * int(other.get_value()))
                return number
            except Exception as e:
                return Error('InvalidSyntaxError', str(e))

    def div(self, other):
        try:
            if isinstance(other, Number):
                number = Number(self.get_value() / other.get_value())
                return number
            else:
                try:
                    number = Number(self.get_value() / int(other.get_value()))
                    return number
                except Exception as e:
                    return Error('InvalidSyntaxError', str(e))
        except ZeroDivisionError:
            return Error('DivisionByZeroError', 'you are trying to divide a number by 0')

    def abs_div(self, other):
        try:
            if isinstance(other, Number):
                number = Number(self.get_value() // other.get_value())
                return number
            else:
                try:
                    number = Number(self.get_value() // int(other.get_value()))
                    return number
                except Exception as e:
                    return Error('InvalidSyntaxError', str(e))
        except ZeroDivisionError:
            return Error('DivisionByZeroError', 'you are trying to divide a number by 0')

    def pow(self, other):
        if isinstance(other, Number):
            return Number(self.get_value() ** other.get_value())
        else:
            try:
                number = Number(self.get_value() ** int(other.get_value()))
                return number
            except Exception as e:
                return Error('InvalidSyntaxError', str(e))

    def less_than(self, other):
        if isinstance(other, Number):
            return Boolean(self.get_value() < other.get_value())

    def greater_than(self, other):
        if isinstance(other, Number):
            return Boolean(self.get_value() > other.get_value())

    def equal_to(self, other):
        if isinstance(other, Number):
            return Boolean(self.get_value() == other.get_value())

    def less_than_or_equal_to(self, other):
        if isinstance(other, Number):
            return Boolean(self.get_value() <= other.get_value())

    def greater_than_or_equal_to(self, other):
        if isinstance(other, Number):
            return Boolean(self.get_value() >= other.get_value())


class Float(Number):
    def __init__(self, value):
        super().__init__(value)
        self.set_name("Float")

    def get_value(self):
        return float(super().get_value())

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.get_value())


class Integer(Number):
    def __init__(self, value):
        super().__init__(value)
        self.set_name("Integer")

    def get_value(self):
        return int(super().get_value())

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.get_value())


class String(Primitive):
    def __init__(self, value):
        super().__init__()
        self.set_value(value)
        self.set_name("String")

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.get_value()

    def get_value(self):
        return str(super().get_value())

    def plus(self, other):
        if isinstance(other, String):
            return String(self.get_value() + other.get_value())

    def minus(self, other):
        if isinstance(other, String):
            return String(self.get_value().replace(other.get_value(), ''))

    def mul(self, other):
        if isinstance(other, Number):
            return String(self.get_value() * other.get_value())

    def less_than(self, other):
        if isinstance(other, String):
            return Boolean(self.get_value() < other.get_value())

    def greater_than(self, other):
        if isinstance(other, String):
            return Boolean(self.get_value() > other.get_value())

    def equal_to(self, other):
        if isinstance(other, String):
            return Boolean(self.get_value() == other.get_value())

    def less_than_or_equal_to(self, other):
        if isinstance(other, String):
            return Boolean(self.get_value() <= other.get_value())

    def greater_than_or_equal_to(self, other):
        if isinstance(other, String):
            return Boolean(self.get_value() >= other.get_value())


class Boolean(Primitive):
    def __init__(self, boolean, **kwargs):
        super().__init__(**kwargs)
        self.set_name("Boolean")
        self.set_value(boolean)

    def get_value(self):
        return bool(super().get_value())

    def less_than(self, other):
        return int(bool(self.get_value())) < int(bool(other.get_value()))

    def greater_than(self, other):
        return int(bool(self.get_value())) > int(bool(other.get_value()))

    def equal_to(self, other):
        return bool(self.get_value()) == bool(other.get_value())

    def less_than_or_equal_to(self, other):
        return self.less_than(other) or self.equal_to(other)

    def greater_than_or_equal_to(self, other):
        return self.greater_than(other) or self.equal_to(other)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.get_value())


class Empty(Primitive):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_name('Empty')
        self.set_value('')

    def is_empty(self):
        return True

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'None'
