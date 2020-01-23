# from utils.builtins.funtions import Display
# from utils.builtins.funtions import Decision

OPERATORS = {
    '//=': '',
    '**=': '',
    '++': '',
    '--': '',
    '**': '',
    '//': '',
    '+=': '',
    '-=': '',
    '*=': '',
    '/=': '',
    '%=': '',
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
    '^': '',
    '&': '',
    '~': '',
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
    'whenever': '',
    'with': '',
    'endwith': '',
    'as': '',
    'from': '',
    'import': '',
    'in': '',
    'is': '',
    'case': '',
    'of': '',
    'for': '',
    'endfor': '',
    'do': '',
    'then': '',
    'foreach': '',
    'endforeach': '',
    'try': '',
    'new': '',
    'async': '',
    'await': '',
    'self': '',
    'this': '',
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
    'require': '',
    'include': '',
    'extends': '',
    'export': '',
    'implements': '',
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
    'none': None,
    'byte': '',
    'object': '',
}


SYS_DEFAULT_OBJECT_IMPORTS = {
    'true': {'value': True, 'type': 'bool'},
    'false': {'value': False, 'type': 'bool'},
    'typeof': {'value': None, 'type': 'object'},
    'range': {'value': None, 'type': 'object'},
    'date': {'value': None, 'type': 'object'},
    'len': {'value': None, 'type': 'object'},
    'sizeof': {'value': None, 'type': 'object'},
    'display': {'value': None, 'type': 'object'},
    'input': {'value': None, 'type': 'object'},
    'exception': {'value': Exception, 'type': 'object'}
}

SYS_OTHER_OBJECT = {
    'os': {'value': None, 'type': 'object'},
    'sys': {'value': None, 'type': 'object'},
    'time': {'value': None, 'type': 'object'},
    'thread': {'value': None, 'type': 'object'},
    'process': {'value': None, 'type': 'object'},
    'socket': {'value': None, 'type': 'object'},
    'http': {'value': None, 'type': 'object'},
    'math': {'value': None, 'type': 'object'},
    'file': {'value': None, 'type': 'object'}
}

BUILTINS = {
    'operators': OPERATORS,
    'keywords': KEYWORDS,
    'classes': TYPES,
    'objects': SYS_DEFAULT_OBJECT_IMPORTS
}

DEFAULT_STARTUP_ENVIRON = {
    'info': {
        'script_name': '',  # get_script_name from kwargs
        'script_path': '',  # get script path
        'script_source': '',
        'start_line': 0,
        'stop_line': 0,
        'script_argv': []
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
