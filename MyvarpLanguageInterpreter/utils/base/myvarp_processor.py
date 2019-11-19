class MyvarpWordProcessor:
    def __init__(self, interpreter, word):
        self._word = word
        self._result = None
        self._result_type = None
        self._expression = None
        self._interpreter = interpreter
        self._expected_types_left: list = [None]
        self._expected_types_right: list = [None]
        self._left_object: MyvarpWordProcessor = None
        self._right_object: MyvarpWordProcessor = None
        self._collected_word: MyvarpWordProcessor = None


    def get_word(self):
        return self._word

    def get_collected_word(self):
        return self._collected_word

    def get_interpreter(self):
        return self._interpreter

    def get_result(self):
        return self._result_type

    def get_result_type(self):
        return self._result_type

    def get_expression(self):
        return self._expression

    def get_left_object(self):
        return self._left_object

    def get_right_object(self):
        return self._right_object

    def get_type_at_left(self):
        if self.get_left_object() is None:
            return None
        return self.get_left_object().get_result_type()

    def get_type_at_right(self):
        if self.get_right_object() is None:
            return None
        return self.get_right_object().get_result_type()

    def get_expected_types_for_left(self):
        return self._expected_types_left

    def get_expected_types_for_right(self):
        return self._expected_types_right

    def set_collected_word(self, word):
        if self._collected_word is None:
            self._collected_word = word
        else:
            pass

        if self.get_collected_word().get_result_type() in self.get_expected_types_for_right():
            self.operate()


    def set_expression(self, obj):
        self._expression = obj

    def set_result(self, obj):
        self._result = obj

    def set_result_type(self, obj):
        self._result_type = obj

    def set_left_object(self, obj):
        self._left_object = obj

    def set_right_object(self, obj):
        self._right_object = obj

    def set_expected_types_for_left(self, obj):
        if isinstance(obj, list):
            self._expected_types_left = obj
        else:
            self._expected_types_left = [obj]

    def set_expected_types_for_right(self, obj):
        if isinstance(obj, list):
            self._expected_types_right = obj
        else:
            self._expected_types_right = [obj]

    def validate_left_object(self):
        return self.get_type_at_left() in self.get_expected_types_for_left()

    def validate_right_object(self):
        return self.get_type_at_right() in self.get_expected_types_for_right()

    def add_word_to_right(self, word):
        self.set_collected_word(generate_word_processor(self.get_interpreter(), word))
        # set right to generated and check value until expected type is acquired else error

    def operate(self):
        pass
        # self.operate(prev, next) using interpreter scope


class EmptyLiteral(MyvarpWordProcessor):
    def __init__(self, interpreter):
        super().__init__(interpreter, "")
        self.set_expected_types_for_right(['keyword', 'identifier', 'data'])
        self.set_left_object(None)

    def operate(self):
        if self.validate_left_object() and self.validate_right_object():
            right = self.get_interpreter().wait_for_init()
            self.set_result_type(right.get_type())
            word = None

            if right.is_type_of('keyword'):
                word = None  # KeyWordProcessor(right)
            elif right.is_type_of('identifier'):
                word = None  # IdentifierWordProcessor(right)
            elif right.is_type_of('data'):
                word = None  # DataWordProcessor(right)
            else:
                self.set_result_type('exception')
                # TODO: do error here

            self.get_interpreter().set_last_word(self)
            self.set_right_object(word)


class IdentifierLiteral(MyvarpWordProcessor):
    def __init__(self, interpreter, word):
        super().__init__(interpreter, word)
        self.set_expected_types_for_left([None, 'operator', 'expression.helper.@.?.$.{,[,,,('])
        self.set_expected_types_for_right([None, 'identifier', 'run'])
        self.set_left_object(interpreter.get_last_word())
        self.set_result_type('identifier')
        # print(self.get_word())

    def operate(self):
        if self.validate_left_object() and self.validate_right_object():
            word = self.get_collected_word()
            if word.get_type() == 'expression.helper.run':
                # run
                print('running', self.get_word())
                pass
            elif word.get_type().contains('operator'):
                # run
                print('operator seen')
                pass
            # TODO : future check if next is keyword
            else:
                # TODO : error
                print('operator seen')
                pass


class EqualLiteral(MyvarpWordProcessor):
    def __init__(self, interpreter):
        super().__init__(interpreter, "=")
        self.set_expected_types_for_left('identifier')
        self.set_expected_types_for_right(['identifier', 'data-expression', 'data'])
        self.set_left_object(interpreter.get_last_word())

    def operate(self):
        if self.validate_left_object():
            right = self.get_interpreter().wait_for_data()
            if right is not None:
                word = None  # DataWordProcessor(right)
                self.set_right_object(word)
                if self.validate_right_object():
                    pass
                    # self.get_interpreter().get_memory . do_assignment
                    # with self.get_right_object().get_word() self.get_right_object().get_result()
                    # set self result type
                    self.get_interpreter().set_last_word(self)



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


