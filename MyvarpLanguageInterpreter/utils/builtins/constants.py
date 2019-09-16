# from utils.builtins.funtions import Display
# from utils.builtins.funtions import Decision

OPERATORS = {
    '++': '',
    '--': '',
    '**': '',
    '//': '',
    '+=': '',
    '-=': '',
    '*=': '',
    '/=': '',
    '==': '',
    '>=': '',
    '<=': '',
    '!=': '',
    '=': '',
    '/': '',
    '*': '',
    '+': '',
    '-': '',
    '%': '',
    '>': '',
    '<': '',
    '!': '',
    '.': ''
}

KEYWORDS = {
    'if': "",
    'else': '',
    'elseif': '',
    'func': '',
    'endif': '',
    'endfunc': '',
    'class': '',
    'interface': '',
    'abstract': '',
    'return': '',
    'when': '',
    'with': '',
    'endwith': '',
    'as': '',
    'from': '',
    'import': '',
    'in': '',
    'of': '',
    'for': '',
    'endfor': '',
    'do': '',
    'then': '',
    'foreach': '',
    'endforeach': '',
    'try': '',
    'new': '',
    'ref': '',
    'public': '',
    'private': '',
    'protected': '',
    'static': '',
    'final': '',
    'const': '',
    'except': '',
    'break': '',
    'continue': '',
}

TYPES = {
    'number': '',
    'int': '',
    'float': '',
    'string': '',
    'list': '',
    'dict': '',
    'set': '',
    'tuple': '',
    'bool': '',
    'byte': '',
    'object': '',
    'true': True,
    'false': False,
    'none': None,
    'range': range,
    'exception': Exception
}

FUNCTIONS = {
    'display': 'Display()'
}

BUILTINS = {
    'operators': OPERATORS,

    'keywords': KEYWORDS,

    'classes': TYPES,

    'functions': FUNCTIONS
}

DEFAULT_STARTUP_ENVIRON = {

    'info': {
        'script_name': '',  # get_script_name from kwargs
        'script_path': '',  # get script path
        'script_source': '',
        'start_line': 0,
        'stop_line': 0
    },
}


EXPECT_AFTER_DATA = [
    'syntax.helper',
    'syntax.newline',
    'builtins.operator',
    'method.call',
    'builtins.if',
    'builtins.as',
    'builtins.comparator'
]

EXPRESSIONS_PATTERNS = [
    'data.',
    'data.identifier',
    'data.||operator||data.',
    'data.identifier||operator.accessor||data.identifier||data.collection.tuple',
    'builtins.keyword||expression||helper||scope'
    'builtins.keyword||data.identifier||helper|scope'
    'builtins.keyword||data.expression||helper||scope'
    'data.identifier||operator.=||data.|expression.helper.\\'
]

EXPRESSIONS = [
    'assignment',
    'algebraic_expression',
    'do_while',
    'for_loop',
    'while_loop',
    'decision_tree',
    'method_call',
    'method_accessing'
    'function_call'
]

"""
condition                       expect

*stack.is empty                 keyword - builtins
                                data - int, bool, string etc
                                identifier : function , variable name

*identifier                     operation
                                assignment
                                method call
                                next line | enter key
                                parenthesis_closer

*operator                       raw data
                                identifier
                                next line | spaces

*function opener                function closer
                                identifier
                                raw data
                                keyword arguments (assignment in parenthesis, type hinting, type declaration)
                                //NOTE : type declaration can be var_name = data_type | var_name as data_type

*collection [] {} ()            expect group item(s) or index or key for []

*circle brackets ()             ; : | {

public private protected        identifier | class | interface | abstract

@  and .                        identifier

string                          ; or space or () function call

, comma                         identifier | raw data

after scope ends pop scope opener with closer eg { - } |  : anything else

:return:
"""
