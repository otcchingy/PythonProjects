from utils.base.myvarp_word import Word


class Operation:
    def __init__(self, left_node=None, operator=None, right_node=None):
        self.operator = operator
        self.left_node = left_node
        self.right_node = right_node

    def set_left_node(self, value):
        self.left_node = value

    def set_right_node(self, value):
        self.right_node = value

    def get_left_node(self):
        return self.left_node

    def get_right_node(self):
        return self.right_node

    def get_operator(self):
        return self.operator

    def __str__(self):
        left = '' if self.left_node is None else (self.left_node if self.left_node.__dict__.keys().__contains__(
            '_value') is False else self.left_node.get_value())
        right = '' if self.right_node is None else (self.right_node if self.right_node.__dict__.keys().__contains__(
            '_value') is False else self.right_node.get_value())
        return f'({left}, {self.operator.get_value()}, {right})'

    def __repr__(self):
        return f'Operation({self.left_node}, {self.operator}, {self.right_node})'


class BinaryOperation(Operation):
    def __repr__(self):
        return f'BinaryOperation({self.left_node}, {self.operator}, {self.right_node})'


class UnaryOperation(Operation):
    def get_child_node(self):
        return self.left_node or self.right_node

    def __str__(self):
        return super().__str__().replace('(, ', '(').replace(', )', ')')

    def __repr__(self):
        return f'UnaryOperation({self.left_node}, {self.operator}, {self.right_node})'


class Identifier:
    def __init__(self, var_name):
        self.name = var_name

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Identifier<{self.name}>'


class KeyWord(Word):
    def __init__(self, word: Word):
        super().__init__(word.get_type(), word.get_value())


class VarAccessOperation(UnaryOperation):
    def __init__(self, identifier):
        super().__init__(None, Word('memory.access', '?'), identifier)


class VarAssignOperation(BinaryOperation):
    def __init__(self, var_name, op, value):
        super().__init__(var_name, op, value)


class DecisionOperation:
    def __init__(self, if_cases, else_case):
        self._if_cases = if_cases
        self._else_case = else_case

    def get_if_cases(self):
        return self._if_cases

    def get_else_case(self):
        return self._else_case

    def has_else_case(self):
        return self.get_else_case() is not None

    def __repr__(self):
        return f'DecisionOperation(<cases {self.get_if_cases()}, else: {self.get_else_case()}>)'