WORD_PROCESSORS = {
    '': EmptyLiteral,
    'operator.=': EqualLiteral,
    'operator.+': EmptyLiteral,
    'operator.-': EmptyLiteral,
    'operator.*': EmptyLiteral,
    'operator./': EmptyLiteral,
    'operator.%': EmptyLiteral,
    'operator.&': EmptyLiteral,
    'operator.~': EmptyLiteral,
    'operator.^': EmptyLiteral,
    'operator.++': EmptyLiteral,
    'operator.--': EmptyLiteral,
    'operator.//': EmptyLiteral,
    'operator.**': EmptyLiteral,
    'operator.+=': EmptyLiteral,
    'operator.-=': EmptyLiteral,
    'operator.*=': EmptyLiteral,
    'operator./=': EmptyLiteral,
    'operator.%=': EmptyLiteral,
    'operator.//=': EmptyLiteral,
    'operator.**=': EmptyLiteral,
    'operator.>': EmptyLiteral,
    'operator.<': EmptyLiteral,
    'operator.!': EmptyLiteral,
    'operator.==': EmptyLiteral,
    'operator.<=': EmptyLiteral,
    'operator.>=': EmptyLiteral,
    'operator.!=': EmptyLiteral,
    'operator.accessor': EmptyLiteral,
    'expression.helper.#': EqualLiteral,
    'expression.helper.:': EqualLiteral,
    'expression.helper.;': EqualLiteral,
    'expression.helper.,': EqualLiteral,
    'expression.helper.$': EqualLiteral,
    'expression.helper.@': EqualLiteral,
    'expression.helper.?': EqualLiteral,
    'expression.helper.|': EqualLiteral,
    'expression.helper.\\': EqualLiteral,
    'expression.helper.run': EmptyLiteral,
    'data.identifier': IdentifierLiteral,
    'builtins.data.byte': EmptyLiteral,
    'builtins.data.bool': EmptyLiteral,
    'builtins.data.list': EmptyLiteral,
    'builtins.data.dict': EmptyLiteral,
    'builtins.data.set': EmptyLiteral,
    'builtins.data.tuple': EmptyLiteral,
    'builtins.data.object': EmptyLiteral,
    'builtins.data.string': EmptyLiteral,
    'builtins.data.number': EmptyLiteral,
    'builtins.data.number.float': EmptyLiteral,
    'builtins.data.number.integer': EmptyLiteral,
    'builtins.keyword.if': EmptyLiteral,
    'builtins.keyword.else': EmptyLiteral,
    'builtins.keyword.elseif': EmptyLiteral,
    'builtins.keyword.while': EmptyLiteral,
    'builtins.keyword.switch': EmptyLiteral,
    'builtins.keyword.case': EmptyLiteral,
    'builtins.keyword.for': EmptyLiteral,
    'builtins.keyword.in': EmptyLiteral,
    'builtins.keyword.is': EmptyLiteral,
    'builtins.keyword.not': EmptyLiteral,
    'builtins.keyword.as': EmptyLiteral,
    'builtins.keyword.from': EmptyLiteral,
    'builtins.keyword.with': EmptyLiteral,
    'builtins.keyword.whenever': EmptyLiteral,
    'builtins.keyword.do': EmptyLiteral,
    'builtins.keyword.of': EmptyLiteral,
    'builtins.keyword.then': EmptyLiteral,
    'builtins.keyword.when': EmptyLiteral,
    'builtins.keyword.try': EmptyLiteral,
    'builtins.keyword.catch': EmptyLiteral,
    'builtins.keyword.except': EmptyLiteral,
    'builtins.keyword.continue': EmptyLiteral,
    'builtins.keyword.break': EmptyLiteral,
    'builtins.keyword.new': EmptyLiteral,
    'builtins.keyword.ref': EmptyLiteral,
    'builtins.keyword.const': EmptyLiteral,
    'builtins.keyword.final': EmptyLiteral,
    'builtins.keyword.static': EmptyLiteral,
    'builtins.keyword.private': EmptyLiteral,
    'builtins.keyword.public': EmptyLiteral,
    'builtins.keyword.protected': EmptyLiteral,
    'builtins.keyword.interface': EmptyLiteral,
    'builtins.keyword.abstract': EmptyLiteral,
    'builtins.keyword.extends': EmptyLiteral,
    'builtins.keyword.implements': EmptyLiteral,
    'builtins.keyword.foreach': EmptyLiteral,
    'builtins.keyword.class': EmptyLiteral,
    'builtins.keyword.endforeach': EmptyLiteral,
    'builtins.keyword.endif': EmptyLiteral,
    'builtins.keyword.endwhile': EmptyLiteral,
    'builtins.keyword.endfor': EmptyLiteral,
    'builtins.keyword.endwith': EmptyLiteral,
    'builtins.keyword.endswitch': EmptyLiteral,
    'builtins.keyword.endfunc': EmptyLiteral,
    'builtins.keyword.endclass': EmptyLiteral,
    'builtins.keyword.import': EmptyLiteral,
    'builtins.keyword.export': EmptyLiteral,
    'builtins.keyword.include': EmptyLiteral,
    'builtins.keyword.require': EmptyLiteral,
    'expression.collection.opener.(': EmptyLiteral,
    'expression.collection.opener.{': EmptyLiteral,
    'expression.collection.opener.[': EmptyLiteral,
    'expression.collection.closer.)': EmptyLiteral,
    'expression.collection.closer.}': EmptyLiteral,
    'expression.collection.closer.]': EmptyLiteral
}


def generate_word_processor(i, word):
    print(word)
    if word.get_type().__contains__('data'):
        return WORD_PROCESSORS[f'{word.get_type()}'](i, word)
    else:
        return WORD_PROCESSORS[f'{word.get_type()}'](i)